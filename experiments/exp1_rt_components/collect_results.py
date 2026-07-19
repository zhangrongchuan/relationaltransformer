"""Collect metrics from train_*.out logs into a comparison table.

Parses eval lines printed by rt.main:
    step=NNN, \t{auc|r2}/{db}/{table}/{split}: value
Model selection: best val step; reports test metric at that step.
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

PAT = re.compile(
    r"step=(\d+),\s*\t?(auc|r2)/([\w-]+)/([\w-]+)/(val|test): ([-\d.]+)"
)
# db and table never contain '_'; the variant may (e.g. drop05_local32)
NAME_PAT = re.compile(r"train_([^_]+)_([^_]+)_(.+)_s(\d+)_(\d+)\.out")


def parse_log(path):
    """-> {(db, table): {step: {'val': x, 'test': y}}}"""
    traj = defaultdict(dict)
    for line in open(path, errors="replace"):
        m = PAT.search(line)
        if m:
            step, _metric, db, table, split, val = m.groups()
            traj[(db, table)].setdefault(int(step), {})[split] = float(val)
    return traj


def summarize(traj):
    out = {}
    for key, steps in traj.items():
        rows = [
            (s, v.get("val"), v.get("test"))
            for s, v in sorted(steps.items())
            if v.get("val") is not None and v.get("test") is not None
        ]
        if not rows:
            continue
        best = max(rows, key=lambda r: r[1])
        out[key] = {
            "step0_val": rows[0][1],
            "step0_test": rows[0][2],
            "best_step": best[0],
            "best_val": best[1],
            "test_at_best_val": best[2],
            "last_step": rows[-1][0],
            "n_evals": len(rows),
        }
    return out


def main():
    res_dir = Path(__file__).parents[1] / "results"
    records = []
    for f in sorted(res_dir.glob("train_*.out")):
        m = NAME_PAT.match(f.name)
        if not m:
            continue
        db, table, variant, seed, jobid = m.groups()
        for (edb, etable), s in summarize(parse_log(f)).items():
            records.append(
                dict(
                    db=edb, table=etable, variant=variant, seed=int(seed),
                    jobid=int(jobid), **s,
                )
            )

    with open(res_dir / "variant_results.json", "w") as f:
        json.dump(records, f, indent=2)

    # table: task x variant
    tasks = sorted({(r["db"], r["table"]) for r in records})
    variants = sorted({r["variant"] for r in records})
    print(f"{'task':34s} | " + " | ".join(f"{v:>22s}" for v in variants))
    print("-" * (36 + 25 * len(variants)))
    for db, table in tasks:
        cells = []
        for v in variants:
            rs = [
                r for r in records
                if r["db"] == db and r["table"] == table and r["variant"] == v
            ]
            if rs:
                r = max(rs, key=lambda x: x["jobid"])
                cells.append(
                    f"v{r['best_val']:.4f}/t{r['test_at_best_val']:.4f}"
                )
            else:
                cells.append("-")
        print(f"{db+'/'+table:34s} | " + " | ".join(f"{c:>22s}" for c in cells))
    print("\n(v=best val, t=test at best-val step; step0 = zero-shot before contd steps)")

    # zero-shot (step 0) comparison
    print(f"\n{'task':34s} | step0 (pre-contd) per variant")
    for db, table in tasks:
        cells = []
        for v in variants:
            rs = [
                r for r in records
                if r["db"] == db and r["table"] == table and r["variant"] == v
            ]
            if rs:
                r = max(rs, key=lambda x: x["jobid"])
                cells.append(f"{v}: v{r['step0_val']:.4f}")
            else:
                cells.append(f"{v}: -")
        print(f"{db+'/'+table:34s} | " + " | ".join(cells))


if __name__ == "__main__":
    main()
