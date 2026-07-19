"""Official RT normal + no-self-label AUROC on all 10 paper clf tasks.

Loads each official leave-db-out pretrain ckpt (zero-shot), evaluates full
test split under normal (self_label_dropout=0) and no-self-label (=1.0).
Gives the missing baseline column so the robustness claim is cross-task.
"""

import json
import sys
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import roc_auc_score
from torch.utils.data import DataLoader

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from rt.data import RelationalDataset  # noqa: E402
from rt.model import RelationalTransformer  # noqa: E402

CKPT = Path("~/scratch/rt_ckpts").expanduser()
TASKS = [
    ("rel-amazon", "item-churn", "churn"),
    ("rel-amazon", "user-churn", "churn"),
    ("rel-avito", "user-clicks", "num_click"),
    ("rel-avito", "user-visits", "num_click"),
    ("rel-f1", "driver-dnf", "did_not_finish"),
    ("rel-f1", "driver-top3", "qualifying"),
    ("rel-hm", "user-churn", "churn"),
    ("rel-stack", "user-badge", "WillGetBadge"),
    ("rel-stack", "user-engagement", "contribution"),
    ("rel-trial", "study-outcome", "outcome"),
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
        yhat = yh["boolean"][it].flatten().float()
        y = b["boolean_values"][it].flatten().float()
        nid = b["node_idxs"][it].flatten()
        for n, p, yy in zip(nid.tolist(), yhat.tolist(), y.tolist()):
            if n not in P:
                P[n] = p
                Y[n] = yy
    ids = sorted(P)
    yb = [int(Y[i] > 0) for i in ids]
    if len(set(yb)) < 2:
        return None
    return round(float(roc_auc_score(yb, [P[i] for i in ids])), 4)


def main():
    device = "cuda"
    torch.multiprocessing.set_sharing_strategy("file_system")
    torch.set_num_threads(1)
    sel = int(sys.argv[1]) if len(sys.argv) > 1 else None
    tasks = [TASKS[sel]] if sel is not None else TASKS
    for db, table, target in tasks:
        key = f"{db}/{table}"
        out_path = (Path(__file__).resolve().parents[1] / "results"
                    / f"rt_noself_{db}_{table}.json")
        if out_path.exists():
            continue
        ck = CKPT / f"pretrain_{db}_{table}.pt"
        if not ck.exists():
            print(f"skip {key}: no ckpt")
            continue
        net = RelationalTransformer(
            num_blocks=12, d_model=256, d_text=384, num_heads=8, d_ff=1024
        )
        net.load_state_dict(torch.load(ck, map_location="cpu"))
        net = net.to(device).to(torch.bfloat16).eval()
        normal = ev(net, db, table, target, 0.0, device)
        noself = ev(net, db, table, target, 1.0, device)
        print(f"RTNOSELF {key} normal={normal} noself={noself}", flush=True)
        out_path.write_text(json.dumps(
            {"db": db, "table": table, "normal": normal, "noself": noself},
            indent=2))


if __name__ == "__main__":
    main()
