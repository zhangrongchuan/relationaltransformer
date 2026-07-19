"""Inference-time context scaling probe (free precursor to training scaling).

Message passing is size-agnostic: a model trained at seq_len=2048 can consume
larger graphs at inference. Evaluate existing best checkpoints at increasing
context budgets to preview whether more context helps before paying for
retraining.
"""

import json
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from experiments.exp2_rowgraph.rowgraph_model import RowGraphNet  # noqa: E402
from experiments.exp2_rowgraph.rowgraph_train import (  # noqa: E402
    evaluate, make_ds,
)

CKPTS = {
    "dropE09_no_warm_s0": {},
    "no_warm_s0": {},
}
SIZES = [2048, 4096, 8192]
DB, TABLE, COL = "rel-f1", "driver-dnf", "did_not_finish"


def main():
    device = "cuda"
    torch.multiprocessing.set_sharing_strategy("file_system")
    out = []
    for name, flags in CKPTS.items():
        net = RowGraphNet(**flags).to(device)
        ckpt = Path(f"ckpts/rowgraph/{DB}_{TABLE}_{name}/best.pt")
        net.load_state_dict(torch.load(ckpt, map_location="cpu"))
        net.eval()
        for size in SIZES:
            rec = {"ckpt": name, "seq_len": size}
            for split in ["val", "test"]:
                for mode, drop in [("normal", 0.0), ("noself", 1.0)]:
                    ds = make_ds([(DB, TABLE, COL, [])], split, size, 0, drop)
                    m, n = evaluate(net, ds, "clf", device)
                    rec[f"{split}_{mode}"] = round(m, 4)
            out.append(rec)
            print(json.dumps(rec), flush=True)
    Path("experiments/results/context_scaling_probe.json").write_text(
        json.dumps(out, indent=2)
    )


if __name__ == "__main__":
    main()
