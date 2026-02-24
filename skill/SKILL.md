# Corpus Analysis Skill

A librarian's toolkit for semantic analysis of document collections. Combines traditional information science methods with modern NLP.

## When to Use This Skill

- Analyzing a collection of documents to discover themes/topics
- Clustering documents by semantic similarity
- Understanding the structure of a corpus
- Preparing collections for further analysis or organization

## Environment

```bash
source ~/.venv/librarian/bin/activate
```

All tools run in the `librarian` virtualenv.

## The Toolkit

### 1. Ingestion Tools

**trafilatura** — Web content extraction
```python
from trafilatura import fetch_url, extract
downloaded = fetch_url('https://example.com/article')
text = extract(downloaded)
```

**beautifulsoup4** — HTML parsing for complex sites

### 2. Topic Modeling Methods

Choose based on your needs:

| Method | Best For | Interpretability | Speed | When to Use |
|--------|----------|------------------|-------|-------------|
| **LDA** | General topic discovery | High | Fast | First pass, exploratory analysis |
| **LSA/LSI** | Dimensionality reduction, similarity | Medium | Fast | When you need document vectors |
| **NMF** | Sparse, interpretable topics | High | Fast | When topics should be distinct |
| **BERTopic** | Modern semantic clustering | Medium | Slower | Best quality, need GPU for large corpora |
| **KeyNMF** | Seeded/focused topics | High | Medium | When you know what you're looking for |

### 3. Decision Logic

```
START
│
├─ Do you know what topics you're looking for?
│   ├─ YES → KeyNMF (seeded topic modeling)
│   └─ NO → Continue
│
├─ How large is your corpus?
│   ├─ < 1000 docs → BERTopic (best quality)
│   ├─ 1000-10000 → LDA or NMF (fast, interpretable)
│   └─ > 10000 → LDA with sampling, or LSA
│
├─ Do you need document similarity/vectors?
│   ├─ YES → LSA or sentence-transformers
│   └─ NO → Continue
│
├─ Do topics need to be mutually exclusive?
│   ├─ YES → NMF
│   └─ NO → LDA (allows topic mixing)
│
└─ Default → Start with LDA, refine with BERTopic
```

## Quick Start Examples

### LDA with Gensim

```python
from gensim import corpora
from gensim.models import LdaModel
from gensim.parsing.preprocessing import preprocess_string

# Preprocess documents
docs = [preprocess_string(doc) for doc in raw_documents]

# Create dictionary and corpus
dictionary = corpora.Dictionary(docs)
corpus = [dictionary.doc2bow(doc) for doc in docs]

# Train LDA
lda = LdaModel(corpus, num_topics=10, id2word=dictionary, passes=15)

# View topics
for idx, topic in lda.print_topics(-1):
    print(f"Topic {idx}: {topic}")
```

### BERTopic

```python
from bertopic import BERTopic

# Simple usage
topic_model = BERTopic()
topics, probs = topic_model.fit_transform(documents)

# View topics
topic_model.get_topic_info()
```

### KeyNMF (Seeded)

```python
from turftopic import KeyNMF

# Seed with a focus phrase
model = KeyNMF(n_components=10, seed_phrase="economic policy inflation")
model.fit(documents)

# View topics
model.print_topics()
```

### Web Scraping with Trafilatura

```python
from trafilatura import fetch_url, extract
from trafilatura.settings import use_config

# Configure for thorough extraction
config = use_config()
config.set("DEFAULT", "EXTRACTION_TIMEOUT", "30")

# Fetch and extract
url = "https://example.com/article"
downloaded = fetch_url(url)
text = extract(downloaded, config=config)
```

## Corpus Management

Store corpora in `data/corpora/` with this structure:

```
data/corpora/
├── {corpus-name}/
│   ├── metadata.json      # Source info, date collected, settings
│   ├── raw/               # Original files
│   ├── processed/         # Cleaned text
│   └── analysis/          # Model outputs
```

### metadata.json Template

```json
{
  "name": "corpus-name",
  "description": "What this corpus contains",
  "sources": ["url1", "url2"],
  "collected": "2026-02-24",
  "document_count": 100,
  "preprocessing": {
    "lowercase": true,
    "remove_stopwords": true,
    "min_word_length": 3
  }
}
```

## References

- `references/methods-comparison.md` — Detailed comparison of methods
- `references/preprocessing-guide.md` — Text cleaning best practices
- `references/evaluation-metrics.md` — How to evaluate topic quality

## See Also

- `skills/organizing-systems/` — For organizing the outputs
- Towards Data Science article on hybrid approaches (January 2026)
