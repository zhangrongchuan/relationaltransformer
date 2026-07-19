"""Evaluate trained variant checkpoints under the no-self-label protocol.

For each (task, variant) checkpoint:
  - normal eval        (self labels present, standard sampler)
  - no-self-label eval (sampler self_label_dropout=1.0: every same-entity
    target-column cell removed from context) == RT paper Table 4 protocol

label_reliance = normal - no_self_label. A variant that learned structural
reasoning keeps a smaller gap and a higher no-self-label score.

Usage: pixi run python experiments/eval_ablation.py [--glob PATTERN]
Outputs experiments/results/eval_ablation.json (incremental)
"""

import json
import sys
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import r2_score, roc_auc_score
from torch.utils.data import DataLoader

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from rt.data import RelationalDataset  # noqa: E402
from rt.model import RelationalTransformer  # noqa: E402
from experiments.exp1_rt_components.train_variant import VARIANTS  # noqa: E402

TASKS = {
    ("rel-f1", "driver-dnf"): ("did_not_finish", [], "clf"),
    ("rel-trial", "study-outcome"): ("outcome", [], "clf"),
    ("rel-avito", "ad-ctr"): ("num_click", [], "reg"),
    ("rel-event", "user-repeat"): ("target", [], "clf"),
}
CKPT_ROOT = Path(__file__).parents[2] / "ckpts" / "variants"


@torch.inference_mode()
def eval_once(net, ds, task_type, device):
    ds.sampler.shuffle_py(0)
    loader = DataLoader(ds, batch_size=None, num_workers=6, pin_memory=True)
    preds, labels = {}, {}
    for batch in loader:
        true_bs = batch.pop("true_batch_size")
        for k in batch:
            batch[k] = batch[k].to(device, non_blocking=True)
        batch["masks"][true_bs:, :] = False
        batch["is_targets"][true_bs:, :] = False
        batch["is_padding"][true_bs:, :] = True
        _, yhat_dict = net(batch)
        it = batch["is_targets"]
        if task_type == "clf":
            yhat = yhat_dict["boolean"][it].flatten()
            y = batch["boolean_values"][it].flatten()
        else:
            yhat = yhat_dict["number"][it].flatten()
            y = batch["number_values"][it].flatten()
        nid = batch["node_idxs"][it].flatten()
        for n, p, yy in zip(nid.tolist(), yhat.float().tolist(), y.float().tolist()):
            if n not in preds:
                preds[n] = p
                labels[n] = yy
    ids = sorted(preds)
    y = np.array([labels[i] for i in ids])
    p = np.array([preds[i] for i in ids])
    if task_type == "clf":
        return float(roc_auc_score((y > 0).astype(int), p)), len(ids)
    return float(r2_score(y, p)), len(ids)


def model_flags(variant):
    f = VARIANTS[variant]
    return {
        "time_rope": f.get("time_rope", False),
        "entity_flag": f.get("entity_flag", False),
    }


def sampler_kwargs(variant):
    f = VARIANTS[variant]
    return {
        "local_k": f.get("eval_local_k", 0),
        "periphery_cell_cap": f.get("eval_periphery_cell_cap", 0),
    }


def main():
    device = "cuda"
    out_path = Path(__file__).parents[1] / "results" / "eval_ablation.json"
    results = json.loads(out_path.read_text()) if out_path.exists() else []
    done = {(r["db"], r["table"], r["variant"], r["split"]) for r in results}

    for ckpt_dir in sorted(CKPT_ROOT.glob("*_s0")):
        parts = ckpt_dir.name.rsplit("_s", 1)[0]
        # {db}_{table}_{variant}[_scratch]
        for (db, table) in TASKS:
            prefix = f"{db}_{table}_"
            if parts.startswith(prefix):
                variant = parts[len(prefix):]
                break
        else:
            continue
        base_variant = variant.removesuffix("_scratch")
        if base_variant not in VARIANTS:
            print(f"skip {ckpt_dir.name}: unknown variant {base_variant}")
            continue
        ckpt = ckpt_dir / f"{db}_{table}_best.pt"
        if not ckpt.exists():
            print(f"skip {ckpt_dir.name}: no best ckpt")
            continue
        if (db, table, variant, "val") in done:
            continue

        target_col, drop_cols, ttype = TASKS[(db, table)]
        net = RelationalTransformer(
            num_blocks=12, d_model=256, d_text=384, num_heads=8, d_ff=1024,
            **model_flags(base_variant),
        )
        sd = torch.load(ckpt, map_location="cpu")
        # ckpts saved from a torch.compile-wrapped net carry _orig_mod. keys
        sd = {k.removeprefix("_orig_mod."): v for k, v in sd.items()}
        missing, unexpected = net.load_state_dict(sd, strict=False)
        assert not unexpected and set(missing) <= {"same_entity_emb"}, (
            ckpt, missing, unexpected,
        )
        net = net.to(device).to(torch.bfloat16).eval()

        rec = {"db": db, "table": table, "variant": variant, "split": "val"}
        for mode, dropout in [("normal", 0.0), ("no_self_label", 1.0)]:
            ds = RelationalDataset(
                tasks=[(db, table, target_col, "val", drop_cols)],
                batch_size=32, seq_len=1024, rank=0, world_size=1,
                max_bfs_width=256, embedding_model="all-MiniLM-L12-v2",
                d_text=384, seed=0,
                self_label_dropout=dropout,
                **sampler_kwargs(base_variant),
            )
            m, n = eval_once(net, ds, ttype, device)
            rec[mode] = round(m, 4)
            rec["n"] = n
        rec["label_reliance"] = round(rec["normal"] - rec["no_self_label"], 4)
        results.append(rec)
        print(json.dumps(rec), flush=True)
        out_path.write_text(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
