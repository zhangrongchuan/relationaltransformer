# Experiments directory index

> **Code layout (reorganized 2026-07)**: reusable model code lives in the top-level **`rowgraph/`**
> package (`model.py` network, `train.py` training entry, `gen_codebooks.py` + `codebooks_k64.json`
> regression codebook). This directory holds only experiment/analysis scripts; legacy paths such as
> `exp2_rowgraph/rowgraph_*.py` are symlinks into `rowgraph/`, kept only for backward compatibility
> with historical commands and in-flight jobs.
> Standard usage: `pixi run python rowgraph/train.py <db> <table> <variant> [seed] [steps] [seq_len] [d_model]`

## exp1_rt_components/ — Experiment 1: RT diagnosis and component improvements (done)

**Question**: Does RT's zero-shot mainly rely on copying labels? How severe is the sampling waste?
**Conclusion**: see `exp1_rt_components/FINAL_REPORT.md` (full analysis), `DEFENSE_SUMMARY.md` (defense summary), `L0_diagnosis_report.md` (diagnosis report).

| File | Purpose |
|---|---|
| diag_context.py | L0 diagnosis: composition of the 1024-cell budget (neighbors account for 54-98%) |
| diag_variance.py | L0 diagnosis: resampling variance (flip rate 34-43%, ensemble +1.4~3.4) |
| diag_copy_baseline.py | L0 diagnosis: copy-label baseline (≈RT zero-shot) |
| train_variant.py | Component training entry (contd/scratch; rope/eflag/drop/local/pcap) |
| eval_ablation.py | no-self-label ablation protocol (evidence source for the drop09 two-way control) |
| eval_sampling_variants.py | Controlled evaluation of sampling-component noise (K=8) |
| eval_paper_table.py / collect_paper_table.py | Paper-table 10-task full-test alignment (baseline 70.0 vs paper 69.7) |
| collect_results.py | Training-log aggregation |
| run_*.sbatch | Corresponding SLURM submission scripts |

**Key result**: drop09 from-scratch training = normal +3.0 / no-self-label +20.3 (dependence halved); applying the same mechanism at the contd stage backfires → anti-shortcut must be enforced from the pretraining start.

## exp2_rowgraph/ — Experiment 2: RowGraphNet new backbone (in progress)

**Design** (ULTRA/POSTRA ideas + our experimental lessons): rows = nodes, PK-FK = edges;
within-row cell encodings are pooled into a "name card" (warm-started from the RT encoder) → seed-conditioned
message passing between rows → scoring against candidate value nodes (True/False via the boolean encoder,
regression via 33 z-space bins with the numeric encoder; label edges flow one-directionally = structured ICL;
label-edge dropout = anti-copy-label).

| File | Purpose |
|---|---|
| rowgraph_model.py | RowGraphNet (2.05M parameters) |
| rowgraph_train.py | Training entry (from-scratch leave-db-out, module toggles) |
| rowgraph_coverage.py | Row-level coverage statistics (4x cells → 3.3-5x rows) |

**Existing results**:
- Module proof @20k (backed up in results/rowgraph_grid20k/): message passing +20.0,
  label edges +14.6, Δt +4.5 (all with independent evidence)
- 50k flagship: **dropE09_no_warm test 0.8008 / no-self-label 0.7404** (RT-scratch
  0.749/0.366; 1/10 the parameters) — thresholds 1 and 3 passed
- Mechanism finding: warm start imports copy-label bias; copy-label behavior forms gradually over training
  (each eval logs normal+noself simultaneously, so the divergence curve can be plotted)
- Threshold not passed: study-outcome stuck at ~0.51 (wide-row dilution hypothesis → attention pooling)

**Third wave (running)**: dropE09_no_warm multi-seed, dropE05 milder setting,
attn pooling trio, user-repeat generalization.

## Shared

- `run_eval_jobs.sbatch` — generic GPU job submitter (shared by both experiments)
- `results/` — all experiment results (json/logs/report data)
- top-level `rowgraph_*.py` symlinks — compatibility for in-flight SLURM jobs, removable later
