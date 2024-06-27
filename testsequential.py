import os
import sys
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load model and tokenizer
device = "cuda"
model_id = "mistralai/Mistral-7B-Instruct-v0.2"
saved_dir = os.path.join("/scratch/network/ak3987/.cache/saved_tokenizers", model_id)
tokenizer = AutoTokenizer.from_pretrained(saved_dir)
saved_dir = os.path.join("/scratch/network/ak3987/.cache/saved_models", model_id)
model = AutoModelForCausalLM.from_pretrained(saved_dir)

# Read command-line arguments
question_file = "fall2022questions.txt"
role = sys.argv[1]
temperature = float(sys.argv[2])
repetition = sys.argv[3]

# Retrieve questions list
with open(question_file, "r") as file:
	questions = [line.strip() for line in file.readlines()]

# Combine questions list into one entity
combined_questions = "\n".join(questions)

# Prepare initial message and combined user questions
messages = [
    {"role": "user", "content": "You are taking the role of a college " + str(role) + " in an introductory computer science class. You are given the following evaluation and told to ONLY answer true or false to these 10 questions. Therefore, do NOT explain your answer choice. Simply provide the correct answer."},
    {"role": "assistant", "content": "Sure, I will only provide the correct answers. What questions do you have?"},
    {"role": "user", "content": combined_questions}
]

# Encode messages
encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt", legacy=False)

# Move inputs and model to the device
model_inputs = encodeds.to(device)
model.to(device)

# Generate responses
generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True)

# Decode responses
decoded = tokenizer.batch_decode(generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)[0]

# Extract only the assistant's response
start_index = decoded.find("True or false: In Java, the elements of an array of type int[] are stored contiguously in the computer’s memory (i.e., in consecutive memory locations).") + len("True or false: In Java, the elements of an array of type int[] are stored contiguously in the computer’s memory (i.e., in consecutive memory locations).")
response = decoded[start_index:].strip()

# Print the response
print(f"Repetition: {repetition}, Role: {role}, Temperature: {temperature}")
print(f"Response: {response}\n\n\n")
