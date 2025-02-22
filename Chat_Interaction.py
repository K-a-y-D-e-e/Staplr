import tkinter as tk
from tkinter import scrolledtext
import requests
import json

def generate_llm_response(prompt):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = json.dumps({
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    })
    
    try:
        response = requests.post(url, headers=headers, data=data)
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
        response_json = response.json()
        return response_json.get("response", "Failed to get response.")
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"

def process_chat_input():
    user_input = chat_input.get("1.0", tk.END).strip()
    if user_input:
        chat_display.insert(tk.END, f"You: {user_input}\n", "user")
        response = generate_llm_response(user_input)
        chat_display.insert(tk.END, f"Staplr: {response}\n", "bot")
        chat_input.delete("1.0", tk.END)

root = tk.Tk()
root.title("Staplr - Chat Interaction")
root.geometry("600x500")
root.configure(bg="#f0f0f0")

chat_display = scrolledtext.ScrolledText(root, width=70, height=15, wrap=tk.WORD)
chat_display.pack(pady=10)
chat_display.tag_config("user", foreground="blue")
chat_display.tag_config("bot", foreground="green")

chat_input = tk.Text(root, height=2, width=50)
chat_input.pack(pady=5)

chat_button = tk.Button(root, text="Send", command=process_chat_input, bg="#4CAF50", fg="white")
chat_button.pack()

root.mainloop()
