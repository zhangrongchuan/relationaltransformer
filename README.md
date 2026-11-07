# ReGRow

A lightweight graph neural network for cross-database entity classification, built on [Relational Transformer (RT)](https://github.com/snap-stanford/relational-transformer). ReGRow combines row-level message passing with a query-conditioned relation graph; the d256 model has 2.78M parameters.

Training uses classification **and regression** tasks from the source databases. Evaluation is classification-only, on a held-out database with no parameter updates.

## Setup

Install [pixi](https://pixi.sh/latest/#installation), then run from the repository root:

```bash
pixi install
cd rustler
pixi run maturin develop --uv --release
cd ..
```

## Data

Place preprocessed data in `~/scratch/pre/<db>/`. All seven databases are needed: `rel-amazon`, `rel-avito`, `rel-event`, `rel-f1`, `rel-hm`, `rel-stack`, and `rel-trial`.

```bash
pip install -U huggingface_hub
mkdir -p ~/scratch/pre
huggingface-cli download hvag976/relational-transformer --repo-type dataset --local-dir ~/scratch/pre --local-dir-use-symlinks False
```

## Train

Train on the other databases and evaluate F1 classification tasks:

```bash
pixi run python rowgraph/train.py --db rel-f1 --task all-clf \
  --variant relgraph_no_warm --d-model 256 --seed 2
```

Defaults: 100,000 steps, batch size 32, 2048 cells per context, lr `1e-3`, wd `0.1`. Plan for one GPU and approximately 16 CPU cores / 64G RAM.

- Use `--task driver-dnf` to evaluate DNF only.
- Set `--d-model` to `128`, `256`, `512`, or `744` for the width experiments.
- Use `--variant no_warm` for the no-relation-graph ablation.
- For the paper's d256 settings, use `--wd 0.3` on Avito and `--lr 2e-3` on Stack.
- Run `pixi run python rowgraph/train.py --help` for all options.

Checkpoints are selected by Standard validation AUROC. Final evaluation reports both Standard and History Masked test AUROC.

## Results

Each task writes its checkpoint, configuration, validation log, and final metrics to:

```text
results/<model_id>/<db>/<task>/<start_time>_s<seed>/
```

See [results/README.md](results/README.md) for existing parameter, ablation, and case-study results. Relation-graph runs predating the **2026-11-02 relation-key fix** require retraining; corrected d256 runs are stored in `results/relfix_d256/`.

## Repository Layout

| Path | Contents |
|---|---|
| [`rowgraph/`](rowgraph/) | Model and training entry point |
| [`rt/`](rt/), [`rustler/`](rustler/) | RT data pipeline and Rust sampler |
| [`analysis/`](analysis/README.md) | Parameter analysis, ablations, multi-hop studies, and evaluation tools |
| [`results/`](results/README.md) | Saved experiments and historical source snapshots |