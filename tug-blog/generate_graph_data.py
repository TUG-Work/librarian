#!/usr/bin/env python3
"""Generate graph data with similarity matrix for visualization."""

import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load existing dashboard data
with open("dashboard/data.json") as f:
    dashboard_data = json.load(f)

# Load all documents
docs = []
for article in dashboard_data["articles"]:
    filename = f"raw/{article['category']}--{article['slug']}.txt"
    with open(filename) as f:
        docs.append(f.read())

# Compute TF-IDF and similarity matrix
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
tfidf = vectorizer.fit_transform(docs)
sim_matrix = cosine_similarity(tfidf)

# Round similarity values for smaller JSON
sim_list = [[round(float(x), 3) for x in row] for row in sim_matrix]

# Build output
output = {
    "articles": dashboard_data["articles"],
    "similarity": sim_list
}

with open("dashboard/graph-data.json", "w") as f:
    json.dump(output, f)

print(f"Generated graph data for {len(docs)} articles")
print(f"Similarity matrix: {len(sim_list)}x{len(sim_list[0])}")

# Show some stats
import numpy as np
sim_array = np.array(sim_matrix)
np.fill_diagonal(sim_array, 0)  # Ignore self-similarity
print(f"Max similarity: {sim_array.max():.3f}")
print(f"Mean similarity: {sim_array.mean():.3f}")
print(f"Pairs above 0.3: {(sim_array > 0.3).sum() // 2}")
