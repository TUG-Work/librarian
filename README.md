# Librarian

A corpus analysis agent combining formal information science methods with LLM judgment.

## Vision

The Librarian Agent orchestrates the formal tools of information science to support information architects. LLMs are good at intuiting semantic relationships but do so as a black box. Information science has decades of rigorous, reproducible, auditable methods.

**Combining LLM judgment with formal IS tools produces something better than either alone: auditable intermediate representations at each analytical stage.**

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     LIBRARIAN AGENT                             │
│  Orchestrates skills, manages deliberation, interfaces with IA  │
└─────────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
   ┌──────────┐        ┌──────────┐        ┌──────────┐
   │INGESTION │        │  TOPIC   │        │CLUSTERING│
   │          │        │ MODELING │        │          │
   └──────────┘        └──────────┘        └──────────┘
         │                    │                    │
         ▼                    ▼                    ▼
   ┌──────────┐        ┌──────────┐        ┌──────────┐
   │VOCABULARY│        │ TAXONOMY │        │  GRAPH   │
   └──────────┘        └──────────┘        └──────────┘
```

## What's Here

### Skills (`skill-librarian/`)

Agent skills encoding professional practice knowledge:

- **Ingestion Skill** — Receive, examine, characterize a corpus. Produces a Collection Record.
- Topic Modeling (planned)
- Clustering (planned)
- Vocabulary Analysis (planned)
- Taxonomy Builder (planned)
- Concept Graph (planned)

### Toolkit (`skill/`)

Method references and Python environment setup for corpus analysis.

### TUG Blog Corpus (`tug-blog/`)

Example corpus: 40 articles from The Understanding Group blog.

- `dashboard/` — Interactive visualization at https://librarian-murex.vercel.app
- `raw/` — Scraped article text
- Analysis scripts

## Key Concepts

### Collection Record

The output of the Ingestion Skill. A structured description of:
- What's in the corpus
- Its statistical profile
- Prior organization detected
- Quality issues
- Feasibility assessments for different methods
- Recommendations for next steps

See `skill-librarian/ingestion/references/collection-record-schema.json`

### Three-Phase Workflow

1. **Reference Interview** — Light-touch questions to understand purpose
2. **Capabilities Briefing** — What's possible given this corpus
3. **Collaborative Triage** — Options with tradeoffs, co-designed approach

### Theoretical Foundation

Grounded in Glushko's *Discipline of Organizing* framework. See `skill-librarian/references/planning-doc.md`.

## Local Development

```bash
# Create Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r skill/requirements.txt

# Run dashboard locally
cd tug-blog/dashboard
python -m http.server 8888
```

## Dashboard

https://librarian-murex.vercel.app

- Main view: Articles by persona with gap analysis
- Graph view: Topic clusters visualization
