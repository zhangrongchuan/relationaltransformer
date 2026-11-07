# RelGraph conference paper

This directory contains a NeurIPS 2026-style conference-paper draft based on the
RelGraph presentation and the repository's recorded experiments.

## Files

- `main.tex`: paper entry point and abstract
- `sections/`: Introduction, Related Works, Task Formulation, Methodology,
  Result, and Analysis, in that order
- `figures/relgraph_architecture.pdf`: architecture figure reused from the
  presentation
- `references.bib`: bibliography
- `checklist.tex`: NeurIPS paper checklist
- `neurips_2026.sty`: local NeurIPS 2026 style
- `main.pdf`: compiled paper

In the current working draft, the abstract through Methodology occupy pages
1--5 and Results begin on page 6.  Results and Analysis have not yet been
restructured to the final page budget; the current main text is nine pages and
must be compressed to eight before submission.

## Build

From this directory:

```bash
tectonic -C -k --keep-logs main.tex
```

A standard TeX installation can instead use:

```bash
latexmk -pdf main.tex
```

The current source uses the anonymous submission mode. For a camera-ready
version, replace `\usepackage{neurips_2026}` with
`\usepackage[main,final]{neurips_2026}` and fill in the author block.

## Result provenance and submission caveats

The Standard baseline table distinguishes published Entity Mean, Griffin, and
RT values from local full-test RowGraph evaluations. Standard/NSL drops use
paired local checkpoints and never mix a published Standard score with a local
NSL score.

Three of the 20 proposed-model task entries selected the step-0 checkpoint:

- RowGraph-Base / Trial Study Outcome:
  `../experiments/results/classification/base_no_warm/rel-trial/study-outcome/summary.json`
- RelGraph / Amazon Item Churn:
  `../experiments/results/classification/relgraph_no_warm/rel-amazon/item-churn/summary.json`
- RelGraph / Stack User Badge:
  `../experiments/results/classification/relgraph_no_warm/rel-stack/user-badge/summary.json`

The exploratory task-disjoint numbers are preserved from the presentation, but
their per-checkpoint selection artifacts were not retained. Training logs also
recorded capped test metrics at each evaluation interval, although automatic
checkpoint selection used validation metrics only. The paper discloses both
facts and treats the current results as development evidence.

Before submission, the strongest follow-up is a clean rerun that (i) chooses
checkpoints using source databases only, (ii) never evaluates test data before
selection, (iii) disallows unoptimized checkpoints, (iv) archives a clean source
revision and every selection artifact, and (v) reports multiple seeds.
