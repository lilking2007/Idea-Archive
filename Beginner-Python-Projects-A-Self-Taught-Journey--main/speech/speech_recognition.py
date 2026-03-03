import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to recognize speech
def recognize_speech():
    # List available microphones
    mic_list = sr.Microphone.list_microphone_names()
    print("Available microphones:")
    for i, mic_name in enumerate(mic_list):
        print(f"{i}: {mic_name}")

    # Use the default microphone (usually index 0)
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)  # Calibrate for ambient noise
        print("Listening for your command...")

        # Listen for the first phrase
        try:
            audio = recognizer.listen(source, timeout=5)  # Added timeout for listening
            print("Recognizing...")
            
            # Recognize speech using Google Web Speech API
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command
            
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that. Please try again.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Call the function to start speech recognition
if __name__ == "__main__":
    recognize_speech()