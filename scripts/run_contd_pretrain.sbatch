#!/bin/bash
#SBATCH --qos = student_high_res
#SBATCH --partition=slowlane
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --gpus=A40:1
#SBATCH --time=0-12:00:00
#SBATCH --output=rt_contd_pretrain_%j.out
#SBATCH --job-name=rt_contd_pretrain

set -euo pipefail

cd /mnt/nfs/home/st191486/rongchuan/relationaltransformer
export WANDB_MODE=disabled

pixi run python scripts/example_contd_pretrain.py
