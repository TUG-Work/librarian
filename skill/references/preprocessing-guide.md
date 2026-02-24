# Text Preprocessing Guide

Good preprocessing is often more important than model choice. Garbage in, garbage out.

## The Preprocessing Pipeline

```
Raw Text
    │
    ▼
┌─────────────────┐
│ 1. Extraction   │ ← Get text from HTML, PDF, etc.
└────────┬────────┘
         ▼
┌─────────────────┐
│ 2. Cleaning     │ ← Remove noise, normalize
└────────┬────────┘
         ▼
┌─────────────────┐
│ 3. Tokenization │ ← Split into words/sentences
└────────┬────────┘
         ▼
┌─────────────────┐
│ 4. Normalization│ ← Lowercase, lemmatize, stem
└────────┬────────┘
         ▼
┌─────────────────┐
│ 5. Filtering    │ ← Remove stopwords, rare terms
└────────┬────────┘
         ▼
Clean Tokens
```

## 1. Text Extraction

**trafilatura** — Best for web pages
```python
from trafilatura import fetch_url, extract

html = fetch_url('https://example.com/article')
text = extract(html, include_comments=False, include_tables=False)
```

**PyPDF2** — For PDFs (basic)
```python
from PyPDF2 import PdfReader

reader = PdfReader("document.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()
```

**pdfplumber** — For PDFs (better layout handling)
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    text = "\n".join(page.extract_text() for page in pdf.pages)
```

## 2. Cleaning

### Basic Cleaning
```python
import re

def clean_text(text):
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove special characters (keep letters, numbers, basic punctuation)
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    
    return text
```

### Common Noise Patterns

| Pattern | Regex | Notes |
|---------|-------|-------|
| URLs | `https?://\S+` | Web links |
| Emails | `\S+@\S+` | Email addresses |
| Twitter handles | `@\w+` | Social media |
| Hashtags | `#\w+` | Keep or remove depending on task |
| Numbers | `\d+` | Often noise in topic modeling |
| HTML entities | `&\w+;` | &amp;, &nbsp;, etc. |

## 3. Tokenization

### Word Tokenization

**NLTK** — Standard tokenizer
```python
from nltk.tokenize import word_tokenize
tokens = word_tokenize("This is a sentence.")
# ['This', 'is', 'a', 'sentence', '.']
```

**spaCy** — Better for complex text
```python
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp("This is a sentence.")
tokens = [token.text for token in doc]
```

### Sentence Tokenization

```python
from nltk.tokenize import sent_tokenize
sentences = sent_tokenize(text)
```

## 4. Normalization

### Lowercasing
```python
text = text.lower()
```

**When to skip:** Named Entity Recognition, sentiment analysis where CAPS = emphasis

### Lemmatization (preferred)

Reduces words to base form: "running" → "run", "better" → "good"

```python
# spaCy (best)
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp(text)
lemmas = [token.lemma_ for token in doc]

# NLTK
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
lemmas = [lemmatizer.lemmatize(word) for word in tokens]
```

### Stemming (faster, cruder)

Chops word endings: "running" → "run", "better" → "better" (no change)

```python
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
stems = [stemmer.stem(word) for word in tokens]
```

**Lemmatization vs Stemming:**
- Lemmatization: Slower, more accurate, needs POS tags
- Stemming: Faster, can create non-words, good for search

## 5. Filtering

### Stopword Removal

```python
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

# Add domain-specific stopwords
stop_words.update(['said', 'would', 'also', 'one', 'two'])

filtered = [w for w in tokens if w.lower() not in stop_words]
```

### Frequency Filtering

```python
from collections import Counter

word_counts = Counter(all_tokens)

# Remove very rare words (appear < 5 times)
min_freq = 5
# Remove very common words (appear in > 50% of docs)
max_doc_freq = 0.5

filtered = [w for w in tokens if word_counts[w] >= min_freq]
```

### Length Filtering

```python
# Remove very short tokens
filtered = [w for w in tokens if len(w) > 2]
```

## Complete Pipeline Example

```python
import re
import spacy
from nltk.corpus import stopwords

nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words('english'))

def preprocess(text):
    # Clean
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Tokenize and lemmatize with spaCy
    doc = nlp(text.lower())
    
    # Filter
    tokens = [
        token.lemma_ 
        for token in doc 
        if token.is_alpha 
        and len(token) > 2
        and token.lemma_ not in stop_words
    ]
    
    return tokens

# Process corpus
processed_docs = [preprocess(doc) for doc in raw_documents]
```

## Method-Specific Considerations

| Method | Preprocessing Notes |
|--------|---------------------|
| **LDA** | Heavy preprocessing helps. Remove stopwords, lemmatize, filter by frequency. |
| **LSA** | TF-IDF handles some normalization. Still remove stopwords. |
| **BERTopic** | Minimal preprocessing. Transformers handle context. Keep punctuation. |
| **KeyNMF** | Moderate preprocessing. Lemmatization helps, keep some structure. |

## Common Mistakes

1. **Over-preprocessing for neural methods** — BERTopic works better with natural text
2. **Under-preprocessing for LDA** — Junk in = junk topics out
3. **Removing domain terms** — Don't filter out rare but important technical terms
4. **Ignoring encoding issues** — Always decode to UTF-8 first
5. **Losing document boundaries** — Keep track of which tokens came from which document
