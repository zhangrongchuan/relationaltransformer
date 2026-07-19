"""Minimal single-process driver to STEP THROUGH RowGraphNet.forward.

The training script uses multiprocessing DataLoaders (hard to debug) and a
full loop. This loads ONE F1 batch single-process (num_workers=0) and calls
forward once, so breakpoints in rowgraph_model.py fire immediately on the
first (and only) call. Ideal for understanding the model code.

How to use:
  - set a breakpoint inside RowGraphNet.forward (rowgraph_model.py)
  - launch this via .vscode "① Debug 模型前向" config, or:
      pixi run python experiments/exp2_rowgraph/debug_forward.py [variant] [seq_len]
  - step through; shapes are printed at each milestone below

Args (all optional):
  variant  : full | no_warm | relgraph_no_warm | dropE09_no_warm | ...
  seq_len  : cells per sample (small = smaller graph, default 512)
"""

import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from rt.data import RelationalDataset  # noqa: E402
from experiments.exp2_rowgraph.rowgraph_model import RowGraphNet  # noqa: E402
from experiments.exp2_rowgraph.rowgraph_train import VARIANTS  # noqa: E402

# ---- knobs (also overridable via argv) -------------------------------------
DB, TABLE, TARGET = "rel-f1", "driver-dnf", "did_not_finish"
variant = sys.argv[1] if len(sys.argv) > 1 else "relgraph_no_warm"
seq_len = int(sys.argv[2]) if len(sys.argv) > 2 else 512
BATCH = 4
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def main():
    print(f"[debug] variant={variant} seq_len={seq_len} device={DEVICE}")

    cfg = dict(VARIANTS[variant])
    cfg.pop("train_label_dropout", None)  # not a model arg
    cfg.pop("warm_start", None)  # not a model arg (only affects weights)
    net = RowGraphNet(n_layers=cfg.pop("n_layers", 6), **cfg).to(DEVICE)
    print(f"[debug] model params = {sum(p.numel() for p in net.parameters()):,}")

    # single-process dataset — NO DataLoader, so everything is in this process
    ds = RelationalDataset(
        tasks=[(DB, TABLE, TARGET, "val", [])],
        batch_size=BATCH, seq_len=seq_len, rank=0, world_size=1,
        max_bfs_width=256, embedding_model="all-MiniLM-L12-v2",
        d_text=384, seed=0,
    )
    batch = ds[0]                      # <-- one batch of raw cells
    batch.pop("true_batch_size")
    for k in batch:
        batch[k] = batch[k].to(DEVICE)

    print("\n[debug] === INPUT (raw cells from sampler) ===")
    print(f"  node_idxs      {tuple(batch['node_idxs'].shape)}  (谁属于哪一行)")
    print(f"  is_targets sum {int(batch['is_targets'].sum())}   (要预测的空)")
    print(f"  非padding格子   {int((~batch['is_padding']).sum())}")

    # <<< SET YOUR BREAKPOINT INSIDE RowGraphNet.forward AND STEP FROM HERE >>>
    out = net(batch)

    print("\n[debug] === OUTPUT ===")
    print(f"  loss           {out['loss'].item():.4f}")
    if "clf_logit" in out:
        print(f"  clf_logit      {tuple(out['clf_logit'].shape)}  (每个图 True-False 的分差)")
    if "reg_pred" in out:
        print(f"  reg_pred       {tuple(out['reg_pred'].shape)}")

    # exercise the backward too, so you can inspect gradients
    out["loss"].backward()
    gsum = sum(p.grad.abs().sum().item() for p in net.parameters()
               if p.grad is not None)
    print(f"\n[debug] backward OK, grad 绝对值总和 = {gsum:.1f}")
    print("[debug] done.")


if __name__ == "__main__":
    main()
