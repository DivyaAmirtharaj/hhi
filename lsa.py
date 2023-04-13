import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Create a list of all the file names in the directory
files = os.listdir('test/')

# Create a list of the full file paths
file_paths = ['test/' + f for f in files]

# Read in the text from each file
docs = []
for fp in file_paths:
    with open(fp, 'r') as f:
        doc = f.read()
        docs.append(doc)

# Create a TF-IDF vectorizer
vectorizer = TfidfVectorizer(stop_words='english', min_df=2, max_df=0.8)

# Vectorize the documents
X = vectorizer.fit_transform(docs)

# Create an LSA model and fit it to the vectorized documents
lsa_model = TruncatedSVD(n_components=10, algorithm='randomized', random_state=42)
lsa = lsa_model.fit_transform(X)

# Normalize the LSA vectors
lsa = Normalizer(copy=False).fit_transform(lsa)

# Print the top 10 words for each LSA component
terms = vectorizer.get_feature_names_out()
for i, comp in enumerate(lsa_model.components_):
    terms_comp = zip(terms, comp)
    sorted_terms = sorted(terms_comp, key=lambda x:x[1], reverse=True)[:10]
    print("Concept %d:" % i)
    for term in sorted_terms:
        print(term[0])
    print(" ")

# calculate pairwise cosine similarity between all documents
similarity_matrix = cosine_similarity(X)
np.fill_diagonal(similarity_matrix, 0)
print("\nPairwise document similarity (0 means not similar, 1 means identical):\n", similarity_matrix)

for i, doc in enumerate(docs):
    # Sort the similarity scores in descending order
    sorted_indices = np.argsort(similarity_matrix[i])[::-1]
    # Print the top 3 most similar documents
    print(f"Top 3 similar documents to '{i}':")
    for j in sorted_indices[1:4]:
        print(f"\t- {j} (similarity score: {similarity_matrix[i][j]})")