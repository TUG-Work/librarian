# Topic Modeling Methods: Detailed Comparison

## Overview

This reference covers the major approaches to semantic analysis of document collections, from classical information retrieval methods to modern neural approaches.

---

## 1. Latent Semantic Analysis (LSA/LSI)

**Origin:** Deerwester et al., 1990 — foundational information retrieval technique

**How it works:**
1. Build term-document matrix (TF-IDF weighted)
2. Apply Singular Value Decomposition (SVD)
3. Reduce to k dimensions (latent semantic space)
4. Documents and terms now live in same vector space

**Strengths:**
- Fast and deterministic
- Produces document vectors for similarity comparisons
- Well-understood mathematically
- Handles synonymy (different words, same meaning)

**Weaknesses:**
- Doesn't handle polysemy well (same word, different meanings)
- Topics aren't easily interpretable
- Assumes Gaussian distribution (not true for word counts)

**When to use:**
- Document similarity/retrieval
- Dimensionality reduction before clustering
- When you need reproducible results

**Python:**
```python
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(max_features=10000)
tfidf = vectorizer.fit_transform(documents)

svd = TruncatedSVD(n_components=100)
doc_vectors = svd.fit_transform(tfidf)
```

---

## 2. Latent Dirichlet Allocation (LDA)

**Origin:** Blei, Ng, Jordan, 2003 — the workhorse of topic modeling

**How it works:**
1. Assumes generative model: documents are mixtures of topics, topics are distributions over words
2. Uses Bayesian inference to discover latent topic structure
3. Each document gets a topic distribution; each topic gets a word distribution

**Strengths:**
- Highly interpretable topics
- Handles mixed-topic documents naturally
- Well-established evaluation metrics
- Fast with optimized implementations

**Weaknesses:**
- Bag-of-words assumption (ignores word order)
- Requires choosing number of topics in advance
- Can produce incoherent topics without good preprocessing
- Sensitive to hyperparameters

**When to use:**
- Exploratory analysis of unknown corpus
- When interpretability matters
- Medium-sized corpora (1K-100K documents)

**Python:**
```python
from gensim.models import LdaModel
from gensim import corpora

dictionary = corpora.Dictionary(tokenized_docs)
corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

lda = LdaModel(
    corpus,
    num_topics=20,
    id2word=dictionary,
    passes=15,
    alpha='auto'
)
```

---

## 3. Non-negative Matrix Factorization (NMF)

**Origin:** Lee & Seung, 1999 — parts-based representation

**How it works:**
1. Build term-document matrix (TF-IDF)
2. Factorize into two non-negative matrices: W (documents × topics) and H (topics × terms)
3. Non-negativity constraint produces additive, parts-based representation

**Strengths:**
- Topics are additive (easy to interpret)
- Faster than LDA for large vocabularies
- Produces sparser, more distinct topics
- Deterministic (unlike LDA)

**Weaknesses:**
- Doesn't model topic mixtures as elegantly as LDA
- Sensitive to initialization
- Less principled probabilistic interpretation

**When to use:**
- When you want distinct, non-overlapping topics
- For sparse representations
- When speed matters

**Python:**
```python
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(max_features=10000)
tfidf = vectorizer.fit_transform(documents)

nmf = NMF(n_components=20, random_state=42)
doc_topics = nmf.fit_transform(tfidf)
topic_terms = nmf.components_
```

---

## 4. BERTopic

**Origin:** Grootendorst, 2022 — neural topic modeling

**How it works:**
1. Embed documents using sentence-transformers (BERT-based)
2. Reduce dimensionality with UMAP
3. Cluster with HDBSCAN
4. Extract topic representations using c-TF-IDF

**Strengths:**
- Captures semantic meaning, not just word co-occurrence
- Handles short texts better than classical methods
- Produces coherent topics out-of-the-box
- Modular pipeline (can swap components)

**Weaknesses:**
- Slower than classical methods
- Requires more memory (transformer models)
- Black-box embedding step
- May need GPU for large corpora

**When to use:**
- When topic quality matters most
- Short documents (tweets, abstracts, titles)
- When you have computational resources

**Python:**
```python
from bertopic import BERTopic

topic_model = BERTopic(
    language="english",
    calculate_probabilities=True,
    verbose=True
)
topics, probs = topic_model.fit_transform(documents)

# Visualize
topic_model.visualize_topics()
topic_model.visualize_barchart()
```

---

## 5. KeyNMF (Seeded Topic Modeling)

**Origin:** Turftopic library, 2024 — contextual seeded modeling

**How it works:**
1. Embed documents and vocabulary with sentence-transformers
2. For each document, extract keywords by cosine similarity to document embedding
3. Build keyword matrix weighted by similarity
4. If seeded: weight documents by relevance to seed phrase
5. Apply NMF to (weighted) keyword matrix

**Strengths:**
- Can focus on specific research questions
- Interpretable like NMF
- Uses contextual embeddings
- Stable and reproducible

**Weaknesses:**
- Seed phrase quality affects results
- Still relatively new

**When to use:**
- When you know what you're looking for
- Hypothesis-driven research
- Domain-specific analysis

**Python:**
```python
from turftopic import KeyNMF

# Unseeded
model = KeyNMF(n_components=10)

# Seeded
model = KeyNMF(
    n_components=10,
    seed_phrase="monetary policy interest rates"
)

model.fit(documents)
model.print_topics()
```

---

## Comparison Matrix

| Aspect | LSA | LDA | NMF | BERTopic | KeyNMF |
|--------|-----|-----|-----|----------|--------|
| **Speed** | ★★★★★ | ★★★★ | ★★★★ | ★★ | ★★★ |
| **Interpretability** | ★★ | ★★★★ | ★★★★ | ★★★ | ★★★★ |
| **Short texts** | ★★ | ★★ | ★★ | ★★★★★ | ★★★★ |
| **Large corpora** | ★★★★★ | ★★★★ | ★★★★ | ★★ | ★★★ |
| **Semantic quality** | ★★★ | ★★★ | ★★★ | ★★★★★ | ★★★★ |
| **Reproducibility** | ★★★★★ | ★★★ | ★★★★ | ★★★ | ★★★★ |
| **Domain focus** | ★ | ★★ | ★★ | ★★ | ★★★★★ |

---

## Historical Context

These methods represent different eras of information science thinking:

1. **1990s — Vector Space Models:** LSA treats meaning as geometry. Documents and words are points in space; similarity is distance.

2. **2000s — Probabilistic Models:** LDA treats meaning as probability. Topics are latent variables that explain observed word patterns.

3. **2010s — Neural Embeddings:** Word2Vec, Doc2Vec showed that neural networks could learn semantic representations.

4. **2020s — Transformer Era:** BERT and successors capture context-dependent meaning. BERTopic bridges this to topic modeling.

5. **Current — Hybrid Approaches:** KeyNMF and similar methods combine neural embeddings with interpretable classical methods.

The field has not abandoned older methods—each serves different needs. A librarian chooses tools based on the question, not the fashion.
