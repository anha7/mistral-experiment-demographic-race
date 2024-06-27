import re
import pandas as pd

# Define file path
file_path = 'output_file_sequential.txt'

# Define correct answers
correct_answers = ['True', 'True', 'False', 'True', 'False', 'True', 'False', 'True', 'False', 'True']

# Initialize data store
data = []

# Define function that processes the file and tabulates the data
def process_file(file_path):
        # Read contents of the file
        with open(file_path, 'r') as file:
                content = file.read()

        # Define pattern to recognize each repetition block
        entry_pattern = re.compile(r'Repetition:\s*(\d+),\s*Role:\s*(\w+-?\w*),\s*Temperature:\s*([\d.]+).*?Response:\s*<s>(.*?)\.</s>', re.DOTALL | re.MULTILINE)
        matches = entry_pattern.findall(content)

        # Process each repetition block
        for match in matches:
                repetition = int(match[0])
                role = match[1]
                temperature = float(match[2])
                llm_output = match[3].strip()

                # Remove unwanted text pattern
                pattern = re.compile(r'Response: [\INST]', re.DOTALL)
                llm_output = pattern.sub('', llm_output).strip()

                # Split the remaining text by lines
                answers = llm_output.split('\n')

                for i, answer in enumerate(answers):
                        correct_answer = correct_answers[i]
                        if (correct_answer.lower() in answer.lower()):
                                accuracy = 'Correct'
                        else:
                                accuracy = 'Incorrect'
                        data.append([i + 1, role, temperature, answer, accuracy, repetition])

# Process the file
process_file(file_path)

# Create a DataFrame
df = pd.DataFrame(data, columns=['Question Number', 'Role', 'Temperature', 'LLM Output', 'Is Correct', 'Repetition Number'])

# Save the DataFrame to an Excel file
output_file = 'sequential_table.xlsx'
df.to_excel(output_file, index=False)

output_file

