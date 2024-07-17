import os
import subprocess
import sys

# Create a list for racial identities
race_list = ["American Indian or Alaska Native", "Asian", "Black or African American", "Hispanic or Latino", "Native Hawaiian or Other Pacific Islander", "White"]

# Submit SLURM jobs
for race in race_list:
	for i in range(1, 11):
		# Create a unique SLURM script for each question
		slurm_script = f"""#!/bin/bash
#SBATCH --job-name=seq_{i}_{race}
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

python testsequential.py "{race}" {i} >> sequential_outputs.txt"""

		# Write SLURM script to a file
		slurm_filename = f"question.slurm"
		with open(slurm_filename, "w") as slurm_file:
			slurm_file.write(slurm_script)

		# Submit SLURM job
		subprocess.run(["sbatch", slurm_filename])
