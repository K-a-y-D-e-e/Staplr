import ollama

def chat_with_mistral(prompt):
    """Send a prompt to the locally installed Mistral model and return the response."""
    try:
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"] if "message" in response else "AI response error."
    except Exception as e:
        return f"Error communicating with Mistral: {str(e)}"
