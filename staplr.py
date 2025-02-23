import threading
import datetime
from ai_assistant import chat_with_mistral
from calendar_sync import add_event, check_reminders
from text_to_speech import speak_text
from email_helper import suggest_email_template, autocomplete_sentence

def handle_email_commands(command):
    """Handles email-related commands like template suggestions and autocomplete."""
    if command.startswith("email template"):
        template_type = command.replace("email template ", "").strip()
        response = suggest_email_template(template_type)
        return response
    elif command.startswith("autocomplete"):
        partial_text = command.replace("autocomplete ", "").strip()
        response = autocomplete_sentence(partial_text)
        return response
    else:
        return "Invalid email command. Try 'email template <type>' or 'autocomplete <text>'."

def extract_text_in_quotes(text):
    """Extracts text inside double or single quotes for TTS."""
    import re
    matches = re.findall(r'"([^"]+)"|\'([^\']+)\'', text)
    return matches[0][0] if matches else None

def process_staplr_query(user_input):
    """Processes user input and returns a response."""
    user_input = user_input.strip().lower()

    # Reminder Handling
    if user_input.startswith("remind me of"):
        try:
            parts = user_input.replace("remind me of", "").strip().split(" at ")
            if len(parts) == 2:
                description, time_str = parts[0].strip(), parts[1].strip()
                date = datetime.datetime.now().strftime("%Y-%m-%d")
                duration = "30 mins"
                reminder = True  

                add_event(date, time_str, duration, description, reminder)
                return f"Reminder set for '{description}' at {time_str}."
            else:
                return "Invalid format. Try: 'Remind me of <event> at <HH:MM>'"
        except Exception as e:
            return f"Error setting reminder: {e}"

    # Event Handling
    elif user_input.startswith("add event"):
        try:
            parts = user_input.replace("add event", "").strip().split(" at ")
            if len(parts) == 2:
                description, time_str = parts[0].strip(), parts[1].strip()
                date = datetime.datetime.now().strftime("%Y-%m-%d")
                duration = "30 mins"
                reminder = False  

                add_event(date, time_str, duration, description, reminder)
                return f"Event '{description}' added at {time_str}."
            else:
                return "Invalid format. Try: 'Add event <description> at <HH:MM>'"
        except Exception as e:
            return f"Error adding event: {e}"

    # TTS Handling (Text-to-Speech)
    elif '"' in user_input or "'" in user_input:
        text = extract_text_in_quotes(user_input)
        if text:
            threading.Thread(target=speak_text, args=(text,), daemon=True).start()
            return f"Speaking: {text}"
        else:
            return "I didn't find any text inside quotes to read."

    # Email Assistance
    elif user_input.startswith("email template") or user_input.startswith("autocomplete"):
        return handle_email_commands(user_input)

    # Exit Command
    elif user_input == "exit":
        return "Exiting Staplr."

    # Default Chat Assistant
    else:
        return chat_with_mistral(user_input)

def main():
    """Main function to handle console-based interaction."""
    print("Staplr Assistant is running. Type 'exit' to quit.")
    
    # Start reminder checking thread
    reminder_thread = threading.Thread(target=check_reminders, daemon=True)
    reminder_thread.start()

    while True:
        user_input = input("Ask Staplr: ").strip()
        response = process_staplr_query(user_input)
        print(response)

        if user_input.lower() == "exit":
            break

if __name__ == "__main__":
    main()
