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
- sections/abstract.tex: explicit placeholder.
- references.bib: bibliography placeholder; uncomment the two bibliography
  lines in main.tex once citations are added.
- Regression remains an explicit placeholder until its design is fixed.
- A technical appendix is intentionally not included yet: all current model
  definitions are written once in the main Methodology to avoid duplication.
- checklist.tex: official checklist with TODO answers that must be
  completed before submission.

## Page-limit note

The current Methodology is intentionally uncompressed and reaches page 10
in the official layout. It is a complete writing/audit draft, not yet a
page-limit-compliant full NeurIPS submission. Once all paper sections and
the regression design are stable, material can be moved to a technical
appendix without changing the notation or model definition.
