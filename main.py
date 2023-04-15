#!/usr/bin/env python3
import openai
import os
import nltk
import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import re
import string

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

def tokenize(file_name):
        nltk.download('punkt')
        with open(file_name, 'r') as f:
                text = f.read()
        tokens = nltk.word_tokenize(text)
        token_count = len(tokens)
        return(token_count)

def main(usr_prompt, dir):
        # Read text from file
        with open(dir, 'r') as f:
                text = f.read()
        generated_text = ''

       # Set up GPT request parameters
        model = 'text-davinci-002'  # or another model ID
        max_context_len = 4096      # maximum context length for the selected model
        batch_size = math.ceil(len(text) // (max_context_len - 1000))      # number of batches to split the text into
        try:
                batch_len = len(text) // batch_size + 1  # length of each batch
        except Exception as e:
                print(e)

        # Split the input text into batches
        try:
                batches = [text[i:i+batch_len] for i in range(0, len(text), batch_len)]

                # Call the GPT API for each batch and accumulate the results
                generated_text = ''
                for batch in batches:
                        prompt = f"Answer this question from the perspective of I: , {usr_prompt}:\n{batch}\n\nOutput:"
                        response = openai.Completion.create(
                                engine=model,
                                prompt=prompt,
                                max_tokens=1000,  # or another max token count
                                n=1,              # or another number of responses to generate
                                stop=None         # or another stopping sequence
                        )
                        generated_text += response.choices[0].text.strip()
        except Exception as e:
                print(e)
        return(generated_text)       

prompts = ['What does justice mean to you?', 'How much of a priority is it for you to have justice for what happened to you during the conflict with ISIS?', 'Who should be held accountable?', 'And how should they be held accountable?', 'What do the respondents say about their current priorities/concerns and what do they need the most to rebuild their lives? How this is connected to their response on justice and peace?']

for file_name in os.listdir('dedoose_data/e_justice'):
        results = ''
        for prompt in prompts:
                results += prompt+"\n\n"
                results += main(prompt, f'dedoose_data/e_justice/{file_name}')+"\n\n"
        outfile_name = os.path.join('results/', file_name)
        with open(outfile_name, 'w', encoding='utf-8') as f:
                f.write(results)
                print(outfile_name)
