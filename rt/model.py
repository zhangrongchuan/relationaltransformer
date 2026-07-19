import json
import os
from functools import partial
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from einops import rearrange
from einops._torch_specific import allow_ops_in_compiled_graph
from ml_dtypes import bfloat16
from torch import nn
from torch.nn.attention import SDPBackend, sdpa_kernel
from torch.nn.attention.flex_attention import create_block_mask, flex_attention

allow_ops_in_compiled_graph()
flex_attention = torch.compile(flex_attention)


def apply_time_rope(x, rope_cos, rope_sin):
    """Partial RoPE over the leading `2*n_freq` dims of each head.

    x: (b, h, s, d_head); rope_cos/sin: (b, s, n_freq).
    Rotating q and k by their own timestamp phase makes attention scores
    depend only on the time difference between query and key tokens.
    """
    n = rope_cos.shape[-1]
    x1 = x[..., :n]
    x2 = x[..., n : 2 * n]
    c = rope_cos[:, None, :, :]  # broadcast over heads
    s = rope_sin[:, None, :, :]
    return torch.cat(
        [x1 * c - x2 * s, x1 * s + x2 * c, x[..., 2 * n :]], dim=-1
    )


class MaskedAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.num_heads = num_heads

        self.wq = nn.Linear(d_model, d_model, bias=False)
        self.wk = nn.Linear(d_model, d_model, bias=False)
        self.wv = nn.Linear(d_model, d_model, bias=False)
        self.wo = nn.Linear(d_model, d_model, bias=False)

    def forward(self, x, block_mask, rope=None):
        q = self.wq(x)
        k = self.wk(x)
        v = self.wv(x)

        q = rearrange(q, "b s (h d) -> b h s d", h=self.num_heads)
        k = rearrange(k, "b s (h d) -> b h s d", h=self.num_heads)
        v = rearrange(v, "b s (h d) -> b h s d", h=self.num_heads)

        if rope is not None:
            q = apply_time_rope(q, *rope)
            k = apply_time_rope(k, *rope)

        if block_mask is None:
            with sdpa_kernel(SDPBackend.FLASH_ATTENTION):
                x = F.scaled_dot_product_attention(q, k, v)
        else:
            x = flex_attention(q, k, v, block_mask=block_mask)

        x = rearrange(x, "b h s d -> b s (h d)")
        x = self.wo(x)
        return x


class FFN(nn.Module):
    def __init__(self, d_model, d_ff):
        super().__init__()

        self.w1 = nn.Linear(d_model, d_ff, bias=False)
        self.w2 = nn.Linear(d_ff, d_model, bias=False)
        self.w3 = nn.Linear(d_model, d_ff, bias=False)

    def forward(self, x):
        return self.w2(F.silu(self.w1(x)) * self.w3(x))


class RelationalBlock(nn.Module):
    def __init__(
        self,
        d_model,
        num_heads,
        d_ff,
    ):
        super().__init__()

        self.norms = nn.ModuleDict(
            {l: nn.RMSNorm(d_model) for l in ["feat", "nbr", "col", "full", "ffn"]}
        )
        self.attns = nn.ModuleDict(
            {
                l: MaskedAttention(d_model, num_heads)
                for l in ["feat", "nbr", "col", "full"]
            }
        )
        self.ffn = FFN(d_model, d_ff)

    def forward(self, x, block_masks, rope=None):
        for l in ["col", "feat", "nbr", "full"]:
            x = x + self.attns[l](
                self.norms[l](x), block_mask=block_masks[l], rope=rope
            )
        x = x + self.ffn(self.norms["ffn"](x))
        return x


def _make_block_mask(mask, batch_size, seq_len, device):
    def _mod(b, h, q_idx, kv_idx):
        return mask[b, q_idx, kv_idx]

    return create_block_mask(
        mask_mod=_mod,
        B=batch_size,
        H=None,
        Q_LEN=seq_len,
        KV_LEN=seq_len,
        device=device,
        _compile=True,
    )


class RelationalTransformer(nn.Module):
    def __init__(
        self,
        num_blocks,
        d_model,
        d_text,
        num_heads,
        d_ff,
        time_rope=False,
        entity_flag=False,
    ):
        super().__init__()

        self.time_rope = time_rope
        self.entity_flag = entity_flag
        d_head = d_model // num_heads
        # partial RoPE: rotate half of each head's dims; geometric wavelengths
        # from 1 day to ~100 years (timestamps arrive as epoch seconds)
        n_freq = d_head // 4
        wavelengths_days = torch.logspace(0, 4.56, n_freq, base=10.0)
        self.register_buffer(
            "rope_inv_freq", 2 * torch.pi / wavelengths_days, persistent=False
        )
        if entity_flag:
            self.same_entity_emb = nn.Parameter(torch.zeros(d_model))

        self.enc_dict = nn.ModuleDict(
            {
                "number": nn.Linear(1, d_model, bias=True),
                "text": nn.Linear(d_text, d_model, bias=True),
                "datetime": nn.Linear(1, d_model, bias=True),
                "col_name": nn.Linear(d_text, d_model, bias=True),
                "boolean": nn.Linear(1, d_model, bias=True),
            }
        )
        self.dec_dict = nn.ModuleDict(
            {
                "number": nn.Linear(d_model, 1, bias=True),
                "text": nn.Linear(d_model, d_text, bias=True),
                "datetime": nn.Linear(d_model, 1, bias=True),
                "boolean": nn.Linear(d_model, 1, bias=True),
            }
        )
        self.norm_dict = nn.ModuleDict(
            {
                "number": nn.RMSNorm(d_model),
                "text": nn.RMSNorm(d_model),
                "datetime": nn.RMSNorm(d_model),
                "col_name": nn.RMSNorm(d_model),
                "boolean": nn.RMSNorm(d_model),
            }
        )
        self.mask_embs = nn.ParameterDict(
            {
                t: nn.Parameter(torch.randn(d_model))
                for t in ["number", "text", "datetime", "boolean"]
            }
        )
        self.blocks = nn.ModuleList(
            [RelationalBlock(d_model, num_heads, d_ff) for i in range(num_blocks)]
        )
        self.norm_out = nn.RMSNorm(d_model)
        self.d_model = d_model

    def forward(self, batch):
        node_idxs = batch["node_idxs"]
        f2p_nbr_idxs = batch["f2p_nbr_idxs"]
        col_name_idxs = batch["col_name_idxs"]
        table_name_idxs = batch["table_name_idxs"]
        is_padding = batch["is_padding"]
        batch_size, seq_len = node_idxs.shape

        batch_size, seq_len = node_idxs.shape
        device = node_idxs.device

        # Padding mask for attention pairs (allow only non-pad -> non-pad)
        pad = (~is_padding[:, :, None]) & (~is_padding[:, None, :])  # (B, S, S)

        # cells in the same node
        same_node = node_idxs[:, :, None] == node_idxs[:, None, :]  # (B, S, S)

        # kv index is among q's foreign -> primary neighbors
        kv_in_f2p = (node_idxs[:, None, :, None] == f2p_nbr_idxs[:, :, None, :]).any(
            -1
        )  # (B, S, S)

        # q index is among kv's primary -> foreign neighbors (reverse relation)
        q_in_f2p = (node_idxs[:, :, None, None] == f2p_nbr_idxs[:, None, :, :]).any(
            -1
        )  # (B, S, S)

        # Same column AND same table
        same_col_table = (col_name_idxs[:, :, None] == col_name_idxs[:, None, :]) & (
            table_name_idxs[:, :, None] == table_name_idxs[:, None, :]
        )  # (B, S, S)

        # Final boolean masks (apply padding once here)
        attn_masks = {
            "feat": (same_node | kv_in_f2p) & pad,
            "nbr": q_in_f2p & pad,
            "col": same_col_table & pad,
            "full": pad,
        }

        # Make them contiguous for better kernel performance
        for l in attn_masks:
            attn_masks[l] = attn_masks[l].contiguous()

        # Convert to block masks
        make_block_mask = partial(
            _make_block_mask,
            batch_size=batch_size,
            seq_len=seq_len,
            device=device,
        )
        block_masks = {
            l: make_block_mask(attn_mask) for l, attn_mask in attn_masks.items()
        }

        # per-sequence seed (prediction-time) anchor from the target position
        is_targets = batch["is_targets"]
        has_target = is_targets.any(-1)
        tpos = is_targets.float().argmax(-1)  # (B,)

        rope = None
        if self.time_rope:
            ts = batch["timestamps"].long()  # (B, S) epoch seconds
            ts_valid = batch["timestamps"] != -(2**31)
            seed_ts = ts.gather(1, tpos[:, None]).squeeze(1)
            seed_ts = torch.where(has_target, seed_ts, torch.zeros_like(seed_ts))
            # relative days to prediction time; atemporal tokens pinned at 0.
            # angles computed in fp32 (buffer may have been cast to bf16 by
            # net.to(bfloat16), so re-cast here)
            t_rel = (ts - seed_ts[:, None]).float() / 86400.0
            t_rel = torch.where(ts_valid, t_rel, torch.zeros_like(t_rel))
            angles = t_rel[..., None] * self.rope_inv_freq.float()
            rope = (
                torch.cos(angles).to(torch.bfloat16),
                torch.sin(angles).to(torch.bfloat16),
            )

        x = 0
        x = x + (
            self.norm_dict["col_name"](
                self.enc_dict["col_name"](batch["col_name_values"])
            )
            * (~is_padding)[..., None]
        )

        if self.entity_flag:
            # tokens structurally tied to the seed row: the seed row itself,
            # its f2p entities, and any row referencing one of those entities
            seed_node = node_idxs.gather(1, tpos[:, None]).squeeze(1)  # (B,)
            seed_f2p = f2p_nbr_idxs.gather(
                1, tpos[:, None, None].expand(-1, 1, f2p_nbr_idxs.shape[-1])
            ).squeeze(1)  # (B, 5)
            ent = torch.cat([seed_node[:, None], seed_f2p], dim=1)  # (B, 6)
            ent = torch.where(ent >= 0, ent, torch.full_like(ent, -(2**30)))
            related = (node_idxs[:, :, None] == ent[:, None, :]).any(-1) | (
                (f2p_nbr_idxs[:, :, :, None] == ent[:, None, None, :])
                .any(-1)
                .any(-1)
            )
            related = related & ~is_padding & has_target[:, None]
            x = x + self.same_entity_emb * related[..., None]

        for i, t in enumerate(["number", "text", "datetime", "boolean"]):
            x = x + (
                self.norm_dict[t](self.enc_dict[t](batch[t + "_values"]))
                * ((batch["sem_types"] == i) & ~batch["masks"] & ~is_padding)[..., None]
            )
            x = x + (
                self.mask_embs[t]
                * ((batch["sem_types"] == i) & batch["masks"] & ~is_padding)[..., None]
            )

        for i, block in enumerate(self.blocks):
            x = block(x, block_masks, rope=rope)

        x = self.norm_out(x)

        loss_out = x.new_zeros(())
        yhat_out = {"number": None, "text": None, "datetime": None, "boolean": None}

        B, S, _ = x.shape
        sem_types = batch["sem_types"]  # (B,S) ints 0..3
        masks = batch["masks"].bool()  # (B,S) where to train

        for i, t in enumerate(["number", "text", "datetime", "boolean"]):
            yhat = self.dec_dict[t](x)  # (B,S, D_t)
            y = batch[f"{t}_values"]  # (B,S, D_y)
            sem_type_mask = (sem_types == i) & masks  # (B,S) mask for this type

            if not sem_type_mask.any():
                if t in yhat_out:
                    # still touch the param to avoid unused param error
                    loss_out = loss_out + (yhat.sum() * 0.0)
                    yhat_out[t] = yhat
                continue

            if t in ("number", "datetime"):
                loss_t = F.huber_loss(yhat, y, reduction="none").mean(-1)
            elif t == "boolean":
                loss_t = F.binary_cross_entropy_with_logits(
                    yhat, (y > 0).float(), reduction="none"
                ).mean(-1)
            elif t == "text":
                raise ValueError("masking text not supported")

            # masked sum for this type
            loss_out = loss_out + (loss_t * sem_type_mask).sum()

            if t in yhat_out:
                yhat_out[t] = yhat

        loss_out = loss_out / masks.sum()

        return loss_out, yhat_out
