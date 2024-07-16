import os
import subprocess
import sys

# Grab file of questions
question_file = "fall2022questions.txt"

with open(question_file, "r") as file:
	questions = [line.strip() for line in file.readlines()]

# Create a list for gender identities
gender_list = ["cisgender-woman", "cisgender-man", "transgender-woman", "transgender-man", "non-binary", "genderfluid", "genderqueer"]

# Submit SLURM jobs
for gender in gender_list:
	for i, question in enumerate(questions):		
		for j in range(1, 11):
			# Create a unique SLURM script for each question
			slurm_script = f"""#!/bin/bash
#SBATCH --job-name=sep_{i+1}_{gender}_{j}
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
cd /scratch/network/ak3987/mixtral_experiment_demographic_gender

python testseparate.py {i+1} "{question}" {gender} {j} >> separate_outputs.txt"""

			# Write SLURM script to a file
			slurm_filename = f"question.slurm"
			with open(slurm_filename, "w") as slurm_file:
				slurm_file.write(slurm_script)

			# Submit SLURM job
			subprocess.run(["sbatch", slurm_filename])
