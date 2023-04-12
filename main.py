#!/usr/bin/env python3
import openai
import os

openai.api_key = os.environ['api_key']

def user_prompt():
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

def batch_requests():
        # Read text from file
        with open('dedoose_data/e_justice/001 ZY.txt', 'r') as f:
                text = f.read()

       # Set up GPT request parameters
        model = 'text-davinci-002'  # or another model ID
        max_context_len = 4096      # maximum context length for the selected model
        batch_size = 3             # number of batches to split the text into
        batch_len = len(text) // batch_size + 1  # length of each batch

        # Split the input text into batches
        batches = [text[i:i+batch_len] for i in range(0, len(text), batch_len)]

        # Call the GPT API for each batch and accumulate the results
        generated_text = ''
        for batch in batches:
                prompt = f"Give me a summary of the following input:\n{batch}\n\nOutput:"
                response = openai.Completion.create(
                        engine=model,
                        prompt=prompt,
                        max_tokens=1000,  # or another max token count
                        n=1,              # or another number of responses to generate
                        stop=None         # or another stopping sequence
                )
                generated_text += response.choices[0].text.strip()

        # Print the generated text
        print(generated_text)