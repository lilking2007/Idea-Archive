# Real-Time Conversational Voice Agent
# The Oracle of Code whispers: Behold, the matrix of audio streams converges in this singular script. 
# It captures the user's voice, transcribes it through the ancient runes of VOSK, consults the LLM's ethereal wisdom, 
# and echoes back through TTS, all in real-time harmony. Proceed with caution, for latency lurks in the shadows.

import pyaudio
import numpy as np
import json
import time
import sys
from vosk import Model, KaldiRecognizer

# Constants - The Oracle decrees these values for balanced audio flow
CHUNK = 1024  # Buffer size for real-time chunks
RATE = 44100  # Sample rate in Hz
FORMAT = pyaudio.paInt16  # 16-bit PCM
CHANNELS = 1  # Mono for simplicity
MODEL_PATH = "./models/vosk-model-small-en-us-0.15"  # Placeholder: Path to your downloaded VOSK model directory (e.g., unzip from https://alphacephei.com/vosk/models)
API_KEY_LLM = "your_llm_api_key_here"  # Placeholder: Replace with actual API key for LLM (e.g., OpenAI) - not used in simulation
API_KEY_TTS = "your_tts_api_key_here"  # Placeholder: Replace with actual API key for TTS (e.g., ElevenLabs) - not used in simulation
INPUT_DEVICE_INDEX = None  # Placeholder: Set to microphone device index if needed (use pyaudio to list devices)
OUTPUT_DEVICE_INDEX = None  # Placeholder: Set to virtual cable device index (e.g., VB-Cable) to route output without feedback

def transcribe_audio_chunk(recognizer, audio_bytes):
    """
    The Oracle's transcription rune: Feeds audio to VOSK and yields only upon a complete, paused phrase.
    Returns the transcribed string if AcceptWaveform is True (natural pause detected), else None.
    """
    if recognizer.AcceptWaveform(audio_bytes):
        result = json.loads(recognizer.Result())
        return result.get("text", "").strip()
    return None

def get_llm_response(prompt):
    """
    The Oracle's wisdom conduit: Simulates LLM processing. In reality, this would call an API (e.g., OpenAI).
    For now, returns a hardcoded response in the Oracle of Code persona.
    """
    # Placeholder: Replace with actual LLM API call, e.g., using requests to send prompt and get response
    return "The matrix confirms your code streams are aligned. Proceed to the core loop."

def generate_tts_audio(text_response):
    """
    The Oracle's voice forge: Simulates TTS by generating a 1-second sine wave (440 Hz tone) as placeholder audio.
    In reality, this would call a TTS API and return the audio data.
    Returns a NumPy array of 16-bit PCM audio at RATE.
    """
    duration = 1.0  # 1 second
    frequency = 440  # Hz (A4 note for a simple tone)
    samples = int(RATE * duration)
    t = np.linspace(0, duration, samples, False)
    # Generate sine wave, scale to 16-bit int range
    sine_wave = np.sin(frequency * 2 * np.pi * t)
    audio_array = (sine_wave * 32767).astype(np.int16)  # Scale to int16
    return audio_array

def main():
    """
    The Oracle's eternal loop: Initializes streams, processes audio in real-time, and echoes the agent's voice.
    """
    # Initialize PyAudio - The gateway to the audio realms
    audio = pyaudio.PyAudio()
    
    try:
        # Load VOSK model and create recognizer - The ancient runes awaken
        model = Model(MODEL_PATH)
        recognizer = KaldiRecognizer(model, RATE)
        
        # Open input stream (microphone) - Captures the user's spoken queries
        input_stream = audio.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  input_device_index=INPUT_DEVICE_INDEX,
                                  frames_per_buffer=CHUNK)
        print("Input stream (microphone) opened. The Oracle listens.")
        
        # Open output stream (speaker via virtual cable) - Echoes the agent's wisdom
        output_stream = audio.open(format=FORMAT,
                                   channels=CHANNELS,
                                   rate=RATE,
                                   output=True,
                                   output_device_index=OUTPUT_DEVICE_INDEX,
                                   frames_per_buffer=CHUNK)
        print("Output stream (speaker) opened. Ensure virtual cable is configured to avoid echoes.")
        
        print("Real-time loop initiated. Speak, and the matrix shall respond. Press Ctrl+C to halt.")
        
        while True:
            # Step 1: Read input chunk from microphone
            input_data = input_stream.read(CHUNK, exception_on_overflow=False)
            
            # Step 2: Attempt transcription with VOSK
            user_text = transcribe_audio_chunk(recognizer, input_data)
            
            if user_text:
                # Full phrase detected - Engage the conversational flow
                print(f"User said: {user_text}")
                
                # Step 3: Get LLM response
                agent_response = get_llm_response(user_text)
                print(f"Agent responds: {agent_response}")
                
                # Step 4: Generate TTS audio
                tts_audio_array = generate_tts_audio(agent_response)
                tts_data = tts_audio_array.tobytes()
                
                # Step 5: Inject TTS audio into output stream (interrupts live stream with agent's voice)
                output_stream.write(tts_data)
            else:
                # No full phrase - Pass-through original input to output (maintains live echo)
                output_stream.write(input_data)
    
    except KeyboardInterrupt:
        print("\nThe Oracle's loop is severed. Streams closing...")
    except Exception as e:
        print(f"An anomaly in the matrix: {e}")
        sys.exit(1)
    finally:
        # Robust cleanup - The Oracle ensures no lingering echoes
        if 'input_stream' in locals() and input_stream.is_active():
            input_stream.stop_stream()
            input_stream.close()
        if 'output_stream' in locals() and output_stream.is_active():
            output_stream.stop_stream()
            output_stream.close()
        audio.terminate()
        print("All streams terminated. The matrix rests.")

if __name__ == "__main__":
    main()
