"""L0 Diagnostic 4: label-copy baselines (no learning).

Two baselines per forecast task:

  A. context-copy   : predict from self-label cells present in RT's sampled
                      1024-cell context (mean & most-recent variants).
                      = "what a pure copy model achieves with RT's retrieval"
  B. history-copy   : predict from the entity's FULL past label history in the
                      raw relbench task table (perfect retrieval ceiling).

Gap A vs B quantifies label information lost by random context sampling.
Comparing RT zero-shot vs these quantifies how much of RT is label copying.

CPU only. Outputs experiments/results/diag_copy_baseline.{json,md}
"""

import json
import sys
from pathlib import Path

import numpy as np
import polars as pl

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from rt.data import RelationalDataset, get_column_index  # noqa: E402
from rt.tasks import forecast_clf_tasks, forecast_reg_tasks  # noqa: E402
from sklearn.metrics import roc_auc_score, r2_score  # noqa: E402

SEQ_LEN = 1024
BATCH_SIZE = 32
MAX_TARGETS = 4096  # cap per task/split for the context-copy part
TS_MIN = -(2**31)
RELBENCH = Path("~/scratch/relbench").expanduser()


# ---------------------------------------------------------------- part A
def load_table_offsets(db_name):
    path = Path(f"~/scratch/pre/{db_name}/table_info.json").expanduser()
    with open(path) as f:
        info = json.load(f)
    return sorted(
        ((k, v["node_idx_offset"]) for k, v in info.items()),
        key=lambda kv: kv[1],
        reverse=True,
    )


def node_to_table(node_idx, offsets_desc):
    for name, off in offsets_desc:
        if node_idx >= off:
            return name
    return "?"


def context_copy(db, table, target_col, drop_cols, split, task_type):
    ds = RelationalDataset(
        tasks=[(db, table, target_col, split, drop_cols)],
        batch_size=BATCH_SIZE,
        seq_len=SEQ_LEN,
        rank=0,
        world_size=1,
        max_bfs_width=256,
        embedding_model="all-MiniLM-L12-v2",
        d_text=384,
        seed=0,
    )
    ds.sampler.shuffle_py(0)
    target_idx = get_column_index(target_col, table, db)
    offsets_desc = load_table_offsets(db)

    labels, pred_mean, pred_recent, n_self = [], [], [], []
    seen = set()
    n_batches = len(ds)
    for bi in range(n_batches):
        if len(labels) >= MAX_TARGETS:
            break
        item = ds[bi]
        true_bs = item["true_batch_size"]
        node_idxs = item["node_idxs"].numpy()
        f2p = item["f2p_nbr_idxs"].numpy()
        col_idxs = item["col_name_idxs"].numpy()
        is_target = item["is_targets"].numpy()
        is_pad = item["is_padding"].numpy()
        ts = item["timestamps"].numpy()
        boolv = item["boolean_values"].float().numpy()[:, :, 0]
        numv = item["number_values"].float().numpy()[:, :, 0]
        vals = boolv if task_type == "clf" else numv

        for s in range(true_bs):
            tpos = np.where(is_target[s])[0]
            if len(tpos) == 0:
                continue
            tpos = tpos[0]
            seed_node = int(node_idxs[s, tpos])
            if seed_node in seen:  # sampler wraps around on last batch
                continue
            seen.add(seed_node)
            seed_ents = set(int(x) for x in f2p[s, tpos] if x >= 0)
            task_table_name = node_to_table(seed_node, offsets_desc).split(":")[0]

            y = vals[s, tpos]
            sl_vals, sl_ts = [], []
            for i in np.where(~is_pad[s])[0]:
                if is_target[s, i] or int(node_idxs[s, i]) == seed_node:
                    continue
                if col_idxs[s, i] != target_idx:
                    continue
                tbl = node_to_table(int(node_idxs[s, i]), offsets_desc).split(":")[0]
                if tbl != task_table_name:
                    continue
                row_ents = set(int(x) for x in f2p[s, i] if x >= 0)
                if seed_ents & row_ents:
                    sl_vals.append(vals[s, i])
                    sl_ts.append(ts[s, i])

            labels.append(float(y))
            n_self.append(len(sl_vals))
            if sl_vals:
                pred_mean.append(float(np.mean(sl_vals)))
                pred_recent.append(float(sl_vals[int(np.argmax(sl_ts))]))
            else:
                pred_mean.append(np.nan)
                pred_recent.append(np.nan)

    labels = np.array(labels)
    pm, pr = np.array(pred_mean), np.array(pred_recent)
    # fallback for rows without self labels: train-agnostic constant
    fill = 0.5 if task_type == "clf" else 0.0
    pm_f = np.where(np.isnan(pm), fill, pm)
    pr_f = np.where(np.isnan(pr), fill, pr)

    def metric(y, p):
        try:
            if task_type == "clf":
                yb = (y > 0).astype(int)
                if len(set(yb)) < 2:
                    return None
                return round(float(roc_auc_score(yb, p)), 4)
            return round(float(r2_score(y, p)), 4)
        except Exception:
            return None

    return {
        "n": len(labels),
        "frac_no_self_label": round(float(np.isnan(pm).mean()), 3),
        "copy_mean": metric(labels, pm_f),
        "copy_recent": metric(labels, pr_f),
    }


# ---------------------------------------------------------------- part B
def load_task_parquet(db, table, split):
    base = RELBENCH / db / "tasks" / table
    p = base / f"{split}.parquet"
    return pl.read_parquet(p)


def detect_cols(df, target_col):
    ts_col = None
    for c, dt in df.schema.items():
        if dt in (pl.Datetime, pl.Date) or isinstance(dt, pl.Datetime):
            ts_col = c
            break
    ent_cols = [
        c for c in df.columns if c not in (ts_col, target_col, "index")
    ]
    assert ts_col is not None and len(ent_cols) == 1, (
        f"cols={list(df.columns)} ts={ts_col} ent={ent_cols}"
    )
    return ts_col, ent_cols[0]


def history_copy(db, table, target_col, eval_split, task_type):
    train = load_task_parquet(db, table, "train")
    ts_col, ent_col = detect_cols(train, target_col)
    ev = load_task_parquet(db, table, eval_split)
    if eval_split == "test" and (
        target_col not in ev.columns or ev[target_col].null_count() == len(ev)
    ):
        return None  # hidden test labels
    ev = ev.drop_nulls(subset=[target_col])
    # history = everything strictly before the eval row's timestamp,
    # including earlier rows of the eval split itself (temporally valid)
    hist_frames = [train.select([ts_col, ent_col, target_col])]
    if eval_split == "test":
        val = load_task_parquet(db, table, "val")
        if target_col in val.columns:
            hist_frames.append(val.select([ts_col, ent_col, target_col]))
    hist_frames.append(ev.select([ts_col, ent_col, target_col]))
    hist = pl.concat(hist_frames)

    hist = hist.sort(ts_col)
    global_mean = float(train[target_col].mean())

    # group history once: entity -> (ts int array, label array)
    ghist = {}
    for (k,), g in hist.group_by(ent_col):
        ghist[k] = (
            g[ts_col].cast(pl.Int64).to_numpy(),
            g[target_col].to_numpy(),
        )

    ev_ts = ev[ts_col].cast(pl.Int64).to_numpy()
    ev_ent = ev[ent_col].to_numpy()
    ev_y = ev[target_col].to_numpy()

    y, pm, pr, nh = [], [], [], []
    for rts, rent, ry in zip(ev_ts, ev_ent, ev_y):
        h = ghist.get(rent)
        if h is not None:
            mask = h[0] < rts
            vals = h[1][mask]
        else:
            vals = np.array([])
        y.append(float(ry))
        nh.append(len(vals))
        if len(vals):
            pm.append(float(np.nanmean(vals)))
            pr.append(float(vals[-1]))
        else:
            pm.append(global_mean)
            pr.append(global_mean)

    y = np.array(y)
    pm, pr = np.array(pm), np.array(pr)

    def metric(p):
        try:
            if task_type == "clf":
                yb = (y > 0).astype(int)
                if len(set(yb)) < 2:
                    return None
                return round(float(roc_auc_score(yb, p)), 4)
            return round(float(r2_score(y, p)), 4)
        except Exception:
            return None

    return {
        "n": len(y),
        "frac_no_history": round(float(np.mean(np.array(nh) == 0)), 3),
        "hist_mean": metric(pm),
        "hist_recent": metric(pr),
        "avg_history_len": round(float(np.mean(nh)), 1),
    }


def main():
    tasks = [(t, "clf") for t in forecast_clf_tasks] + [
        (t, "reg") for t in forecast_reg_tasks
    ]
    out_json = Path(__file__).parents[1] / "results" / "diag_copy_baseline.json"
    prev = {}
    if out_json.exists():
        prev = {(r["db"], r["table"]): r for r in json.loads(out_json.read_text())}
    results = []
    for (db, table, target_col, drop_cols), ttype in tasks:
        print(f"=== {db}/{table} ({ttype}) ===", flush=True)
        rec = {"db": db, "table": table, "task_type": ttype}
        cached = prev.get((db, table), {})
        if "context_val" in cached and "error" not in (cached["context_val"] or {}):
            rec["context_val"] = cached["context_val"]
        try:
            rec["history_val"] = history_copy(db, table, target_col, "val", ttype)
            print(f"  history val: {rec['history_val']}", flush=True)
        except Exception as e:
            rec["history_val"] = {"error": str(e)[:200]}
            print(f"  history val FAILED: {e}", flush=True)
        try:
            rec["history_test"] = history_copy(db, table, target_col, "test", ttype)
            print(f"  history test: {rec['history_test']}", flush=True)
        except Exception as e:
            rec["history_test"] = {"error": str(e)[:200]}
        if "context_val" not in rec:
            try:
                rec["context_val"] = context_copy(
                    db, table, target_col, drop_cols, "val", ttype
                )
                print(f"  context val: {rec['context_val']}", flush=True)
            except Exception as e:
                rec["context_val"] = {"error": str(e)[:200]}
                print(f"  context val FAILED: {e}", flush=True)
        results.append(rec)
        with open(
            Path(__file__).parents[1] / "results" / "diag_copy_baseline.json", "w"
        ) as f:
            json.dump(results, f, indent=2)

    # markdown
    lines = [
        "# L0 Diagnostic: label-copy baselines (val)",
        "",
        "| task | type | ctx-copy mean | ctx-copy recent | no-self-lbl % | hist-copy mean | hist-copy recent | no-hist % | hist len |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in results:
        c = r.get("context_val") or {}
        h = r.get("history_val") or {}
        lines.append(
            f"| {r['db']}/{r['table']} | {r['task_type']} "
            f"| {c.get('copy_mean')} | {c.get('copy_recent')} "
            f"| {c.get('frac_no_self_label', '')} "
            f"| {h.get('hist_mean')} | {h.get('hist_recent')} "
            f"| {h.get('frac_no_history', '')} | {h.get('avg_history_len', '')} |"
        )
    with open(Path(__file__).parents[1] / "results" / "diag_copy_baseline.md", "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
