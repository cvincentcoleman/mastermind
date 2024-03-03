#!/usr/bin/env python3

from openai import AsyncOpenAI, audio
import os
from scipy.io.wavfile import write
from dotenv import load_dotenv
import sounddevice as sd
import asyncio
import base64
import pyperclip



# pull this from my .env file
# Load the .env file
load_dotenv()

client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPENAI_API_KEY"),
)

def giveCommand():

    fs = 44100  # Sample rate
    seconds = 15  # Duration of recording

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

    
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

fileName = "screencapture.png"

async def main() -> None:
    os.system(f"screencapture -i {fileName}")

    giveCommand()

    command = await transcribe()
    print("")
    print("Command: " + command)

    os.remove("command.wav")


    # Define the modification you want to make
    modification_prompt = f"I'm writing a detox test. Please provide code to perform the following task: {command}.\n\n Include the lines of code necessary to perform the task. ONLY include code in your response with no codeblock formatting."

    print("")
    print("Working on that...")

    base64_image = encode_image(fileName)

    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": modification_prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            },
        ],
        model="gpt-4-vision-preview"
    )

    print("")
    print("Working out the details...")
    
    print(chat_completion.choices[0].message.content)
    
    pyperclip.copy(chat_completion.choices[0].message.content)
    

    # chat_completion = await client.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": chat_completion.choices[0].message.content + "\n\n Strip everything from this response and only return the code. Strip extra characters like ``` or ```jsx",
    #         }
    #     ],
    #     model="gpt-3.5-turbo"
    # )

    # newCode = chat_completion.choices[0].message.content


    print("")
    print("✨ Code copied to your keyboard! ✨")
    print("")

asyncio.run(main())
