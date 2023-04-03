#!/usr/bin/env python3
import openai
import os

openai.api_key = os.environ['api_key']
messages = [
        {"role": "system", "content": "You are a helpful assistant."},
]
while True:
    message = input("Prompt: ")
    if message:
        messages.append(
                {"role": "user", "content": message},
        )
        chat_completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
        )
    answer = chat_completion.choices[0].message.content
    print(f"ChatGPT: {answer}")
    messages.append({"role": "assistant", "content": answer})