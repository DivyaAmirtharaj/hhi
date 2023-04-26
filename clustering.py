import os
import openai
from database import Database
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from nltk.stem.snowball import SnowballStemmer
import nltk
import string
import numpy as np
from demographics import Demographics

openai.api_key = os.environ['api_key']

class Clustering:
    def __init__(self) -> None:
        self.database = Database()
        self.demographics = Demographics()
        self.uuids = self.database.get_user('', True)
        self.demographic_details = self._demographic_scrape()

    def _data_scrape(self, qids):
        data = {}
        for user in self.uuids:
            try:
                responses = [self.database.get_responses(user, qid) for qid in qids]
                res = " ".join(responses)
            except Exception as e:
                pass
            if res:
                data[user] = res
        return data

    def _demographic_scrape(self):
        dem_users = {}
        for user in self.uuids:
            demographics = {
                "sex": self.demographics.get_data("sex", user),
                "age": self.demographics.get_data("age", user),
                "marital_status": self.demographics.get_data("marital_status", user),
                "widow": self.demographics.get_data("widow", user),
                "ethnicity": self.demographics.get_data("ethnicity", user),
                "religion": self.demographics.get_data("religion", user)
            }
            dem_users[user] = demographics
        #print(dem_users)
        return dem_users

    # Preprocess the text by removing stop words, punctuation, and special characters
    def _preprocess_text(self, text):
        stop_words = ["they", "their", "the", "a", "an", "them", "this", "that", "to", "be", "for", "and", "from", "my", "it", "is", "r", "i", "of", "me", "perspective", "respondent", "r", "we", "these", "respondents", "rs", "were", "was"]
        tokenized_responses = []
        for response in text:
            doc = response.translate(str.maketrans("", "", string.punctuation))
            tokens = doc.lower().split()
            stemmer = SnowballStemmer("english")
            lemma = nltk.wordnet.WordNetLemmatizer()
            tokens = [stemmer.stem(lemma.lemmatize(token)) for token in tokens if token not in stop_words]
            tokenized_responses.append(' '.join(tokens))
        return tokenized_responses
    
    def kmeans(self, data_dict, k, section):
        # create the TF-IDF vectorizer and transform the phrases
        #print(data)
        keys = list(data_dict.keys())
        data = list(data_dict.values())
        tfidf = TfidfVectorizer()
        vectorized_phrases = tfidf.fit_transform(data)

        # Compute the first two principal components of the TF-IDF matrix
        pca = TruncatedSVD(n_components=2)
        X_pca = pca.fit_transform(vectorized_phrases.toarray())

        # compute the cosine similarity matrix
        similarity_matrix = cosine_similarity(vectorized_phrases)
        # create k-means object with 3 clusters
        kmeans = KMeans(n_clusters=k, random_state=42, init='random', n_init='auto')

        # fit the k-means object to the similarity matrix
        clusters = kmeans.fit_predict(similarity_matrix)
        # assume 'labels' is a list/array containing the cluster labels for each data point
        unique_labels, label_counts = np.unique(clusters, return_counts=True)

        # print the number of elements in each cluster
        total_counts = sum(label_counts)
        for label, count in zip(unique_labels, label_counts):
            percent = round(count/total_counts * 100, 2)
            print(f"Cluster {label} accounted for {percent}% of the responses")
        #print(clusters)

        cluster_dict = {}
        cluster_demographics = {}
        for i, cluster in enumerate(clusters):
            user = keys[i]
            if cluster in cluster_dict and cluster in cluster_demographics:
                cluster_dict[cluster].append(data[i])
                cluster_demographics[cluster].append(self.demographic_details[user])
            else:
                cluster_dict[cluster] = [data[i]]
                cluster_demographics[cluster] = [self.demographic_details[user]]
        #print(cluster_demographics[0])

        for key in cluster_demographics:
            age_count = []
            married_count = []
            widow_count = []
            for i in range(len(cluster_demographics[key])):
                age = cluster_demographics[key][i]["age"]
                married = cluster_demographics[key][i]["marital_status"]
                widow = cluster_demographics[key][i]["widow"]
                if age != 'NULL' and age:
                    try:
                        age_num = int(age.split("-")[0])
                        age_count.append(age_num)
                    except:
                        pass
                if married == "True" or married == "False":
                    married_count.append(married)
                if widow == "True" or widow == "False":
                    widow_count.append(widow)
            avg_age = round(sum(age_count) / len(age_count), 2)
            percent_married = round(sum([1 for x in married_count if x=="True"]) / len(married_count) * 100, 2)
            percent_widow = round(sum([1 for x in widow_count if x=="True"]) / len(widow_count) * 100, 2)
            print(f"The responses in cluster {key} were on average {avg_age} years old, and {percent_married}% are/were married and {percent_widow}% are widowed")


        batched_matrix = {cluster: cluster_dict[cluster][:9] for cluster in cluster_dict}

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Explain in detail why the phrases were clustered the way they are, major themes found in each, and how each cluster is differentiated {batched_matrix}",
            temperature=0.7,
            max_tokens=950,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        similar = response.choices[0].text.strip()
        print(similar)

        # Plot the data points with different colors for each cluster
        plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters)
        plt.xlabel("PC1")
        plt.ylabel("PC2")
        plt.title("K-means clustering of phrases")
        #plt.show()
        plt.savefig(f"{section}.png")

if __name__ == '__main__':
    c = Clustering()
    '''justice_qids = [785919]
    justice_data = c._data_scrape(justice_qids)
    c.kmeans(justice_data, 3, 'justice)'''
    
    '''optimism_qids = [972241, 898570]
    optimism_data = c._data_scrape(optimism_qids)
    c.kmeans(optimism_data, 2, 'optimism')'''

    accountability_qids = [458111, 243034, 245609, 174244]
    accountability_data = c._data_scrape(accountability_qids)
    c.kmeans(accountability_data, 2, 'accountability')
