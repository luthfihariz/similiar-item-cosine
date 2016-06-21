import pandas as pd
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import json

start = time.time()

ds = pd.read_csv('query_result.csv')

# Create a TF-IDF matrix of unigrams, bigrams, and trigrams for each product.

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0)
tfidf_matrix = tf.fit_transform(ds['item_description'])

# Compute similarity between all products using SciKit Leanr's linear_kernel (which in this case is equivalent to cosine similarity).
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

similiarities = []
ids = []

# Iterate through each item's similar items and store the 20 most-similar.
for idx, row in ds.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-20:-1]
    similar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices]

    similiarities.append(json.dumps(similar_items[1:],()))
    ids.append(ds['id'][idx])


# Similarities and their scores are stored in new csv.
d = {'id': ids,'similiar_items': similiarities}
dataFrame = pd.DataFrame(d)
dataFrame.to_csv('trained_data.csv', index=False)
