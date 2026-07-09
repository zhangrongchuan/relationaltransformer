#!/bin/bash
#SBATCH --partition=slowlane
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --gpus=A40:1
#SBATCH --time=0-02:00:00
#SBATCH --output=rt_finetune_%j.out
#SBATCH --job-name=rt_finetune

set -euo pipefail

cd /mnt/nfs/home/st191486/rongchuan/relationaltransformer
export WANDB_MODE=disabled

pixi run python scripts/example_finetune.py
