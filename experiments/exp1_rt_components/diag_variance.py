"""L0 Diagnostic 3: context-resampling variance of RT predictions (GPU).

For each task: load the zero-shot checkpoint (pretrain_{db}_{task}.pt =
leave-db-out pretraining), evaluate the SAME val targets K times with
different sampled contexts (sampler epoch 0..K-1), and measure:

  - per-target prediction std across resamples
  - single-context metric (mean/std over the K runs)
  - ensemble metric (mean prediction across K contexts)
  - decision flip rate (clf): fraction of targets that cross the global
    median score across resamples

If ensemble >> single-context, sampling noise is a real bottleneck.

Usage: pixi run python experiments/diag_variance.py [task_index ...]
Outputs experiments/results/diag_variance.json (incremental)
"""

import json
import sys
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import r2_score, roc_auc_score
from torch.utils.data import DataLoader

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from rt.data import RelationalDataset  # noqa: E402
from rt.model import RelationalTransformer  # noqa: E402

CKPT_DIR = Path("~/scratch/rt_ckpts").expanduser()

TASKS = [
    # (db, table, target_col, drop_cols, task_type, K resamples)
    # full val pass per resample; K chosen so runtime stays bounded
    ("rel-f1", "driver-dnf", "did_not_finish", [], "clf", 8),
    ("rel-f1", "driver-position", "position", [], "reg", 8),
    ("rel-trial", "study-outcome", "outcome", [], "clf", 8),
    ("rel-avito", "ad-ctr", "num_click", [], "reg", 8),
    ("rel-event", "user-repeat", "target", [], "clf", 8),
    ("rel-event", "user-attendance", "target", [], "reg", 8),
    ("rel-avito", "user-clicks", "num_click", [], "clf", 8),
    ("rel-hm", "user-churn", "churn", [], "clf", 4),
]


def build_model(device):
    net = RelationalTransformer(
        num_blocks=12, d_model=256, d_text=384, num_heads=8, d_ff=1024
    )
    return net.to(device).to(torch.bfloat16)


@torch.inference_mode()
def eval_epoch(net, ds, task_type, device, epoch):
    """One pass over val targets with contexts sampled at `epoch` seed."""
    ds.sampler.shuffle_py(epoch)
    loader = DataLoader(ds, batch_size=None, num_workers=6, pin_memory=True)
    preds, labels = {}, {}
    n = 0
    for batch in loader:
        true_bs = batch.pop("true_batch_size")
        for k in batch:
            batch[k] = batch[k].to(device, non_blocking=True)
        batch["masks"][true_bs:, :] = False
        batch["is_targets"][true_bs:, :] = False
        batch["is_padding"][true_bs:, :] = True

        _, yhat_dict = net(batch)
        it = batch["is_targets"]
        if task_type == "clf":
            yhat = yhat_dict["boolean"][it].flatten()
            y = batch["boolean_values"][it].flatten()
        else:
            yhat = yhat_dict["number"][it].flatten()
            y = batch["number_values"][it].flatten()
        node_ids = batch["node_idxs"][it].flatten()

        for nid, p, yy in zip(
            node_ids.tolist(), yhat.float().tolist(), y.float().tolist()
        ):
            if nid not in preds:
                preds[nid] = p
                labels[nid] = yy
                n += 1
    return preds, labels


def metric_fn(task_type, y, p):
    if task_type == "clf":
        yb = (np.array(y) > 0).astype(int)
        return float(roc_auc_score(yb, p))
    return float(r2_score(y, p))


def run_task(db, table, target_col, drop_cols, task_type, K, device):
    ckpt = CKPT_DIR / f"pretrain_{db}_{table}.pt"
    net = build_model(device)
    net.load_state_dict(torch.load(ckpt, map_location="cpu"))
    net.eval()

    ds = RelationalDataset(
        tasks=[(db, table, target_col, "val", drop_cols)],
        batch_size=32,
        seq_len=1024,
        rank=0,
        world_size=1,
        max_bfs_width=256,
        embedding_model="all-MiniLM-L12-v2",
        d_text=384,
        seed=0,
    )

    all_preds, all_labels = [], None
    for epoch in range(K):
        preds, labels = eval_epoch(net, ds, task_type, device, epoch)
        all_preds.append(preds)
        if all_labels is None:
            all_labels = labels
        print(f"  epoch {epoch}: {len(preds)} targets", flush=True)

    # intersect target ids present in all runs
    ids = set(all_preds[0])
    for p in all_preds[1:]:
        ids &= set(p)
    ids = sorted(ids)
    P = np.array([[all_preds[e][i] for i in ids] for e in range(K)])  # (K, N)
    y = np.array([all_labels[i] for i in ids])

    single = [metric_fn(task_type, y, P[e]) for e in range(K)]
    ens = metric_fn(task_type, y, P.mean(0))

    out = {
        "db": db,
        "table": table,
        "task_type": task_type,
        "n_targets": len(ids),
        "K": K,
        "pred_std_mean": round(float(P.std(0).mean()), 4),
        "pred_std_p90": round(float(np.percentile(P.std(0), 90)), 4),
        "single_metric_mean": round(float(np.mean(single)), 4),
        "single_metric_std": round(float(np.std(single)), 4),
        "ensemble_metric": round(ens, 4),
        "ensemble_gain": round(ens - float(np.mean(single)), 4),
    }
    if task_type == "clf":
        med = np.median(P, axis=None)
        above = P > med
        flip = (above.any(0) & (~above).any(0)).mean()
        out["decision_flip_rate"] = round(float(flip), 3)
    return out


def main():
    device = "cuda"
    sel = [int(a) for a in sys.argv[1:]] or list(range(len(TASKS)))
    out_path = Path(__file__).parents[1] / "results" / "diag_variance.json"
    results = []
    if out_path.exists():
        results = json.loads(out_path.read_text())
    done = {(r["db"], r["table"]) for r in results}

    for i in sel:
        db, table, target_col, drop_cols, ttype, K = TASKS[i]
        if (db, table) in done:
            print(f"skip {db}/{table} (done)")
            continue
        print(f"=== {db}/{table} ===", flush=True)
        try:
            r = run_task(db, table, target_col, drop_cols, ttype, K, device)
            results.append(r)
            print(json.dumps(r, indent=1), flush=True)
        except Exception as e:
            import traceback

            traceback.print_exc()
            results.append({"db": db, "table": table, "error": str(e)[:300]})
        out_path.write_text(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
