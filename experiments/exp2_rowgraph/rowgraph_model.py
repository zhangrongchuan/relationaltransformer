"""RowGraphNet: row-level conditioned message passing backbone (prototype).

Design (agreed in discussion):
  level 1 (intra-row):  cell encoders (RT-compatible, warm-startable) pooled
                        into one row vector per row  ("business card")
  level 2 (inter-row):  typed message passing over the FK row graph,
                        conditioned on the seed row (labeling trick)
  candidate value nodes: True/False via boolean encoder, K z-space bins via
                        number encoder; context task rows send one-directional
                        has_label edges into their answer's candidate node
  readout:              score(seed, candidate); clf = score diff,
                        reg = expectation over softmax(bin scores)

Graphs are built on-the-fly from the standard RT cell batches (no sampler
format change needed): cells sharing node_idx form a row.
"""

import math

import torch
import torch.nn.functional as F
from torch import nn

TS_MIN = -(2 ** 31)
GID_OFF = 2 ** 32  # batch offset for globally unique row ids
SEM_NUMBER, SEM_TEXT, SEM_DATETIME, SEM_BOOLEAN = 0, 1, 2, 3


def scatter_mean_max(src, index, n):
    d = src.shape[-1]
    mean = torch.zeros(n, d, device=src.device, dtype=src.dtype)
    cnt = torch.zeros(n, device=src.device, dtype=src.dtype)
    mean.index_add_(0, index, src)
    cnt.index_add_(0, index, torch.ones_like(index, dtype=src.dtype))
    mean = mean / cnt.clamp(min=1)[:, None]
    mx = torch.full((n, d), -1e4, device=src.device, dtype=src.dtype)
    mx.scatter_reduce_(0, index[:, None].expand(-1, d), src, "amax")
    return torch.cat([mean, mx], dim=-1)


class MPLayer(nn.Module):
    """One round of typed message passing."""

    def __init__(self, d, etypes=("f2p", "p2f", "label")):
        super().__init__()
        self.w_self = nn.Linear(d, d)
        self.w_edge = nn.ModuleDict({t: nn.Linear(d, d) for t in etypes})
        self.norm = nn.LayerNorm(d)

    def forward(self, h, edges):
        agg = torch.zeros_like(h)
        deg = torch.zeros(h.shape[0], device=h.device, dtype=h.dtype)
        for t, e in edges.items():
            src, dst, w = e[0], e[1], e[2]
            cond = e[3] if len(e) > 3 else None
            if src.numel() == 0:
                continue
            z = self.w_edge[t](h[src])
            if cond is not None:
                z = z + cond
            m = F.relu(z) * w[:, None]
            agg.index_add_(0, dst, m)
            deg.index_add_(0, dst, w)
        agg = agg / deg.clamp(min=1)[:, None]
        return self.norm(h + F.relu(self.w_self(h)) + agg)


class RowGraphNet(nn.Module):
    def __init__(
        self,
        d_model=256,
        d_text=384,
        n_layers=6,
        n_bins=33,
        use_time=True,
        use_label_edges=True,
        pool="meanmax",
        use_relgraph=False,
    ):
        super().__init__()
        self.use_time = use_time
        self.use_label_edges = use_label_edges
        self.pool = pool
        if pool == "attn":
            # learned-query attention over cells within a row: wide rows keep
            # their salient fields instead of diluting them into the mean
            self.attn_w = nn.Linear(d_model, d_model)
            self.attn_q = nn.Parameter(torch.randn(d_model) / d_model ** 0.5)

        # cell encoders — names/shapes match RT for warm starting
        self.enc_dict = nn.ModuleDict(
            {
                "number": nn.Linear(1, d_model),
                "text": nn.Linear(d_text, d_model),
                "datetime": nn.Linear(1, d_model),
                "col_name": nn.Linear(d_text, d_model),
                "boolean": nn.Linear(1, d_model),
            }
        )
        self.norm_dict = nn.ModuleDict(
            {
                k: nn.RMSNorm(d_model)
                for k in ["number", "text", "datetime", "col_name", "boolean"]
            }
        )

        self.row_proj = nn.Linear(2 * d_model, d_model)
        self.seed_emb = nn.Parameter(torch.zeros(d_model))
        self.cand_emb = nn.Parameter(torch.zeros(d_model))

        # relative-time encoding: wavelengths 1 day .. ~100 years
        n_freq = 16
        wl = torch.logspace(0, 4.56, n_freq)
        self.register_buffer("inv_freq", 2 * math.pi / wl, persistent=False)
        self.time_proj = nn.Linear(2 * n_freq, d_model)

        # z-space bin centers (targets are z-scored by the pipeline).
        # tails at 0.5%/99.5% (±2.58σ): heavy-tailed regression targets
        # (ltv/sales) would otherwise be clipped at ±2.05σ, capping R².
        probs = torch.linspace(0.005, 0.995, n_bins)
        centers = math.sqrt(2.0) * torch.erfinv(2 * probs - 1)
        self.register_buffer("bin_centers", centers, persistent=False)
        self.n_bins = n_bins

        self.layers = nn.ModuleList([MPLayer(d_model) for _ in range(n_layers)])
        self.use_relgraph = use_relgraph
        if use_relgraph:
            # ULTRA-style relation graph: nodes = FK relation types
            # (child_table, parent_table) observed in the subgraph; edges =
            # the four structural interactions; boundary = the seed row's
            # query relation. Output conditions the main GNN's messages.
            self.rel_query_emb = nn.Parameter(torch.randn(d_model) * 0.02)
            self.rel_layers = nn.ModuleList(
                [MPLayer(d_model, etypes=("h2h", "t2t", "h2t", "t2h"))
                 for _ in range(2)]
            )
            self.rel_cond = nn.Linear(d_model, d_model)
            nn.init.zeros_(self.rel_cond.weight)
            nn.init.zeros_(self.rel_cond.bias)
        self.readout = nn.Sequential(
            nn.Linear(2 * d_model, d_model), nn.ReLU(), nn.Linear(d_model, 1)
        )

    # ------------------------------------------------------------------
    def encode_cells(self, batch, valid):
        """(B,S) cell embeddings via type encoders + column-name embedding."""
        sem = batch["sem_types"]
        x = self.norm_dict["col_name"](
            self.enc_dict["col_name"](batch["col_name_values"].float())
        )
        vals = {
            SEM_NUMBER: ("number", batch["number_values"].float()),
            SEM_TEXT: ("text", batch["text_values"].float()),
            SEM_DATETIME: ("datetime", batch["datetime_values"].float()),
            SEM_BOOLEAN: ("boolean", batch["boolean_values"].float()),
        }
        for code, (name, v) in vals.items():
            enc = self.norm_dict[name](self.enc_dict[name](v))
            x = x + enc * (sem == code)[..., None]
        return x * valid[..., None]

    # ------------------------------------------------------------------
    def forward(self, batch):
        node = batch["node_idxs"].long()
        is_pad = batch["is_padding"]
        is_tgt = batch["is_targets"]
        masks = batch["masks"]
        ts = batch["timestamps"].long()
        B, S = node.shape
        dev = node.device

        has_tgt = is_tgt.any(-1)
        graphs = has_tgt.nonzero(as_tuple=True)[0]  # sequences that count
        G = graphs.numel()
        if G == 0:
            raise ValueError("batch has no targets")
        # remap: graph g in [0,G) is sequence graphs[g]
        seq2g = torch.full((B,), -1, device=dev, dtype=torch.long)
        seq2g[graphs] = torch.arange(G, device=dev)

        tpos = is_tgt.float().argmax(-1)  # (B,)
        bidx = torch.arange(B, device=dev)
        seed_node = node[bidx, tpos]
        seed_ts = ts[bidx, tpos]
        seed_table = batch["table_name_idxs"][bidx, tpos]
        target_col = batch["col_name_idxs"][bidx, tpos]
        target_sem = batch["sem_types"][bidx, tpos]  # 3=boolean else numeric

        # ---------------- rows ----------------
        valid = (~is_pad) & (~masks) & has_tgt[:, None]
        gid = node + bidx[:, None] * GID_OFF
        flat_gid = gid[valid]
        uniq, inv = torch.unique(flat_gid, return_inverse=True)
        R = uniq.numel()
        row_g = seq2g[(uniq // GID_OFF)]

        cell_emb = self.encode_cells(batch, valid)[valid]  # (Ncells,d)
        if self.pool == "attn":
            sc = torch.tanh(self.attn_w(cell_emb)) @ self.attn_q  # (Ncells,)
            mx = torch.full((R,), -1e4, device=dev, dtype=sc.dtype)
            mx.scatter_reduce_(0, inv, sc, "amax")
            e = torch.exp(sc - mx[inv])
            z = torch.zeros(R, device=dev, dtype=sc.dtype)
            z.index_add_(0, inv, e)
            alpha = e / z[inv].clamp(min=1e-6)
            attn = torch.zeros(R, cell_emb.shape[-1], device=dev, dtype=cell_emb.dtype)
            attn.index_add_(0, inv, cell_emb * alpha[:, None])
            mean = torch.zeros_like(attn)
            cnt = torch.zeros(R, device=dev, dtype=cell_emb.dtype)
            mean.index_add_(0, inv, cell_emb)
            cnt.index_add_(0, inv, torch.ones_like(sc))
            mean = mean / cnt.clamp(min=1)[:, None]
            h_row = self.row_proj(torch.cat([attn, mean], dim=-1))
        else:
            h_row = self.row_proj(scatter_mean_max(cell_emb, inv, R))

        # representative cell per row -> row-level fields
        pos = torch.arange(flat_gid.numel(), device=dev)
        first = torch.full((R,), flat_gid.numel(), device=dev, dtype=torch.long)
        first.scatter_reduce_(0, inv, pos, "amin")
        flat_f2p = batch["f2p_nbr_idxs"].long()[valid]  # (Ncells,5)
        flat_ts = ts[valid]  # (Ncells,)
        row_f2p = flat_f2p[first]
        row_ts = flat_ts[first]
        assert (uniq[torch.searchsorted(uniq, seed_gid := (seed_node + bidx * GID_OFF)[graphs])] == seed_gid).all(), "seed row missing from graph"

        # time encoding relative to the seed timestamp of the row's graph
        if self.use_time:
            g_seed_ts = seed_ts[graphs]  # (G,)
            dt = (g_seed_ts[row_g] - row_ts).float() / 86400.0
            ok = (row_ts != TS_MIN) & (g_seed_ts[row_g] != TS_MIN)
            dt = torch.where(ok, dt, torch.zeros_like(dt))
            ang = dt[:, None] * self.inv_freq.float()
            h_row = h_row + self.time_proj(
                torch.cat([torch.cos(ang), torch.sin(ang)], dim=-1)
            )

        # seed marker (labeling trick boundary)
        seed_row = torch.searchsorted(uniq, seed_gid)
        h_row[seed_row] = h_row[seed_row] + self.seed_emb

        # ---------------- FK edges ----------------
        par_gid = row_f2p + (uniq // GID_OFF)[:, None] * GID_OFF
        child = (
            torch.arange(R, device=dev)[:, None].expand(-1, row_f2p.shape[1]).reshape(-1)
        )
        par_flat = par_gid.reshape(-1)
        loc = torch.searchsorted(uniq, par_flat.clamp(min=0))
        found = (
            (row_f2p.reshape(-1) >= 0)
            & (loc < R)
            & (uniq[loc.clamp(max=R - 1)] == par_flat)
        )
        e_src = child[found]
        e_dst = loc[found]
        ones = torch.ones(e_src.numel(), device=dev, dtype=h_row.dtype)

        # ---------------- relation graph (ULTRA h2h/h2t/t2h/t2h) ----------
        fk_cond = None
        if self.use_relgraph and e_src.numel() > 0:
            flat_table = batch["table_name_idxs"].long()[valid]
            row_table = flat_table[first]  # (R,)
            PK = 2 ** 21
            e_g = row_g[e_src]  # graph of each edge
            e_ct = row_table[e_src]  # child table
            e_pt = row_table[e_dst]  # parent table
            rel_key = (e_g * PK + e_ct) * PK + e_pt
            rel_uniq, rel_inv = torch.unique(rel_key, return_inverse=True)
            Nr = rel_uniq.numel()
            r_g = rel_uniq // (PK * PK)
            r_ct = (rel_uniq // PK) % PK
            r_pt = rel_uniq % PK

            # query relations: edges whose child row is the seed row
            is_seed_row = torch.zeros(R, dtype=torch.bool, device=dev)
            is_seed_row[seed_row] = True
            q_rel = torch.zeros(Nr, dtype=torch.bool, device=dev)
            q_rel[rel_inv[is_seed_row[e_src]]] = True

            h_rel = (
                q_rel[:, None].to(h_row.dtype) * self.rel_query_emb[None, :]
            )
            sg = r_g[:, None] == r_g[None, :]
            eye = torch.eye(Nr, dtype=torch.bool, device=dev)
            pairs = {
                "h2h": sg & (r_ct[:, None] == r_ct[None, :]) & ~eye,
                "t2t": sg & (r_pt[:, None] == r_pt[None, :]) & ~eye,
                "h2t": sg & (r_ct[:, None] == r_pt[None, :]) & ~eye,
                "t2h": sg & (r_pt[:, None] == r_ct[None, :]) & ~eye,
            }
            rel_edges = {}
            for t, m in pairs.items():
                ss, dd = m.nonzero(as_tuple=True)
                rel_edges[t] = (
                    ss, dd, torch.ones(ss.numel(), device=dev, dtype=h_row.dtype)
                )
            for lyr in self.rel_layers:
                h_rel = lyr(h_rel, rel_edges)
            # per-FK-edge conditioning vector (zero-init projection)
            fk_cond = self.rel_cond(h_rel)[rel_inv]

        # ---------------- candidate value nodes ----------------
        g_sem = target_sem[graphs]
        is_clf = g_sem == SEM_BOOLEAN
        n_cand = torch.where(is_clf, 2, self.n_bins)
        cand_off = torch.cumsum(
            torch.cat([torch.zeros(1, device=dev, dtype=torch.long), n_cand[:-1]]), 0
        )
        C = int(n_cand.sum())
        cand_g = torch.repeat_interleave(torch.arange(G, device=dev), n_cand)
        # candidate values: [0,1] for clf; bin centers for reg
        idx_in_g = torch.arange(C, device=dev) - cand_off[cand_g]
        cand_val = torch.where(
            is_clf[cand_g],
            idx_in_g.float(),
            self.bin_centers.float()[idx_in_g.clamp(max=self.n_bins - 1)],
        )
        # intrinsic identity: encode the candidate VALUE with the value encoder
        h_c_bool = self.norm_dict["boolean"](self.enc_dict["boolean"](cand_val[:, None]))
        h_c_num = self.norm_dict["number"](self.enc_dict["number"](cand_val[:, None]))
        h_cand = torch.where(is_clf[cand_g][:, None], h_c_bool, h_c_num) + self.cand_emb

        # ---------------- has_label edges (context task rows -> answers) ----
        l_src = torch.empty(0, device=dev, dtype=torch.long)
        l_dst = torch.empty(0, device=dev, dtype=torch.long)
        l_w = torch.empty(0, device=dev, dtype=h_row.dtype)
        if self.use_label_edges:
            lab = (
                valid
                & (batch["col_name_idxs"] == target_col[:, None])
                & (batch["table_name_idxs"] == seed_table[:, None])
                & (node != seed_node[:, None])
            )
            lab_flat = lab[valid]  # (Ncells,) mask on flat cells
            if lab_flat.any():
                rows_l = inv[lab_flat]
                g_l = row_g[rows_l]
                v_bool = batch["boolean_values"].float()[..., 0][valid][lab_flat]
                v_num = batch["number_values"].float()[..., 0][valid][lab_flat]
                clf_l = is_clf[g_l]
                # clf: edge to candidate 0/1
                dst_clf = cand_off[g_l] + (v_bool > 0).long()
                # reg: two-hot edges to the two nearest bins
                z = v_num.clamp(self.bin_centers[0].item(), self.bin_centers[-1].item())
                ri = torch.searchsorted(self.bin_centers.float(), z).clamp(
                     1, self.n_bins - 1)
                li = ri - 1
                lc, rc = self.bin_centers.float()[li], self.bin_centers.float()[ri]
                wr = ((z - lc) / (rc - lc).clamp(min=1e-6)).clamp(0, 1)
                dst_l = cand_off[g_l] + li
                dst_r = cand_off[g_l] + ri
                l_src = torch.cat([rows_l[clf_l], rows_l[~clf_l], rows_l[~clf_l]])
                l_dst = torch.cat([dst_clf[clf_l], dst_l[~clf_l], dst_r[~clf_l]])
                l_w = torch.cat(
                    [
                        torch.ones(int(clf_l.sum()), device=dev),
                        (1 - wr)[~clf_l],
                        wr[~clf_l],
                    ]
                ).to(h_row.dtype)

        # ---------------- message passing over [rows ; candidates] --------
        h = torch.cat([h_row, h_cand], dim=0)
        edges = {
            "f2p": (e_src, e_dst, ones, fk_cond),
            "p2f": (e_dst, e_src, ones, fk_cond),
            "label": (l_src, R + l_dst, l_w),  # one-directional into candidates
        }
        for layer in self.layers:
            h = layer(h, edges)

        # ---------------- readout ----------------
        h_seed = h[seed_row]  # (G,d)
        scores = self.readout(
            torch.cat([h_seed[cand_g], h[R:]], dim=-1)
        ).squeeze(-1)  # (C,)

        # labels
        y_bool = batch["boolean_values"].float()[bidx, tpos, 0][graphs]
        y_num = batch["number_values"].float()[bidx, tpos, 0][graphs]

        out = {"is_clf": is_clf, "graphs": graphs}
        loss = torch.zeros((), device=dev)

        if is_clf.any():
            gi = is_clf.nonzero(as_tuple=True)[0]
            s0 = scores[cand_off[gi]]
            s1 = scores[cand_off[gi] + 1]
            logit = s1 - s0
            loss = loss + F.binary_cross_entropy_with_logits(
                logit, (y_bool[gi] > 0).float(), reduction="sum"
            )
            out["clf_logit"] = logit
            out["clf_y"] = y_bool[gi]
            out["clf_graphs"] = graphs[gi]
        if (~is_clf).any():
            gi = (~is_clf).nonzero(as_tuple=True)[0]
            sc = scores[
                cand_off[gi][:, None] + torch.arange(self.n_bins, device=dev)[None]
            ]  # (Greg, n_bins)
            z = y_num[gi].clamp(
                self.bin_centers[0].item(), self.bin_centers[-1].item()
            )
            ri = torch.searchsorted(self.bin_centers.float(), z).clamp(1, self.n_bins - 1)
            li = ri - 1
            lc, rc = self.bin_centers.float()[li], self.bin_centers.float()[ri]
            wr = ((z - lc) / (rc - lc).clamp(min=1e-6)).clamp(0, 1)
            twohot = torch.zeros_like(sc)
            twohot.scatter_(1, li[:, None], (1 - wr)[:, None])
            twohot.scatter_add_(1, ri[:, None], wr[:, None])
            loss = loss + -(twohot * F.log_softmax(sc, dim=-1)).sum()
            out["reg_pred"] = (F.softmax(sc, dim=-1) * self.bin_centers.float()).sum(-1)
            out["reg_y"] = y_num[gi]
            out["reg_graphs"] = graphs[gi]

        out["loss"] = loss / G
        return out
