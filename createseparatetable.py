import re
import pandas as pd

# Define file path
file_path = "separate_outputs.txt"

# Define correct answers
correct_answers = [
	"2.0",
	"2.0",
	"1",
	"compile-time error or run-time exception",
	"true",
	"True",
	"True",
	"False",
	"True",
	"False",
	"Yes",
	"No",
	"No",
	"Yes",
	"No",
	"True",
	"False",
	"True",
	"False",
	"True",
	"True",
	"False",
	"True",
	"False",
	"Unknown"
]

# Initialize data store
data = []

# Define function that processes each file and tabulates the data
def process_file(file_path):
	# Read contents of the file
	with open(file_path, 'r') as file:
		content = file.read()

	# Define patterns to recognize the repetition number, role, temperature, and LLM response
	entry_pattern = re.compile(r'Question:\s*(\d+),\s*Repetition:\s*(\d+),\s*Gender:\s*(\w+-?\w*)\s*Response:\s*\[\/INST\]\s*(.*?)\s*(?=(Question:|$))', re.DOTALL)

	# Find all matches within the contents
	matches = entry_pattern.findall(content)

	for match in matches:
		question_number = int(match[0])
		repetition = int(match[1])
		gender = match[2]
		llm_output = match[3].strip()

		# Check if LLM answered question correctly
		correct_answer = correct_answers[question_number - 1]
		if(correct_answer.lower() in llm_output.lower()):
			accuracy = 'Correct'
		else:
			accuracy = 'Incorrect'

		# Tabulate all data
		data.append([question_number, gender, llm_output, accuracy, repetition])


# Loop through each question and process the corresponding file
process_file(file_path)

# Create a DataFrame
df1 = pd.DataFrame(data=data, columns=['Question Number', 'Gender', 'LLM Output', 'Is Correct', 'Repetition Number'])

# Save the DataFrame to an Excel file
output_file = 'separate_table.xlsx'
df1.to_excel(output_file, index=False)

output_file
