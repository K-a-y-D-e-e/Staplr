import json
import time
import datetime
from text_to_speech import speak_text

EVENTS_FILE = "events.json"

def load_events():
    try:
        with open(EVENTS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_events(events):
    with open(EVENTS_FILE, "w") as file:
        json.dump(events, file, indent=4)

def add_event(date, time_str, duration, description, reminder):
    events = load_events()
    new_event = {
        "date": date,
        "time": time_str,
        "duration": duration,
        "description": description,
        "reminder": reminder
    }
    events.append(new_event)
    save_events(events)
    print("Event added successfully!")

def check_reminders():
    """Checks if there are any reminders and speaks them when the time comes."""
    while True:
        events = load_events()
        current_time = datetime.datetime.now().strftime("%H:%M")
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")

        for event in events:
            if event["reminder"] and event["date"] == current_date and event["time"] == current_time:
                reminder_message = f"Reminder: {event['description']} at {event['time']}"
                print(reminder_message)
                speak_text(reminder_message)

        time.sleep(60)  # Check every minute
