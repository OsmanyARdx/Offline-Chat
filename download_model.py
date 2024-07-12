from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "ollama/dolphin-llama3"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Save the model and tokenizer to your project directory
model.save_pretrained('C:/Users/Osmany/OneDrive/Desktop/hub/AppFast/dolphin_llama3_model')
tokenizer.save_pretrained('C:/Users/Osmany/OneDrive/Desktop/hub/AppFast/dolphin_llama3_model')
