#!/bin/bash
#SBATCH --job-name=sequential_professor_2.0_10
#SBATCH --output=output.txt
#SBATCH --error=error.txt
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G
#SBATCH --gres=gpu:1
#SBATCH --time=24:00:00
#SBATCH --mail-user=ak3987@princeton.edu

module purge
module load anaconda3/2024.2
conda activate /home/ak3987/.conda/envs/mixtral_env
cd /scratch/network/ak3987/mixtral_testing

python testsequential.py professor 2.0 10 >> output_file_sequential