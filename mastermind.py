#!/usr/bin/env python3

from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import asyncio

# pull this from my .env file
# Load the .env file
load_dotenv()

client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPENAI_API_KEY"),
)

fileName = input("Enter the file: ")
prompt = input("Enter your prompt: ")



async def main() -> None:

    # Read the React Native file into a string
    with open(fileName, 'r') as file:
        file_content = file.read()

    # Define the modification you want to make
    modification_prompt = f"{file_content}\n\n# Now, modify the above code to {prompt}.\n\n Include the whole file. ONLY include code in your response."

    print("")
    print("Working on that...")

    chat_completion = await client.chat.completions.create(
        messages=[
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
