import threading
import datetime
from ai_assistant import chat_with_mistral
from calendar_sync import add_event, load_events, check_reminders
from text_to_speech import speak_text

def main():
    # Start the reminder checker in the background
    reminder_thread = threading.Thread(target=check_reminders, daemon=True)
    reminder_thread.start()

    while True:
        user_input = input("Ask Staplr: ").strip().lower()

        if user_input.startswith("remind me of"):
            try:
                parts = user_input.replace("remind me of", "").strip().split(" at ")
                if len(parts) == 2:
                    description, time_str = parts[0].strip(), parts[1].strip()
                    date = datetime.datetime.now().strftime("%Y-%m-%d")  # Defaults to today
                    duration = "30 mins"
                    reminder = True  # Always set reminders to true

                    add_event(date, time_str, duration, description, reminder)
                    print(f"Reminder set for '{description}' at {time_str}.")
                else:
                    print("Invalid format. Try: 'Remind me of <event> at <HH:MM>'")
            except Exception as e:
                print(f"Error setting reminder: {e}")

        elif user_input.startswith("add event"):
            try:
                parts = user_input.replace("add event", "").strip().split(" at ")
                if len(parts) == 2:
                    description, time_str = parts[0].strip(), parts[1].strip()
                    date = datetime.datetime.now().strftime("%Y-%m-%d")
                    duration = "30 mins"
                    reminder = False  # Default: no reminder unless specified

                    add_event(date, time_str, duration, description, reminder)
                    print(f"Event '{description}' added at {time_str}.")
                else:
                    print("Invalid format. Try: 'Add event <description> at <HH:MM>'")
            except Exception as e:
                print(f"Error adding event: {e}")

        elif user_input.startswith("speak"):
            text = user_input.replace("speak", "").strip()
            if text:
                speak_text(text)  # Directly use TTS
            else:
                print("Please provide text to speak.")

        elif user_input == "exit":
            print("Exiting Staplr.")
            break

        else:
            response = chat_with_mistral(user_input)
            print(response)

if __name__ == "__main__":
    main()
