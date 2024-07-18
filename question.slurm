#!/bin/bash
#SBATCH --job-name=seq_10
#SBATCH --output=output.txt
#SBATCH --error=error.txt
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G
#SBATCH --gres=gpu:1
#SBATCH --time=48:00:00

module purge
module load anaconda3/2024.2
conda activate /home/ak3987/.conda/envs/mixtral_env
cd /scratch/network/ak3987/mixtral_experiment_demographic_race

python testsequential.py "White" 10 >> sequential_outputs.txt