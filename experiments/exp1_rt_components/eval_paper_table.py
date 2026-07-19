"""Paper-aligned evaluation: official zero-shot ckpts, FULL TEST split.

Covers the 10 classification tasks of the paper's cross-model table
(RT zero-shot column: mean AUROC 69.7) and evaluates, per task:
  - baseline sampler   (reproduces the paper number)
  - pcap4              (periphery_cell_cap=4)
  - local32_pcap4      (local_k=32 + pcap4)
each with K resampled contexts (K=8 small / 4 medium / 1 giant tasks);
for K>1 also reports the K-context ensemble.

Usage: pixi run python experiments/eval_paper_table.py <task_idx>
Output: experiments/results/eval_paper_table.json (incremental)
"""

import json
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from rt.data import RelationalDataset  # noqa: E402
from experiments.exp1_rt_components.diag_variance import (  # noqa: E402
    build_model, eval_epoch, metric_fn, CKPT_DIR,
)

# (db, table, target_col, K, paper_zero_shot_auroc)
TASKS = [
    ("rel-amazon", "item-churn", "churn", 1, 70.9),
    ("rel-amazon", "user-churn", "churn", 1, 64.0),
    ("rel-avito", "user-clicks", "num_click", 4, 59.5),
    ("rel-avito", "user-visits", "num_click", 4, 61.8),
    ("rel-f1", "driver-dnf", "did_not_finish", 8, 81.2),
    ("rel-f1", "driver-top3", "qualifying", 8, 89.3),
    ("rel-hm", "user-churn", "churn", 4, 62.8),
    ("rel-stack", "user-badge", "WillGetBadge", 1, 80.1),
    ("rel-stack", "user-engagement", "contribution", 4, 75.7),
    ("rel-trial", "study-outcome", "outcome", 8, 51.8),
]
SAMPLERS = {
    "baseline": {},
    "pcap4": {"periphery_cell_cap": 4},
    "local32_pcap4": {"local_k": 32, "periphery_cell_cap": 4},
}


def main():
    device = "cuda"
    idx = int(sys.argv[1])
    db, table, target_col, K, paper = TASKS[idx]
    # per-task file avoids write races between parallel jobs
    out_path = (
        Path(__file__).parents[1] / "results" / f"eval_paper_table_{idx}.json"
    )

    net = build_model(device)
    net.load_state_dict(
        torch.load(CKPT_DIR / f"pretrain_{db}_{table}.pt", map_location="cpu")
    )
    net.eval()

    for sname, skw in SAMPLERS.items():
        ds = RelationalDataset(
            tasks=[(db, table, target_col, "test", [])],
            batch_size=32, seq_len=1024, rank=0, world_size=1,
            max_bfs_width=256, embedding_model="all-MiniLM-L12-v2",
            d_text=384, seed=0, **skw,
        )
        all_preds, labels0 = [], None
        for epoch in range(K):
            preds, labels = eval_epoch(net, ds, "clf", device, epoch)
            all_preds.append(preds)
            labels0 = labels0 or labels
            print(f"{sname} epoch {epoch}: {len(preds)} targets", flush=True)
        ids = sorted(set.intersection(*(set(p) for p in all_preds)))
        P = np.array([[p[i] for i in ids] for p in all_preds])
        y = np.array([labels0[i] for i in ids])
        single = [metric_fn("clf", y, P[e]) for e in range(K)]
        rec = {
            "db": db, "table": table, "sampler": sname, "split": "test",
            "n": len(ids), "K": K, "paper_zero_shot": paper,
            "single_mean": round(float(np.mean(single)), 4),
            "single_std": round(float(np.std(single)), 4),
        }
        if K > 1:
            rec["ensemble"] = round(metric_fn("clf", y, P.mean(0)), 4)
        # incremental save with a simple lock-free append (jobs write distinct
        # tasks; last-writer-wins collisions are avoided by read-modify-write
        # of the freshest file content per record)
        results = json.loads(out_path.read_text()) if out_path.exists() else []
        results = [
            r for r in results
            if not (r["db"] == db and r["table"] == table and r["sampler"] == sname)
        ]
        results.append(rec)
        out_path.write_text(json.dumps(results, indent=2))
        print(json.dumps(rec), flush=True)


if __name__ == "__main__":
    main()
