#!/usr/bin/env python3
"""
Generate a Corpus Briefing for the TUG Blog corpus.
Implements the Briefing Skill three-phase workflow.
"""

import json
from datetime import datetime

# Load Collection Record
with open("collection-record.json") as f:
    cr = json.load(f)

# === PHASE 1: Reference Interview ===
# (In practice, this comes from conversation. Here we encode what we know.)

interview_summary = {
    "stated_purpose": "Improve blog findability and engagement through better organization",
    "inferred_need": "Readers can't find relevant content; content isn't targeted to specific personas",
    "audience": "Website visitors (prospects matching Sara/Laura/Ben/Sue personas)",
    "constraints": "Working with existing 40-article corpus; personas already defined"
}

# === PHASE 2: Capabilities Briefing ===

inv = cr["inventory"]
stats = cr["statistical_profile"]
struct = cr["structure"]
qual = cr["quality_assessment"]
feas = cr["feasibility"]

# Length assessment
length = stats["length_distribution"]
if length["std"] < length["mean"] * 0.5:
    length_assessment = "Documents are fairly uniform in length — good for consistent analysis."
elif length["std"] < length["mean"]:
    length_assessment = f"Document lengths vary moderately ({length['min']:,} to {length['max']:,} characters). Standard methods will work."
else:
    length_assessment = f"Document lengths vary widely ({length['min']:,} to {length['max']:,} characters). Consider segmenting by type."

# Vocabulary assessment
vocab = stats["vocabulary"]
richness = vocab["richness"]
if richness == "low":
    vocab_assessment = "The vocabulary is controlled and consistent — this corpus will cluster well."
elif richness == "moderate":
    vocab_assessment = f"Vocabulary diversity is moderate ({vocab['unique_terms']:,} unique terms). Typical for focused domain content."
else:
    vocab_assessment = "High vocabulary diversity suggests broad or technical content. Watch for noise."

# Prior organization
prior = struct["prior_organization"]
if prior["has_categories"] and prior["coverage"] > 0.9:
    cats = ", ".join(f"**{c}**" for c in prior["categories"])
    prior_summary = f"Your documents already have categories: {cats} ({len(prior['categories'])} categories, {prior['coverage']*100:.0f}% coverage)."
elif prior["has_categories"]:
    prior_summary = f"Partial categorization exists ({prior['coverage']*100:.0f}% coverage). We can extend it or start fresh."
else:
    prior_summary = "No prior categories detected. Topic modeling or clustering will discover natural groupings."

# Quality notes
quality_notes = []
for flag in qual["flags"]:
    quality_notes.append(f"- {flag}")

# Build the briefing markdown
briefing_md = f"""# Corpus Briefing: TUG Blog

## Your Corpus at a Glance

You have **{inv['document_count']} documents** totaling about **{inv['total_tokens']:,} words**.

{length_assessment}

{vocab_assessment}

## What's Already Organized

{prior_summary}

This is a clean 50/50 split based on URL structure. We can:
- Validate these categories against what the content actually says
- Discover subcategories within each  
- Look for articles that bridge both categories

## What Analysis Can Reveal

| Approach | Feasibility | What You'd Get |
|----------|-------------|----------------|
| **Topic Modeling** | {feas['topic_modeling']['recommended_approach']} | 6-10 themes with key terms. Reveals what each category is really about. |
| **Clustering** | {feas['clustering']['recommended_approach']} | Document groups by similarity. Shows which articles are related regardless of category. |
| **Taxonomy Validation** | ✅ | Confirm or refine existing categories based on content analysis. |
| **Concept Graph** | ✅ | Visual map of how ideas connect. Good for "related articles" feature. |

## Quality Notes

{chr(10).join(quality_notes) if quality_notes else "No significant issues detected."}

## What Would Help

- **Audience metadata**: Adding who each article serves (Sara, Laura, Ben, Sue) would enable persona-based navigation.
- **Publication dates**: Would enable trend analysis (what topics are you writing about lately?).
- **Content type tags**: Distinguishing thought-leadership vs. how-to vs. case-study would add a useful facet.
"""

# === PHASE 3: Collaborative Triage ===

options = [
    {
        "name": "Topic-First",
        "description": "Run topic modeling to discover themes, then map articles to personas based on which topics each persona cares about.",
        "effort": "medium",
        "output": "Topic tags for each article + inferred persona assignments",
        "tradeoff": "Personas inferred from topics, not directly assessed",
        "skills_required": ["topic_modeling", "vocabulary_analysis"]
    },
    {
        "name": "Persona-First",
        "description": "Use LLM judgment to classify each article by primary persona, then analyze topic distribution within each persona segment.",
        "effort": "medium", 
        "output": "Direct persona assignments + per-persona topic profile",
        "tradeoff": "More manual review needed, but more accurate personas",
        "skills_required": ["vocabulary_analysis", "topic_modeling"]
    },
    {
        "name": "Full Faceted",
        "description": "Build multiple facets simultaneously: topic, persona, content type, concepts. Cross-reference everything.",
        "effort": "high",
        "output": "Rich metadata enabling multiple browse paths",
        "tradeoff": "More upfront work, but most complete result",
        "skills_required": ["topic_modeling", "vocabulary_analysis", "taxonomy_builder", "concept_graph"]
    }
]

triage_md = """
## Recommended Approaches

Given your goal of improving blog findability and persona targeting:

### Option A: Topic-First
Run topic modeling to discover themes, then map articles to personas based on 
which topics each persona cares about.

- **Effort:** Medium (2-3 hours)
- **Output:** Topic tags for each article + persona assignments
- **Tradeoff:** Personas inferred from topics, not directly assessed

### Option B: Persona-First  
Use LLM judgment to classify each article by primary persona, then analyze 
topic distribution within each persona segment.

- **Effort:** Medium (2-3 hours)
- **Output:** Direct persona assignments + per-persona topic profile
- **Tradeoff:** More manual review needed, but more accurate personas

### Option C: Full Faceted
Build multiple facets simultaneously: topic, persona, content type, concepts.
Cross-reference everything.

- **Effort:** High (4-6 hours)
- **Output:** Rich metadata enabling multiple browse paths
- **Tradeoff:** More upfront work, but most complete result

## My Suggestion

For a 40-article blog, **Option B (Persona-First)** is probably the sweet spot. 
The corpus is small enough that LLM classification will be accurate, and you'll 
get direct persona assignments rather than inferred ones.

That said, you've already done initial persona assignments in the dashboard. 
The next high-value step would be **Option A (Topic-First)** to discover what 
themes exist within each persona segment — this reveals content gaps and 
cross-referencing opportunities.

If you want the full picture for a website redesign, **Option C** is worth the 
extra effort.

Your call — which sounds right?
"""

# Combine briefing
full_briefing = briefing_md + triage_md

# === OUTPUT: Briefing Package ===

briefing_package = {
    "collection_record_id": cr["id"],
    "generated": datetime.now().isoformat(),
    
    "interview_summary": interview_summary,
    
    "briefing_markdown": full_briefing,
    
    "options": options,
    
    "suggested_option": "Persona-First",
    "suggestion_rationale": "Corpus is small enough for accurate LLM classification. Direct persona assignments are more useful than inferred ones. Initial assignments already exist and can be validated.",
    
    "next_steps": {
        "if_topic_first": ["topic_modeling", "vocabulary_analysis"],
        "if_persona_first": ["vocabulary_analysis", "manual_review"],
        "if_full_faceted": ["topic_modeling", "vocabulary_analysis", "taxonomy_builder", "concept_graph"]
    }
}

# Write outputs
with open("briefing-package.json", "w") as f:
    json.dump(briefing_package, f, indent=2)

with open("briefing.md", "w") as f:
    f.write(full_briefing)

print("=" * 60)
print("CORPUS BRIEFING GENERATED")
print("=" * 60)
print(full_briefing)
print("\n" + "=" * 60)
print("Output files: briefing-package.json, briefing.md")
