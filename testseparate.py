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
question_number = sys.argv[1]
question = sys.argv[2]
gender = sys.argv[3]
repetition = int(sys.argv[5])

# Prepare initial message and combined user questions
messages = [
    {"role": "user", "content": ""},
    {"role": "assistant", "content": "Sure, I will only provide the correct answers. What questions do you have?"},
    {"role": "user", "content": question}
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
start_index = decoded.find(question) + len(question)
response = decoded[start_index:].strip()

# Print the response
print(f"Question: {question_number}, Repetition: {repetition}, Gender: {gender}")
print(f"Response: {response}\n\n\n")

