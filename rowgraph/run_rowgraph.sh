#!/bin/bash
#SBATCH --job-name=rowgraph
#SBATCH --qos=student_high_res
#SBATCH --partition=slowlane
#SBATCH --gpus=A40:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=96G
#SBATCH --time=0-12:00:00
#SBATCH --output=results/rowgraph_%j.out

cd /mnt/nfs/home/st191486/rongchuan/relationaltransformer
export WANDB_MODE=disabled

pixi run python rowgraph/train.py \
  --db rel-f1 \
  --task driver-dnf \
  --variant no_warm \
  --seed 0 \
  --steps 100000 \
  --seq-len 2048 \
  --d-model 256

# regression (adaptive k-means codebook; use --mem=128G for amazon/hm/stack)
# pixi run python rowgraph/train.py \
#   --db rel-amazon \
#   --task item-ltv \
#   --variant cb_no_warm \
#   --seed 0 \
#   --steps 100000 \
#   --seq-len 2048 \
#   --d-model 256
