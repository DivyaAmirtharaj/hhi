from database import Database
import os
import openai
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

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
        self.uuids = self.database.get_user('', True)
        logging.basicConfig(filename='example.log', level=logging.DEBUG)

    def extract_keywords(self):
        answer = ''
        for user in self.uuids:
            res = self.database.get_responses(user, 458111)
            if res:
                answer += res

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f'Extract keywords from this text:{answer}',
            temperature=0.7,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        keywords = response.choices[0].text.strip()
        print(keywords)
        return keywords

    def create_analysis_questions(self, themes):
        answer = ''
        for user in self.uuids:
            res = self.database.get_responses(user, 458111)
            if res:
                answer += res

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f'Based on these themes:{themes}, and this text {answer}, create a list of questions that could be used for analysis',
            temperature=0.7,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        questions = response.choices[0].text.strip()
        print(questions)
        return questions
    
    def answer_analysis_questions(self, questions):
        pass

    def theme_analysis(self):
        answer = ''
        for user in self.uuids:
            res = self.database.get_responses(user, 458111)
            if res:
                answer += res

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f'Extract the main themes from this text and write thesis statements for each theme:{answer}',
            temperature=0.7,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        themes = response.choices[0].text.strip()
        return themes
    
    def document_similarity(self):
        docs = []
        for user in self.uuids:
            res = self.database.get_responses(user, 458111)
            if res:
                docs.append(res)

        # Create a TF-IDF matrix
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(docs)

        # Apply SVD to reduce the dimensionality of the matrix
        svd = TruncatedSVD(n_components=2, random_state=42)
        lsa_matrix = svd.fit_transform(tfidf_matrix)

        # Calculate cosine similarity between documents
        similarity_matrix = cosine_similarity(lsa_matrix)

        # Print the similarity matrix
        print(similarity_matrix)
        # Get the index of the maximum similarity score for each document
        most_similar = np.argmax(similarity_matrix - np.eye(similarity_matrix.shape[0]), axis=1)

        # Print the most similar documents
        for i, idx in enumerate(most_similar):
            print(f"Document {i+1} is most similar to Document {idx+1}")

    def sentiment(self):
        # sentiment analysis of some kind
        pass

if __name__ == '__main__':
    a = Analysis()
    #keywords = a.extract_keywords()
    #themes = a.theme_analysis()
    #questions = a.create_analysis_questions(themes)
    a.document_similarity()

    
