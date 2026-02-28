# Corpus Briefing Skill

The human-facing skill that implements the three-phase workflow. Translates a Collection Record into a conversation with the information architect.

## When to Use This Skill

- After the Ingestion Skill produces a Collection Record
- When a human asks "what should we do with this corpus?"
- When presenting analysis options to stakeholders
- Before dispatching work to analytical skills

This skill is the **bridge between ingestion and action**. It ensures the human understands the landscape of options before committing to an approach.

---

## The Three-Phase Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    CORPUS BRIEFING SKILL                        │
└─────────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│    PHASE 1      │  │    PHASE 2      │  │    PHASE 3      │
│   Reference     │  │  Capabilities   │  │  Collaborative  │
│   Interview     │  │    Briefing     │  │     Triage      │
│                 │  │                 │  │                 │
│ 1-2 questions   │  │ What's possible │  │ Options with    │
│ Understand need │  │ given the data  │  │ tradeoffs       │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

## Phase 1: Reference Interview

### Purpose

Understand what the human is actually trying to accomplish. The first question asked is rarely the actual need.

### Practice

Ask **one or two** clarifying questions, then move forward. Don't be a gatekeeper.

### Key Question

> "What are you trying to accomplish with this corpus?"

Listen for purpose signals:

| Signal | Likely Purpose | Analytical Emphasis |
|--------|----------------|---------------------|
| "help people find things" | Navigation | Browse structures, categories |
| "moving to a new system" | Migration | Mapping, gap analysis |
| "audit" or "compliance" | Governance | Classification against standards |
| "search isn't working" | Search improvement | Vocabulary, synonyms, tagging |
| "understand what we have" | Content audit | Inventory, themes, gaps |
| "find patterns" | Research | Topic modeling, clustering |

### Optional Follow-up

If purpose is clear, skip. Otherwise:

> "Who will use the results of this work?"

### Output

A brief statement of:
- **Stated purpose** — what they said
- **Inferred need** — what problem they're solving
- **Audience** — who will use the output

### Example

```
User: "I want to organize our blog posts by topic."

Interview Output:
- Purpose: Topic-based organization for navigation
- Need: Readers can't find relevant content
- Audience: Website visitors browsing the blog
```

---

## Phase 2: Capabilities Briefing

### Purpose

Present what's possible **given this specific corpus**. Not a statistics dump — a landscape of options.

### Practice

Translate the Collection Record into plain language. Show the human what they're working with and what that enables.

### Structure

```markdown
## Your Corpus at a Glance

[Size and scope in human terms]

## What's Already Organized

[Prior organization detected — categories, metadata, structure]

## What Analysis Can Reveal

[Feasible methods and what each would produce]

## What Would Help

[Additional information or preprocessing that would unlock more options]
```

### Template

```markdown
## Your Corpus at a Glance

You have **{document_count} documents** totaling about **{total_tokens:,} words**.

{length_assessment}

{vocabulary_assessment}

## What's Already Organized

{prior_organization_summary}

## What Analysis Can Reveal

Given this corpus, here's what's feasible:

{feasibility_table}

## What Would Help

{enhancement_suggestions}
```

### Generating the Briefing

From the Collection Record:

**Length Assessment:**
```python
if std < mean * 0.5:
    "Documents are fairly uniform in length — good for consistent analysis."
elif std < mean:
    "Document lengths vary moderately. Standard methods will work."
else:
    "Document lengths vary widely (from {min} to {max} chars). Consider segmenting by type."
```

**Vocabulary Assessment:**
```python
if richness == "low":
    "The vocabulary is controlled and consistent — this corpus will cluster well."
elif richness == "moderate":
    "Vocabulary diversity is typical for focused domain content."
else:
    "High vocabulary diversity suggests broad or technical content. Watch for noise."
```

**Prior Organization Summary:**
```python
if has_categories and coverage > 0.9:
    "Your documents already have categories ({categories}). We can validate these against the content or discover substructure within them."
elif has_categories:
    "Partial categorization exists ({coverage:.0%} coverage). We can extend it or start fresh."
else:
    "No prior categories detected. Topic modeling or clustering will discover natural groupings."
```

**Feasibility Table:**
```markdown
| Approach | Feasibility | What You'd Get |
|----------|-------------|----------------|
| Topic Modeling | {feasible} | {n} themes with key terms for each |
| Clustering | {feasible} | Document groups by similarity |
| Taxonomy Extraction | {feasible} | Category structure with assignments |
| Concept Mapping | {feasible} | Network showing how ideas connect |
```

**Enhancement Suggestions:**
```python
suggestions = []
if not has_dates:
    suggestions.append("Adding publication dates would enable trend analysis.")
if not has_authors:
    suggestions.append("Adding author metadata would enable voice/style analysis.")
if stubs_detected > 0:
    suggestions.append(f"Review {stubs_detected} short documents for completeness.")
if vocabulary_richness == "high":
    suggestions.append("Consider a stopword list for your domain to reduce noise.")
```

### Example Briefing

```markdown
## Your Corpus at a Glance

You have **40 documents** totaling about **39,000 words**.

Document lengths vary moderately (400 to 18,000 characters). One long piece 
(Dan Klyn's sermon notes) may need separate handling to avoid dominating 
the analysis.

Vocabulary diversity is moderate — typical for focused domain content. 
About 4,600 unique terms with a healthy mix of IA terminology.

## What's Already Organized

Your documents already have categories: **ia-practice** (20) and **ia-theory** (20).

This is a clean 50/50 split based on URL structure. We can:
- Validate these categories against what the content actually says
- Discover subcategories within each
- Look for articles that bridge both categories

## What Analysis Can Reveal

| Approach | What You'd Get |
|----------|----------------|
| **Topic Modeling** | 6-10 themes with key terms. Reveals what each category is really about. |
| **Clustering** | Document groups by similarity. Shows which articles are related regardless of category. |
| **Concept Extraction** | Key terms and phrases. Foundation for tagging and cross-references. |
| **Concept Graph** | Visual map of how ideas connect. Good for "related articles" feature. |

## What Would Help

- **Audience metadata**: Adding who each article serves (Sara, Laura, Ben, Sue) 
  would enable persona-based navigation.
- **Publication dates**: Would enable trend analysis (what topics are you 
  writing more about lately?).
- **Stub review**: One article (politics-of-classification) is only 400 chars — 
  may be incomplete.
```

---

## Phase 3: Collaborative Triage

### Purpose

Help the human choose an approach. Present 2-3 options with honest tradeoffs. Don't decide unilaterally.

### Practice

Frame as **options with tradeoffs**, not recommendations. The human applies judgment; we provide clarity.

### Structure

```markdown
## Recommended Approaches

Given your goal of {purpose}, here are your options:

### Option A: {Name}
{Description}
- **Effort:** {Low/Medium/High}
- **Output:** {What they'd get}
- **Tradeoff:** {What they give up}

### Option B: {Name}
{Description}
- **Effort:** {Low/Medium/High}  
- **Output:** {What they'd get}
- **Tradeoff:** {What they give up}

### Option C: {Name} (if applicable)
{Description}

## My Suggestion

{Brief recommendation with rationale, acknowledging it's their call}
```

### Option Patterns

**For Navigation/Findability:**
- Option A: Topic-based categories (topic modeling → taxonomy)
- Option B: Faceted browse (extract multiple dimensions)
- Option C: Search optimization (vocabulary + tagging)

**For Content Audit:**
- Option A: Full inventory with gap analysis
- Option B: Sample-based themes overview
- Option C: Quality-focused review

**For Migration:**
- Option A: Map to target taxonomy
- Option B: Clean-slate reorganization
- Option C: Hybrid (map what fits, reorganize the rest)

**For Research:**
- Option A: Exploratory topic modeling
- Option B: Hypothesis-driven clustering
- Option C: Concept network analysis

### Example Triage

```markdown
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
get direct persona assignments rather than inferred ones. You can always add 
topic tags as a second pass.

But if you want to see what topics emerge naturally first, Option A is faster 
and might reveal surprises.

Your call — which sounds right?
```

---

## Output: The Briefing Package

After running through all three phases, produce:

```json
{
  "interview_summary": {
    "stated_purpose": "string",
    "inferred_need": "string", 
    "audience": "string"
  },
  "briefing_markdown": "string (the Phase 2 briefing)",
  "options": [
    {
      "name": "string",
      "description": "string",
      "effort": "low | medium | high",
      "output": "string",
      "tradeoff": "string",
      "skills_required": ["skill names"]
    }
  ],
  "suggested_option": "string (option name)",
  "suggestion_rationale": "string",
  "next_skill": "string (skill to invoke if they proceed)"
}
```

---

## Collaboration Protocols

### Input

- Collection Record from Ingestion Skill
- (Optional) Human context from conversation

### Output

- Briefing Package (JSON)
- Human-readable briefing (Markdown)

### Handoff

Once the human chooses an option, dispatch to the appropriate skill:

| Choice | Dispatch To |
|--------|-------------|
| Topic modeling | Topic Modeling Skill |
| Clustering | Clustering Skill |
| Taxonomy work | Taxonomy Builder Skill |
| Concept extraction | Vocabulary Skill |
| Graph visualization | Concept Graph Skill |
| LLM enrichment | Vocabulary Skill (enrichment mode) |

Pass along:
1. The Collection Record
2. The interview summary (purpose, audience)
3. Any constraints the human specified

---

## Anti-Patterns

1. **Statistics dump** — Don't lead with TTR and hapax counts. Translate to implications.
2. **Single recommendation** — Always present options. The human decides.
3. **Decision paralysis** — 2-3 options max. More creates overwhelm.
4. **Jargon** — "Topic coherence score" means nothing to most people. Say "how clear the themes are."
5. **Gatekeeping** — If they want to skip straight to analysis, let them. Offer guidance, don't block.

---

## References

- Reference Interview practice: `../ingestion/references/reference-interview.md`
- Corpus profiling interpretation: `../ingestion/references/corpus-profiling-guide.md`
- Planning doc: `../references/planning-doc.md`

---

## See Also

- `../ingestion/SKILL.md` — Produces the Collection Record this skill consumes
- `../topic_modeling/SKILL.md` — Common next step
- `../taxonomy/SKILL.md` — For category-focused work
