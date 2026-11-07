"""Train/eval entry for the RowGraphNet prototype (module-proof grid).

Protocol: from-scratch, leave-db-out (same task mix as RT-scratch baselines),
so results compare directly against our matched RT-scratch numbers.

Checkpoint selection sees the Standard VALIDATION split only.  Periodic evals
report the normal and the no-self-label validation metric (sampler
self_label_dropout=1.0), so label reliance is tracked continuously; the test
splits are evaluated exactly once, on the selected checkpoint, at the end.
The step-0 evaluation (untrained initialisation) is logged but never selected.

The training mixture depends only on the held-out database, so several eval
tasks of that database can share one training run (as RT does); each task
still selects, evaluates and archives its own checkpoint.

Usage:
  pixi run python rowgraph/train.py --db rel-f1 --task driver-dnf \
      --variant relgraph_no_warm --seed 0
  pixi run python rowgraph/train.py --db rel-f1 --task all-clf \
      --variant relgraph_no_warm --d-model 512 --seed 0

variants:
  full      = mp6 + time + label_edges + warm_start
  no_mp     = 0 message-passing layers
  no_time   = no Δt encoding
  no_labels = no has_label edges
  no_warm   = random-init cell encoders
  dropE09   = full + train-time label-edge dropout 0.9 (anti-shortcut)
"""

import argparse
import json
import os
import random
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import roc_auc_score
from torch.utils.data import DataLoader

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rt.data import RelationalDataset  # noqa: E402
from rt.tasks import all_tasks, forecast_clf_tasks  # noqa: E402
from rowgraph.model import RowGraphNet  # noqa: E402

VARIANTS = {
    "full": {},
    "no_mp": {"n_layers": 0},
    "no_time": {"use_time": False},
    "no_labels": {"use_label_edges": False},
    "no_warm": {"warm_start": False},
    "dropE09": {"train_label_dropout": 0.9},
    "dropE09_no_warm": {"train_label_dropout": 0.9, "warm_start": False},
    "dropE05_no_warm": {"train_label_dropout": 0.5, "warm_start": False},
    "attn": {"pool": "attn"},
    "attn_no_warm": {"pool": "attn", "warm_start": False},
    "attn_dropE09_no_warm": {
        "pool": "attn", "train_label_dropout": 0.9, "warm_start": False,
    },
    "relgraph_no_warm": {"use_relgraph": True, "warm_start": False},
    # ablation: no candidate nodes / label edges, MLP heads on the seed row;
    # context labels stay visible as cells of their task rows
    "relgraph_nocand_no_warm": {
        "use_relgraph": True, "use_candidates": False, "warm_start": False,
    },
    "relgraph_dropE09_no_warm": {
        "use_relgraph": True, "train_label_dropout": 0.9, "warm_start": False,
    },
}
CKPT = Path("~/scratch/rt_ckpts").expanduser()
REPO = Path(__file__).resolve().parents[1]


def default_out_dir():
    """Where results go, decided by which script was invoked — not by a flag.

    Run rowgraph/train.py (the production entry) -> <repo>/results
    Run anything under experiments/ (incl. the compat symlinks) -> experiments/results

    Uses argv[0] rather than __file__ because __file__ resolves symlinks and
    would collapse both entry points onto the same path.
    """
    inv = Path(sys.argv[0]).absolute()  # absolute(), not resolve(): keep symlink path
    if "experiments" in inv.parts:
        return REPO / "experiments" / "results"
    return REPO / "results"


def warm_start_encoders(net, db, table):
    sd = torch.load(CKPT / f"pretrain_{db}_{table}.pt", map_location="cpu")
    own = net.state_dict()
    loaded = 0
    for k, v in sd.items():
        if (k.startswith("enc_dict") or k.startswith("norm_dict")) and k in own:
            own[k].copy_(v.float())
            loaded += 1
    print(f"warm-started {loaded} encoder tensors", flush=True)


def make_ds(tasks, split, seq_len, seed, dropout=0.0):
    return RelationalDataset(
        tasks=[(d, t, c, split, dc) for d, t, c, dc in tasks],
        batch_size=32, seq_len=seq_len, rank=0, world_size=1,
        max_bfs_width=256, embedding_model="all-MiniLM-L12-v2",
        d_text=384, seed=seed, self_label_dropout=dropout,
    )


@torch.inference_mode()
def evaluate(net, ds, task_type, device, max_batches=None):
    if task_type != "clf":
        raise ValueError("Only classification evaluation is supported")
    net.eval()
    ds.sampler.shuffle_py(0)
    loader = DataLoader(ds, batch_size=None, num_workers=4, pin_memory=True)
    preds, ys = {}, {}
    for bi, batch in enumerate(loader):
        if max_batches is not None and bi >= max_batches:
            break
        tb = batch.pop("true_batch_size")
        for k in batch:
            batch[k] = batch[k].to(device, non_blocking=True)
        batch["masks"][tb:, :] = False
        batch["is_targets"][tb:, :] = False
        batch["is_padding"][tb:, :] = True
        if not batch["is_targets"].any():
            continue
        out = net(batch)
        node = batch["node_idxs"]
        tpos = batch["is_targets"].float().argmax(-1)
        seed_nodes = node[torch.arange(node.shape[0], device=device), tpos]
        if task_type == "clf" and "clf_logit" in out:
            for g, p, y in zip(
                out["clf_graphs"].tolist(),
                out["clf_logit"].float().tolist(),
                (out["clf_y"] > 0).long().tolist(),
            ):
                nid = int(seed_nodes[g])
                if nid not in preds:
                    preds[nid], ys[nid] = p, y
    net.train()
    ids = sorted(preds)
    y = np.array([ys[i] for i in ids])
    p = np.array([preds[i] for i in ids])
    return float(roc_auc_score(y, p)), len(ids)


def parse_args(argv):
    """Flags are preferred; the legacy positional form still works so that
    already-queued SLURM jobs keep running:
        train.py <db> <table> <variant> [seed] [steps] [seq_len] [d_model]
    """
    tasks = sorted({f"{t[0]}/{t[1]}" for t in forecast_clf_tasks})
    p = argparse.ArgumentParser(
        prog="rowgraph/train.py",
        description="Train RowGraphNet from scratch, leave-database-out "
                    "(the eval database is never seen during training).",
        epilog="eval tasks:\n  " + "\n  ".join(tasks),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--db", required=True, help="eval database, e.g. rel-f1")
    p.add_argument("--task", "--table", required=True, dest="tables",
                   nargs="+",
                   help="eval task(s) of --db, e.g. driver-dnf; several tasks, "
                        "or 'all-clf' for every classification task of --db, "
                        "share one training run")
    p.add_argument("--variant", required=True, choices=sorted(VARIANTS),
                   help="model configuration (see VARIANTS)")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--steps", type=int, default=100_000, dest="max_steps",
                   help="training steps (default: 100000)")
    p.add_argument("--seq-len", type=int, default=2048, dest="seq_len",
                   help="context length in cells (default: 2048)")
    p.add_argument("--d-model", type=int, default=256, dest="d_model",
                   help="model width (default: 256)")
    p.add_argument("--lr", type=float, default=1e-3,
                   help="peak learning rate of the one-cycle schedule "
                        "(default: 1e-3)")
    p.add_argument("--wd", type=float, default=0.1,
                   help="AdamW weight decay (default: 0.1)")
    p.add_argument("--out-dir", type=Path, default=default_out_dir(),
                   dest="out_dir",
                   help=f"results root (default: {default_out_dir()})")

    if len(argv) >= 3 and not argv[0].startswith("-"):  # legacy positional
        names = ["seed", "max_steps", "seq_len", "d_model"]
        defaults = [0, 20_000, 2048, 256]  # legacy default steps was 20k
        kw = {n: (int(argv[3 + i]) if len(argv) > 3 + i else d)
              for i, (n, d) in enumerate(zip(names, defaults))}
        print("NOTE: positional args are deprecated; use "
              "--db/--task/--variant/--seed/--steps/--seq-len/--d-model",
              flush=True)
        return argparse.Namespace(
            db=argv[0], tables=[argv[1]], variant=argv[2], lr=1e-3, wd=0.1,
            out_dir=default_out_dir(), **kw)
    return p.parse_args(argv)


def resolve_eval_tasks(db, tables):
    """--task names -> forecast task tuples of `db` ('all-clf' = every
    classification forecast task of the database)."""
    if tables == ["all-clf"]:
        specs = [t for t in forecast_clf_tasks if t[0] == db]
    else:
        specs = []
        for table in tables:
            match = [t for t in forecast_clf_tasks if t[0] == db and t[1] == table]
            assert len(match) == 1, f"unknown classification eval task {db}/{table}"
            specs.append(match[0])
    assert specs, f"no eval tasks for {db}"
    assert len({t[1] for t in specs}) == len(specs), "duplicate eval task"
    return specs


def main():
    args = parse_args(sys.argv[1:])
    db, variant = args.db, args.variant
    seed, max_steps, lr, wd = args.seed, args.max_steps, args.lr, args.wd
    seq_len, d_model = args.seq_len, args.d_model
    assert variant in VARIANTS, f"unknown variant {variant}; pick from {sorted(VARIANTS)}"
    assert max_steps > 0

    cfg = dict(VARIANTS[variant])
    train_dropout = cfg.pop("train_label_dropout", 0.0)
    warm = cfg.pop("warm_start", True)

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cpu":
        print("WARNING: no CUDA device found, running on CPU (very slow — "
              "use --steps for a short smoke test only)", flush=True)
    # required with many short-lived DataLoaders (rt/main.py does the same);
    # default fd-socket sharing exhausts descriptors and crashes mid-training
    torch.multiprocessing.set_sharing_strategy("file_system")
    torch.set_num_threads(1)

    eval_specs = resolve_eval_tasks(db, args.tables)

    if len(eval_specs) > 1:
        assert not warm, "warm start loads a per-task checkpoint; use one --task"
    net = RowGraphNet(
        d_model=d_model, n_layers=cfg.pop("n_layers", 6), **cfg
    ).to(device)
    if warm:
        assert d_model == 256, "warm start requires d_model=256"
        warm_start_encoders(net, db, eval_specs[0][1])
    n_params = sum(p.numel() for p in net.parameters())
    print(f"params={n_params:,}", flush=True)

    train_tasks = [t for t in all_tasks if t[0] != db]
    train_ds = make_ds(train_tasks, "train", seq_len, seed, dropout=train_dropout)

    opt = torch.optim.AdamW(net.parameters(), lr=lr, weight_decay=wd)
    sched = torch.optim.lr_scheduler.OneCycleLR(
        opt, max_lr=lr, total_steps=max_steps, pct_start=0.2,
        anneal_strategy="linear",
    )

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    suffix = ""
    if seq_len != 2048:
        suffix += f"_ctx{seq_len}"
    if d_model != 256:
        suffix += f"_d{d_model}"
    if lr != 1e-3:
        suffix += f"_lr{lr:g}"
    if wd != 0.1:
        suffix += f"_wd{wd:g}"
    # per-run archive: results/{model}/{dataset}/{task}/{start-timestamp}_s{seed}/
    # timestamp YYYYmmdd-HHMMSS is sortable, so `ls` lists runs chronologically
    model_id = f"rowgraph_{variant}{suffix}"
    started = datetime.now()

    # def _git(*args):
    #     try:
    #         return subprocess.check_output(
    #             ["git", *args], stderr=subprocess.DEVNULL, text=True
    #         ).strip()
    #     except Exception:
    #         return None

    # one job per eval task: own datasets, selection state and archive
    jobs = []
    for spec in eval_specs:
        table = spec[1]
        job = {
            "table": table,
            "task_type": "clf",
            "evals": {
                ("val", "normal"): make_ds([spec], "val", seq_len, 0, 0.0),
                ("val", "noself"): make_ds([spec], "val", seq_len, 0, 1.0),
                ("test", "normal"): make_ds([spec], "test", seq_len, 0, 0.0),
                ("test", "noself"): make_ds([spec], "test", seq_len, 0, 1.0),
            },
            "tag": f"{db}_{table}_{variant}_s{seed}{suffix}",
            "best_val": -1e9,
            "best_rec": None,
        }
        # legacy checkpoint location — kept exactly as before, never deleted
        job["ckpt_dir"] = Path("ckpts/rowgraph") / job["tag"]
        job["ckpt_dir"].mkdir(parents=True, exist_ok=True)
        # one directory per run: concurrent runs that finish loading in the
        # same second used to share it and overwrite each other's best.pt
        parent = out_dir / model_id / db / table
        parent.mkdir(parents=True, exist_ok=True)
        stem = f"{started.strftime('%Y%m%d-%H%M%S')}_s{seed}"
        for k in range(100):
            job["run_dir"] = parent / (stem if k == 0 else f"{stem}-{k}")
            try:
                job["run_dir"].mkdir()
                break
            except FileExistsError:
                continue
        else:
            raise RuntimeError(f"no free run directory under {parent}/{stem}")

        (job["run_dir"] / "config.json").write_text(json.dumps({
            "model_id": model_id, "variant": variant, "db": db, "table": table,
            "task_type": job["task_type"], "seed": seed, "max_steps": max_steps,
            "seq_len": seq_len, "d_model": d_model,
            "warm_start": warm, "train_label_dropout": train_dropout,
            "lr": lr, "weight_decay": wd, "batch_size": 32,
            "optimizer": "AdamW", "scheduler": "OneCycleLR(pct_start=0.2,linear)",
            "selection": "argmax val_normal over evals every 2048 steps, "
                         "excluding step 0 (untrained initialisation), on a "
                         "fixed 8192-example prefix of the Standard validation "
                         "split; test splits are never seen before selection, so "
                         "both test_normal and test_noself are unselected "
                         "out-of-sample readouts of the selected checkpoint",
            "protocol": "from-scratch, leave-db-out (eval db unseen during training)",
            "eval_tasks": [t[1] for t in eval_specs],  # share this training run
            "params": n_params,
            "device": device,
            "gpu": torch.cuda.get_device_name(0) if device == "cuda" else None,
            "started": started.isoformat(timespec="seconds"),
            "host": os.uname().nodename,
            "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
            # "git_commit": _git("rev-parse", "HEAD"),
            # "git_dirty": bool(_git("status", "--porcelain")),
            "legacy_ckpt_dir": str(job["ckpt_dir"]), "tag": job["tag"],
            "cmd": " ".join(sys.argv),
        }, indent=2))
        print(f"RUN_DIR {job['run_dir']}", flush=True)
        jobs.append(job)

    # Validation only during training: the test splits must not enter any
    # selection decision, so they are evaluated once at the end (final_full).
    # The selection set is a fixed 8,192-example prefix of the Standard
    # validation split (f1/trial validation is smaller and is used in full);
    # 2,048 was too noisy a criterion to take a max over ~50 evaluations.
    SEL_BATCHES, MON_BATCHES = 256, 64

    def run_evals(job, step):
        rec = {"step": step, "tag": job["tag"]}
        for mode, nb in (("normal", SEL_BATCHES), ("noself", MON_BATCHES)):
            acc_auroc, n = evaluate(net, job["evals"][("val", mode)], job["task_type"],
                                    device, max_batches=nb)
            rec[f"val_{mode}"] = round(acc_auroc, 4)
            rec["n_val" if mode == "normal" else "n_val_noself"] = n
        print("EVAL " + json.dumps(rec), flush=True)
        with open(job["run_dir"] / "evals.jsonl", "a") as fh:
            fh.write(json.dumps(rec) + "\n")
        return rec

    def select(job, rec):
        # step 0 is the untrained initialisation: logged for the learning
        # curve, never selectable
        if rec["step"] > 0 and rec["val_normal"] > job["best_val"]:
            job["best_val"] = rec["val_normal"]
            job["best_rec"] = rec
            torch.save(net.state_dict(), job["ckpt_dir"] / "best.pt")
            torch.save(net.state_dict(), job["run_dir"] / "best.pt")

    steps = 0
    epoch = 0
    t0 = time.time()
    while steps < max_steps:
        train_ds.sampler.shuffle_py(epoch)
        epoch += 1
        loader = DataLoader(
            train_ds, batch_size=None, num_workers=8, pin_memory=True,
        )
        for batch in loader:
            if steps >= max_steps:
                break
            if steps % 2048 == 0:
                for job in jobs:
                    select(job, run_evals(job, steps))
            batch.pop("true_batch_size")
            '''
            node_idxs: [B,S]  B=batch size, S=seq_len(num of cells)  ID of the row containing the cell
            table_name_idxs: [B,S]  B=batch size, S=seq_len(num of cells)  ID of the table containing the cell
            col_name_idxs: [B,S]  B=batch size, S=seq_len(num of cells)  ID of the column containing the cell
            sem_types: [B,S]  B=batch size, S=seq_len(num of cells)  semantic type / data type of the cell
            class_value_idxs: [B,S]  B=batch size, S=seq_len(num of cells)  ID of the text value in the text vocabulary

            text_values: [B,S,D]  B=batch size, S=seq_len(num of cells), D=embedding_dim  text embedding of the cell
            datetime_values: [B,S,1]  B=batch size, S=seq_len(num of cells), 2=timestamp+delta_t  timestamp embedding of the cell
            boolean_values: [B,S,1]  B=batch size, S=seq_len(num of cells)  boolean-value embedding of the cell
            number_values: [B,S,1]  B=batch size, S=seq_len(num of cells)  numeric-value embedding of the cell

            f2p_nbr_idxs: [B,S,N]  N=number of neighbors IDs of parent rows referenced by this row through foreign keys

            masks: [B,S]  B=batch size, S=seq_len(num of cells)  whether the cell value should be hidden
            is_targets: [B,S]  B=batch size, S=seq_len(num of cells)  whether the cell is a prediction target
            '''

            for k in batch:
                batch[k] = batch[k].to(device, non_blocking=True)
            out = net(batch)
            opt.zero_grad(set_to_none=True)
            out["loss"].backward()
            torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
            opt.step()
            sched.step()
            steps += 1
            if steps % 500 == 0:
                ips = steps / (time.time() - t0)
                print(
                    f"step {steps} loss={out['loss'].item():.4f} {ips:.2f} it/s",
                    flush=True,
                )

    for job in jobs:
        job["final_rec"] = run_evals(job, steps)
        select(job, job["final_rec"])
        print("BEST " + json.dumps(job["best_rec"]), flush=True)
    elapsed = round(time.time() - t0, 1)

    # final FULL evaluation of each task's best checkpoint (paper-comparable
    # numbers). Load the run's own copy: ckpt_dir is keyed by tag only, so two
    # jobs with the same tag (duplicate submit, smoke test) would overwrite
    # each other.
    for job in jobs:
        run_dir = job["run_dir"]
        net.load_state_dict(torch.load(run_dir / "best.pt", map_location=device))
        final_full = {"tag": job["tag"]}
        for (split, mode), ds in job["evals"].items():
            acc_auroc, n = evaluate(net, ds, job["task_type"], device)  # no cap = full split
            final_full[f"{split}_{mode}"] = round(acc_auroc, 4)
            final_full["n_" + split] = n
        print("FINAL_FULL " + json.dumps(final_full), flush=True)
        summary = {
            "tag": job["tag"], "model_id": model_id, "db": db,
            "table": job["table"], "seed": seed, "best": job["best_rec"],
            "final": job["final_rec"], "final_full": final_full,
            "finished": datetime.now().isoformat(timespec="seconds"),
            "elapsed_sec": elapsed,
        }
        with open(out_dir / f"rowgraph_{job['tag']}.json", "w") as f:  # legacy flat file
            json.dump(summary, f, indent=2)
        (run_dir / "summary.json").write_text(json.dumps(summary, indent=2))
        (run_dir / "final_full.json").write_text(json.dumps(final_full, indent=2))
        # keep this run's log next to its results: RUN_LOG names it when one
        # SLURM job runs several trainings, otherwise it is the job's own log
        # (sbatch writes logs to results/logs/ regardless of --out-dir)
        jid = os.environ.get("SLURM_JOB_ID")
        logs = [Path(os.environ["RUN_LOG"])] if os.environ.get("RUN_LOG") else (
            list((REPO / "results" / "logs").glob(f"*_{jid}.out")) if jid else [])
        for log in logs:
            if log.exists():
                shutil.copy2(log, run_dir / "slurm.out")
        print(f"RUN_ARTIFACTS {run_dir}", flush=True)


if __name__ == "__main__":
    main()
