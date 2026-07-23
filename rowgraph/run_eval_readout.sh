#!/bin/bash
#SBATCH --job-name=readout
#SBATCH --qos=student_high_res
#SBATCH --partition=slowlane
#SBATCH --gpus=A40:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --time=0-12:00:00
#SBATCH --output=experiments/results/readout_%j.out

cd /mnt/nfs/home/st191486/rongchuan/relationaltransformer
export WANDB_MODE=disabled

# Re-score finished codebook checkpoints under global vs local readout (inference only).
# Flagship first, then base.
pixi run python experiments/exp2_rowgraph/eval_readout.py relgraph_cb_no_warm
pixi run python experiments/exp2_rowgraph/eval_readout.py cb_no_warm
