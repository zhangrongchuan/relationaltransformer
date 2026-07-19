"""Merge eval_paper_table_*.json and print the paper-aligned comparison."""

import json
from pathlib import Path

import numpy as np

RES = Path(__file__).parents[1] / "results"


def main():
    rows = {}
    for f in sorted(RES.glob("eval_paper_table_*.json")):
        for r in json.loads(f.read_text()):
            rows[(r["db"], r["table"], r["sampler"])] = r

    tasks = sorted({(r["db"], r["table"]) for r in rows.values()})
    print(
        f"{'task':28s} {'paper':>6s} {'ours-base':>12s} {'pcap4':>12s} "
        f"{'l32+pcap4':>12s} {'ens(base)':>10s} {'n':>8s}"
    )
    cols = {"paper": [], "base": [], "pcap": [], "lp": [], "ens": []}
    for db, table in tasks:
        b = rows.get((db, table, "baseline"))
        p = rows.get((db, table, "pcap4"))
        l = rows.get((db, table, "local32_pcap4"))
        if not b:
            continue

        def fmt(r):
            if not r:
                return "-"
            s = f"{r['single_mean']*100:.1f}"
            if r["K"] > 1:
                s += f"±{r['single_std']*100:.1f}"
            return s

        ens = f"{b['ensemble']*100:.1f}" if b and "ensemble" in b else "-"
        print(
            f"{db+'/'+table:28s} {b['paper_zero_shot']:>6.1f} {fmt(b):>12s} "
            f"{fmt(p):>12s} {fmt(l):>12s} {ens:>10s} {b['n']:>8,}"
        )
        cols["paper"].append(b["paper_zero_shot"])
        cols["base"].append(b["single_mean"] * 100)
        cols["pcap"].append((p or b)["single_mean"] * 100)
        cols["lp"].append((l or b)["single_mean"] * 100)
        cols["ens"].append(
            b["ensemble"] * 100 if "ensemble" in b else b["single_mean"] * 100
        )
    n = len(cols["paper"])
    if n:
        print("-" * 100)
        print(
            f"{'MEAN over ' + str(n) + ' tasks':28s} "
            f"{np.mean(cols['paper']):>6.1f} {np.mean(cols['base']):>12.1f} "
            f"{np.mean(cols['pcap']):>12.1f} {np.mean(cols['lp']):>12.1f} "
            f"{np.mean(cols['ens']):>10.1f}"
        )
        print("\n(ens uses baseline single where K=1; pcap/l32 fall back to "
              "baseline if missing)")


if __name__ == "__main__":
    main()
