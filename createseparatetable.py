import re
import pandas as pd

# Define file paths
file_paths = [
	'output_file_1.txt', 'output_file_2.txt', 'output_file_3.txt', 'output_file_4.txt',
	'output_file_5.txt', 'output_file_6.txt', 'output_file_7.txt', 'output_file_8.txt',
	'output_file_9.txt', 'output_file_10.txt'
]

# Define questions
questions = [
	'true or false: In Java, every variable has a type (such as int, double, or String) that is known at compile time.',
	'true or false: In Java, the result of applying one of the arithmetic operators (+, -, *, or /) to two double operands always evaluates to a value of type double (and never produces a run-time exception).',
	'true or false: In Java, if you attempt to use a local variable of type int in an expression before that variable has been assigned a value, Java will substitute the value 0.'
	'true or false: In Java, if a variable is declared and initialized in the body of a for loop, that variable cannot be accessed outside that loop.'
	'true or false: In Java, if you name a variable with all uppercase letters and initialize it to some value, attempting to subsequently change its value would lead to a compile-time error.'
	'true or false: In Java, after you create and initialize an int[] array, you cannot change its length.'
	'true or false: In Java, if a[] is an array of type char[] and length 10, then a[0.0] is a valid expression that gives its first element.'
	'true or false: In Java, it is possible to declare, create, and initialize a String[] array without using the keyword new.'
	'true or false: In Java, if a[] and b[] are two different arrays of the same type and length, then the expression (a == b) evaluates to true if the corresponding array elements are equal, and false otherwise.'
	'true or false: In Java, the elements of an array of type int[] are stored contiguously in the computer’s memory (i.e., in consecutive memory locations).'
]

# Define correct answers
correct_answers = ['True.', 'True.', 'False.', 'True.', 'False.', 'True.', 'False.', 'True.', 'False.', 'True.']

# Initialize data store
data = []

# Define function that processes each file and tabulates the data
def process_file(file_path, question_number, question, correct_answer):
	# Read contents of the file
	with open(file_path, 'r') as file:
		content = file.read()

	# Define patterns to recognize the repetition number, role, temperature, and LLM response
	entry_pattern = re.compile(
        	r'Repetition:\s*(\d+),\s*Role:\s*(\w+-?\w*),\s*Temperature:\s*([\d.]+).*?Response:\s*<s>(.*?)\.</s>',
	        re.DOTALL)


	# Define pattern that removes the prompt portion from the LLM output
	prompt_pattern = re.compile(
        	rf'\[INST\] You are taking the role of a college \w+-?\w* in an introductory computer science class. You are given the following evaluation and told to ONLY answer true or false to the questions. Therefore, do NOT explain your answer choice. Simply provide the correct answer. \[/INST\]Sure, I will only provide the correct answers. What questions do you have\?</s> \[INST\] {re.escape(question)} \[/INST\]', 
        	re.DOTALL)

	# Find all matches within the contents
	matches = entry_pattern.findall(content)

	for match in matches:
		repetition = int(match[0])
		role = match[1]
		temperature = float(match[2])
		llm_output = match[3].strip()

		# Remove prompt portion from the LLM output
		llm_output = prompt_pattern.sub('', llm_output).strip()

		# Check if LLM answered question correctly
		if(llm_output.split()[0] == correct_answer):
			accuracy = 'Correct'
		else:
			accuracy = 'Incorrect'

		# Tabulate all data
		data.append([question_number, role, temperature, llm_output, accuracy, repetition])


# Loop through each question and process the corresponding file
for i in range(10):
	process_file(file_paths[i], i+1, questions[1], correct_answers[i])

# Create a DataFrame
df1 = pd.DataFrame(data=data, columns=['Question Number', 'Role', 'Temperature', 'LLM Output', 'Is Correct', 'Repetition Number'])

# Save the DataFrame to an Excel file
output_file = 'separate_table.xlsx'
df1.to_excel(output_file, index=False)

output_file
