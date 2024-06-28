import os
import subprocess
import sys

# Get question and  output file
output_file_separate = "combined_outputs.txt"

# Ensure the common output file is empty at the start
with open(output_file_separate, "w") as f:
	f.write("")

# Create a list for questions
questions_list = [
	(1, "True or false: In Java, every variable has a type (such as int, double, or String) that is known at compile time."),
	(2, "True or false: In Java, the result of applying one of the arithmetic operators (+, -, *, or /) to two double operands always evaluates to a value of type double (and never produces a run-time exception)."),
	(3, "True or false: In Java, if you attempt to use a local variable of type int in an expression before that variable has been assigned a value, Java will substitute the value 0."),
	(4, "True or false: In Java, if a variable is declared and initialized in the body of a for loop, that variable cannot be accessed outside that loop."),
	(5, "True or false: In Java, if you name a variable with all uppercase letters and initialize it to some value, attempting to subsequently change its value would lead to a compile-time error."),
	(6, "True or false: In Java, after you create and initialize an int[] array, you cannot change its length."),
	(7, "True or false: In Java, if a[] is an array of type char[] and length 10, then a[0.0] is a valid expression that gives its first element."),
	(8, "True or false: In Java, it is possible to declare, create, and initialize a String[] array without using the keyword new."),
	(9, "True or false: In Java, if a[] and b[] are two different arrays of the same type and length, then the expression (a == b) evaluates to true if the corresponding array elements are equal, and false otherwise."),
	(10, "True or false: In Java, the elements of an array of type int[] are stored contiguously in the computer’s memory (i.e., in consecutive memory locations).")
]

# Create a list for roles
role_list = ["first-year", "senior", "professor"]

# Create a list for temperatures
temperature_list = [0.0, 1.0, 2.0] 

# Submit SLURM jobs
for j, question in questions_list:
	for role in role_list:
		for temperature in temperature_list:
			for i in range(1, 11):
				# Create a unique SLURM script for each question
				slurm_script = f"""#!/bin/bash
#SBATCH --job-name={j}_{role}_{temperature}_{i}
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

python testseparate.py {j} "{question}" {role} {temperature} {i} >> output_file_separate"""

				# Write SLURM script to a file
				slurm_filename = f"question.slurm"
				with open(slurm_filename, "w") as slurm_file:
					slurm_file.write(slurm_script)

				# Submit SLURM job
				subprocess.run(["sbatch", slurm_filename])
