# L0 诊断报告：RT 的三个瓶颈的定量证据

日期：2026-07-10 ｜ 数据：RelBench 21 个 forecast 任务，val split
脚本：`diag_context.py`（构成统计）、`diag_variance.py`（重采样方差）、`diag_copy_baseline.py`（抄标签基线）

## 摘要

三份独立诊断相互印证，把我们提出的三个假设全部量化坐实，并给出瓶颈优先级：

1. **预算浪费（最严重、普遍）**：1024 个 cell 中 54%–98% 花在与目标实体无直接关系的"周边"内容上；21 个任务的中位数约 90%。
2. **采样随机性（真实、可观测）**：同一目标换 8 次 context，分类任务 9%–43% 的样本预测翻面；8-context ensemble 免费提升最高 +3.4 AUROC / +3.1 R²。
3. **抄标签捷径（结构性）**：不学习的 context-copy 基线在多数分类任务上逼平甚至超过 RT zero-shot；self-label 为 0 的任务（study-outcome / study-adverse）上 RT 输出近乎常数。

## 诊断 1：context 构成（每任务 256 序列）

关键列摘录（完整表见 `results/diag_context.md`）：

| 任务 | self-lbl 均值 | 0-self-lbl 序列 | 周边占比 | 事件 Δt 中位 |
|---|---|---|---|---|
| rel-amazon/user-churn | 3.6 | 11% | **93%** | 389d |
| rel-hm/user-churn | 5.6 | 10% | **92%** | 119d |
| rel-trial/study-outcome | **0.0** | **100%** | 93% | 842d |
| rel-trial/study-adverse | **0.0** | **100%** | 94% | 874d |
| rel-trial/site-success | 1.2 | 59% | **98%** | 2025d |
| rel-f1/driver-dnf | 17.2 | 2% | 56% | 756d |
| rel-avito/ad-ctr | 0.4 | 63% | 69% | 4.6d |

发现：

- **周边支配预算**。最好情况（rel-f1，schema 小）也有 54%；大库 90%+。周边主要是 2-hop 维表和其他实体的事件（races/circuits、别的用户对同一商品的评论）。这是 row-pooling / 预算控制的直接依据。
- **目标实体的直接事件只占很小一部分**（driver-dnf 72 cell ≈ 7%；user-churn 约 10 行事件）。
- **随机 BFS 没有时间偏好**：多数库事件 Δt 中位数以年计（论证 local/recency 采样）。rel-trial 最极端（5.5 年）。
- **RT 论文 Table 11 的 self-label 分布被复现**：study-outcome/study-adverse 恰好 0。

## 诊断 2：重采样方差（zero-shot ckpt，K=8 次重采样，全 val）

| 任务 | 单次 metric | ensemble | 增益 | 翻面率 |
|---|---|---|---|---|
| rel-f1/driver-dnf (auc) | 0.733±0.009 | 0.747 | **+1.4** | **34%** |
| rel-f1/driver-position (r2) | 0.308±0.011 | 0.339 | **+3.1** | – |
| rel-event/user-repeat (auc) | 0.709±0.021 | 0.743 | **+3.4** | **43%** |
| rel-hm/user-churn (auc) | 0.640±0.000 | 0.650 | +1.1 | 9% |
| rel-avito/ad-ctr (r2) | 0.007±0.003 | 0.015 | +0.7 | – |
| rel-avito/user-clicks (auc) | 0.533±0.003 | 0.534 | +0.0 | 15% |
| rel-trial/study-outcome (auc) | 0.531±0.003 | 0.532 | +0.0 | 25% |

发现：

- **采样噪声真实存在且可观**：有历史信息的任务翻面率 34–43%，ensemble 有免费增益 → 采样策略（C）和推理期 multi-context ensembling 都有价值空间。
- **study-outcome 的方差结构证明抄标签依赖**：预测 std 仅 0.03（driver-dnf 为 0.32）——没有 self-label 可抄时，模型对 context 变化几乎无反应，输出近常数（AUROC 0.53）。attention 并没有从结构信息中提取判别信号。
- 注：rel-event/user-attendance 因标签零膨胀（大多为 0）在 R² 下退化，两份诊断结果均异常（copy R²=1.0 / RT R²=0.0），后续该任务不用于回归结论。

## 诊断 3：抄标签基线（无学习）

ctx-copy = 用 RT 实际采到的 context 里的 self-label 预测；hist-copy = 完美检索全历史（严格 ts<t）。

分类任务（AUROC）对比 RT zero-shot（论文/我们的方差诊断）：

| 任务 | ctx-copy | hist-copy | RT zero-shot |
|---|---|---|---|
| rel-stack/user-engagement | **0.846** | 0.831 | ~0.85 |
| rel-event/user-ignore | **0.844** | 0.814 | – |
| rel-stack/user-badge | **0.824** | 0.810 | – |
| rel-f1/driver-top3 | 0.752 | 0.781 | – |
| rel-f1/driver-dnf | 0.700 | 0.699 | 0.733 |
| rel-event/user-repeat | 0.637 | **0.732** | 0.709 |
| rel-avito/user-visits | 0.513 | **0.615** | – |
| rel-trial/study-outcome | 0.500 | 0.500 | 0.531 |

发现：

- **RT zero-shot ≈ 抄标签基线 + 一点点**。driver-dnf 上 RT 比 copy 高约 3 个点；user-repeat 上 RT（0.709）甚至低于完美检索 copy（0.732）。这以独立方式复现了 RT 论文 Table 4 的结论，且更狠：**一个不学习的基线在多任务上逼平 7000 万级预训练模型的 zero-shot**。
- **检索损失定量化**（hist-copy − ctx-copy 的差）：user-visits +10、user-repeat +9.4、driver-top3 +2.9 个点——这部分是纯粹被随机采样"丢掉"的标签信息，local/recency 采样（C）直接对应。
- **无标签任务两者都是 0.5**：这类任务上唯一的出路是结构推理（B 的动机）。

## 瓶颈排序与组件映射

| 排序 | 瓶颈 | 证据 | 对应组件 |
|---|---|---|---|
| 1 | 抄标签捷径，无结构推理 | copy≈RT；0-label 任务近随机且预测无方差 | **B** dropout（train 防捷径）、eflag（结构先验） |
| 2 | 检索/采样丢信息 + 噪声 | hist>ctx 差 3–10 点；翻面 34–43%；ensemble 免费增益 | **C** local/global、推理期 ensemble |
| 3 | 预算浪费在周边 | 周边中位 ~90% | row pooling（未实现，后续） |
| 4 | 无时间感 | Δt 中位数年计；timestamps 未进模型 | **A** 时间 RoPE |

注意 A 排最后不代表不重要——它是 C 的"感知配套"（采样保证近期事件进 context，RoPE 让模型知道它们是近期的），预期 A×C 有正交互。

## 实验协议教训（第一波试错）

同库 contd-pretrain（RT 论文的 contd 协议）在 lr=1e-4 下会因分布漂移让 eval 任务从 step 0 开始持续掉分（driver-dnf 0.736→0.618），导致 best-val 停在 step 0、变体无从分化。已改为**跨库 contd**：在 leave-db-out 原分布上继续训练并激活变体机制，eval 任务保持严格 zero-shot。
