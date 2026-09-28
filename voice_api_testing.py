import os
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Define your input and output files
input_voice_file = "Recording (2).m4a"    # Your testing audio file
output_speech_file = "generated_speech.wav"  # The file TTS will create

print("--- Step 1: Voice to Text (Transcription) ---")
try:
    # Open the local audio file in binary mode
    with open(input_voice_file, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(input_voice_file, file.read()),
            model="whisper-large-v3", # Ultra-fast transcription
            temperature=0.0
        )
    
    # Store the resulting text
    extracted_text = transcription.text
    print(f"Successfully transcribed!\nResult: \"{extracted_text}\"\n")

except Exception as e:
    print(f"Error during transcription: {e}")
    extracted_text = None


# Run Text-to-Speech only if the first step succeeded
if extracted_text:
    print("--- Step 2: Text to Speech (Synthesis) ---")
    try:
        # Generate new spoken audio from the text
        response = client.audio.speech.create(
            model="canopylabs/orpheus-v1-english", # Groq's high-fidelity English TTS model
            voice="troy",                         # Choose your voice style (e.g., "troy", "hannah")
            input=f"You just said: {extracted_text}", # Feeding the transcribed text back in
            response_format="wav"                 # Supported: wav, mp3, etc.
        )
        
        # Save the audio stream to a file
        response.write_to_file(output_speech_file)
        print(f"Successfully generated speech! Audio saved to: {output_speech_file}")

    except Exception as e:
        print(f"Error during speech generation: {e}")
