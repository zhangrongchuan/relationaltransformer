#!/bin/bash
#SBATCH --job-name=rowgraph
#SBATCH --qos=student_high_res
#SBATCH --partition=slowlane
#SBATCH --gpus=A40:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --time=0-12:00:00
#SBATCH --output=results/logs/%x_%j.out

cd /mnt/nfs/home/st191486/rongchuan/relationaltransformer
export PATH="$HOME/.local/bin:$PATH"   # pixi

pixi run python rowgraph/train.py \
  --db rel-f1 \
  --task driver-dnf \
  --variant no_warm \
  --seed 0
