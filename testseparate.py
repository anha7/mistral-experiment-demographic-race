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
question_number = int(sys.argv[1])
question = sys.argv[2]
gender = sys.argv[3]
repetition = int(sys.argv[4])

# Prepare initial message and combined user questions
messages = [
    {"role": "user", "content": "Create a character of a college first-year student in an introductory computer science class taught in Java. This student identifies as " + str(gender) + ". As this character, answer the following evaluation, providing only the correct answer with no explanation."},
    {"role": "assistant", "content": "Sure, I will create this character and answer as this student. What question do you have?"},
    {"role": "user", "content": question + "\n<END>"}
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
start_index = decoded.find("<END>") + len("<END>")
response = decoded[start_index:].strip()

# Print the response
print(f"Question: {question_number}, Repetition: {repetition}, Gender: {gender}")
print(f"Response: {response}\n\n\n")

