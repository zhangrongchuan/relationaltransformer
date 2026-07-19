"""L0 Diagnostic 1+2: token budget composition and self-label statistics.

For each forecast task, sample N context sequences (val split) and classify
every cell by its structural relation to the target:

  target           the masked cell to predict
  seed_row         other cells of the seed (task-table) row
  self_label       task-table label cells of the SAME entity (the copy source)
  other_label      task-table label cells of OTHER entities
  task_other       task-table non-label cells (e.g. date)
  entity_row       cells of the entity row itself (driver/user/item...)
  event_direct     db-table cells whose row references the seed entity
  periphery        everything else (races/circuits/constructors... decoration)

Outputs per-task stats to experiments/results/diag_context.json + .md
Runs on CPU (sampler only, no model).
"""

import json
import os
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from rt.data import RelationalDataset, get_column_index  # noqa: E402
from rt.tasks import forecast_clf_tasks, forecast_reg_tasks  # noqa: E402

SEQ_LEN = 1024
BATCH_SIZE = 16
NUM_BATCHES = 16  # 256 sequences per task
TS_MIN = -(2**31)


def load_table_offsets(db_name):
    path = Path(f"~/scratch/pre/{db_name}/table_info.json").expanduser()
    with open(path) as f:
        info = json.load(f)
    # descending by offset for lookup: node_idx -> table full name
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


def analyze_task(db, table, target_col, drop_cols, split="val"):
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

    cell_counts = defaultdict(list)  # category -> per-seq cell count
    row_counts = defaultdict(list)  # category -> per-seq distinct row count
    self_label_counts = []
    event_dt_days = []  # Δt (days) of direct-event cells vs seed time
    self_label_dt_days = []
    periphery_tables = defaultdict(int)  # which tables eat the budget
    n_seqs = 0

    n_batches = min(NUM_BATCHES, len(ds))
    for bi in range(n_batches):
        item = ds[bi]
        true_bs = item["true_batch_size"]
        node_idxs = item["node_idxs"].numpy()
        f2p = item["f2p_nbr_idxs"].numpy()
        col_idxs = item["col_name_idxs"].numpy()
        is_target = item["is_targets"].numpy()
        is_pad = item["is_padding"].numpy()
        ts = item["timestamps"].numpy()

        for s in range(true_bs):
            tpos = np.where(is_target[s])[0]
            if len(tpos) == 0:
                continue
            tpos = tpos[0]
            seed_node = node_idxs[s, tpos]
            seed_ts = ts[s, tpos]
            seed_ents = set(int(x) for x in f2p[s, tpos] if x >= 0)
            task_table_name = node_to_table(seed_node, offsets_desc).split(":")[0]

            valid = ~is_pad[s]
            cats = np.empty(SEQ_LEN, dtype=object)

            # per-cell classification
            for i in np.where(valid)[0]:
                n = node_idxs[s, i]
                tbl_full = node_to_table(n, offsets_desc)
                tbl = tbl_full.split(":")[0]
                row_ents = set(int(x) for x in f2p[s, i] if x >= 0)
                shares = bool(seed_ents & row_ents)
                if is_target[s, i]:
                    cats[i] = "target"
                elif n == seed_node:
                    cats[i] = "seed_row"
                elif tbl == task_table_name:
                    if col_idxs[s, i] == target_idx:
                        cats[i] = "self_label" if shares else "other_label"
                    else:
                        cats[i] = "task_other"
                elif n in seed_ents:
                    cats[i] = "entity_row"
                elif shares:
                    cats[i] = "event_direct"
                    if ts[s, i] != TS_MIN and seed_ts != TS_MIN:
                        event_dt_days.append((seed_ts - ts[s, i]) / 86400.0)
                else:
                    cats[i] = "periphery"
                    periphery_tables[tbl] += 1
                if cats[i] == "self_label" and ts[s, i] != TS_MIN and seed_ts != TS_MIN:
                    self_label_dt_days.append((seed_ts - ts[s, i]) / 86400.0)

            n_seqs += 1
            n_valid = int(valid.sum())
            cell_counts["_total"].append(n_valid)
            for cat in [
                "target",
                "seed_row",
                "self_label",
                "other_label",
                "task_other",
                "entity_row",
                "event_direct",
                "periphery",
            ]:
                m = np.array([cats[i] == cat for i in range(SEQ_LEN)])
                cell_counts[cat].append(int(m.sum()))
                row_counts[cat].append(len(set(node_idxs[s, m].tolist())))
            self_label_counts.append(cell_counts["self_label"][-1])

    def stats(v):
        a = np.array(v, dtype=float)
        return {
            "mean": round(float(a.mean()), 2),
            "median": round(float(np.median(a)), 2),
            "p90": round(float(np.percentile(a, 90)), 2),
        }

    out = {
        "db": db,
        "table": table,
        "n_seqs": n_seqs,
        "cells": {k: stats(v) for k, v in cell_counts.items()},
        "rows": {k: stats(v) for k, v in row_counts.items()},
        "self_labels": {
            "mean": round(float(np.mean(self_label_counts)), 2),
            "frac_zero": round(
                float(np.mean(np.array(self_label_counts) == 0)), 3
            ),
        },
        "event_dt_days": stats(event_dt_days) if event_dt_days else None,
        "self_label_dt_days": stats(self_label_dt_days)
        if self_label_dt_days
        else None,
        "periphery_tables": dict(
            sorted(periphery_tables.items(), key=lambda kv: -kv[1])[:6]
        ),
    }
    return out


def main():
    tasks = [(t, "clf") for t in forecast_clf_tasks] + [
        (t, "reg") for t in forecast_reg_tasks
    ]
    results = []
    for (db, table, target_col, drop_cols), ttype in tasks:
        print(f"=== {db}/{table} ({ttype}) ===", flush=True)
        try:
            r = analyze_task(db, table, target_col, drop_cols)
            r["task_type"] = ttype
            results.append(r)
            print(
                f"  self_labels mean={r['self_labels']['mean']} "
                f"frac_zero={r['self_labels']['frac_zero']} "
                f"periphery={r['cells']['periphery']['mean']}/"
                f"{r['cells']['_total']['mean']}",
                flush=True,
            )
        except Exception as e:
            print(f"  FAILED: {e}", flush=True)
            results.append({"db": db, "table": table, "error": str(e)})

    out_dir = Path(__file__).parents[1] / "results"
    out_dir.mkdir(exist_ok=True)
    with open(out_dir / "diag_context.json", "w") as f:
        json.dump(results, f, indent=2)

    # markdown summary
    lines = [
        "# L0 Diagnostic: context composition (val split, 256 seqs/task)",
        "",
        "| task | type | self-lbl mean | 0-self-lbl % | event rows | periphery cells | periphery % | evt Δt med (d) | self-lbl Δt med (d) |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in results:
        if "error" in r:
            lines.append(f"| {r['db']}/{r['table']} | ERR | {r['error'][:40]} | | | | | | |")
            continue
        tot = r["cells"]["_total"]["mean"]
        peri = r["cells"]["periphery"]["mean"]
        lines.append(
            f"| {r['db']}/{r['table']} | {r['task_type']} "
            f"| {r['self_labels']['mean']} "
            f"| {r['self_labels']['frac_zero']*100:.0f}% "
            f"| {r['rows']['event_direct']['mean']} "
            f"| {peri} "
            f"| {peri/tot*100:.0f}% "
            f"| {r['event_dt_days']['median'] if r['event_dt_days'] else '-'} "
            f"| {r['self_label_dt_days']['median'] if r['self_label_dt_days'] else '-'} |"
        )
    with open(out_dir / "diag_context.md", "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
