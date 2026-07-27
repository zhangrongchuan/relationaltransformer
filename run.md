# 直接跑（有 GPU 的机器，不走 SLURM）

```bash
cd /mnt/nfs/home/st191486/rongchuan/relationaltransformer
export WANDB_MODE=disabled
```

## RowGraph base (d256)

```bash
pixi run python rowgraph/train.py --db rel-f1 --task driver-dnf --variant no_warm
```

## RelGraph (d256)

```bash
pixi run python rowgraph/train.py --db rel-f1 --task driver-dnf --variant relgraph_no_warm
```

## RelGraph + 自适应回归码本（回归任务用）

```bash
pixi run python rowgraph/train.py --db rel-amazon --task item-ltv --variant relgraph_cb_no_warm
```

---

# 参数

| flag | 默认 | 说明 |
|---|---|---|
| `--db` | 必填 | 评估数据库（训练时完全不见 = 零样本） |
| `--task` | 必填 | 任务名（`--table` 是别名） |
| `--variant` | 必填 | 模型配置，见下表 |
| `--seed` | 0 | 随机种子，多 seed 用于报 ±std |
| `--steps` | 100000 | 训练步数（冒烟测试用 2000） |
| `--seq-len` | 2048 | 上下文 cell 数（RT 用 1024；4096+ 实测更差） |
| `--d-model` | 256 | 模型宽度（512 收益不明显；warm_start 只支持 256） |

`--help` 会列出全部合法任务和 variant。

## variant

主力四个：

| variant | 关系图 | drop09 | 码本 | 参数 |
|---|---|---|---|---|
| `no_warm` | ✗ | ✗ | ✗ | 2.05M |
| `dropE09_no_warm` | ✗ | ✓ | ✗ | 2.05M |
| `relgraph_no_warm` | ✓ | ✗ | ✗ | 2.78M |
| `relgraph_cb_no_warm` | ✓ | ✗ | ✓ | 2.78M |

消融/历史：`full`（热启动 RT 编码器，会导入抄标签偏见）、`no_mp`、`no_time`、
`no_labels`、`dropE09`、`dropE05_no_warm`、`attn*`、`relgraph_dropE09_no_warm`、
`cb_no_warm`。

> `no_warm` 后缀 = 不热启动。主力配置都带它。

## 任务

**分类**：amazon/{user,item}-churn · avito/user-{clicks,visits} ·
event/user-{repeat,ignore} · f1/driver-{dnf,top3} · hm/user-churn ·
stack/user-{badge,engagement} · trial/study-outcome

**回归**：amazon/{item,user}-ltv · avito/ad-ctr · event/user-attendance ·
f1/driver-position · hm/item-sales · stack/post-votes ·
trial/{site-success,study-adverse}

分类/回归自动判断，不用指定。

---

# 常用

```bash
# 冒烟测试（几分钟，确认环境没问题）
pixi run python rowgraph/train.py --db rel-f1 --task driver-dnf --variant no_warm --steps 2000

# 多 seed
pixi run python rowgraph/train.py --db rel-f1 --task driver-dnf --variant relgraph_no_warm --seed 1

# 对齐 RT 的上下文长度
pixi run python rowgraph/train.py --db rel-f1 --task driver-dnf --variant relgraph_no_warm --seq-len 1024

# 后台跑 + 日志
nohup pixi run python rowgraph/train.py --db rel-f1 --task driver-dnf --variant relgraph_no_warm \
  > run.log 2>&1 &
```

# SLURM

```bash
sbatch --job-name=rg_f1_dnf --partition=slowlane --time=0-12:00:00 --mem=48G -c 8 \
  experiments/run_eval_jobs.sbatch rowgraph/train.py \
  --db rel-f1 --task driver-dnf --variant relgraph_no_warm
```

内存：大库（amazon/hm/stack）分类 `--mem=128G -c 6`、回归 `--mem=96G -c 6`；
小库（f1/avito/trial）`--mem=48G -c 8`。48G 跑大库会 OOM。
`fastlane` 分区上限 4h，训练必须用 `slowlane`。

# 结果

```
experiments/results/rowgraph_{variant}/{db}/{table}/{时间戳}/
    config.json      完整配置（含 git commit）
    evals.jsonl      每次 eval 的 normal + noself
    best.pt          最佳权重
    final_full.json  全量 test 结果
```

> 旧的位置参数写法（`train.py rel-f1 driver-dnf no_warm 0 100000 2048 256`）
> 仍然可用，但已弃用，会打一行提示。注意它的 steps 默认值是 20000。
