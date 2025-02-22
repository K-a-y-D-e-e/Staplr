from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
from flask import Flask, request, jsonify

# Initialize Flask App
app = Flask(__name__)

##### NLP MODEL (CONTEXTUAL AWARENESS) #####
model_name = "mistralai/Mistral-7B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")
chatbot = pipeline("text-generation", model=model, tokenizer=tokenizer)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    response = chatbot(user_input, max_length=150, do_sample=True)[0]['generated_text']
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
