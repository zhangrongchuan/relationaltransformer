"""Official RT normal + no-self-label R^2 on the paper's 8 regression tasks.

Mirrors rt_noself_alltasks.py but for regression: reads yhat_dict["number"],
scores with r2_score. Zero-shot leave-db-out ckpts, full test split.

Usage: pixi run python experiments/exp2_rowgraph/rt_reg_noself.py [task_idx]
"""

import json
import sys
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import r2_score
from torch.utils.data import DataLoader

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from rt.data import RelationalDataset  # noqa: E402
from rt.model import RelationalTransformer  # noqa: E402

CKPT = Path("~/scratch/rt_ckpts").expanduser()
# paper regression table order
TASKS = [
    ("rel-amazon", "item-ltv", "ltv"),
    ("rel-amazon", "user-ltv", "ltv"),
    ("rel-avito", "ad-ctr", "num_click"),
    ("rel-f1", "driver-position", "position"),
    ("rel-hm", "item-sales", "sales"),
    ("rel-stack", "post-votes", "popularity"),
    ("rel-trial", "site-success", "success_rate"),
    ("rel-trial", "study-adverse", "num_of_adverse_events"),
]


@torch.inference_mode()
def ev(net, db, table, target, drop, device):
    ds = RelationalDataset(
        tasks=[(db, table, target, "test", [])], batch_size=32, seq_len=1024,
        rank=0, world_size=1, max_bfs_width=256,
        embedding_model="all-MiniLM-L12-v2", d_text=384, seed=0,
        self_label_dropout=drop,
    )
    ds.sampler.shuffle_py(0)
    P, Y = {}, {}
    for b in DataLoader(ds, batch_size=None, num_workers=4, pin_memory=True):
        tb = b.pop("true_batch_size")
        for k in b:
            b[k] = b[k].to(device, non_blocking=True)
        b["masks"][tb:] = False
        b["is_targets"][tb:] = False
        b["is_padding"][tb:] = True
        _, yh = net(b)
        it = b["is_targets"]
        yhat = yh["number"][it].flatten().float()
        y = b["number_values"][it].flatten().float()
        nid = b["node_idxs"][it].flatten()
        for n, p, yy in zip(nid.tolist(), yhat.tolist(), y.tolist()):
            if n not in P:
                P[n] = p
                Y[n] = yy
    ids = sorted(P)
    return round(float(r2_score([Y[i] for i in ids], [P[i] for i in ids])), 4)


def main():
    device = "cuda"
    torch.multiprocessing.set_sharing_strategy("file_system")
    torch.set_num_threads(1)
    sel = int(sys.argv[1]) if len(sys.argv) > 1 else None
    tasks = [TASKS[sel]] if sel is not None else TASKS
    res_dir = Path(__file__).resolve().parents[1] / "results"
    for db, table, target in tasks:
        out_path = res_dir / f"rt_reg_{db}_{table}.json"
        if out_path.exists():
            continue
        ck = CKPT / f"pretrain_{db}_{table}.pt"
        if not ck.exists():
            print(f"skip {db}/{table}: no ckpt")
            continue
        net = RelationalTransformer(
            num_blocks=12, d_model=256, d_text=384, num_heads=8, d_ff=1024
        )
        net.load_state_dict(torch.load(ck, map_location="cpu"))
        net = net.to(device).to(torch.bfloat16).eval()
        normal = ev(net, db, table, target, 0.0, device)
        noself = ev(net, db, table, target, 1.0, device)
        print(f"RTREG {db}/{table} normal={normal} noself={noself}", flush=True)
        out_path.write_text(json.dumps(
            {"db": db, "table": table, "normal": normal, "noself": noself},
            indent=2))


if __name__ == "__main__":
    main()
