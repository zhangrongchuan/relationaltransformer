# results/ — production results

`rowgraph/train.py` writes here by default (`--out-dir` overrides).

```
results/rowgraph_{variant}/{db}/{task}/{YYYYmmdd-HHMMSS}/
    config.json      full config (incl. git commit, parameter count, codebook state)
    evals.jsonl      normal + noself at every eval point (for the dependence curve)
    best.pt          best weights selected by val_normal+val_noself
    final_full.json  dual-protocol result of the best weights on the full val/test
    slurm.out         a copy of that run's SLURM log (if run on the cluster)
    rowgraph_{tag}.json  flat summary in the same dir (legacy-script compatibility)
```

Experimental/exploratory runs go under `experiments/results/`;
early archives are in `experiments/results-step1-exp1&exp2 early test/`.
Aggregation scripts (e.g. `experiments/exp2_rowgraph/final_table.py`) search all of these.
