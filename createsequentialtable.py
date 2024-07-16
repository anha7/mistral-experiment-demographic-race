import re
import pandas as pd

# Define file path
file_path = 'output_file_sequential.txt'

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

# Define function that processes the file and tabulates the data
def process_file(file_path):
        # Read contents of the file
        with open(file_path, 'r') as file:
                content = file.read()

        # Define pattern to recognize each repetition block
        entry_pattern = re.compile(r'Repetition:\s*(\d+),\s*Gender:\s*(\w+-?\w*),\s*Response:\s*\[\/INST\]\s*(.*?)\s*(?=(Repetition:|$))', re.DOTALL)
        matches = entry_pattern.findall(content)

        # Process each repetition block
        for match in matches:
                repetition = int(match[0])
                gender = match[1]
                llm_output = match[2].strip()

                # Split the remaining text by lines
                answers = re.split(r'\n+', llm_output)
                answers = [a.strip() for a in answers if a.strip()]

                for i, answer in enumerate(answers[:10]):
                        correct_answer = correct_answers[i]
                        if (correct_answer.lower() in answer.lower()):
                                accuracy = 'Correct'
                        else:
                                accuracy = 'Incorrect'
                        data.append([i + 1, gender, answer, accuracy, repetition])

# Process the file
process_file(file_path)

# Create a DataFrame
df = pd.DataFrame(data, columns=['Question Number', 'Gender', 'LLM Output', 'Is Correct', 'Repetition Number'])

# Save the DataFrame to an Excel file
output_file = 'sequential_table.xlsx'
df.to_excel(output_file, index=False)

output_file

