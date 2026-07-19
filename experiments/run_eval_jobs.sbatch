#!/bin/bash
#SBATCH --qos=student_high_res
#SBATCH --partition=fastlane
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --gpus=A40:1
#SBATCH --time=0-04:00:00
#SBATCH --output=experiments/results/evaljob_%x_%j.out
#SBATCH --job-name=rt_eval

set -euo pipefail
cd /mnt/nfs/home/st191486/rongchuan/relationaltransformer
export WANDB_MODE=disabled
pixi run python "$@"
