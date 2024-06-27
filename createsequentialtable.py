import re
import pandas as pd

# Define file path
file_path = 'output_file_sequential_2.txt'

# Define correct answers (without periods)
correct_answers = ['True', 'True', 'False', 'True', 'False', 'True', 'False', 'True', 'False', 'True']

# Initialize data store
data = []

# Define function that processes the file and tabulates the data
def process_file(file_path):
        # Read contents of the file
        with open(file_path, 'r') as file:
                content = file.read()

        # Define pattern to recognize each repetition block
        entry_pattern = re.compile(r'Repetition:\s*(\d+),\s*Role:\s*(\w+-?\w*),\s*Temperature:\s*([\d.]+).*?Response:\s*<s>(.*?)\.</s>', re.DOTALL)
        matches = entry_pattern.findall(content)

        for match in matches:
                repetition = int(match[0])
                role = match[1]
                temperature = float(match[2])
                llm_output = match[3].strip()

                # Remove the introductory and instructional text
                intro_text_pattern = re.compile(
                    r'Response:\s*<s>\s*\[INST\] You are taking the role of a college \w+-?\w* in an introductory computer science class. '
                    r'You are given the following evaluation and told to ONLY answer true or false to these 10 questions. Therefore, do NOT explain your answer choice. '
                    r'Simply provide the correct answer. \[/INST\]Sure, I will only provide the correct answers. What questions do you have\?</s> \[INST\] '
                    r'True or false: In Java, every variable has a type \(such as int, double, or String\) that is known at compile time.\s*'
                    r'True or false: In Java, the result of applying one of the arithmetic operators \(\+, -, \*, or /\) to two double operands always evaluates to a value of type double \(and never produces a run-time exception\).\s*'
                    r'True or false: In Java, if you attempt to use a local variable of type int in an expression before that variable has been assigned a value, Java will substitute the value 0.\s*'
                    r'True or false: In Java, if a variable is declared and initialized in the body of a for loop, that variable cannot be accessed outside that loop.\s*'
                    r'True or false: In Java, if you name a variable with all uppercase letters and initialize it to some value, attempting to subsequently change its value would lead to a compile-time error.\s*'
                    r'True or false: In Java, after you create and initialize an int\[\] array, you cannot change its length.\s*'
                    r'True or false: In Java, if a\[\] is an array of type char\[\] and length 10, then a\[0.0\] is a valid expression that gives its first element.\s*'
                    r'True or false: In Java, it is possible to declare, create, and initialize a String\[\] array without using the keyword new.\s*'
                    r'True or false: In Java, if a\[\] and b\[\] are two different arrays of the same type and length, then the expression \(a == b\) evaluates to true if the corresponding array elements are equal, and false otherwise.\s*'
                    r'True or false: In Java, the elements of an array of type int\[\] are stored contiguously in the computer’s memory \(i.e., in consecutive memory locations\).\s*\[/INST\]', 
                    re.DOTALL)
                llm_output = intro_text_pattern.sub('', llm_output).strip()

                # Remove other unwanted text patterns
                parts_pattern = re.compile(r'\d+\.\s|True or False answers for the given questions in Java programming:|True or false answers:|True or false responses:', re.DOTALL | re.IGNORECASE)
                llm_output = parts_pattern.sub('', llm_output).strip()

                # Split the remaining text by lines
                answers = llm_output.split('\n')

                for i, answer in enumerate(answers[:10]):
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

