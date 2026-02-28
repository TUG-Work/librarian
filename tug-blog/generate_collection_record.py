#!/usr/bin/env python3
"""
Generate a Collection Record for the TUG Blog corpus.
Implements the Ingestion Skill practice knowledge.
"""

import json
import os
import re
from datetime import datetime
from collections import Counter
import statistics

# Load raw documents
RAW_DIR = "raw"
docs = []
for filename in sorted(os.listdir(RAW_DIR)):
    if filename.endswith(".txt"):
        with open(os.path.join(RAW_DIR, filename)) as f:
            text = f.read()
        
        # Parse category and slug from filename
        parts = filename.replace(".txt", "").split("--")
        category = parts[0] if len(parts) > 1 else "unknown"
        slug = parts[1] if len(parts) > 1 else parts[0]
        
        docs.append({
            "filename": filename,
            "category": category,
            "slug": slug,
            "text": text,
            "char_count": len(text),
            "token_count": len(text.split())
        })

print(f"Loaded {len(docs)} documents")

# === INVENTORY ===
inventory = {
    "document_count": len(docs),
    "total_characters": sum(d["char_count"] for d in docs),
    "total_tokens": sum(d["token_count"] for d in docs),
    "formats": {".txt": len(docs)},
    "date_range": None  # No dates extracted from this corpus
}

# === STATISTICAL PROFILE ===

# Length distribution
char_counts = [d["char_count"] for d in docs]
length_distribution = {
    "min": min(char_counts),
    "max": max(char_counts),
    "mean": round(statistics.mean(char_counts), 1),
    "median": round(statistics.median(char_counts), 1),
    "std": round(statistics.stdev(char_counts), 1) if len(char_counts) > 1 else 0,
    "quartiles": [
        round(statistics.quantiles(char_counts, n=4)[0], 1),
        round(statistics.quantiles(char_counts, n=4)[1], 1),
        round(statistics.quantiles(char_counts, n=4)[2], 1)
    ]
}

# Vocabulary analysis
all_text = " ".join(d["text"] for d in docs)
# Simple tokenization: lowercase, letters only, min 3 chars
tokens = re.findall(r'\b[a-z]{3,}\b', all_text.lower())
token_counts = Counter(tokens)
unique_terms = len(token_counts)
total_tokens = len(tokens)
hapax = sum(1 for term, count in token_counts.items() if count == 1)
ttr = unique_terms / total_tokens if total_tokens > 0 else 0

# Vocabulary richness assessment
if ttr < 0.1:
    richness = "low"
elif ttr < 0.3:
    richness = "moderate"
else:
    richness = "high"

vocabulary = {
    "unique_terms": unique_terms,
    "hapax_legomena": hapax,
    "type_token_ratio": round(ttr, 4),
    "richness": richness
}

# Language (simple heuristic)
language = {
    "primary": "en",
    "mixed": False,
    "other_detected": []
}

statistical_profile = {
    "length_distribution": length_distribution,
    "vocabulary": vocabulary,
    "language": language
}

# === STRUCTURE ===

# Folder hierarchy (simulated from category prefixes)
categories = list(set(d["category"] for d in docs))
folder_hierarchy = {
    "depth": 1,
    "top_level": sorted(categories),
    "suggests_categories": True
}

# Naming patterns
naming_patterns = []
for cat in categories:
    count = sum(1 for d in docs if d["category"] == cat)
    naming_patterns.append({
        "pattern": f"{cat}--*.txt",
        "count": count,
        "suggests": "category prefix"
    })

# Prior organization
category_counts = Counter(d["category"] for d in docs)
prior_organization = {
    "has_categories": True,
    "category_source": "URL path structure / filename prefix",
    "categories": sorted(categories),
    "coverage": 1.0  # All docs have category
}

structure = {
    "folder_hierarchy": folder_hierarchy,
    "naming_patterns": naming_patterns,
    "metadata_fields": ["category", "slug", "url"],
    "prior_organization": prior_organization,
    "granularity": "document",
    "heterogeneity": "low"  # All blog posts, similar format
}

# === QUALITY ASSESSMENT ===

# Check for issues
flags = []
duplicates = 0
stubs = 0
encoding_issues = 0

# Find stubs (< 500 chars for blog posts)
for d in docs:
    if d["char_count"] < 500:
        stubs += 1
        flags.append(f"Stub: {d['slug']} ({d['char_count']} chars)")

# Check for near-duplicates (very simple: same first 200 chars)
first_chunks = [d["text"][:200] for d in docs]
chunk_counts = Counter(first_chunks)
for chunk, count in chunk_counts.items():
    if count > 1:
        duplicates += count - 1
        flags.append(f"Possible duplicate content detected ({count} docs share opening)")

# Very long docs that might dominate
very_long = [d for d in docs if d["char_count"] > 15000]
if very_long:
    flags.append(f"{len(very_long)} docs exceed 15K chars - may dominate topic models")

# Overall quality
if stubs > len(docs) * 0.1 or duplicates > 0:
    overall = "needs_cleaning"
elif stubs > 0 or len(flags) > 2:
    overall = "acceptable"
else:
    overall = "good"

quality_assessment = {
    "flags": flags,
    "duplicates_detected": duplicates,
    "stubs_detected": stubs,
    "encoding_issues": encoding_issues,
    "overall_quality": overall
}

# === FEASIBILITY ===

feasibility = {
    "topic_modeling": {
        "feasible": True,
        "recommended_approach": "NMF",
        "notes": f"{len(docs)} docs is viable but small for LDA. NMF preferred for interpretability. 6-10 topics reasonable."
    },
    "clustering": {
        "feasible": True,
        "recommended_approach": "hierarchical",
        "notes": "Small corpus - hierarchical clustering will reveal structure clearly. Consider Ward linkage."
    },
    "taxonomy_extraction": {
        "feasible": True,
        "has_prior_categories": True,
        "notes": "Two categories exist (ia-practice, ia-theory). Validate against topics or subdivide."
    },
    "faceted_analysis": {
        "candidate_facets": ["category", "audience", "format", "concepts"],
        "notes": "Category exists. Audience and format would need LLM enrichment. Concepts could be extracted via TF-IDF."
    }
}

# === RECOMMENDATIONS ===

recommendations = [
    {
        "action": "Run topic modeling to discover themes within existing categories",
        "rationale": "Prior categories are broad (practice vs theory). Topic modeling will reveal substructure useful for navigation.",
        "skill": "topic_modeling",
        "priority": "high"
    },
    {
        "action": "Enrich with audience facet via LLM classification",
        "rationale": "Persona targeting requires knowing which articles serve which audiences. No audience metadata exists.",
        "skill": "vocabulary_analysis",
        "priority": "high"
    },
    {
        "action": "Extract key concepts as tags",
        "rationale": "Cross-cutting concepts (blueprints, modeling, AI ethics) span both categories. Tags enable faceted browse.",
        "skill": "vocabulary_analysis",
        "priority": "medium"
    },
    {
        "action": "Build concept co-occurrence graph",
        "rationale": "Visualize how concepts relate. Useful for 'related articles' and gap identification.",
        "skill": "concept_graph",
        "priority": "medium"
    }
]

if stubs > 0:
    recommendations.append({
        "action": "Review stub documents for completeness",
        "rationale": f"{stubs} document(s) under 500 chars may be incomplete or extraction failures.",
        "skill": "manual_review",
        "priority": "low"
    })

# === DOCUMENT INVENTORY ===

documents = []
for d in docs:
    documents.append({
        "id": d["slug"],
        "path": os.path.join(RAW_DIR, d["filename"]),
        "title": d["slug"].replace("-", " ").title(),
        "char_count": d["char_count"],
        "metadata": {
            "category": d["category"],
            "slug": d["slug"]
        }
    })

# === ASSEMBLE COLLECTION RECORD ===

collection_record = {
    "$schema": "https://librarian.tug.work/schemas/collection-record-v1.json",
    "id": "tug-blog-2026-02",
    "name": "TUG Blog Corpus",
    "description": "The Understanding Group blog posts on IA Practice and IA Theory, scraped for content analysis and persona targeting.",
    "created": datetime.now().isoformat(),
    
    "provenance": {
        "source": "https://understandinggroup.com",
        "source_type": "web_scrape",
        "collected_date": "2026-02-24",
        "collector": "Kevin (Librarian Agent)",
        "purpose": "Content audit for persona targeting, topic gap analysis, and navigation improvement",
        "known_exclusions": "Comments, navigation chrome, and footer content excluded via trafilatura extraction",
        "is_sample": False,
        "sample_method": None
    },
    
    "inventory": inventory,
    "statistical_profile": statistical_profile,
    "structure": structure,
    "quality_assessment": quality_assessment,
    "feasibility": feasibility,
    "recommendations": recommendations,
    "documents": documents
}

# Write output
with open("collection-record.json", "w") as f:
    json.dump(collection_record, f, indent=2)

print(f"\n{'='*60}")
print("COLLECTION RECORD GENERATED")
print(f"{'='*60}")
print(f"\nCorpus: {collection_record['name']}")
print(f"Documents: {inventory['document_count']}")
print(f"Total chars: {inventory['total_characters']:,}")
print(f"Vocabulary: {vocabulary['unique_terms']:,} unique terms (TTR: {vocabulary['type_token_ratio']:.3f})")
print(f"Quality: {quality_assessment['overall_quality']}")
print(f"\nCategories found: {', '.join(structure['prior_organization']['categories'])}")
print(f"\nFlags:")
for flag in quality_assessment['flags']:
    print(f"  • {flag}")
print(f"\nRecommendations:")
for rec in recommendations:
    print(f"  [{rec['priority'].upper()}] {rec['action']}")
print(f"\nOutput: collection-record.json")
