import customtkinter as ctk
from staplr import process_staplr_query

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class StaplrUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Staplr Assistant")
        self.geometry("600x400")

        self.input_box = ctk.CTkEntry(self, placeholder_text="Ask Staplr...")
        self.input_box.pack(pady=20, fill="x", padx=20)

        self.output_box = ctk.CTkTextbox(self, height=200)
        self.output_box.pack(pady=10, fill="both", expand=True, padx=20)

        self.submit_btn = ctk.CTkButton(self, text="Send", command=self.process_input)
        self.submit_btn.pack(pady=10)

    def process_input(self):
        user_input = self.input_box.get()
        if user_input:
            response = process_staplr_query(user_input)
            self.output_box.insert("end", f"You: {user_input}\nStaplr: {response}\n\n")
            self.input_box.delete(0, "end")

# Run UI
if __name__ == "__main__":
    app = StaplrUI()
    app.mainloop()
