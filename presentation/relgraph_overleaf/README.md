# RelGraph Overleaf presentation

This folder is a self-contained 16:9 Beamer presentation for the RowGraph-Base / RelGraph project.

## Use in Overleaf

1. Upload the entire `relgraph_overleaf` folder as a new project.
2. Set `main.tex` as the main document.
3. Compile with **pdfLaTeX**.
4. Edit the three metadata commands near the top of `main.tex`:

```tex
\newcommand{\PresenterName}{Zhang Rongchuan}
\newcommand{\PresenterAffiliation}{Institute for Artificial Intelligence}
\newcommand{\TalkVenue}{Master Thesis}
```

The title is split deliberately with `\TitleLineOne` and `\TitleLineTwo`; edit those two commands instead of inserting additional manual line breaks.

The three-column summary cards use natural content height. Their top edges align, while their bottom edges may differ; this avoids artificial blank space inside shorter cards.

The current deck contains 19 active main slides and no backup slides. Optional shortcut-mechanism, regression-diagnostic, relation-ablation, and takeaway frames remain commented in `main.tex`. The sampler and both schematic examples use the paper's 2,048-cell configuration and distinguish the serialized sequence from the unmasked cells supplied to the encoder. For a shorter 12--15 minute talk, hide either the detailed Base-forward slide or the full task-level results slide.

## Result conventions

- Classification Standard/NSL values are paired local evaluations where stated.
- The published RT Standard score is used only on the Standard benchmark-comparison slide; all paired RT values are local reproductions of released checkpoints.
- The active architecture and readout slides present binary classification only. Regression appears only as work to finalize and benchmark.
- NSL is presented as a robustness stress test, not as a perfectly frozen causal intervention.

The architecture PNGs in `figures/` are copied into this folder so that the project can compile independently on Overleaf.
