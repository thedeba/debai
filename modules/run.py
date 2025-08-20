from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "/Users/macbook/Desktop/debai/debai",
    device_map="auto",                # automatically splits layers across devices
    torch_dtype="auto",
    offload_folder="offload" 
    )
tokenizer = AutoTokenizer.from_pretrained("/Users/macbook/Desktop/debai/debai")
import torch

messages = [
    {"role": "user", "content": "বাংলাদেশের ইতিহাস?"},
]

#device = "cuda" if torch.cuda.is_available() else "cpu"
device = "mps" if torch.backends.mps.is_available() else "cpu"
inputs = tokenizer.apply_chat_template(
    messages,
    tokenize = True,
    add_generation_prompt = True,
    return_tensors = "pt",
).to(device)

outputs = model.generate(input_ids = inputs, max_new_tokens = 2048, use_cache = True,
                         temperature = 0.5, min_p = 0.1)
tokenizer.batch_decode(outputs, skip_special_tokens=True)
output_string = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

# Split the output string by the 'assistant' role marker and get the last part
assistant_response = output_string.split('assistant')[-1]

print(assistant_response)