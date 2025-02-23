import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from staplr import process_staplr_query  # Handles user queries
from file_handler import process_file  # Extracts file content
from text_to_speech import speak_text  # Reads text aloud

# Set UI Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class StaplrUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.last_file_content = None  # Store last attached file content
        self.file_name = None  # Store file name for reference

        self.title("Staplr Assistant")
        self.geometry("600x450")

        # Input Field
        self.input_box = ctk.CTkEntry(self, placeholder_text="Ask Staplr...")
        self.input_box.pack(pady=10, fill="x", padx=20)
        self.input_box.bind("<Return>", lambda event: self.process_input())  # Bind Enter key

        # Output Display
        self.output_box = ctk.CTkTextbox(self, height=200)
        self.output_box.pack(pady=10, fill="both", expand=True, padx=20)

        # Button Frame
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=10, fill="x", padx=20)

        # Buttons
        self.submit_btn = ctk.CTkButton(self.button_frame, text="Send", command=self.process_input)
        self.submit_btn.pack(side="left", padx=10)

        self.attach_btn = ctk.CTkButton(self.button_frame, text="Attach File", command=self.attach_file)
        self.attach_btn.pack(side="left", padx=10)

        self.read_btn = ctk.CTkButton(self.button_frame, text="Read Aloud", command=self.read_aloud)
        self.read_btn.pack(side="left", padx=10)

        self.clear_btn = ctk.CTkButton(self.button_frame, text="Clear", command=self.clear_output)
        self.clear_btn.pack(side="left", padx=10)

        self.help_btn = ctk.CTkButton(self.button_frame, text="Help", command=self.show_help)
        self.help_btn.pack(side="left", padx=10)    

        # File Label
        self.file_label = ctk.CTkLabel(self, text="No file selected", text_color="lightgray")
        self.file_label.pack(pady=5)

    def attach_file(self):
        """Opens file dialog to select a Word (.docx) file and stores the content."""
        file_path = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
        if file_path:
            self.file_name = file_path.split("/")[-1]  # Extract file name
            self.file_label.configure(text=f"Selected: {self.file_name}")
            self.last_file_content = process_file(file_path)  # Store the file content
            self.display_output(f"\n📂 File Attached: {self.file_name}\n\n{self.last_file_content}\n")

    def read_aloud(self):
        """Uses TTS to read the attached file out loud."""
        if self.last_file_content:
            speak_text(self.last_file_content)  # Pass the extracted text to TTS
            self.display_output("📖 Reading the attached file...")
        else:
            self.display_output("⚠️ No file attached. Please attach a file first.")

    def process_input(self):
        """Handles user queries."""
        user_input = self.input_box.get().strip()

        if user_input.lower() in ["read this file", "read this file for me", "read it aloud"]:
            if self.last_file_content:
                speak_text(self.last_file_content)  # Read the file aloud
                response = "📖 Reading the attached file..."
            else:
                response = "⚠️ No file attached. Please attach a file first."
        else:
            response = process_staplr_query(user_input)

        self.display_output(f"You: {user_input}\nStaplr: {response}\n")
        self.input_box.delete(0, "end")

    def clear_output(self):
        """Clears the output display."""
        self.output_box.delete("1.0", "end")

    def display_output(self, text):
        """Utility function to insert text into the output box."""
        self.output_box.insert("end", text + "\n")
        self.output_box.see("end")  # Auto-scroll to the latest entry

    def show_help(self):
        """Displays the available features and how to use them."""
        help_text = (
            "📌 **Staplr Features:**\n"
            "- 🔊 **Text to Speech**: Reads aloud text from attached documents.\n"
            "- ⏰ **Setting/Scheduling a Reminder**: Use 'Remind me of <event> at <HH:MM>' to schedule reminders.\n"
            "- ✉️ **Helps With Writing an Email**: Provides email suggestions.\n"
            "- 📊 **EDA Analysis**: Performs exploratory data analysis on CSV files.\n\n"
            "📢 **Prompt Guidelines:**\n"
            "- Use 'Read this file' to have the document read aloud.\n"
            "- Use 'Perform EDA on this file' to analyze a CSV file.\n"
            "- Use 'Remind me of <event> at <HH:MM>' to set a reminder.\n"
            "- Ask in natural language for email suggestions."
        )
        self.display_output(help_text)

# Run UI
if __name__ == "__main__":
    app = StaplrUI()
    app.mainloop()
