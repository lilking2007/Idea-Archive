import speech.speech_recognition as sr

def live_speech_to_text():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    try:
        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Ready to listen! Speak now.")

            # Continuously listen to the microphone
            while True:
                print("Listening...")
                audio = recognizer.listen(source, phrase_time_limit=5)  # Optional: adjust time limit as needed

                print("Processing speech...")
                try:
                    # Convert speech to text using Google's Web Speech API
                    text = recognizer.recognize_google(audio, language="en-US")
                    print(f"You said: {text}")
                except sr.UnknownValueError:
                    print("Sorry, I could not understand the audio.")
                except sr.RequestError as e:
                    print(f"Could not request results from the speech service; {e}")
    except OSError as e:
        print(f"Microphone error: {e}. Please check your microphone settings.")
    except KeyboardInterrupt:
        print("\nExiting program. Press Ctrl+C to stop.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    live_speech_to_text()