"""Step 0: row-level coverage stats for the row-graph backbone.

RT reads 1024 CELLS (~100 rows). A row-graph GNN reads ROWS as nodes, so the
same sampling budget covers far more rows. This measures rows/edges per
budget to motivate the backbone switch.
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from rt.data import RelationalDataset  # noqa: E402

TASKS = [
    ("rel-f1", "driver-dnf", "did_not_finish"),
    ("rel-trial", "study-outcome", "outcome"),
    ("rel-amazon", "user-churn", "churn"),
    ("rel-event", "user-repeat", "target"),
]
BUDGETS = [1024, 2048, 4096]


def stats(db, table, col, seq_len, n_seqs=64):
    ds = RelationalDataset(
        tasks=[(db, table, col, "val", [])],
        batch_size=8, seq_len=seq_len, rank=0, world_size=1,
        max_bfs_width=256, embedding_model="all-MiniLM-L12-v2",
        d_text=384, seed=0,
    )
    ds.sampler.shuffle_py(0)
    rows, edges = [], []
    for bi in range(min(n_seqs // 8, len(ds))):
        item = ds[bi]
        node = item["node_idxs"].numpy()
        f2p = item["f2p_nbr_idxs"].numpy()
        pad = item["is_padding"].numpy()
        for s in range(item["true_batch_size"]):
            valid = ~pad[s]
            uniq = set(node[s][valid].tolist())
            rows.append(len(uniq))
            e = 0
            seen = set()
            for i in np.where(valid)[0]:
                n = node[s, i]
                if n in seen:
                    continue
                seen.add(n)
                for p in f2p[s, i]:
                    if p >= 0 and p in uniq:
                        e += 1
            edges.append(e)
    return float(np.mean(rows)), float(np.mean(edges))


def main():
    print(f"{'task':26s} {'budget':>7s} {'rows':>8s} {'edges':>8s}")
    for db, table, col in TASKS:
        base_rows = None
        for b in BUDGETS:
            r, e = stats(db, table, col, b)
            mult = f"({r / base_rows:.1f}x)" if base_rows else "(1.0x)"
            if base_rows is None:
                base_rows = r
            print(f"{db + '/' + table:26s} {b:>7d} {r:>8.0f} {mult:>7s} {e:>8.0f}", flush=True)


if __name__ == "__main__":
    main()
