import re
import pandas as pd

# Define file path
file_path = "output_file_separate.txt"

# Define correct answers
correct_answers = ['True', 'True', 'False', 'True', 'False', 'True', 'False', 'True', 'False', 'True']

# Initialize data store
data = []

# Define function that processes each file and tabulates the data
def process_file(file_path):
	# Read contents of the file
	with open(file_path, 'r') as file:
		content = file.read()

	# Define patterns to recognize the repetition number, role, temperature, and LLM response
	entry_pattern = re.compile(
        	r'Question:\s*(\d+),\s*Repetition:\s*(\d+),\s*Role:\s*(\w+-?\w*),\s*Temperature:\s*([\d.]+).*?Response:\s*<s>(.*?)\.</s>', re.DOTALL)

	# Find all matches within the contents
	matches = entry_pattern.findall(content)

	for match in matches:
		question_number = int(match[0])
		repetition = int(match[1])
		role = match[2]
		temperature = float(match[3])
		llm_output = match[4].strip()

		# Check if LLM answered question correctly
		if(correct_answers[question_number - 1] in llm_output):
			accuracy = 'Correct'
		else:
			accuracy = 'Incorrect'

		# Tabulate all data
		data.append([question_number, role, temperature, llm_output, accuracy, repetition])


# Loop through each question and process the corresponding file
process_file(file_path)

# Create a DataFrame
df1 = pd.DataFrame(data=data, columns=['Question Number', 'Role', 'Temperature', 'LLM Output', 'Is Correct', 'Repetition Number'])

# Save the DataFrame to an Excel file
output_file = 'separate_table.xlsx'
df1.to_excel(output_file, index=False)

output_file
