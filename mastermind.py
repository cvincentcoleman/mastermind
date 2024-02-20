#!/usr/bin/env python3

from openai import AsyncOpenAI, audio
import os
from scipy.io.wavfile import write
from dotenv import load_dotenv
import sounddevice as sd
import asyncio

# pull this from my .env file
# Load the .env file
load_dotenv()

client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPENAI_API_KEY"),
)

def giveCommand():

    fs = 44100  # Sample rate
    seconds = 5  # Duration of recording

    myRecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)

    print("listening...")
    # sd.wait()  # Wait until recording is finished
    input("Press Enter to stop recording")
    sd.stop()
    write('command.wav', fs, myRecording)  # Save as WAV file

    print("done")

async def transcribe():
    audio_file= open("command.wav", "rb")
    transcript = await client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return transcript.text


async def main() -> None:

    fileName = input("Enter the file: ")

    giveCommand()

    command = await transcribe()
    print("")
    print("Command: " + command)

    os.remove("command.wav")

    # Read the React Native file into a string
    with open(fileName, 'r') as file:
        file_content = file.read()

    # Define the modification you want to make
    modification_prompt = f"{file_content}\n\n# Now, modify the above code by with the following request: {command}.\n\n Include the whole file. ONLY include code in your response."

    print("")
    print("Working on that...")

    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "When writing code, please do not use inline styles for React Native. Instead, use the StyleSheet API.",
            },
            {
                "role": "user",
                "content": modification_prompt,
            }
        ],
        model="gpt-3.5-turbo"
    )

    print("")
    print("Working out the details...")

    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": chat_completion.choices[0].message.content + "\n\n Strip everything from this response and only return the code. Strip extra characters like ``` or ```jsx",
            }
        ],
        model="gpt-3.5-turbo"
    )

    newCode = chat_completion.choices[0].message.content

    # Open the file in write mode
    with open(fileName, 'w') as file:
      # Write the new text to the file
        file.write(newCode)

    print("")
    print("✨ File has been updated with the new code ✨")
    print("")

asyncio.run(main())
