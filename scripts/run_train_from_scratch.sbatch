#!/bin/bash
#SBATCH --partition=slowlane
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --gpus=A40:1
#SBATCH --time=0-04:00:00
#SBATCH --output=rt_train_from_scratch_%j.out
#SBATCH --job-name=rt_train_scratch

set -euo pipefail

cd /mnt/nfs/home/st191486/rongchuan/relationaltransformer
export WANDB_MODE=disabled

pixi run python scripts/example_pretrain.py
