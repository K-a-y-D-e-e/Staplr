import pyttsx3

def speak_text(text):
    """Uses TTS to speak the given text."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    speak_text("This is a test for text-to-speech.")
