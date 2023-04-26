from database import Database
import os
import openai
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
from sklearn.cluster import KMeans
from nltk.stem.snowball import SnowballStemmer
import nltk

openai.api_key = os.environ['api_key']

class Themes:
    def __init__(self, qids):
        logging.basicConfig(filename='example.log', level=logging.DEBUG)
        self.database = Database()
        self.question_ids = self.database.get_question_id('', True)
        self.uuids = self.database.get_user('', True)
        self.sections = self.database.get_sections()
        self.qids = qids
        self.keywords = ''

    def _date_scrape(self):
        data = []
        for user in self.uuids:
            try:
                responses = [self.database.get_responses(user, qid) for qid in self.qids]
                res = " ".join(responses)
            except Exception as e:
                pass
            if res:
                data.append(res)
        return data

    def extract_keywords(self, ):
        context = self._date_scrape()[:10]
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
        print(keywords)
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

if __name__ == '__main__':
    a = Themes([785919, 245609, 174244])
    keywords = a.extract_keywords()
    #themes = a.theme_analysis()
    #questions = a.create_analysis_questions(themes)

    '''
    Get the clusters and the phrases associated to each, then run a demographic analysis and display the demographics associated with each
    Run that code above for justice, accountability

    Get major themes for each section, as well as keywords

    Using the clusters above, we are displaying major thesis statements already

    Mathematical display of trauma?  Yes/ no for health concerns and display them in graphs

    Answer the five questions posed
    '''

    
