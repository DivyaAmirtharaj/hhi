import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import Pipeline

# Set up the pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('lsa', TruncatedSVD(n_components=10)),
])

# Set up a list to store the text of each file
docs = []

# Loop through the files in the directory
directory = 'test/'
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        with open(os.path.join(directory, filename), 'r') as file:
            docs.append(file.read())

# Fit the pipeline on the text
pipeline.fit(docs)

# Get the document vectors
doc_vectors = pipeline.cosine_similaritytransform(docs)

# Perform LSA
lsa = TruncatedSVD(n_components=2)
doc_topics = lsa.fit_transform(doc_vectors)

# Create a dataframe to display the results
topics = pd.DataFrame(doc_topics, index=doc_df.index, columns=["topic_1", "topic_2"])

print(topics)