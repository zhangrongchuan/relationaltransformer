# NeurIPS 2026 paper project

This directory is an Overleaf-ready NeurIPS 2026 project. The files
neurips_2026.sty and checklist.tex are copied unchanged from the official
NeurIPS 2026 author kit:

https://media.neurips.cc/Conferences/NeurIPS2026/Formatting_Instructions_For_NeurIPS_2026.zip

## Compile on Overleaf

Upload the contents of this directory as a new Overleaf project and select
main.tex as the main document. Use pdfLaTeX.

## Submission modes

- Anonymous Main Track submission (current):
  **\usepackage{neurips_2026}**
- Camera-ready after acceptance:
  **\usepackage[main,final]{neurips_2026}**
- Non-anonymous preprint:
  **\usepackage[preprint]{neurips_2026}**

Do not modify neurips_2026.sty, add a geometry package, or override the
template's font sizes and margins.

## Current scope

- sections/methodology.tex: full, uncompressed classification Methodology
  with the agreed subsection and subsubsection hierarchy.
- sections/experiments.tex: detailed ten-task classification setup and
  results, including the qualified leave-database-out zero-shot protocol,
  Standard and no-self-label evaluation, RT comparison, parameter analysis,
  relation-conditioning ablation, and current limitations.
- sections/abstract.tex: explicit placeholder.
- references.bib: current RelBench, Relational Transformer, and ULTRA
  references; bibliography generation is enabled in main.tex.
- Regression remains an explicit placeholder until its design is fixed.
- A technical appendix is intentionally not included yet: all current model
  definitions are written once in the main Methodology to avoid duplication.
- checklist.tex: official checklist with TODO answers that must be
  completed before submission.

## Page-limit note

The current Methodology and Experiments are intentionally uncompressed and
form a complete writing/audit draft, not yet a page-limit-compliant full
NeurIPS submission. Once all paper sections, additional experiments, and
the regression design are stable, material can be moved to a technical
appendix without changing the notation or model definition.

## Classification result sources

The canonical machine-readable result files are:

- ../../experiments/results/classification/rgn_clf_results.csv for
  RowGraph-Base and RelGraph full-test Standard/NSL results;
- ../../experiments/results/classification/rt_clf_results.csv for the
  published RT Standard values and the separate locally reproduced RT
  Standard/NSL pairs.

The distinction between published and locally paired RT values is preserved
in both the result archive and the paper tables.
