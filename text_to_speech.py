import pyttsx3
import time

# Initialize TTS engine globally
engine = pyttsx3.init()

def speak_text(text):
    """Speaks the given text while ensuring the first words are not cut off."""
    engine.say(" ")
    engine.runAndWait()  # Dummy run to initialize the engine properly
    time.sleep(0.3)  # Small delay to allow engine readiness

    engine.say(text)
    engine.runAndWait()
