import threading
import datetime
import os
import csv
import docx
from ai_assistant import chat_with_mistral
from calendar_sync import add_event, check_reminders
from text_to_speech import speak_text
from email_helper import suggest_email_template, autocomplete_sentence
from file_handler import process_file  # Import file processing functions
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Start reminder checking in a separate thread
def start_reminder_thread():
    reminder_thread = threading.Thread(target=check_reminders, daemon=True)
    reminder_thread.start()

def perform_eda(file_path):
    """Performs basic EDA on the given CSV file and returns a summary."""
    try:
        df = pd.read_csv(file_path)

        # Select only numeric columns for analysis
        numeric_df = df.select_dtypes(include=['number'])
        if numeric_df.empty:
            return "⚠️ No numeric data available for EDA."

        # Summary statistics
        summary = numeric_df.describe().to_string()

        # Handling missing values
        missing_values = df.isnull().sum().to_string()

        # Correlation matrix
        correlation_matrix = numeric_df.corr()
        heatmap_path = "eda_correlation_heatmap.png"
        
        # Save correlation heatmap
        plt.figure(figsize=(10, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Heatmap")
        plt.savefig(heatmap_path)
        plt.close()

        return f"📊 **EDA Summary:**\n\n{summary}\n\n🔍 **Missing Values:**\n{missing_values}\n\n📌 Correlation heatmap saved as '{heatmap_path}'"

    except Exception as e:
        return f"⚠️ Error processing EDA: {str(e)}"

# Read content from a Word document
def read_word_document(file_path):
    """Reads text from a .docx file."""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text if text.strip() else "The document is empty."
    except Exception as e:
        return f"Error reading Word document: {e}"

# Read CSV file content
def read_csv_file(file_path):
    """Reads content from a CSV file."""
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            data = "\n".join([", ".join(row) for row in reader])
        return data if data.strip() else "The CSV file is empty."
    except Exception as e:
        return f"Error reading CSV file: {e}"

# Process user commands
def process_staplr_query(query):
    query = query.lower()

    if query.startswith("perform eda on this file"):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return "⚠️ No file selected."
        eda_result = perform_eda(file_path)
        return f"📊 EDA Completed:\n{eda_result}"

    elif query.startswith("remind me of"):
        try:
            parts = query.replace("remind me of", "").strip().split(" at ")
            if len(parts) == 2:
                description, time_str = parts[0].strip(), parts[1].strip()
                date = datetime.datetime.now().strftime("%Y-%m-%d")
                duration = "30 mins"
                reminder = True

                add_event(date, time_str, duration, description, reminder)
                return f"✅ Reminder set for '{description}' at {time_str}."
            else:
                return "⚠️ Invalid format. Try: 'Remind me of <event> at <HH:MM>'"
        except Exception as e:
            return f"❌ Error setting reminder: {e}"

    elif query.startswith("add event"):
        try:
            parts = query.replace("add event", "").strip().split(" at ")
            if len(parts) == 2:
                description, time_str = parts[0].strip(), parts[1].strip()
                date = datetime.datetime.now().strftime("%Y-%m-%d")
                duration = "30 mins"
                reminder = False

                add_event(date, time_str, duration, description, reminder)
                return f"✅ Event '{description}' added at {time_str}."
            else:
                return "⚠️ Invalid format. Try: 'Add event <description> at <HH:MM>'"
        except Exception as e:
            return f"❌ Error adding event: {e}"

    elif query == "exit":
        return "👋 Exiting Staplr."

    else:
        # Ensure Mistral only acts within predefined rules
        system_prompt = "You are an AI assistant named Staplr. You MUST follow only the functions defined in Staplr.py and should not generate responses outside them. If the query is unrelated, respond with: 'I can only assist with predefined functions.'"
        return chat_with_mistral(query)
    
# Main function to run Staplr in terminal mode
def main():
    start_reminder_thread()

    while True:
        user_input = input("Ask Staplr: ").strip()
        response = process_staplr_query(user_input)
        print(response)

        if response == "👋 Exiting Staplr.":
            break

if __name__ == "__main__":
    main()
