# Librarian Agent Skills

A collection of skills for corpus analysis, combining formal information science methods with LLM judgment.

## Architecture

The Librarian Agent orchestrates multiple skills, each encoding the practice knowledge of a trained information professional.

```
┌─────────────────────────────────────────────────────────────────┐
│                     LIBRARIAN AGENT                             │
│  Orchestrates skills, manages deliberation, interfaces with IA  │
└─────────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   INGESTION     │  │  TOPIC MODELING │  │   CLUSTERING    │
│                 │  │                 │  │                 │
│ Receive,examine │  │ Discover themes │  │ Group documents │
│ characterize    │  │ LDA/NMF/BERT    │  │ k-means/hier.   │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  VOCABULARY     │  │    TAXONOMY     │  │  CONCEPT GRAPH  │
│                 │  │                 │  │                 │
│ Terms, TF-IDF   │  │ Facets, SKOS    │  │ Co-occurrence   │
│ Controlled vocab│  │ Classification  │  │ Centrality      │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

## Core Thesis

LLMs are good at intuiting semantic relationships but do so as a black box. Information science has decades of rigorous, reproducible, auditable methods for the same tasks.

**Combining LLM judgment with formal IS tools produces something better than either alone: auditable intermediate representations at each analytical stage.**

## Skills

### Available Now

| Skill | Purpose | Status |
|-------|---------|--------|
| [Ingestion](./ingestion/SKILL.md) | Receive, examine, characterize a corpus | ✅ Ready |

### Planned

| Skill | Purpose | Status |
|-------|---------|--------|
| Topic Modeling | Discover themes via LDA/NMF/BERTopic | 🔜 Next |
| Clustering | Group documents by similarity | Planned |
| Vocabulary Analysis | Term extraction, controlled vocab | Planned |
| Taxonomy Builder | Faceted classification, SKOS export | Planned |
| Concept Graph | Co-occurrence networks, centrality | Planned |

## Workflow

### Phase 1: Ingestion

Every engagement starts with the Ingestion Skill producing a **Collection Record** — a structured description of what's in the corpus and what's possible.

### Phase 2: Reference Interview (Light Touch)

One or two clarifying questions to understand purpose:
- What are you trying to accomplish?
- Who will use the results?

### Phase 3: Capabilities Briefing

Present what's possible given the corpus:
- Here's your corpus and its characteristics
- Here are the analyses that are feasible
- Here's what would help unlock more options

### Phase 4: Collaborative Triage

Help the human IA choose an approach:
- Two or three options with tradeoffs
- What each takes (time, resources, manual input)
- Which skills to engage

## Shared Artifacts

Skills communicate through shared artifacts with defined schemas:

| Artifact | Producer | Consumers |
|----------|----------|-----------|
| Collection Record | Ingestion | All downstream skills |
| Topic Model Result | Topic Modeling | Taxonomy, Graph |
| Cluster Assignment | Clustering | Taxonomy |
| Vocabulary List | Vocabulary | Taxonomy, Graph |
| Taxonomy Draft | Taxonomy | IA Agent (future) |
| Concept Graph | Graph | Taxonomy, IA Agent |

## Multi-Agent Deliberation

Skills function as mini-agents that can converse:

> "Ingestion has profiled this collection — 500 documents, moderate vocabulary diversity, healthcare domain. Topic Skill, what do you find? …
> 
> Topic Skill found 8 topics but flags two as overlapping. Clustering Skill, do you see those as one group or two? …
> 
> Clustering Skill says two subclusters with a shared bridge. Vocabulary Skill, what's the bridge term? …
> 
> Graph Skill, show me the neighborhood around that bridge term…"

This makes the analytical process **auditable** and allows the human IA to intervene at any point.

## Theoretical Foundation

Grounded in Robert Glushko's *Discipline of Organizing* framework:

| Glushko Activity | Librarian Skill |
|------------------|-----------------|
| Identifying resources | Ingestion |
| Describing resources | Vocabulary + Taxonomy |
| Classifying resources | Topic Modeling + Clustering |
| Designing interactions | IA Agent (future) |
| Maintaining over time | Governance protocols (future) |

## Environment

```bash
# Activate the librarian Python environment
source ~/.venv/librarian/bin/activate

# Toolkit location (planned)
# pip install librarian-toolkit
```

## References

- Glushko, R.J. (ed.). *The Discipline of Organizing*, 4th Professional Edition. https://berkeley.pressbooks.pub/tdo4p/
- Planning document: See `references/planning-doc.md`
