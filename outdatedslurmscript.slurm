#!/bin/bash
#SBATCH --job-name=hf-trial   # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem=32G         # total memory (4G is default)
#SBATCH --gres=gpu:1             # number of gpus per node
#SBATCH --time=00:20:00          # total run time limit (HH:MM:SS)
#SBATCH --mail-type=begin        # send email when job begins
#SBATCH --mail-type=end          # send email when job ends
#SBATCH --mail-user=ak3987@princeton.edu

module purge
module load anaconda3/2024.2
conda activate /home/ak3987/.conda/envs/mixtral_env

cd /scratch/network/ak3987/mixtral_testing

python testfall2022questions.py
