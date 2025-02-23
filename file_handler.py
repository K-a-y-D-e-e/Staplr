import csv
from docx import Document
import os

def read_word_document(file_path):
    """Reads content from a Word (.docx) document."""
    try:
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs]) or "📄 (Word file is empty)"
    except Exception as e:
        return f"⚠️ Error reading Word document: {e}"

def read_csv_file(file_path):
    """Reads data from a CSV file and formats it as a string."""
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            data = [", ".join(row) for row in reader]  # Formatting rows as strings
        return "\n".join(data) if data else "📊 (CSV file is empty)"
    except Exception as e:
        return f"⚠️ Error reading CSV file: {e}"

def process_file(file_path):
    """Determines file type and reads its content."""
    if not os.path.exists(file_path):
        return "⚠️ Error: File not found."

    if file_path.endswith(".docx"):
        return read_word_document(file_path)
    
    elif file_path.endswith(".csv"):
        return read_csv_file(file_path)
    
    return "⚠️ Unsupported file type. Please upload a .docx or .csv file."
