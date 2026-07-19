"""Noise-controlled evaluation of inference-time sampling variants.

Uses the ORIGINAL zero-shot checkpoint (no variant training) and evaluates
each sampling configuration K=8 times with different sampler epochs on the
full val split. Reports mean±std per config -> clean estimate of the
eval-time effect of local_k / periphery_cell_cap, plus the ensemble metric.

Usage: pixi run python experiments/eval_sampling_variants.py
Output: experiments/results/eval_sampling_variants.json
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

K = 8
TASKS = [
    ("rel-f1", "driver-dnf", "did_not_finish", [], "clf"),
    ("rel-trial", "study-outcome", "outcome", [], "clf"),
    ("rel-avito", "ad-ctr", "num_click", [], "reg"),
    ("rel-event", "user-repeat", "target", [], "clf"),
]
SAMPLERS = {
    "baseline": {},
    "local32": {"local_k": 32},
    "pcap4": {"periphery_cell_cap": 4},
    "local32_pcap4": {"local_k": 32, "periphery_cell_cap": 4},
    "local16_pcap4": {"local_k": 16, "periphery_cell_cap": 4},
}


def main():
    device = "cuda"
    out_path = Path(__file__).parents[1] / "results" / "eval_sampling_variants.json"
    results = json.loads(out_path.read_text()) if out_path.exists() else []
    done = {(r["db"], r["table"], r["sampler"]) for r in results}

    for db, table, target_col, drop_cols, ttype in TASKS:
        net = None
        for sname, skw in SAMPLERS.items():
            if (db, table, sname) in done:
                continue
            if net is None:
                net = build_model(device)
                net.load_state_dict(
                    torch.load(
                        CKPT_DIR / f"pretrain_{db}_{table}.pt", map_location="cpu"
                    )
                )
                net.eval()
            ds = RelationalDataset(
                tasks=[(db, table, target_col, "val", drop_cols)],
                batch_size=32, seq_len=1024, rank=0, world_size=1,
                max_bfs_width=256, embedding_model="all-MiniLM-L12-v2",
                d_text=384, seed=0, **skw,
            )
            all_preds, labels0 = [], None
            for epoch in range(K):
                preds, labels = eval_epoch(net, ds, ttype, device, epoch)
                all_preds.append(preds)
                labels0 = labels0 or labels
            ids = sorted(set.intersection(*(set(p) for p in all_preds)))
            P = np.array([[p[i] for i in ids] for p in all_preds])
            y = np.array([labels0[i] for i in ids])
            single = [metric_fn(ttype, y, P[e]) for e in range(K)]
            rec = {
                "db": db, "table": table, "sampler": sname,
                "task_type": ttype, "n": len(ids), "K": K,
                "single_mean": round(float(np.mean(single)), 4),
                "single_std": round(float(np.std(single)), 4),
                "ensemble": round(metric_fn(ttype, y, P.mean(0)), 4),
            }
            results.append(rec)
            print(json.dumps(rec), flush=True)
            out_path.write_text(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
