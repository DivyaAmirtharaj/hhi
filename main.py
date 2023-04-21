from database import Database
import os
import openai
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from nltk.stem import PorterStemmer
import string

openai.api_key = os.environ['api_key']

# LDA -> helps identify underlying topics that are present in a large corpus of text
# LSA -> identify which interview answers are most similar to each other
# Create analysis questions and answer them -> look at the questions for each section and try and create overarching analysis questions based on themes
    # string together the data from the responses to answer them
# Sentiment analysis across questions -> generally identify the questions that could be the most polarizing or triggering and measure sentiment of the responses?
# Answer the given questions in the prompt

# 1. Create a list of all the different sections
# 2. Loop through and create a list of questions for each section
# Side note, I should make some more of the normalized responses into bools for easier demographics details
# 3. Summarize the types of responses and then group responses by similarity

class Analysis:
    def __init__(self) -> None:
        logging.basicConfig(filename='example.log', level=logging.DEBUG)
        self.database = Database()
        self.question_ids = self.database.get_question_id('', True)
        self.uuids = self.database.get_user('', True)
        self.sections = self.database.get_sections()
        self.section_questions = {section: self.database.get_section_questions(section) for section in self.sections }

    def __get_response(self, qid):
        full_response = ''
        for user in self.uuids:
            res = self.database.get_responses(user, qid)
            if res:
                response += res
        return full_response

    def extract_keywords(self, qid):
        context = self.__get_response(qid)

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f'Extract keywords from this text: {context}',
            temperature=0.7,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        keywords = response.choices[0].text.strip()
        return keywords

    def create_analysis_questions(self, qid, themes):
        context = self.__get_response(qid)

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f'Based on these themes:{themes}, and this text {context}, create a list of questions that could be used for analysis',
            temperature=0.7,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        questions = response.choices[0].text.strip()
        return questions
    
    def answer_analysis_questions(self, analysis_questions):
        pass

    def theme_analysis(self, qid):
        context = self.__get_response(qid)

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f'Extract the main themes from this text and write thesis statements for each theme:{context}',
            temperature=0.7,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        themes = response.choices[0].text.strip()
        return themes
    
    def document_similarity(self, qid):
        docs = []
        for user in self.uuids:
            res = self.database.get_responses(user, qid)
            if res:
                docs.append(res)
        
        stop_words = ["yes", "no", "maybe", "the", "a", "an", "them", "this", "that", "to", "be", "for", "and", "from", "my", "it", "is", "r", "i", "of", "me", "perspective", "respondent", "r", "we", "these", "respondent's", "r's"]
        tokenized_responses = []
        for response in docs:
            doc = response.translate(str.maketrans("", "", string.punctuation))
            tokens = doc.lower().split()
            tokens = [token for token in tokens if token not in stop_words]
            stemmer = PorterStemmer()
            stemmed_tokens = [stemmer.stem(token) for token in tokens]
            tokenized_responses.append(' '.join(stemmed_tokens))
       
        question = "Who should be held accountable?"
        sample = tokenized_responses[:15]

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f'Group these responses to the question {question} by similarity and explain in detail why:{sample}',
            temperature=0.5,
            max_tokens=2049,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        similar = response.choices[0].text.strip()
        print(similar)
        #return similar
    
    def sentiment(self):
        # sentiment analysis of some kind
        pass

if __name__ == '__main__':
    a = Analysis()
    #keywords = a.extract_keywords()
    #themes = a.theme_analysis()
    #questions = a.create_analysis_questions(themes)
    #a.document_similarity()

    
