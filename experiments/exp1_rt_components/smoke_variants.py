"""GPU smoke test: all variants forward+backward+ckpt-load, 4 steps each."""

import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from rt.data import RelationalDataset  # noqa: E402
from rt.model import RelationalTransformer  # noqa: E402

CKPT = Path("~/scratch/rt_ckpts/pretrain_rel-f1_driver-dnf.pt").expanduser()


def run(variant_flags, name):
    net = RelationalTransformer(
        num_blocks=12, d_model=256, d_text=384, num_heads=8, d_ff=1024,
        **variant_flags,
    )
    sd = torch.load(CKPT, map_location="cpu")
    missing, unexpected = net.load_state_dict(sd, strict=False)
    assert not unexpected, unexpected
    assert set(missing) <= {"same_entity_emb"}, missing
    net = net.to("cuda").to(torch.bfloat16)

    ds = RelationalDataset(
        tasks=[("rel-f1", "driver-top3", "qualifying", "train", [])],
        batch_size=8, seq_len=1024, rank=0, world_size=1, max_bfs_width=256,
        embedding_model="all-MiniLM-L12-v2", d_text=384, seed=0,
    )
    opt = torch.optim.AdamW(net.parameters(), lr=1e-4)
    for i in range(4):
        batch = ds[i]
        batch.pop("true_batch_size")
        for k in batch:
            batch[k] = batch[k].to("cuda")
        loss, _ = net(batch)
        opt.zero_grad()
        loss.backward()
        opt.step()
        print(f"{name} step {i}: loss={loss.item():.4f}", flush=True)
    # eval-style forward with padded batch
    with torch.inference_mode():
        batch = ds[5]
        tb = batch.pop("true_batch_size")
        for k in batch:
            batch[k] = batch[k].to("cuda")
        batch["masks"][tb:, :] = False
        batch["is_targets"][tb:, :] = False
        batch["is_padding"][tb:, :] = True
        loss, yhat = net(batch)
        print(f"{name} eval: loss={loss.item():.4f}")
    print(f"{name} OK", flush=True)


for name, flags in [
    ("baseline", {}),
    ("rope", {"time_rope": True}),
    ("eflag", {"entity_flag": True}),
    ("rope_eflag", {"time_rope": True, "entity_flag": True}),
]:
    run(flags, name)
print("ALL VARIANTS OK")
