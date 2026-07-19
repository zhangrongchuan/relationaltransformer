"""Unified entrypoint for component experiments.

Protocol: cross-db continued pretraining.
  - start from the leave-db-out checkpoint pretrain_{db}_{table}.pt
  - continue pretraining on the SAME distribution it was trained on
    (all tasks from all dbs EXCEPT the eval db) with the variant mechanism
    active, so the mechanism adapts without domain shift
  - eval task stays fully zero-shot (its db never seen in training)
  - identical steps / lr / seed across variants -> compute-matched comparison

(We first tried same-db contd-pretraining, but it degrades the eval task from
step 0 via catastrophic forgetting, masking component effects.)

Usage:
  pixi run python experiments/train_variant.py <db> <table> <variant> [seed]
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from rt.main import main  # noqa: E402
from rt.tasks import all_tasks, forecast_tasks  # noqa: E402

VARIANTS = {
    "baseline": {},
    "rope": {"time_rope": True},
    "eflag": {"entity_flag": True},
    "rope_eflag": {"time_rope": True, "entity_flag": True},
    # B: anti-shortcut label dropout (train-time only)
    "drop05": {"self_label_dropout": 0.5},
    "drop09": {"self_label_dropout": 0.9},
    # C: local/global sampling (train + eval contexts)
    "local32": {"local_k": 32, "eval_local_k": 32},
    # B x C
    "drop05_local32": {
        "self_label_dropout": 0.5, "local_k": 32, "eval_local_k": 32,
    },
    # combos with model-side components
    "rope_local32": {"time_rope": True, "local_k": 32, "eval_local_k": 32},
    # budget control: periphery rows capped to 4 cells
    "pcap4": {"periphery_cell_cap": 4, "eval_periphery_cell_cap": 4},
    "local32_pcap4": {
        "local_k": 32, "eval_local_k": 32,
        "periphery_cell_cap": 4, "eval_periphery_cell_cap": 4,
    },
}

if __name__ == "__main__":
    db, table, variant = sys.argv[1], sys.argv[2], sys.argv[3]
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    scratch = len(sys.argv) > 5 and sys.argv[5] == "scratch"
    flags = VARIANTS[variant]

    eval_task = [t for t in forecast_tasks if t[0] == db and t[1] == table]
    assert len(eval_task) == 1, eval_task

    tag = "scratch" if scratch else "contd"
    main(
        project="rt-variants",
        eval_splits=["val", "test"],
        eval_freq=8192 if scratch else 1024,
        eval_pow2=False,
        max_eval_steps=64,
        # scratch: from-scratch leave-db-out pretraining (the definitive test
        # for training-time mechanisms: the shortcut must never form)
        load_ckpt_path=None if scratch
        else f"~/scratch/rt_ckpts/pretrain_{db}_{table}.pt",
        save_ckpt_dir=f"ckpts/variants/{db}_{table}_{variant}_{tag}_s{seed}"
        if scratch else f"ckpts/variants/{db}_{table}_{variant}_s{seed}",
        compile_=True,
        seed=seed,
        # leave-db-out mix; eval task's db never seen -> zero-shot eval
        train_tasks=[t for t in all_tasks if t[0] != db],
        eval_tasks=eval_task,
        batch_size=32,
        num_workers=8,
        max_bfs_width=256,
        lr=1e-3 if scratch else 1e-4,
        wd=0.1 if scratch else 0.0,
        lr_schedule=scratch,
        max_grad_norm=1.0,
        max_steps=50_001 if scratch else 2**13 + 1,
        embedding_model="all-MiniLM-L12-v2",
        d_text=384,
        seq_len=1024,
        num_blocks=12,
        d_model=256,
        num_heads=8,
        d_ff=1024,
        **flags,
    )
