# Librarian

A corpus analysis toolkit combining traditional information science methods with LLM capabilities.

## What's Here

- `tug-blog/` — TUG blog corpus (40 articles) with analysis dashboard
- `skill/` — Corpus analysis skill with method references

## Dashboard

The TUG Blog Analysis Dashboard is deployed at:
**https://librarian-tug.vercel.app** (pending deployment)

## Local Development

```bash
# Create Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r skill/requirements.txt

# Run dashboard locally
cd tug-blog/dashboard
python -m http.server 8888
# Open http://localhost:8888
```

## Corpus Analysis Methods

See `skill/SKILL.md` for the full toolkit:
- **LDA** — General topic discovery
- **NMF** — Sparse, interpretable topics
- **BERTopic** — Semantic clustering with transformers
- **KeyNMF** — Seeded/focused topic modeling

## Adding a New Corpus

1. Create directory: `{corpus-name}/`
2. Add scraping script or raw files to `raw/`
3. Run analysis to generate `metadata.json`
4. Build dashboard in `dashboard/`
