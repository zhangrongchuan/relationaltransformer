"""Two final tables over all seeds: (A) mean±std, (B) best-seed.

Sources per (task, config):
  - s0: original sweep FINAL_FULL (evaljob_sw_*) or single-task fills
  - s1/s2: multi-seed FINAL_FULL (evaljob_ms_*)
All numbers are full-test evals of the combined-selection best checkpoint.
"""

import glob
import json
import statistics as st
from collections import defaultdict
from pathlib import Path

RES = Path(__file__).resolve().parents[1] / "results"
ARCH = RES.parent / "results-step1-exp1&exp2 early test"  # 第一阶段归档
DIRS = [RES, RES / "res_classification", ARCH, ARCH / "res_classification"]


def gl(pattern):
    """glob a pattern across both the live and archived results dirs."""
    out = []
    for d in DIRS:
        out.extend(glob.glob(str(d / pattern)))
    return out

PAPER = {
    ("rel-amazon", "item-churn"): (70.9, 51.8), ("rel-amazon", "user-churn"): (64.0, 54.9),
    ("rel-avito", "user-clicks"): (59.5, 53.9), ("rel-avito", "user-visits"): (61.8, 47.9),
    ("rel-f1", "driver-dnf"): (81.2, 69.7), ("rel-f1", "driver-top3"): (89.3, 46.3),
    ("rel-hm", "user-churn"): (62.8, 39.6), ("rel-stack", "user-badge"): (80.1, 54.3),
    ("rel-stack", "user-engagement"): (75.7, 49.9), ("rel-trial", "study-outcome"): (51.8, 52.3),
}
ORDER = list(PAPER)
FILLS = {  # s0 of the two tasks run before the sweep
    ("rel-f1", "driver-dnf", "rob"): (80.1, 74.0),
    ("rel-f1", "driver-dnf", "score"): (82.0, 70.2),
    ("rel-trial", "study-outcome", "rob"): (51.3, 51.3),
    ("rel-trial", "study-outcome", "score"): (52.2, 52.2),
}


def collect():
    """-> {(db, table, cfg): [(normal, noself), ...]}"""
    out = defaultdict(list)
    for k, v in FILLS.items():
        out[k].append(v)
    pats = ["evaljob_sw_*.out", "evaljob_ms_*.out", "evaljob_badge_finaleval_*.out"]
    for pat in pats:
        for f in gl(pat):
            for line in open(f, errors="replace"):
                if "FINAL_FULL " in line:
                    d = json.loads(line[line.index("{"):])
                    tag = d["tag"]
                    for (db, tbl) in ORDER:
                        if tag.startswith(f"{db}_{tbl}_"):
                            cfg = ("rob" if "dropE09" in tag
                                   else "score" if "relgraph" in tag else None)
                            if cfg:
                                out[(db, tbl, cfg)].append(
                                    (d["test_normal"] * 100, d["test_noself"] * 100)
                                )
                            break
    return out


def agg(vals, idx):
    xs = [v[idx] for v in vals]
    if not xs:
        return None
    return (sum(xs) / len(xs), st.pstdev(xs) if len(xs) > 1 else 0.0, max(xs), len(xs))


def main():
    data = collect()
    for title, mode in [("表A：均值±标准差（跨 seed）", "avg"), ("表B：最佳 seed", "best")]:
        print(f"\n{'=' * 96}\n{title}\n{'=' * 96}")
        print(f"{'task':24s} | {'官方RT n/ns':>14s} | {'鲁棒王2M n/ns':>22s} | {'分数王11M n/ns':>22s}")
        print("-" * 96)
        acc = defaultdict(list)
        for k in ORDER:
            pn, ps = PAPER[k]
            cells = [f"{pn:.1f}/{ps:.1f}"]
            for cfg in ("rob", "score"):
                vals = data.get((*k, cfg), [])
                an, as_ = agg(vals, 0), agg(vals, 1)
                if not an:
                    cells.append("…")
                    continue
                if mode == "avg":
                    cells.append(f"{an[0]:.1f}±{an[1]:.1f}/{as_[0]:.1f}±{as_[1]:.1f}(n{an[3]})")
                    acc[cfg + "_n"].append(an[0]); acc[cfg + "_s"].append(as_[0])
                else:
                    cells.append(f"{an[2]:.1f}/{as_[2]:.1f}")
                    acc[cfg + "_n"].append(an[2]); acc[cfg + "_s"].append(as_[2])
            print(f"{k[0] + '/' + k[1]:24s} | {cells[0]:>14s} | {cells[1]:>22s} | {cells[2]:>22s}")
            acc["rt_n"].append(pn); acc["rt_s"].append(ps)
        print("-" * 96)
        m = lambda x: sum(acc[x]) / len(acc[x]) if acc[x] else 0
        print(f"{'MEAN 正常':24s} | {m('rt_n'):>14.1f} | {m('rob_n'):>22.1f} | {m('score_n'):>22.1f}")
        print(f"{'MEAN 无标签':24s} | {m('rt_s'):>14.1f} | {m('rob_s'):>22.1f} | {m('score_s'):>22.1f}")
        print(f"{'删标签掉幅':24s} | {m('rt_n')-m('rt_s'):>14.1f} | "
              f"{m('rob_n')-m('rob_s'):>22.1f} | {m('score_n')-m('score_s'):>22.1f}")


if __name__ == "__main__":
    main()
