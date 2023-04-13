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

def main(usr_prompt):
        # Read text from file
        with open('dedoose_data/clean_dedoose_data/001 ZY.txt', 'r') as f:
                text = f.read()

       # Set up GPT request parameters
        model = 'text-davinci-002'  # or another model ID
        max_context_len = 4096      # maximum context length for the selected model
        batch_size = math.ceil(len(text) // (max_context_len - 1000))      # number of batches to split the text into
        batch_len = len(text) // batch_size + 1  # length of each batch

        # Split the input text into batches
        batches = [text[i:i+batch_len] for i in range(0, len(text), batch_len)]

        # Call the GPT API for each batch and accumulate the results
        generated_text = ''
        for i, batch in enumerate(batches):
                if i != len(batches) - 1:
                        prompt = f"Use this text chunk as context and wait for the next chunk to continue building context"
                        response = openai.Completion.create(
                                engine=model,
                                prompt=prompt,
                                max_tokens=1000,  # or another max token count
                                n=1,              # or another number of responses to generate
                                stop=None         # or another stopping sequence
                        )
                        generated_text += response.choices[0].text.strip()
                else:
                        prompt = f"Based on all the past context you just received and this text, answer this question {usr_prompt}:\n{batch}\n\nOutput:"
                        response = openai.Completion.create(
                                engine=model,
                                prompt=prompt,
                                max_tokens=1000,  # or another max token count
                                n=1,              # or another number of responses to generate
                                stop=None         # or another stopping sequence
                        )
                        print(response)

        # Print the generated text
        print(generated_text)

def chunk():
        # Load the interview transcript
        with open('dedoose_data/clean_dedoose_data/001 ZY.txt', 'r') as f:
                transcript = f.read()

        # Set up GPT request parameters
        chunk_size = 1000
        batch_size = math.ceil(len(transcript) // (chunk_size))      # number of batches to split the text into
        batch_len = len(transcript) // batch_size + 1  # length of each batch
        # Split the input text into batches
        chunks = [transcript[i:i+batch_len] for i in range(0, len(transcript), batch_len)]

        print("number of chunks", len(chunks))
        print("transcript len", len(transcript))

        # Initialize the OpenAI model
        model_engine = "davinci"  # or any other model you want to use
        model_prompt = "The following is an interview transcript.\n\nInterviewer: "

        # Loop through the chunks and build context for the model
        context = ""
        for i, chunk in enumerate(chunks):
                # Add the chunk to the context
                context += chunk
        
        # Generate text based on the context so far
        response = openai.Completion.create(
                engine=model_engine,
                prompt=model_prompt + context,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
        )
        
        # Extract the generated text from the API response
        generated_text = response.choices[0].text
        
        # Print the generated text (optional)
        print(generated_text)
        
        # Check if this is the last chunk
        if i == len(chunks) - 1:
                # If this is the last chunk, use the final context to ask questions
                question = "From the interviewee's perspective: what does justice mean to you?"
                response = openai.Completion.create(
                        engine=model_engine,
                        prompt=model_prompt + context + "\n\nQuestion: " + question,
                        max_tokens=1024,
                        n=1,
                        stop=None,
                        temperature=0.5,
                )
                
                # Extract the answer from the API response
                answer = response.choices[0].text
                
                # Print the answer (optional)
                print(answer)

def context_tokenize():
        # Load text file
        #nltk.download('stopwords')
        with open('dedoose_data/clean_dedoose_data/001 ZY.txt', 'r') as f:
                text = f.read()

        # Tokenize text
        tokens = word_tokenize(re.sub('[^a-zA-Z]+', ' ', text.lower()))

        # Remove stop words and punctuation marks
        stop_words = set(stopwords.words("english"))
        filtered_tokens = [word for word in tokens if word not in stop_words and word not in string.punctuation]
        print(filtered_tokens)

        # Extract most frequent keywords
        keyword_counts = Counter(filtered_tokens)
        keywords = [keyword for keyword, count in keyword_counts.most_common(10)]
        print(keywords)

        # Generate prompts
        prompts = ["Tell me about " + keyword for keyword in keywords]

        # Generate responses
        context = ""
        for prompt in prompts:
                response = openai.Completion.create(
                        engine="davinci",
                        prompt=prompt + "\n",
                        max_tokens=512,
                        n=1,
                        stop=None,
                        temperature=0.5,
                        frequency_penalty=0,
                        presence_penalty=0
                )
        context += response.choices[0].text
        print(context)

'''prompts = ['What does justice mean to you?', 'How much of a priority is it for you to have justice for what happened to you during the conflict with ISIS?', 'Who should be held accountable?', 'And how should they be held accountable?', 'What do the respondents say about their current priorities/concerns and what do they need the most to rebuild their lives? How this is connected to their response on justice and peace?']

for prompt in prompts:
        main(prompt)'''

context_tokenize()