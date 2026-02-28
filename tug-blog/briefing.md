# Corpus Briefing: TUG Blog

## Your Corpus at a Glance

You have **40 documents** totaling about **38,928 words**.

Document lengths vary moderately (423 to 18,348 characters). Standard methods will work.

Vocabulary diversity is moderate (4,610 unique terms). Typical for focused domain content.

## What's Already Organized

Your documents already have categories: **ia-practice**, **ia-theory** (2 categories, 100% coverage).

This is a clean 50/50 split based on URL structure. We can:
- Validate these categories against what the content actually says
- Discover subcategories within each  
- Look for articles that bridge both categories

## What Analysis Can Reveal

| Approach | Feasibility | What You'd Get |
|----------|-------------|----------------|
| **Topic Modeling** | NMF | 6-10 themes with key terms. Reveals what each category is really about. |
| **Clustering** | hierarchical | Document groups by similarity. Shows which articles are related regardless of category. |
| **Taxonomy Validation** | ✅ | Confirm or refine existing categories based on content analysis. |
| **Concept Graph** | ✅ | Visual map of how ideas connect. Good for "related articles" feature. |

## Quality Notes

- Stub: politics-of-classification-resmini (423 chars)
- 1 docs exceed 15K chars - may dominate topic models

## What Would Help

- **Audience metadata**: Adding who each article serves (Sara, Laura, Ben, Sue) would enable persona-based navigation.
- **Publication dates**: Would enable trend analysis (what topics are you writing about lately?).
- **Content type tags**: Distinguishing thought-leadership vs. how-to vs. case-study would add a useful facet.

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
