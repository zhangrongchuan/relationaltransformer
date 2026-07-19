#!/bin/bash
#SBATCH --qos=student_high_res
#SBATCH --partition=fastlane
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=24G
#SBATCH --gpus=A40:1
#SBATCH --time=0-00:30:00
#SBATCH --output=experiments/results/smoke_%j.out
#SBATCH --job-name=rt_smoke

set -euo pipefail
cd /mnt/nfs/home/st191486/rongchuan/relationaltransformer
export WANDB_MODE=disabled
pixi run python experiments/smoke_variants.py
