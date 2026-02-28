# Ingestion Skill

The first skill invoked in any Librarian Agent workflow. Before analysis, classification, or organization can happen, the material must be received, examined, and characterized.

## When to Use This Skill

- A corpus arrives for analysis (documents, web pages, files, database exports)
- Starting any new Librarian engagement
- Before recommending analytical methods
- When asked "what do we have here?"

This skill is **logically prior** to all other Librarian skills. Nothing else runs until ingestion produces a Collection Record.

---

## Practice Knowledge

### What a Librarian Does at Ingestion

When a box of donated materials arrives at a library, or an archival collection comes in for processing, the librarian doesn't dump it on a shelf. There is a discipline to receiving material.

**1. Physical/Digital Inspection: "What do we have here?"**

- How many items? What formats?
- Are there folders, labels, naming conventions suggesting prior organization?
- Is there a manifest, finding aid, or README?
- Digital equivalent: document count, file types, folder structures, naming patterns, metadata fields present

**2. Provenance: "Where did this come from?"**

- Who created it? For what purpose?
- Was it curated or is it a raw dump?
- A carefully curated policy collection behaves differently under analysis than a web crawl, even at the same size

**3. Scope and Boundaries: "What's included and excluded?"**

- Is this everything, or a sample?
- What's obviously missing?
- Librarians processing archival collections are always attentive to what's *absent*, not just what's present

**4. Condition: "What state is it in?"**

- Is text clean or noisy?
- Duplicates? Mixed languages? Inconsistent formatting?
- This is the preprocessing reality check

**5. Resource Characterization: "What kind of resources, really?"**

Following Glushko: not just "500 documents" but what *kind* of resources. A 200-page report and a one-paragraph FAQ are both "documents" but are fundamentally different resources requiring different treatment.

- What's the granularity? (sentence, paragraph, page, document, collection)
- What are the natural boundaries?
- Are resources uniform or heterogeneous?

**6. Prior Organization: "What descriptions already exist?"**

- File names, folder structures, metadata fields, tags, categories
- These are prior organizing decisions — clues about intended use
- Raw material for downstream work

### The Reference Interview (Light Touch)

Before profiling, ask one or two clarifying questions:

- What are you trying to accomplish with this corpus?
- Is this for navigation? Migration? Governance? Compliance? Search improvement?

**Critical constraint:** Reference librarians can seem like gatekeepers. The agent should ask one or two clarifying questions at most, then move forward. Be helpful, not an intake form.

The first question asked is rarely the actual need. It's what the person thinks will get the answer they need. Get behind it to find the need driving the task, and the situation that created the need.

### Common Pitfalls

1. **Jumping to analysis** — Running LDA before understanding what you have
2. **Treating all documents as equal** — A 50-page whitepaper ≠ a 2-line description
3. **Ignoring prior organization** — Folder names and tags are information
4. **Missing provenance** — A web crawl needs different handling than a curated archive
5. **Overlooking absence** — What's *not* in the collection matters

---

## Tool Interface

### Environment

```bash
source ~/.venv/librarian/bin/activate
```

### Core Functions

```python
from librarian.corpus import (
    ingest_directory,
    ingest_urls,
    profile_corpus,
    detect_structure,
    generate_collection_record
)
```

### Ingestion from Directory

```python
# Load documents from a directory
corpus = ingest_directory(
    path="/path/to/documents",
    extensions=[".txt", ".md", ".html", ".pdf"],
    recursive=True,
    extract_metadata=True  # Parse folder names, filenames, front matter
)
```

### Ingestion from URLs

```python
# Scrape and extract from web sources
corpus = ingest_urls(
    urls=["https://example.com/page1", "https://example.com/page2"],
    follow_links=False,
    respect_robots=True,
    extract_metadata=True
)
```

### Corpus Profiling

```python
profile = profile_corpus(corpus)

# Returns:
{
    "document_count": 500,
    "total_chars": 2_450_000,
    "total_tokens": 380_000,
    
    "length_distribution": {
        "min": 145,
        "max": 89_000,
        "mean": 4_900,
        "median": 2_100,
        "std": 8_200,
        "quartiles": [800, 2100, 5400]
    },
    
    "vocabulary": {
        "unique_terms": 12_400,
        "hapax_legomena": 4_200,  # Terms appearing once
        "type_token_ratio": 0.033,
        "vocabulary_richness": "moderate"
    },
    
    "format_distribution": {
        ".txt": 320,
        ".md": 150,
        ".html": 30
    },
    
    "language_detection": {
        "primary": "en",
        "mixed": False
    },
    
    "quality_flags": [
        "12 documents appear to be duplicates",
        "8 documents have < 100 characters (stubs?)",
        "3 documents detected as non-English"
    ]
}
```

### Structure Detection

```python
structure = detect_structure(corpus)

# Returns:
{
    "folder_hierarchy": {
        "depth": 3,
        "top_level_folders": ["policies", "procedures", "archive"],
        "suggests_categories": True
    },
    
    "naming_patterns": [
        {"pattern": "YYYY-MM-DD_*.txt", "count": 230, "suggests": "date-based"},
        {"pattern": "*_v[0-9].txt", "count": 45, "suggests": "versioning"}
    ],
    
    "metadata_fields_found": ["title", "author", "date", "tags"],
    
    "prior_organization": {
        "has_categories": True,
        "category_source": "folder structure",
        "categories_found": ["policies", "procedures", "archive"],
        "coverage": 0.95  # 95% of docs have category assignment
    },
    
    "suggested_granularity": "document",  # vs "section" or "paragraph"
    
    "heterogeneity": "moderate"  # low/moderate/high
}
```

### Generate Collection Record

```python
record = generate_collection_record(
    corpus=corpus,
    profile=profile,
    structure=structure,
    provenance={
        "source": "Web scrape of company blog",
        "collected_date": "2026-02-24",
        "collector": "Kevin (Librarian Agent)",
        "purpose": "Content audit for IA redesign",
        "known_exclusions": "Comments and user-generated content excluded"
    }
)
```

---

## The Collection Record

The output of ingestion. All downstream skills reference this artifact.

### Schema

```json
{
  "$schema": "https://librarian.tug.work/schemas/collection-record-v1.json",
  "id": "uuid",
  "name": "string",
  "description": "string",
  "created": "ISO8601 datetime",
  
  "provenance": {
    "source": "string — where the material came from",
    "source_type": "web_scrape | file_system | database | api | manual_upload",
    "collected_date": "ISO8601 date",
    "collector": "string — who/what collected it",
    "purpose": "string — why it was collected",
    "known_exclusions": "string — what was intentionally left out",
    "is_sample": "boolean",
    "sample_method": "string — if sampled, how"
  },
  
  "inventory": {
    "document_count": "integer",
    "total_characters": "integer",
    "total_tokens": "integer (estimated)",
    "formats": {"extension": "count"},
    "date_range": {"earliest": "date", "latest": "date"} 
  },
  
  "statistical_profile": {
    "length_distribution": {
      "min": "integer",
      "max": "integer", 
      "mean": "float",
      "median": "float",
      "std": "float",
      "quartiles": ["Q1", "Q2", "Q3"]
    },
    "vocabulary": {
      "unique_terms": "integer",
      "hapax_legomena": "integer",
      "type_token_ratio": "float",
      "richness": "low | moderate | high"
    },
    "language": {
      "primary": "ISO 639-1 code",
      "mixed": "boolean",
      "other_detected": ["codes"]
    }
  },
  
  "structure": {
    "folder_hierarchy": {
      "depth": "integer",
      "top_level": ["folder names"],
      "suggests_categories": "boolean"
    },
    "naming_patterns": [
      {"pattern": "regex", "count": "integer", "suggests": "string"}
    ],
    "metadata_fields": ["field names found"],
    "prior_organization": {
      "has_categories": "boolean",
      "category_source": "string",
      "categories": ["category names"],
      "coverage": "float 0-1"
    },
    "granularity": "document | section | paragraph",
    "heterogeneity": "low | moderate | high"
  },
  
  "quality_assessment": {
    "flags": ["string — issues detected"],
    "duplicates_detected": "integer",
    "stubs_detected": "integer (docs < 100 chars)",
    "encoding_issues": "integer",
    "overall_quality": "good | acceptable | needs_cleaning"
  },
  
  "feasibility": {
    "topic_modeling": {
      "feasible": "boolean",
      "recommended_approach": "LDA | NMF | BERTopic",
      "notes": "string"
    },
    "clustering": {
      "feasible": "boolean", 
      "recommended_approach": "kmeans | hierarchical | dbscan",
      "notes": "string"
    },
    "taxonomy_extraction": {
      "feasible": "boolean",
      "has_prior_categories": "boolean",
      "notes": "string"
    },
    "faceted_analysis": {
      "candidate_facets": ["field names or detected dimensions"],
      "notes": "string"
    }
  },
  
  "recommendations": [
    {
      "action": "string — what to do",
      "rationale": "string — why",
      "skill": "string — which skill handles this",
      "priority": "high | medium | low"
    }
  ],
  
  "documents": [
    {
      "id": "string",
      "path": "string",
      "title": "string",
      "char_count": "integer",
      "metadata": {}
    }
  ]
}
```

### Example Collection Record

```json
{
  "id": "tug-blog-2026-02",
  "name": "TUG Blog Corpus",
  "description": "The Understanding Group blog posts on IA Practice and IA Theory",
  "created": "2026-02-24T10:25:08Z",
  
  "provenance": {
    "source": "https://understandinggroup.com",
    "source_type": "web_scrape",
    "collected_date": "2026-02-24",
    "collector": "Kevin (Librarian Agent)",
    "purpose": "Content audit for persona targeting and topic gap analysis",
    "known_exclusions": "Comments, navigation, footer content excluded via trafilatura extraction",
    "is_sample": false
  },
  
  "inventory": {
    "document_count": 40,
    "total_characters": 238782,
    "total_tokens": 42000,
    "formats": {".txt": 40},
    "date_range": null
  },
  
  "statistical_profile": {
    "length_distribution": {
      "min": 423,
      "max": 18610,
      "mean": 5969,
      "median": 4861,
      "std": 4200,
      "quartiles": [3200, 4861, 7100]
    },
    "vocabulary": {
      "unique_terms": 4200,
      "hapax_legomena": 1800,
      "type_token_ratio": 0.10,
      "richness": "moderate"
    },
    "language": {
      "primary": "en",
      "mixed": false
    }
  },
  
  "structure": {
    "folder_hierarchy": {
      "depth": 1,
      "top_level": ["ia-practice", "ia-theory"],
      "suggests_categories": true
    },
    "naming_patterns": [
      {"pattern": "ia-practice--*.txt", "count": 20, "suggests": "category prefix"},
      {"pattern": "ia-theory--*.txt", "count": 20, "suggests": "category prefix"}
    ],
    "metadata_fields": ["url", "category", "slug"],
    "prior_organization": {
      "has_categories": true,
      "category_source": "URL path structure",
      "categories": ["ia-practice", "ia-theory"],
      "coverage": 1.0
    },
    "granularity": "document",
    "heterogeneity": "low"
  },
  
  "quality_assessment": {
    "flags": [
      "1 document has < 500 chars (politics-of-classification-resmini)"
    ],
    "duplicates_detected": 0,
    "stubs_detected": 1,
    "encoding_issues": 0,
    "overall_quality": "good"
  },
  
  "feasibility": {
    "topic_modeling": {
      "feasible": true,
      "recommended_approach": "NMF",
      "notes": "40 docs is small for LDA; NMF preferred. 8-10 topics reasonable."
    },
    "clustering": {
      "feasible": true,
      "recommended_approach": "hierarchical",
      "notes": "Small corpus, hierarchical clustering will show structure clearly"
    },
    "taxonomy_extraction": {
      "feasible": true,
      "has_prior_categories": true,
      "notes": "Two categories exist; may want to validate or subdivide"
    },
    "faceted_analysis": {
      "candidate_facets": ["category", "audience", "content_type"],
      "notes": "Category exists; audience and content_type would need enrichment"
    }
  },
  
  "recommendations": [
    {
      "action": "Run topic modeling to discover themes within categories",
      "rationale": "Prior categories exist but are broad; topics will reveal substructure",
      "skill": "topic_modeling",
      "priority": "high"
    },
    {
      "action": "Enrich with audience facet via LLM classification",
      "rationale": "No audience metadata exists; needed for persona targeting",
      "skill": "vocabulary_analysis",
      "priority": "high"
    },
    {
      "action": "Flag stub document for review",
      "rationale": "politics-of-classification-resmini is only 423 chars; may be incomplete",
      "skill": "manual_review",
      "priority": "low"
    }
  ]
}
```

---

## Collaboration Protocols

### Handoffs to Other Skills

After producing a Collection Record, route work based on findings:

| Finding | Route To | Pass Along |
|---------|----------|------------|
| Prior categories found in metadata | **Taxonomy Builder** | Categories + coverage stats for validation |
| No prior categories | **Topic Modeler** + **Clustering** | Profile for unsupervised discovery |
| High vocabulary diversity | **Concept Graph** | Vocabulary stats for landscape mapping |
| Sparse metadata | **Vocabulary Analyzer** | Candidates for enrichment |
| Very small corpus (< 50 docs) | **Clustering** preferred | Caution flag for LDA |
| Very large corpus (> 10K docs) | Recommend sampling | Sampling strategy |
| Facet candidates identified | **Taxonomy Builder** | Candidate facet list |

### What to Pass Downstream

Always pass:
1. The Collection Record (full JSON)
2. Path to document files
3. Any human input from the reference interview

### Receiving Input

The Ingestion Skill accepts:
- A path to a directory of files
- A list of URLs to scrape
- A database connection string
- A manifest file listing resources
- Raw text/documents passed directly

---

## References

- Glushko, R.J. (ed.). *The Discipline of Organizing*, 4th Professional Edition. Chapter 5: "Resource Description and Metadata." https://berkeley.pressbooks.pub/tdo4p/
- Beecher, F. (2009). "Content Analysis Heuristics." *Boxes and Arrows*. https://boxesandarrows.com/content-analysis-heuristics/
- Lu, X. (2014). *Computational Methods for Corpus Annotation and Analysis*. Springer.
- Society of American Archivists. "Arrangement and Description" guidelines.

---

## See Also

- `skills/librarian/topic_modeling/SKILL.md` — Downstream skill for topic discovery
- `skills/librarian/clustering/SKILL.md` — Downstream skill for document grouping
- `skills/librarian/taxonomy/SKILL.md` — Downstream skill for classification structures
- `skills/corpus-analysis/SKILL.md` — Quick reference for method selection
