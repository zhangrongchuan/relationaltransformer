"""Final 3-way x 2-column comparison table (paper clf tasks).

Columns per task:
  官方RT: normal / noself   (paper number for normal ref, our measured noself)
  鲁棒王 dropE09_no_warm d256: normal / noself
  分数王 relgraph_no_warm d512: normal / noself
"""

import glob
import json
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

PAPER_NORMAL = {
    ("rel-amazon", "item-churn"): 70.9, ("rel-amazon", "user-churn"): 64.0,
    ("rel-avito", "user-clicks"): 59.5, ("rel-avito", "user-visits"): 61.8,
    ("rel-f1", "driver-dnf"): 81.2, ("rel-f1", "driver-top3"): 89.3,
    ("rel-hm", "user-churn"): 62.8, ("rel-stack", "user-badge"): 80.1,
    ("rel-stack", "user-engagement"): 75.7, ("rel-trial", "study-outcome"): 51.8,
}
ORDER = list(PAPER_NORMAL.keys())


def load_rt():
    d = {}
    for f in gl("rt_noself_rel-*.json"):
        r = json.load(open(f))
        d[(r["db"], r["table"])] = (
            (r["normal"] or 0) * 100, (r["noself"] or 0) * 100
        )
    return d


def load_ours():
    rob, score = {}, {}
    # from sweep FINAL_FULL + single-task fills
    fills = {
        ("rel-f1", "driver-dnf", "rob"): (80.1, 74.0),
        ("rel-f1", "driver-dnf", "score"): (82.0, 70.2),
        ("rel-trial", "study-outcome", "rob"): (51.3, 51.3),
        ("rel-trial", "study-outcome", "score"): (52.2, 52.2),
    }
    for (db, tbl, cfg), v in fills.items():
        (rob if cfg == "rob" else score)[(db, tbl)] = v
    for f in gl("evaljob_sw_*.out") + gl("evaljob_badge_finaleval_*.out"):
        for line in open(f, errors="replace"):
            if "FINAL_FULL " in line:
                d = json.loads(line[line.index("{"):])
                tag = d["tag"]
                for (db, tbl) in ORDER:
                    if tag.startswith(f"{db}_{tbl}_"):
                        v = (d["test_normal"] * 100, d["test_noself"] * 100)
                        if "dropE09" in tag:
                            rob[(db, tbl)] = v
                        elif "relgraph" in tag:
                            score[(db, tbl)] = v
    return rob, score


def main():
    rt = load_rt()
    rob, score = load_ours()
    print(f"{'task':24s} | {'官方RT norm/nos':>16s} | "
          f"{'鲁棒王2M norm/nos':>17s} | {'分数王11M norm/nos':>18s}")
    print("-" * 86)
    agg = {"rt_n": [], "rt_s": [], "rb_n": [], "rb_s": [], "sc_n": [], "sc_s": []}
    for k in ORDER:
        rt_v = rt.get(k)
        rb_v = rob.get(k)
        sc_v = score.get(k)
        pn = PAPER_NORMAL[k]
        rt_str = f"{pn:.1f}/{rt_v[1]:.1f}" if rt_v else f"{pn:.1f}/…"
        rb_str = f"{rb_v[0]:.1f}/{rb_v[1]:.1f}" if rb_v else "…"
        sc_str = f"{sc_v[0]:.1f}/{sc_v[1]:.1f}" if sc_v else "…"
        print(f"{k[0] + '/' + k[1]:24s} | {rt_str:>16s} | {rb_str:>17s} | {sc_str:>18s}")
        if rt_v:
            agg["rt_n"].append(pn); agg["rt_s"].append(rt_v[1])
        if rb_v:
            agg["rb_n"].append(rb_v[0]); agg["rb_s"].append(rb_v[1])
        if sc_v:
            agg["sc_n"].append(sc_v[0]); agg["sc_s"].append(sc_v[1])
    print("-" * 86)
    m = lambda x: sum(x) / len(x) if x else 0
    print(f"{'MEAN normal':24s} | {'RT ' + f'{m(agg['rt_n']):.1f}':>16s} | "
          f"{'鲁棒 ' + f'{m(agg['rb_n']):.1f}':>17s} | {'分数 ' + f'{m(agg['sc_n']):.1f}':>18s}")
    print(f"{'MEAN noself':24s} | {'RT ' + f'{m(agg['rt_s']):.1f}':>16s} | "
          f"{'鲁棒 ' + f'{m(agg['rb_s']):.1f}':>17s} | {'分数 ' + f'{m(agg['sc_s']):.1f}':>18s}")
    print(f"\n无标签鲁棒性(normal-noself掉幅均值): "
          f"官方RT掉{m(agg['rt_n'])-m(agg['rt_s']):.1f} | "
          f"鲁棒王掉{m(agg['rb_n'])-m(agg['rb_s']):.1f} | "
          f"分数王掉{m(agg['sc_n'])-m(agg['sc_s']):.1f}")


if __name__ == "__main__":
    main()
