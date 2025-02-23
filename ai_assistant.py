import ollama

def chat_with_mistral(query):
    """Process user query strictly within Staplr's functions."""
    system_prompt = (
        "You are an AI assistant named Staplr. "
        "You MUST follow only the functions defined in Staplr.py. "
        "If the query is unrelated, respond with: '⚠️ I can only assist with predefined functions in Staplr.'"
    )

    response = ollama.chat(model="mistral", messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ])

    return response['message']['content']
