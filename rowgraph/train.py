"""Train/eval entry for the RowGraphNet prototype (module-proof grid).

Protocol: from-scratch, leave-db-out (same task mix as RT-scratch baselines),
so results compare directly against our matched RT-scratch numbers.

Every eval reports BOTH the normal metric and the no-self-label metric
(sampler self_label_dropout=1.0), so label reliance is tracked continuously.

Usage:
  pixi run python experiments/rowgraph_train.py <db> <table> <variant> [seed] [steps] [seq_len]

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
from sklearn.metrics import r2_score, roc_auc_score
from torch.utils.data import DataLoader

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rt.data import RelationalDataset  # noqa: E402
from rt.tasks import (  # noqa: E402
    all_tasks, forecast_clf_tasks, forecast_reg_tasks, forecast_tasks,
)
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
    "relgraph_dropE09_no_warm": {
        "use_relgraph": True, "train_label_dropout": 0.9, "warm_start": False,
    },
    # adaptive regression codebook (per-task 1-D k-means of TRAIN targets,
    # K<=64, see gen_codebooks.py) — everything else identical
    "relgraph_cb_no_warm": {
        "use_relgraph": True, "warm_start": False, "codebook": True,
    },
    "cb_no_warm": {"warm_start": False, "codebook": True},
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


class CodebookResolver:
    """Maps each graph in a batch to its task's regression codebook.

    A graph's task is identified by (target column index, seed-node range) —
    the same table_info/column_index data make_ds uses. At construction we
    assert this key is unambiguous over the given task list.
    """

    def __init__(self, tasks, split, cbjson, kmax, default_centers):
        from rt.data import get_column_index
        sp = {"train": "Train", "val": "Val", "test": "Test"}[split]
        reg_keys = {(t[0], t[1]) for t in forecast_reg_tasks}
        rows, lens, self.by_col = [], [], {}
        # row 0 = default (fixed bins) for clf/unmatched graphs
        rows.append(self._pad(default_centers, kmax))
        lens.append(len(default_centers))
        for db, table, col, _dc in tasks:
            info = json.load(open(
                f"{os.environ['HOME']}/scratch/pre/{db}/table_info.json"))
            key = f"{table}:Db" if f"{table}:Db" in info else f"{table}:{sp}"
            lo = info[key]["node_idx_offset"]
            hi = lo + info[key]["num_nodes"]
            cidx = get_column_index(col, table, db)
            if (db, table) in reg_keys:
                jk = f"{db}/{table}"
                assert jk in cbjson, f"no codebook for reg task {jk}"
                cs = cbjson[jk]["centers"]
                rows.append(self._pad(cs, kmax))
                lens.append(len(cs))
                rid = len(rows) - 1
            else:
                rid = 0  # clf: row unused by the model, default is fine
            for plo, phi, _ in self.by_col.get(cidx, ()):
                assert hi <= plo or phi <= lo, (
                    f"ambiguous task key: col {cidx} ranges overlap")
            self.by_col.setdefault(cidx, []).append((lo, hi, rid))
        self.centers = torch.tensor(rows, dtype=torch.float32)
        self.lens = torch.tensor(lens, dtype=torch.long)

    @staticmethod
    def _pad(cs, kmax):
        cs = list(cs)
        return cs + [cs[-1]] * (kmax - len(cs))  # repeat-pad keeps sortedness

    def __call__(self, batch):
        tgt = batch["is_targets"]
        has = tgt.any(-1)
        if not has.any():
            return None
        tpos = tgt.float().argmax(-1)
        bidx = torch.arange(tgt.shape[0], device=tgt.device)
        seeds = batch["node_idxs"][bidx, tpos].long()[has].cpu().tolist()
        cols = batch["col_name_idxs"][bidx, tpos].long()[has].cpu().tolist()
        rid = []
        for n, c in zip(seeds, cols):
            r = 0
            for lo, hi, cand in self.by_col.get(c, ()):
                if lo <= n < hi:
                    r = cand
                    break
            rid.append(r)
        idx = torch.tensor(rid, dtype=torch.long)
        return self.centers[idx], self.lens[idx]


@torch.inference_mode()
def evaluate(net, ds, task_type, device, max_batches=None, cb_fn=None):
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
        out = net(batch, reg_cb=cb_fn(batch) if cb_fn else None)
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
        elif task_type == "reg" and "reg_pred" in out:
            for g, p, y in zip(
                out["reg_graphs"].tolist(),
                out["reg_pred"].float().tolist(),
                out["reg_y"].float().tolist(),
            ):
                nid = int(seed_nodes[g])
                if nid not in preds:
                    preds[nid], ys[nid] = p, y
    net.train()
    ids = sorted(preds)
    y = np.array([ys[i] for i in ids])
    p = np.array([preds[i] for i in ids])
    if task_type == "clf":
        return float(roc_auc_score(y, p)), len(ids)
    return float(r2_score(y, p)), len(ids)


def parse_args(argv):
    """Flags are preferred; the legacy positional form still works so that
    already-queued SLURM jobs keep running:
        train.py <db> <table> <variant> [seed] [steps] [seq_len] [d_model]
    """
    tasks = sorted({f"{t[0]}/{t[1]}" for t in forecast_tasks})
    p = argparse.ArgumentParser(
        prog="rowgraph/train.py",
        description="Train RowGraphNet from scratch, leave-database-out "
                    "(the eval database is never seen during training).",
        epilog="eval tasks:\n  " + "\n  ".join(tasks),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--db", required=True, help="eval database, e.g. rel-f1")
    p.add_argument("--task", "--table", required=True, dest="table",
                   help="eval task, e.g. driver-dnf")
    p.add_argument("--variant", required=True, choices=sorted(VARIANTS),
                   help="model configuration (see VARIANTS)")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--steps", type=int, default=100_000, dest="max_steps",
                   help="training steps (default: 100000)")
    p.add_argument("--seq-len", type=int, default=2048, dest="seq_len",
                   help="context length in cells (default: 2048)")
    p.add_argument("--d-model", type=int, default=256, dest="d_model",
                   help="model width (default: 256)")
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
            db=argv[0], table=argv[1], variant=argv[2],
            out_dir=default_out_dir(), **kw)
    return p.parse_args(argv)


def main():
    args = parse_args(sys.argv[1:])
    db, table, variant = args.db, args.table, args.variant
    seed, max_steps = args.seed, args.max_steps
    seq_len, d_model = args.seq_len, args.d_model
    assert variant in VARIANTS, f"unknown variant {variant}; pick from {sorted(VARIANTS)}"

    cfg = dict(VARIANTS[variant])
    train_dropout = cfg.pop("train_label_dropout", 0.0)
    warm = cfg.pop("warm_start", True)
    codebook_on = cfg.pop("codebook", False)

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

    eval_task = [t for t in forecast_tasks if t[0] == db and t[1] == table]
    assert len(eval_task) == 1
    # authoritative: read the task type off RelBench's own task lists.
    # (column names are ambiguous — e.g. rel-event uses "target" for both a
    # clf task (user-repeat) and a reg task (user-attendance).)
    in_clf = any(t[0] == db and t[1] == table for t in forecast_clf_tasks)
    in_reg = any(t[0] == db and t[1] == table for t in forecast_reg_tasks)
    assert in_clf != in_reg, f"{db}/{table} not uniquely typed"
    task_type = "clf" if in_clf else "reg"

    net = RowGraphNet(
        d_model=d_model, n_layers=cfg.pop("n_layers", 6), **cfg
    ).to(device)
    if warm:
        assert d_model == 256, "warm start requires d_model=256"
        warm_start_encoders(net, db, table)
    print(f"params={sum(p.numel() for p in net.parameters()):,}", flush=True)

    train_tasks = [t for t in all_tasks if t[0] != db]
    train_ds = make_ds(train_tasks, "train", seq_len, seed, dropout=train_dropout)
    evals = {
        ("val", "normal"): make_ds(eval_task, "val", seq_len, 0, 0.0),
        ("val", "noself"): make_ds(eval_task, "val", seq_len, 0, 1.0),
        ("test", "normal"): make_ds(eval_task, "test", seq_len, 0, 0.0),
        ("test", "noself"): make_ds(eval_task, "test", seq_len, 0, 1.0),
    }

    cb_train, cb_split = None, {"val": None, "test": None}
    if codebook_on:
        cbjson = json.loads(
            (Path(__file__).resolve().parent / "codebooks_k64.json").read_text())
        kmax = max(len(v["centers"]) for v in cbjson.values())
        default = RowGraphNet(d_model=8).bin_centers.tolist()  # fixed 33 bins
        cb_train = CodebookResolver(train_tasks, "train", cbjson, kmax, default)
        for sp in ("val", "test"):
            cb_split[sp] = CodebookResolver(eval_task, sp, cbjson, kmax, default)
        ek = f"{db}/{table}"
        print(f"codebook on: kmax={kmax}, eval task {ek} "
              f"K_eff={cbjson[ek]['K_eff'] if ek in cbjson else 'clf'}", flush=True)

    opt = torch.optim.AdamW(net.parameters(), lr=1e-3, weight_decay=0.1)
    sched = torch.optim.lr_scheduler.OneCycleLR(
        opt, max_lr=1e-3, total_steps=max_steps, pct_start=0.2,
        anneal_strategy="linear",
    )

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    tag = f"{db}_{table}_{variant}_s{seed}"
    if seq_len != 2048:
        tag += f"_ctx{seq_len}"
    if d_model != 256:
        tag += f"_d{d_model}"
    # legacy checkpoint location — kept exactly as before, never deleted
    ckpt_dir = Path("ckpts/rowgraph") / tag
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    # per-run archive: results/{model}/{dataset}/{task}/{start-timestamp}/
    # timestamp YYYYmmdd-HHMMSS is sortable, so `ls` lists runs chronologically
    model_id = f"rowgraph_{variant}"
    if seq_len != 2048:
        model_id += f"_ctx{seq_len}"
    if d_model != 256:
        model_id += f"_d{d_model}"
    started = datetime.now()
    run_dir = out_dir / model_id / db / table / started.strftime("%Y%m%d-%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)

    def _git(*args):
        try:
            return subprocess.check_output(
                ["git", *args], stderr=subprocess.DEVNULL, text=True
            ).strip()
        except Exception:
            return None

    (run_dir / "config.json").write_text(json.dumps({
        "model_id": model_id, "variant": variant, "db": db, "table": table,
        "task_type": task_type, "seed": seed, "max_steps": max_steps,
        "seq_len": seq_len, "d_model": d_model,
        "warm_start": warm, "train_label_dropout": train_dropout,
        "codebook": codebook_on,
        "lr": 1e-3, "weight_decay": 0.1, "batch_size": 32,
        "optimizer": "AdamW", "scheduler": "OneCycleLR(pct_start=0.2,linear)",
        "selection": "val_normal + val_noself (combined, validation-only)",
        "protocol": "from-scratch, leave-db-out (eval db unseen during training)",
        "params": sum(p.numel() for p in net.parameters()),
        "device": device, "started": started.isoformat(timespec="seconds"),
        "host": os.uname().nodename,
        "slurm_job_id": os.environ.get("SLURM_JOB_ID"),
        "git_commit": _git("rev-parse", "HEAD"),
        "git_dirty": bool(_git("status", "--porcelain")),
        "legacy_ckpt_dir": str(ckpt_dir), "tag": tag,
        "cmd": " ".join(sys.argv),
    }, indent=2))
    print(f"RUN_DIR {run_dir}", flush=True)

    def run_evals(step):
        rec = {"step": step, "tag": tag}
        for (split, mode), ds in evals.items():
            m, n = evaluate(net, ds, task_type, device, max_batches=64,
                            cb_fn=cb_split[split])
            rec[f"{split}_{mode}"] = round(m, 4)
            rec["n_" + split] = n
        print("EVAL " + json.dumps(rec), flush=True)
        with open(run_dir / "evals.jsonl", "a") as fh:
            fh.write(json.dumps(rec) + "\n")
        return rec

    best_val, best_rec = -1e9, None
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
                rec = run_evals(steps)
                crit = rec["val_normal"] + rec["val_noself"]
                if crit > best_val:
                    best_val = crit
                    best_rec = rec
                    torch.save(net.state_dict(), ckpt_dir / "best.pt")
                    torch.save(net.state_dict(), run_dir / "best.pt")
            batch.pop("true_batch_size")
            '''
            node_idxs: [B,S]  B=batch size, S=seq_len(num of cells)  cell 所属的行 ID
            table_name_idxs: [B,S]  B=batch size, S=seq_len(num of cells)  cell 所属表的 ID
            col_name_idxs: [B,S]  B=batch size, S=seq_len(num of cells)  cell 所属列的 ID
            sem_types: [B,S]  B=batch size, S=seq_len(num of cells)  cell 的语义类型,数据类型
            class_value_idxs: [B,S]  B=batch size, S=seq_len(num of cells)  文本值在文本词表中的 ID
            
            text_values: [B,S,D]  B=batch size, S=seq_len(num of cells), D=embedding_dim  cell 的文本 embedding
            datetime_values: [B,S,1]  B=batch size, S=seq_len(num of cells), 2=timestamp+delta_t  cell 的时间戳 embedding
            boolean_values: [B,S,1]  B=batch size, S=seq_len(num of cells)  cell 的布尔值 embedding
            number_values: [B,S,1]  B=batch size, S=seq_len(num of cells)  cell 的数值 embedding
            
            f2p_nbr_idxs: [B,S,N]  N=number of neighbors 该行通过外键连接的父行 ID
            
            masks: [B,S]  B=batch size, S=seq_len(num of cells)  该 cell 的值是否应该隐藏
            is_targets: [B,S]  B=batch size, S=seq_len(num of cells)  该 cell 是否是预测目标
            '''
            
            cb = cb_train(batch) if cb_train is not None else None
            for k in batch:
                batch[k] = batch[k].to(device, non_blocking=True)
            out = net(batch, reg_cb=cb)
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

    rec = run_evals(steps)
    if rec["val_normal"] + rec["val_noself"] > best_val:
        best_rec = rec
        torch.save(net.state_dict(), ckpt_dir / "best.pt")
        torch.save(net.state_dict(), run_dir / "best.pt")
    print("BEST " + json.dumps(best_rec), flush=True)

    # final FULL evaluation of the best checkpoint (paper-comparable numbers)
    net.load_state_dict(torch.load(ckpt_dir / "best.pt", map_location=device))
    final_full = {"tag": tag}
    for (split, mode), ds in evals.items():
        m, n = evaluate(net, ds, task_type, device,  # no cap = full split
                        cb_fn=cb_split[split])
        final_full[f"{split}_{mode}"] = round(m, 4)
        final_full["n_" + split] = n
    print("FINAL_FULL " + json.dumps(final_full), flush=True)
    summary = {
        "tag": tag, "model_id": model_id, "db": db, "table": table,
        "seed": seed, "best": best_rec, "final": rec, "final_full": final_full,
        "finished": datetime.now().isoformat(timespec="seconds"),
        "elapsed_sec": round(time.time() - t0, 1),
    }
    with open(out_dir / f"rowgraph_{tag}.json", "w") as f:  # legacy flat file
        json.dump(summary, f, indent=2)
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    (run_dir / "final_full.json").write_text(json.dumps(final_full, indent=2))
    jid = os.environ.get("SLURM_JOB_ID")
    if jid:  # keep this run's SLURM log next to its own results
        # sbatch writes logs to experiments/results/ regardless of --out-dir
        for log in (REPO / "experiments" / "results").glob(f"*_{jid}.out"):
            shutil.copy2(log, run_dir / "slurm.out")
    print(f"RUN_ARTIFACTS {run_dir}", flush=True)


if __name__ == "__main__":
    main()
