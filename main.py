from database import Database
import os
import openai
import logging

openai.api_key = os.environ['api_key']

# LDA -> helps identify underlying topics that are present in a large corpus of text
# LSA -> identify which interview answers are most similar to each other
# Create analysis questions and answer them -> look at the questions for each section and try and create overarching analysis questions based on themes
    # string together the data from the responses to answer them
# Sentiment analysis across questions -> generally identify the questions that could be the most polarizing or triggering and measure sentiment of the responses?
# Answer the given questions in the prompt

class Analysis:
    def __init__(self) -> None:
        self.database = Database()
        self.question_ids = self.database.get_question_id('', True)
        self.uuids = self.database.get_used('', True)
        logging.basicConfig(filename='example.log', level=logging.DEBUG)

    def extract_keywords(self):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f'Given that R: is the respondent, summarize this from the perspective of the respondent:\n\n',
            temperature=0.7,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        keywords = response.choices[0].text.strip()
        return keywords

if __name__ == '__main__':
    a = Analysis()
    a.test()
    
