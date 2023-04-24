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
from sklearn.cluster import KMeans
import ast

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
        
        stop_words = ["respondents", "yes", "no", "maybe", "the", "a", "an", "them", "this", "that", "to", "be", "for", "and", "from", "my", "it", "is", "r", "i", "of", "me", "perspective", "respondent", "r", "we", "these", "respondent's", "r's"]
        tokenized_responses = []
        for response in docs:
            doc = response.translate(str.maketrans("", "", string.punctuation))
            tokens = doc.lower().split()
            tokens = [token for token in tokens if token not in stop_words]
            #stemmer = PorterStemmer()
            #stemmed_tokens = [stemmer.stem(token) for token in tokens]
            tokenized_responses.append(' '.join(tokens))
       
        question = "Who should be held accountable?"
        sample = tokenized_responses[:15]
        print(sample)

        '''response = openai.Completion.create(
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
        #return similar'''
    
    def sentiment(self):
        # sentiment analysis of some kind
        pass
    
    def similarity(self, qid):
        docs = []
        for user in self.uuids:
            #res1 = self.database.get_responses(user, 785919)
            #res2 = self.database.get_responses(user, 458111)
            res1 = self.database.get_responses(user, 785919)
            #res2 = self.database.get_responses(user, 972241)
            #res3 = self.database.get_responses(user, 898570)
            if res1:
                docs.append(res1)
        
        stop_words = ["they", "their", "yes", "no", "maybe", "the", "a", "an", "them", "this", "that", "to", "be", "for", "and", "from", "my", "it", "is", "r", "i", "of", "me", "perspective", "respondent", "r", "we", "these", "respondents", "rs", "were", "was"]
        tokenized_responses = []
        for response in docs:
            doc = response.translate(str.maketrans("", "", string.punctuation))
            tokens = doc.lower().split()
            tokens = [token for token in tokens if token not in stop_words]
            tokenized_responses.append(' '.join(tokens))
        
        # create the TF-IDF vectorizer and transform the phrases
        tfidf = TfidfVectorizer()
        vectorized_phrases = tfidf.fit_transform(tokenized_responses)

        # compute the cosine similarity matrix
        similarity_matrix = cosine_similarity(vectorized_phrases)
        # create k-means object with 3 clusters
        kmeans = KMeans(n_clusters=3, random_state=42)

        # fit the k-means object to the similarity matrix
        clusters = kmeans.fit_predict(similarity_matrix)
        
        # print the cluster labels
        '''for i, cluster in enumerate(clusters):
            print(f"Phrase {i+1} is in cluster {cluster+1}")'''
        
        print(clusters)
        cluster_dict = {}
        for i, cluster in enumerate(clusters):
            if cluster in cluster_dict:
                cluster_dict[cluster].append(tokenized_responses[i])
            else:
                cluster_dict[cluster] = [tokenized_responses[i]]
        #print(cluster_dict)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Explain in detail why the phrases were clustered the way they are, major themes found in each, and how each cluster is differentiated {cluster_dict}",
            temperature=0.7,
            max_tokens=1024,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        similar = response.choices[0].text.strip()
        print(similar)
        #return similar

    def demographic_details(self):
        demo_q = [768766, 818556, 127515, 737666, 866648, 180654, 511429, 158078, 363930, 868157, 388462, 396790, 946197, 4539, 155061, 147984, 725234, 225300, 812253, 431358, 920510]
        docs = []
        for user in self.uuids[:5]:
            res = ''
            for q in demo_q:
                det = self.database.get_responses(user, q)
                if det:
                    res += det
            if res:
                response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f'Using {res}, summarize the demographic details in the format "Age:, Marital Status:, Spouse Status:, Children:, Profession:, Literacy:, Religion:, Ethnicity:" using bools, short answers, or None such that is parseable as a dict by json loads',
                temperature=0.1,
                max_tokens=2049,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
                )
                dem_details = response.choices[0].text.strip()
            docs.append(dem_details)
        print(docs)


if __name__ == '__main__':
    a = Analysis()
    #keywords = a.extract_keywords()
    #themes = a.theme_analysis()
    #questions = a.create_analysis_questions(themes)
    #a.document_similarity(785919)
    a.similarity(785919)
    #a.demographic_details()

    
