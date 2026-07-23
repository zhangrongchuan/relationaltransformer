# results/ — 正式版结果

`rowgraph/train.py` 默认写到这里（`--out-dir` 可覆盖）。

```
results/rowgraph_{variant}/{db}/{task}/{YYYYmmdd-HHMMSS}/
    config.json      完整配置（含 git commit、参数量、码本状态）
    evals.jsonl      每个 eval 点的 normal + noself（可画依赖度曲线）
    best.pt          按 val_normal+val_noself 选出的最佳权重
    final_full.json  最佳权重在全量 val/test 上的双协议结果
    slurm.out        该次运行的 SLURM 日志副本（如果在集群跑）
    rowgraph_{tag}.json  同目录扁平汇总（兼容老脚本）
```

实验/探索性的运行写在 `experiments/results/`；
早期归档在 `experiments/results-step1-exp1&exp2 early test/`。
汇总脚本（如 `experiments/exp2_rowgraph/final_table.py`）会同时搜索这几处。
