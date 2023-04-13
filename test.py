import openai
import nltk
import os
nltk.download('punkt')

openai.api_key = os.environ['api_key']
model_engine = "davinci"
max_tokens = 1000

def generate_text(prompt):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()

def tokenize_text(text):
    tokens = nltk.word_tokenize(text)
    return tokens

with open('dedoose_data/clean_dedoose_data/001 ZY.txt', 'r') as f:
    text = f.read()
    chunks = [chunk.strip() for chunk in text.split("\n\n")]

    context = ""
    for i, chunk in enumerate(chunks):
        context += chunk + " "

        if (i + 1) % 5 == 0 or i == len(chunks) - 1:
            tokens = tokenize_text(context)
            prompt = " ".join(tokens[-500:])
            response = generate_text(prompt)
            context += response

   #print(context)
    
    answer_context = context
    prompt = "Question: What does justice mean to the interviewee?\nAnswer:"

    justice_response = openai.Completion.create(
        engine="davinci",
        prompt=f"{prompt} {answer_context}",
        temperature=0.7,
        max_tokens=100,
        n=1,
        stop=None,
    )

    print(justice_response)
