"""Collect the all-task sweep FINAL_FULL results into the paper-comparison table.

Paper reference = the cross-model table's zero-shot ("No") RT column.
Ours = RowGraphNet robust king (dropE09_no_warm d256/50k) and score king
(relgraph_no_warm d512/100k), FINAL_FULL = full-split eval of the
combined-selection best checkpoint.
"""

import glob
import json
import re
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results"

PAPER_NO = {  # (db, table): paper zero-shot RT AUROC
    ("rel-amazon", "item-churn"): 70.9,
    ("rel-amazon", "user-churn"): 64.0,
    ("rel-avito", "user-clicks"): 59.5,
    ("rel-avito", "user-visits"): 61.8,
    ("rel-f1", "driver-dnf"): 81.2,
    ("rel-f1", "driver-top3"): 89.3,
    ("rel-hm", "user-churn"): 62.8,
    ("rel-stack", "user-badge"): 80.1,
    ("rel-stack", "user-engagement"): 75.7,
    ("rel-trial", "study-outcome"): 51.8,
}

# already-completed tasks (from earlier full-eval trajectories, combined sel.)
PRefilled = {
    ("rel-f1", "driver-dnf", "rob"): (80.1, 74.0),      # dropE09_no_warm best seed
    ("rel-f1", "driver-dnf", "score"): (82.0, 70.2),    # relgraph_no_warm_d512 best seed
    ("rel-trial", "study-outcome", "rob"): (51.3, 51.3),
    ("rel-trial", "study-outcome", "score"): (52.2, 52.2),  # d256 relgraph (no d512 run)
}


def main():
    rows = dict(PRefilled)
    for f in glob.glob(str(RES / "evaljob_sw_*.out")):
        cfg = "rob" if f.endswith("_rob.out") or "_rob_" in f else "score"
        for line in open(f, errors="replace"):
            if line.startswith("FINAL_FULL "):
                d = json.loads(line[11:])
                m = re.match(r"(rel-\w+)_([\w-]+?)_(?:dropE09_no_warm|relgraph_no_warm)", d["tag"])
                if not m:
                    continue
                db, table = m.group(1), m.group(2)
                rows[(db, table, cfg)] = (
                    d["test_normal"] * 100, d["test_noself"] * 100
                )

    print(f"{'task':26s} {'论文RT':>7s} {'鲁棒王':>8s} {'分数王':>8s} "
          f"{'鲁棒-无标签':>10s} {'分数-无标签':>10s}")
    tot = {"paper": [], "rob": [], "score": []}
    for (db, table), p in PAPER_NO.items():
        rb = rows.get((db, table, "rob"))
        sc = rows.get((db, table, "score"))
        fmt = lambda x, i=0: f"{x[i]:.1f}" if x else "…"
        print(f"{db + '/' + table:26s} {p:>7.1f} {fmt(rb):>8s} {fmt(sc):>8s} "
              f"{fmt(rb, 1):>10s} {fmt(sc, 1):>10s}")
        if rb and sc:
            tot["paper"].append(p)
            tot["rob"].append(rb[0])
            tot["score"].append(sc[0])
    if tot["paper"]:
        n = len(tot["paper"])
        avg = lambda k: sum(tot[k]) / n
        print("-" * 75)
        print(f"{'MEAN (' + str(n) + ' tasks done)':26s} {avg('paper'):>7.1f} "
              f"{avg('rob'):>8.1f} {avg('score'):>8.1f}")


if __name__ == "__main__":
    main()
