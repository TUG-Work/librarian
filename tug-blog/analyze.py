#!/usr/bin/env python3
"""Quick topic analysis of TUG blog corpus."""

import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

# Load documents
docs = []
filenames = []

for f in sorted(os.listdir("raw")):
    if f.endswith(".txt"):
        with open(f"raw/{f}") as file:
            docs.append(file.read())
            filenames.append(f)

print(f"Loaded {len(docs)} documents")

# TF-IDF vectorization
vectorizer = TfidfVectorizer(
    max_features=1000,
    stop_words='english',
    min_df=2,
    max_df=0.9
)
tfidf = vectorizer.fit_transform(docs)
feature_names = vectorizer.get_feature_names_out()

print(f"Vocabulary size: {len(feature_names)}")

# NMF topic modeling
n_topics = 8
nmf = NMF(n_components=n_topics, random_state=42, max_iter=500)
doc_topics = nmf.fit_transform(tfidf)
topic_terms = nmf.components_

# Display topics
print(f"\n{'='*60}")
print(f"TOP {n_topics} TOPICS IN TUG BLOG")
print(f"{'='*60}\n")

for idx, topic in enumerate(topic_terms):
    top_words = [feature_names[i] for i in topic.argsort()[:-11:-1]]
    print(f"Topic {idx+1}: {', '.join(top_words)}")

# Find representative docs for each topic
print(f"\n{'='*60}")
print("REPRESENTATIVE ARTICLES PER TOPIC")
print(f"{'='*60}\n")

for idx in range(n_topics):
    top_docs = doc_topics[:, idx].argsort()[-3:][::-1]
    print(f"Topic {idx+1}:")
    for doc_idx in top_docs:
        score = doc_topics[doc_idx, idx]
        name = filenames[doc_idx].replace('.txt', '').replace('--', ' / ')
        print(f"  {score:.2f} - {name}")
    print()

# Category breakdown
print(f"{'='*60}")
print("TOPIC DISTRIBUTION BY CATEGORY")
print(f"{'='*60}\n")

practice_topics = [0] * n_topics
theory_topics = [0] * n_topics

for i, fname in enumerate(filenames):
    dominant = doc_topics[i].argmax()
    if fname.startswith("ia-practice"):
        practice_topics[dominant] += 1
    else:
        theory_topics[dominant] += 1

print("          ", end="")
for t in range(n_topics):
    print(f"T{t+1:2d} ", end="")
print()
print(f"Practice: ", end="")
for c in practice_topics:
    print(f"{c:3d} ", end="")
print()
print(f"Theory:   ", end="")
for c in theory_topics:
    print(f"{c:3d} ", end="")
print()
