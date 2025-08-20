from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# -------------------------------
# Load model & tokenizer from HF Hub
# -------------------------------
model_name = "thedeba/debai"  # HF Hub model path
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
device = "cpu"  # Spaces free tier uses CPU; you can switch to "cuda" if GPU granted
#model.to(device)

# -------------------------------
# FastAPI setup
# -------------------------------
app = FastAPI(title="Debai API")

class Query(BaseModel):
    text: str

@app.post("/generate")
def generate(query: Query):
    messages = [{"role": "user", "content": query.text}]

    # Convert to model input using chat template
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

    # Decode & extract assistant response
    output_string = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    response = output_string.split("assistant")[-1].strip()
    return {"response": response}

@app.get("/")
def root():
    return {"message": "Debai FastAPI is running!"}
