# Experiments 目录索引

## exp1_rt_components/ — 实验一：RT 诊断与组件改进（已完成）

**问题**：RT 的 zero-shot 是否主要靠抄标签？采样浪费有多严重？
**结论**：见 `exp1_rt_components/FINAL_REPORT.md`（完整分析）、`DEFENSE_SUMMARY.md`（答辩总结）、`L0_diagnosis_report.md`（诊断报告）。

| 文件 | 用途 |
|---|---|
| diag_context.py | L0 诊断：1024 格预算构成统计（周边占 54-98%）|
| diag_variance.py | L0 诊断：重采样方差（翻面 34-43%，ensemble +1.4~3.4）|
| diag_copy_baseline.py | L0 诊断：抄标签基线（≈RT zero-shot）|
| train_variant.py | 组件训练入口（contd/scratch；rope/eflag/drop/local/pcap）|
| eval_ablation.py | no-self-label 消融协议（drop09 双向对照的证据来源）|
| eval_sampling_variants.py | 采样组件噪声受控评估（K=8）|
| eval_paper_table.py / collect_paper_table.py | 论文表 10 任务全量 test 对齐（baseline 70.0 vs 论文 69.7）|
| collect_results.py | 训练日志汇总 |
| run_*.sbatch | 对应 SLURM 提交脚本 |

**核心结果**：drop09 从零训练 = 正常 +3.0 / 无标签 +20.3（依赖度减半）；同机制 contd 阶段应用反效果 → 防捷径必须在预训练起点。

## exp2_rowgraph/ — 实验二：RowGraphNet 新骨干（进行中）

**设计**（ULTRA/POSTRA 思想 + 我们的实验教训）：行=节点、PK-FK=边；
行内 cell 编码池化成"名片"（RT 编码器热启动）→ 行间 seed 条件化消息传递
→ 候选值节点打分（True/False 用布尔编码器、回归 33 个 z 空间分桶用数值
编码器；label 边单向流入 = 结构化 ICL；label 边 dropout = 防抄标签）。

| 文件 | 用途 |
|---|---|
| rowgraph_model.py | RowGraphNet（2.05M 参数）|
| rowgraph_train.py | 训练入口（from-scratch leave-db-out，模块开关）|
| rowgraph_coverage.py | 行级覆盖率统计（4x cells → 3.3-5x rows）|

**已有结果**：
- 模块证明 @20k（备份于 results/rowgraph_grid20k/）：消息传递 +20.0、
  label 边 +14.6、Δt +4.5（全部拿到独立证据）
- 50k 头牌：**dropE09_no_warm test 0.8008 / 无标签 0.7404**（RT-scratch
  0.749/0.366；1/10 参数）——门槛 1、3 通过
- 机制发现：热启动会进口抄标签偏见；抄标签行为随训练逐步形成
  （每个 eval 同时记录 normal+noself，可画分叉曲线）
- 未过门槛：study-outcome 卡在 ~0.51（宽行稀释假设 → attention pooling）

**第三波（运行中）**：dropE09_no_warm 多 seed、dropE05 温和档、
attn pooling 三连、user-repeat 泛化。

## 共享

- `run_eval_jobs.sbatch` — 通用 GPU 作业提交器（两个实验共用）
- `results/` — 全部实验结果（json/日志/报告数据）
- 顶层的 `rowgraph_*.py` 软链接 — 兼容运行中的 SLURM 作业，之后可删
