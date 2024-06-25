import os
import subprocess
import sys

# Get question and  output file
output_file_sequential_2 = "combined_outputs.txt"

# Ensure the common output file is empty at the start
with open(output_file_sequential_2, "w") as f:
	f.write("")

# Create a list for roles
role_list = ["first-year", "senior", "professor"]

# Create a list for temperatures
temperature_list = [0.0, 1.0, 2.0] 

# Submit SLURM jobs
for role in role_list:
	for temperature in temperature_list:
		for i in range(1, 11):
			# Create a unique SLURM script for each question
			slurm_script = f"""#!/bin/bash
#SBATCH --job-name=sequential_{role}_{temperature}_{i}
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

python testsequential.py {role} {temperature} {i} >> output_file_sequential_2"""

			# Write SLURM script to a file
			slurm_filename = f"question.slurm"
			with open(slurm_filename, "w") as slurm_file:
				slurm_file.write(slurm_script)

			# Submit SLURM job
			subprocess.run(["sbatch", slurm_filename])
