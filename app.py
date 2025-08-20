import gradio as gr
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load your model from HF Hub
model_name = "/Users/macbook/Desktop/debai/debai"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
device = "mps" if torch.backends.mps.is_available() else "cpu"

def generate_text(query, device="cpu"):
    # Build the chat-style prompt structure
    messages = [
        {"role": "user", "content": query},
    ]

    # Convert to model input
    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
    ).to(device)

    # Generate
    outputs = model.generate(
        input_ids=inputs,
        max_new_tokens=2048,
        use_cache=True,
        temperature=0.5,
        min_p=0.1,
    )

    # Decode and clean the response
    output_string = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    response = output_string.split("assistant")[-1].strip()
    return response



# Gradio interface
demo = gr.Interface(fn=generate_text, inputs="text", outputs="text")
demo.launch()
