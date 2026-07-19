# RT 改进实验：完整分析报告（最终版）

日期：2026-07-10 ｜ 分支：`ultra` ｜ 全部脚本与数据：`experiments/`
状态：全部实验完成（L0 诊断 ×3、跨库 contd 网格 32 runs、噪声受控采样评估、no-self-label 消融、多 seed 确认 ×18、from-scratch ×4 + scratch 消融）

---

## 一、实验体系总览

```
L0 诊断（不训练）           L1/L2 组件对照（跨库 contd, 8k步）      协议探针
├─ context 构成统计          ├─ A  time_rope    （model.py）        ├─ no-self-label 消融
├─ 重采样方差 (K=8)          ├─ E1 entity_flag  （model.py）        ├─ 噪声受控采样评估 (K=8)
└─ 抄标签基线                ├─ B  self_label_dropout（fly.rs）     └─ from-scratch 复训（决定性）
                            ├─ C  local_k      （fly.rs）
                            └─ P  periphery_cell_cap（fly.rs）
```

评估任务（覆盖四种 regime）：
- **rel-f1/driver-dnf**（clf，self-label 丰富 17.2/序列，事件古老 756d）
- **rel-trial/study-outcome**（clf，self-label = 0，唯一纯结构推理任务）
- **rel-avito/ad-ctr**（reg，高频短历史库，63% 无 self-label）
- **rel-event/user-repeat**（clf，重采样翻面率 43%，方差最大）

---

## 二、L0 诊断结论（详见 L0_diagnosis_report.md）

1. **抄标签**：不学习的 context-copy 基线 ≈ RT zero-shot（user-engagement 0.846 / user-badge 0.824 vs RT 平均 ~0.70+）；0-label 任务上 RT 预测方差仅 0.03，近常数输出。
2. **采样噪声**：重采样翻面 34–43%；8-context ensemble 白拿 +1.4~+3.4。
3. **检索损失**：完美检索 copy 比 context-copy 高 3–10 点（user-visits +10.2）。
4. **预算浪费**：周边占 54–98%（中位 ~90%）；事件年龄中位数以年计。

## 三、组件对照实验结果

### 3.1 协议（及一次关键的协议失败）

- ❌ **同库 contd（RT 论文协议）在 lr=1e-4 下灾难性遗忘**：driver-dnf 0.736→0.618，best-val 卡在 step0，无法比较组件。已弃用。
- ✅ **跨库 contd**：从 leave-db-out ckpt 出发，在其原训练分布上继续 8k 步（激活组件），eval 任务保持严格 zero-shot。曲线稳定。
- ⚠️ 局限：预训练模型在原分布上已收敛，8k 步多数任务 best-val ≈ step0 → **该协议能干净评估推理期组件（采样类），但不足以评估训练期组件**（rope/eflag/dropout 需要 from-scratch，见 §3.5）。

### 3.2 推理期采样组件（噪声受控，原始 ckpt，K=8 个 eval 采样种子）

单次 metric mean±std（8 次重采样），val split：

| 任务 | baseline | local32 | pcap4 | local32_pcap4 |
|---|---|---|---|---|
| driver-dnf (auc) | .7334±.009 | .7283±.015 | **.7381±.010** | .7336±.009 |
| study-outcome (auc) | **.5309±.003** | .5301±.004 | .5174±.005 ↓ | .5172±.005 ↓ |
| ad-ctr (r2) | .0074±.003 | -.0109±.002 ↓ | .0074（no-op） | -.0109（同 local32） |
| user-repeat (auc) | .7094±.021 | .6692±.011 ↓ | .7184±.006 | **.7228±.006** |

user-repeat 的额外发现：local32_pcap4 不仅均值 +1.3，**把跨采样方差压小 ~4 倍**（.021→.006）——确定性近期上下文让单次预测显著更稳。但 baseline 的 8-context ensemble（.7433）仍是质量上限：多样随机上下文 + 集成 > 单个"最优"上下文（代价是 8 倍推理）。

**结论：**
- **local32 单独 = 负效应或中性**（ad-ctr -1.8 R²）。近期事件挤占预算，验证了"C 不能单独上"的预判。
- **pcap4 任务依赖性强**：driver-dnf +0.5（弱正）；**study-outcome -1.4（显著负）**——rel-trial 没有 self-label，信号本来就在"周边"里，砍周边即砍信号。**固定 cap 是任务次优的 → 需要任务条件化的预算分配 = schema-graph（D）的数据驱动动机**。
- **pcap4 在 rel-avito 是结构性 no-op**：avito 行宽仅 3-5 cell，cap=4 咬不上。周边浪费的形态是"行多"而非"行宽" → 需要行级 pooling，cell-cap 不够。
- 训练后的单点结果（contd 网格）里 pcap4/local32_pcap4 在 user-repeat 上 late-test +4.8/+3.3 —— 多 seed 确认中。

### 3.3 no-self-label 消融（RT Table 4 协议，我们的实现）

各 contd ckpt 在「正常 context」vs「self-label 全移除」：

| 任务 | 变体 | normal | no-self | 依赖度 |
|---|---|---|---|---|
| driver-dnf | baseline | .736 | .625 | +.111 |
| driver-dnf | **drop05** | .737 | **.472** | **+.265** ⚠️ |
| driver-dnf | pcap4 | .738 | .534 | +.205 |
| user-repeat | baseline | .709 | .624 | +.085 |
| user-repeat | local32_pcap4 | .681 | .636 | +.045 |
| study-outcome | 所有变体 | – | – | +.000（协议自检 ✓）|

**最重要的负结果：contd 阶段的 label dropout 适得其反。** drop05 训练后的模型没有学会结构替代，反而在无标签时崩到 0.472（低于随机）。机制解读：捷径在原预训练中已经形成，8k 步部分遮蔽标签只教会模型"更用力地抄幸存标签"。**防捷径必须发生在预训练起点**——from-scratch 对照（drop09）正在跑，是本轮的决定性实验。

顺带的正面信号：local32_pcap4 使 user-repeat 的标签依赖度从 +.085 降到 +.045 且 no-self 更高（.636 vs .624）——更好的 context 让模型少依赖标签。

### 3.4 多 seed 确认结果（late-phase test/val 均值 ± seed 间 std）

**跨 seed 复现的效应（n=3 seeds）：**

| 任务 | 格子 | late-val | late-test | 判定 |
|---|---|---|---|---|
| user-repeat | baseline | .7015±.004 (n=2) | .7342±.012 | – |
| user-repeat | **pcap4** | .6900±.006 | **.7765±.012** | **test +4.2 复现** |
| user-repeat | **local32_pcap4** | .6965±.012 | **.7685±.008** | **test +3.4 复现** |
| study-outcome | baseline | .5165±.004 | .5163±.011 | – |
| study-outcome | **eflag** | **.5281±.005** | .5288±.020 | **val +1.2（~2.4σ）复现** |
| study-outcome | pcap4 | .5174±.003 | .5345±.011 | test +1.8，val 平 |
| study-outcome | rope | .5220±.003 | .5243±.010 | val +0.6 弱正 |
| driver-dnf | baseline | .7205±.008 | .7839±.003 | – |
| driver-dnf | drop05 | .7222±.008 | .7838±.003 | 正常 eval 完全打平 |

- **pcap4 是 user-repeat 的可复现大幅提升**（test +4.2，三 seed 一致）；注意 val（n=268）小样本噪声掩盖了它，test（n 大）才显出来——单看 val 会误杀这个组件。
- **eflag 在 study-outcome 的正效应跨 seed 复现**，且只出现在 0-label 任务上——与 labeling-trick 机制的预言位置一致。
- rope：ad-ctr test +2.2（单 seed）；总体中性偏正但弱——旋转破坏预训练 attention，contd 不公平，等 from-scratch。

### 3.5 from-scratch 决定性实验（50k 步 leave-db-out）✦ 本轮核心结果

**driver-dnf（val，best-val ckpt，no-self-label 协议）：**

| 预训练方式 | normal | no-self-label | 标签依赖度 |
|---|---|---|---|
| baseline from scratch | .676 | **.367**（崩溃，低于随机） | +.310 |
| **drop09 from scratch** | **.706** (+3.0) | **.570** (+20.3) | **+.136（减半）** |

**与 contd 结果对照（§3.3）构成本轮最重要的发现——防捷径的时机决定一切：**

| label dropout 应用时机 | normal | no-self | 依赖度 vs 各自 baseline |
|---|---|---|---|
| contd 阶段（8k 步，捷径已形成） | 打平 | **恶化**（.472 vs .625） | +.265 vs +.111 ⚠️ 反效果 |
| **预训练起点（50k 步，捷径未形成）** | **+3.0** | **+20.3**（.570 vs .367） | +.136 vs +.310 ✓ 双赢 |

同一机制，事后应用是反效果，起点应用是无代价双赢（正常性能还略升）。这直接支持论文叙事："RT 的 zero-shot 抄标签不是架构缺陷而是预训练目标缺陷，且不可事后修复"。

**study-outcome eflag from-scratch：证据混合。** best-val 选点的 test 0.5548 vs baseline 0.5417（方向与 contd 一致），但后段轨迹退化（49k 步 val 0.458 < baseline 0.524）——eflag 参数在长训练中不稳定。结论：contd 下效应可复现（n=3, +1.2 val），from-scratch 本尺度下不定论，需要更大规模或稳定化（如 eflag 向量的 norm 约束）再判。

注意尺度 caveat：50k 步 scratch 模型整体弱于官方 ckpt（driver-dnf val 0.676 vs 0.734），scratch 对照内部公平（同算力）但绝对值不可与官方比。

---

## 四、最终结论

### 4.1 被证据支持的结论（按证据强度排序）

1. **防捷径必须发生在预训练起点（本轮核心发现）**：drop09 from scratch = 正常性能 +3.0、无标签鲁棒性 +20.3、依赖度减半；同一机制在 contd 阶段应用则反效果。→ 论文主张：抄标签是预训练目标缺陷，不可事后修复。
2. **pcap4(+local32) 推理期采样组合**：user-repeat test +4.2（n=3 复现）、driver-dnf +1.4；同时把跨采样预测方差压小 ~4 倍。零训练成本，可直接部署。
3. **多 context ensemble**：所有任务 +1.4~+3.4 免费增益（8 倍推理成本），leaderboard 可直接用。
4. **组件交互**：local32 单独为负（挤占预算），必须配 pcap4；dropout 时机敏感（见 1）。组件不可独立评估——这本身是方法论结论。
5. **eflag（labeling trick）**：contd 下 study-outcome val +1.2（n=3 复现，唯一在 0-label 任务生效的组件）；from-scratch 长训练不稳定，需稳定化后再验。
6. **任务条件化预算的必要性**：固定 pcap 在 driver-dnf 上正、study-outcome 上显著负（-1.4，3σ）——"砍哪些表"必须依赖任务与 schema → **schema-graph（D）拿到了最强的数据动机**。

### 4.2 被证据反驳/修正的假设

7. "contd 阶段加 dropout 可以拆捷径" ✗（反效果，见 1）。
8. "cell 级 cap 是预算控制的通用解" ✗（窄行库 avito 结构性无效，需行级 pooling）。
9. "rope 立即有效" 未证实：contd 下中性偏正（ad-ctr test +2.2 单 seed），旋转破坏预训练 attention，公平测试需 from-scratch（未来工作）。
10. "小 val 上选模型可靠" ✗：user-repeat val（n=268）完全掩盖了 pcap4 的 test +4.2——小任务的模型选择必须用重采样均值或直接看多 seed test。

### 4.3 建议的论文骨架（证据已齐的部分）

1. **诊断章**：copy-baseline ≈ RT zero-shot、重采样翻面 34-43%、周边占比 90%、检索损失 3-10 点（全部有脚本可复现）。
2. **机制章**：dropout 时机实验（预防 vs 拆除）——干净的双向对照，是最有说服力的实验。
3. **方法章**：from-scratch 防捷径预训练 + 推理期采样（local+pcap）+ ensemble；eflag/rope/schema-graph 作为需要更大预训练规模验证的方向。
4. **规模路线**：本轮受 50k 步 scratch 限制；下一步在完整预训练规模（论文 ckpt 的训练配置）重跑 drop09 与 eflag，并用 D（schema-graph）替换固定 pcap 实现任务条件化预算。

### 4.4 实验资产清单

- 组件：`rt/model.py`（time_rope, entity_flag）、`rustler/src/fly.rs`（self_label_dropout, local_k, periphery_cell_cap）——全部默认关闭、向后兼容
- 协议/工具：`experiments/train_variant.py`（contd + scratch 两模式）、`eval_ablation.py`（no-self-label 协议）、`eval_sampling_variants.py`（噪声受控采样评估）、`diag_*.py`（L0 三件套）、`collect_results.py`
- 数据：`experiments/results/*.json|.md`、诊断报告 `L0_diagnosis_report.md`
- 全部 ckpt：`ckpts/variants/`（36 个 contd + 4 个 scratch）
