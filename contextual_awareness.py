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

# A dictionary to store conversation context per conversation ID.
# In production, consider using a persistent or session-based store.
conversation_context = {}

def generate_prompt(context, user_input):
    """
    Combine the conversation context with the new user input to create a prompt.
    """
    # Customize the prompt format as needed.
    prompt = context + "\nUser: " + user_input + "\nAssistant:"
    return prompt

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    # Optionally use a conversation_id provided by the client; default if not provided.
    conversation_id = data.get("conversation_id", "default")
    user_input = data.get("message", "")
    
    # Retrieve any existing conversation context
    context = conversation_context.get(conversation_id, "")
    
    # Create the prompt by combining past context with the current user input
    prompt = generate_prompt(context, user_input)
    
    # Generate the assistant's response using the pre-trained model
    generated = chatbot(prompt, max_length=150, do_sample=True)[0]['generated_text']
    
    # Extract the assistant's reply by removing the prompt part from the generated text.
    assistant_reply = generated[len(prompt):].strip()
    
    # Update conversation context (consider implementing context window management)
    updated_context = prompt + " " + assistant_reply
    conversation_context[conversation_id] = updated_context
    
    return jsonify({"response": assistant_reply})

if __name__ == "__main__":
    app.run(debug=True)