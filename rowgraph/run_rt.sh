#!/bin/bash
#SBATCH --job-name=rt
#SBATCH --qos=student_high_res
#SBATCH --partition=slowlane
#SBATCH --gpus=A40:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=96G
#SBATCH --time=0-12:00:00
#SBATCH --output=results/rt_%j.out

cd /mnt/nfs/home/st191486/rongchuan/relationaltransformer
export WANDB_MODE=disabled

pixi run python experiments/exp1_rt_components/train_variant.py rel-f1 driver-dnf baseline 0 scratch

# anti-shortcut version (self-label dropout p=0.9 from init)
# pixi run python experiments/exp1_rt_components/train_variant.py rel-f1 driver-dnf drop09 0 scratch
