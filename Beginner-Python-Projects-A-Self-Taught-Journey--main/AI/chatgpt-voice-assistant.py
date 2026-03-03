import os
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
import numpy as np

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
model = 'gpt-3.5-turbo'

# Set up the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()
voice = engine.getProperty('voices')[1]
engine.setProperty('voice', voice.id)
name = "RYAN"
greetings = [
    f"What's up master {name}",
    "Yeah?",
    "Well, hello there, Master of Puns and Jokes - how's it going today?",
    f"Ahoy there, Captain {name}! How's the ship sailing?",
    f"Bonjour, Monsieur {name}! Comment ça va? Wait, why the hell am I speaking French?"
]

# Listen for the wake word "hey pos"
def listen_for_wake_word(source):
    print("Listening for 'Hey POS'...")

    while True:
        try:
            audio = r.listen(source, timeout=5)  # Set timeout for listening
            text = r.recognize_google(audio)
            if "hey pos" in text.lower():
                print("Wake word detected.")
                engine.say(np.random.choice(greetings))
                engine.runAndWait()
                listen_and_respond(source)
            else:
                print("No wake word detected, continuing to listen.")
        except sr.UnknownValueError:
            # If speech is not recognized, continue listening
            pass
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            engine.say(f"Could not request results; {e}")
            engine.runAndWait()
            break  # Exit on error with API request
        except Exception as e:
            print(f"Unexpected error: {e}")
            engine.say(f"Unexpected error occurred: {e}")
            engine.runAndWait()
            break  # Exit on other errors

# Listen for user input and respond with OpenAI API
def listen_and_respond(source):
    print("Listening for input...")

    while True:
        try:
            audio = r.listen(source, timeout=10)  # Set timeout for listening
            text = r.recognize_google(audio)
            print(f"You said: {text}")

            # Allow user to quit
            if "quit" in text.lower() or "exit" in text.lower():
                engine.say("Goodbye, master!")
                engine.runAndWait()
                break

            # Send input to OpenAI API
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": text}]
            )
            response_text = response.choices[0].message.content
            print(f"OpenAI response: {response_text}")

            # Speak the response
            engine.say(response_text)
            engine.runAndWait()

            # Wait a short period before listening again to prevent rapid looping
            time.sleep(1)

        except sr.UnknownValueError:
            # If speech is not recognized, continue listening for the wake word
            print("Could not understand the audio. Please try again.")
            continue

        except sr.RequestError as e:
            # Handle issues with the API request
            print(f"Error with speech recognition service: {e}")
            engine.say(f"Error with speech recognition service: {e}")
            engine.runAndWait()
            break  # Exit on error with recognition service

        except Exception as e:
            print(f"Unexpected error: {e}")
            engine.say(f"Unexpected error occurred: {e}")
            engine.runAndWait()
            break  # Exit on other errors

# Use the default microphone as the audio source
with sr.Microphone() as source:
    # Adjust for ambient noise
    r.adjust_for_ambient_noise(source)
    listen_for_wake_word(source)
