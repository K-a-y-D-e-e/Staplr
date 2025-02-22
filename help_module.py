import tkinter as tk
from tkinter import scrolledtext, messagebox

# Help content for each topic
HELP_CONTENT = {
    "Email Extension": """
    Email Extension
    ----------------
    - Description: Send and receive emails directly through Staplr.
    - Usage: Use the "Send Email" button to compose and send emails. Use the "Check Emails" button to view your inbox.
    - Example: "Staplr, send an email to john@example.com."
    """,
    "Context Awareness": """
    Context Awareness
    -----------------
    - Description: Staplr understands the context of your work and provides relevant suggestions.
    - Usage: Type or speak naturally, and Staplr will respond accordingly.
    - Example: "What's on my calendar today?"
    """,
    "Calendar Sync": """
    Calendar Sync
    -------------
    - Description: Sync with your calendar to view and manage events.
    - Usage: Use the "Calendar Sync" button to view upcoming events.
    - Example: "Staplr, show my schedule for tomorrow."
    """,
    "Data Analytics": """
    Data Analytics
    --------------
    - Description: Analyze your data and provide insights.
    - Usage: Provide a dataset, and Staplr will generate a summary.
    - Example: "Staplr, analyze this data."
    """,
    "TTS": """
    Text-to-Speech (TTS)
    --------------------
    - Description: Text-to-Speech (TTS) technology converts written words into spoken speech. It first reads and understands the text, turning numbers and abbreviations into full words. Then, it figures out how each word should sound and adds natural changes in tone and speed to make it sound more human-like. Finally, the system generates the actual voice and plays it through speakers. Some systems use recordings of real voices, while others create speech using computer-generated sounds. The goal is to make the speech clear, natural, and easy to understand.
    - Usage: Enable TTS in settings or type 'speak'.
    - Example: "Staplr, read this out loud."
    """,
    "Chat Interaction": """
    Chat Interaction
    ----------------
    - Description: Interact with Staplr via a chat interface.
    - Usage: Type your queries, and Staplr will respond.
    - Example: "Staplr, what's the weather today?"
    """,
    "Help Option": """
    Help Option
    -----------
    - Description: Display this help menu for guidance.
    - Usage: Type 'help' or click the help button.
    - Example: "Staplr, help me."
    """
}

# Function to display the help menu
def show_help_menu():
    # Create the main window
    help_window = tk.Toplevel()
    help_window.title("Staplr Help Menu")

    # Add a listbox to display the topics
    topic_listbox = tk.Listbox(help_window, width=40, height=10)
    for topic in HELP_CONTENT.keys():
        topic_listbox.insert(tk.END, topic)
    topic_listbox.pack(padx=10, pady=10)

    # Add a scrolled text widget to display the help content
    help_text_area = scrolledtext.ScrolledText(help_window, width=60, height=20, wrap=tk.WORD)
    help_text_area.pack(padx=10, pady=10)

    # Function to display the selected topic's content
    def show_topic_content(event):
        selected_topic = topic_listbox.get(topic_listbox.curselection())
        help_text_area.delete(1.0, tk.END)  # Clear previous content
        help_text_area.insert(tk.INSERT, HELP_CONTENT[selected_topic])

    # Bind the listbox selection to the function
    topic_listbox.bind('<<ListboxSelect>>', show_topic_content)

    # Add a close button
    close_button = tk.Button(help_window, text="Close", command=help_window.destroy)
    close_button.pack(pady=10)

# Example usage in the main Staplr application
if __name__ == "__main__":
    # Create the main Staplr window
    root = tk.Tk()
    root.title("Staplr")

    # Add a "Help" button to the main window
    help_button = tk.Button(root, text="Help", command=show_help_menu, width=20, height=2)
    help_button.pack(pady=20)

    # Run the application
    root.mainloop()