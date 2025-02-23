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
        numeric_df = df.select_dtypes(include=['number'])
        if numeric_df.empty:
            return "⚠️ No numeric data available for EDA."

        summary = numeric_df.describe().to_string()
        missing_values = df.isnull().sum().to_string()
        correlation_matrix = numeric_df.corr()
        heatmap_path = "eda_correlation_heatmap.png"
        
        plt.figure(figsize=(10, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Heatmap")
        plt.savefig(heatmap_path)
        plt.close()

        return f"📊 **EDA Summary:**\n\n{summary}\n\n🔍 **Missing Values:**\n{missing_values}\n\n📌 Correlation heatmap saved as '{heatmap_path}'"

    except Exception as e:
        return f"⚠️ Error processing EDA: {str(e)}"

def read_word_document(file_path):
    """Reads text from a .docx file."""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text if text.strip() else "The document is empty."
    except Exception as e:
        return f"Error reading Word document: {e}"

def read_csv_file(file_path):
    """Reads content from a CSV file."""
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            data = "\n".join([", ".join(row) for row in reader])
        return data if data.strip() else "The CSV file is empty."
    except Exception as e:
        return f"Error reading CSV file: {e}"

def process_staplr_query(query):
    query = query.lower()

    if query.startswith("perform eda on this file"):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return "⚠️ No file selected."
        return perform_eda(file_path)
    
    elif query.startswith("remind me of"):
        try:
            parts = query.replace("remind me of", "").strip().split(" at ")
            if len(parts) == 2:
                description, time_str = parts[0].strip(), parts[1].strip()
                date = datetime.datetime.now().strftime("%Y-%m-%d")
                duration = "30 mins"
                add_event(date, time_str, duration, description, reminder=True)
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
                add_event(date, time_str, duration, description, reminder=False)
                return f"✅ Event '{description}' added at {time_str}."
            else:
                return "⚠️ Invalid format. Try: 'Add event <description> at <HH:MM>'"
        except Exception as e:
            return f"❌ Error adding event: {e}"
    
    elif query.startswith("speak") or query.startswith("repeat after me"):
        text_to_speak = query.replace("speak", "").replace("repeat after me", "").strip()
        if text_to_speak:
            speak_text(text_to_speak)
            return f"🎤 Speaking: {text_to_speak}"
        return "⚠️ No text provided to speak."
    
    elif query == "exit":
        return "👋 Exiting Staplr."
    
    else:
        return "⚠️ I can only assist with predefined functions."
    
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
