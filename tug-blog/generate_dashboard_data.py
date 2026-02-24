#!/usr/bin/env python3
"""Generate enriched metadata for dashboard visualization."""

import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load existing metadata
with open("metadata.json") as f:
    meta = json.load(f)

# Load all documents
docs = {}
for article in meta["articles"]:
    with open(f"raw/{article['filename']}") as f:
        docs[article["slug"]] = f.read()

# Manual persona/pain point assignments based on reading content
# Primary persona + pain points addressed
ENRICHMENTS = {
    # IA Practice articles
    "the-three-laws-of-good-project-roadmapping": {
        "primary_persona": "ben",
        "secondary_personas": ["laura"],
        "pain_points": ["product-decisions", "organizational-alignment"],
        "answers": ["how-do-we-structure-this"],
        "concepts": ["roadmapping", "blueprints"],
        "format": "how-to"
    },
    "three-guidelines-for-making-useful-taxonomies": {
        "primary_persona": "sue",
        "secondary_personas": ["laura"],
        "pain_points": ["digital-strategy", "organizational-alignment"],
        "answers": ["how-can-i-make-it-better"],
        "concepts": ["taxonomies"],
        "format": "how-to"
    },
    "reimagining-collaboration-a-playful-approach-to-facilitating-our-in-tension-alignment-workshop": {
        "primary_persona": "sue",
        "secondary_personas": ["ben"],
        "pain_points": ["organizational-buy-in", "team-integration"],
        "answers": ["how-will-your-team-integrate"],
        "concepts": ["modeling", "alignment", "in-tension"],
        "format": "case-study"
    },
    "applying-a-service-design-lens-to-information-architecture-practice": {
        "primary_persona": "sue",
        "secondary_personas": ["laura"],
        "pain_points": ["cross-channel-concerns", "team-integration"],
        "answers": ["how-do-i-deal-with-cross-channel"],
        "concepts": ["service-design", "blueprints"],
        "format": "thought-leadership"
    },
    "beyond-jargon-the-power-of-plain-language-in-information-architecture": {
        "primary_persona": "laura",
        "secondary_personas": ["sue"],
        "pain_points": ["digital-strategy", "trust-building"],
        "answers": ["how-can-i-make-it-better"],
        "concepts": ["plain-language"],
        "format": "how-to"
    },
    "learn-about-the-three-core-tenets-of-information-architecture-with-dan-klyn": {
        "primary_persona": "sue",
        "secondary_personas": ["ben"],
        "pain_points": ["ia-understanding"],
        "answers": ["how-is-ia-different-from-ux"],
        "concepts": ["otc", "ia-foundations"],
        "format": "framework"
    },
    "help-your-product-managers-succeed-with-blueprints": {
        "primary_persona": "ben",
        "secondary_personas": ["sue"],
        "pain_points": ["product-decisions", "team-integration"],
        "answers": ["how-will-you-work-with-my-dev-team"],
        "concepts": ["blueprints"],
        "format": "how-to"
    },
    "managing-conceptual-debt-using-modeling-to-gain-understanding-1": {
        "primary_persona": "ben",
        "secondary_personas": ["sara"],
        "pain_points": ["product-decisions", "organizational-alignment"],
        "answers": ["how-do-we-fix-this-mess"],
        "concepts": ["conceptual-debt", "modeling"],
        "format": "thought-leadership"
    },
    "model-play-session-2-relationships-of-books-within-your-home": {
        "primary_persona": "sue",
        "secondary_personas": [],
        "pain_points": ["skill-building"],
        "answers": ["how-do-i-learn-modeling"],
        "concepts": ["modeling"],
        "format": "how-to"
    },
    "modeling-for-team-play-1-light-sources-in-your-home": {
        "primary_persona": "sue",
        "secondary_personas": [],
        "pain_points": ["skill-building"],
        "answers": ["how-do-i-learn-modeling"],
        "concepts": ["modeling"],
        "format": "how-to"
    },
    "five-ways-to-tell-if-you-suffer-from-conceptual-debt": {
        "primary_persona": "ben",
        "secondary_personas": ["sara"],
        "pain_points": ["product-decisions", "demonstrating-impact"],
        "answers": ["why-isnt-this-working"],
        "concepts": ["conceptual-debt"],
        "format": "thought-leadership"
    },
    "intension-modeling-gains-alignment-1": {
        "primary_persona": "sue",
        "secondary_personas": ["ben", "sara"],
        "pain_points": ["organizational-buy-in", "team-integration"],
        "answers": ["how-do-we-get-aligned"],
        "concepts": ["modeling", "alignment", "in-tension"],
        "format": "framework"
    },
    "plain-language-model-amp-guide": {
        "primary_persona": "laura",
        "secondary_personas": ["sue"],
        "pain_points": ["digital-strategy", "trust-building"],
        "answers": ["how-can-i-make-it-better"],
        "concepts": ["plain-language", "modeling"],
        "format": "how-to"
    },
    "is-your-companys-complexity-essential-or-artificial": {
        "primary_persona": "sara",
        "secondary_personas": ["ben"],
        "pain_points": ["limited-resources", "demonstrating-impact"],
        "answers": ["whats-the-roi"],
        "concepts": ["complexity"],
        "format": "thought-leadership"
    },
    "dan-klyns-sermon-notes-for-wiad-bristol-2021": {
        "primary_persona": "sue",
        "secondary_personas": [],
        "pain_points": ["ia-understanding"],
        "answers": ["what-is-ia-really"],
        "concepts": ["ia-foundations", "otc"],
        "format": "thought-leadership"
    },
    "talking-about-tugs-information-architecture-staycation-workshop": {
        "primary_persona": "sue",
        "secondary_personas": ["sara"],
        "pain_points": ["skill-building", "ia-understanding"],
        "answers": ["how-do-i-learn-ia"],
        "concepts": ["ia-foundations"],
        "format": "interview"
    },
    "talking-about-tugs-modeling-for-clarity-workshop": {
        "primary_persona": "sue",
        "secondary_personas": ["ben"],
        "pain_points": ["skill-building"],
        "answers": ["how-do-i-learn-modeling"],
        "concepts": ["modeling"],
        "format": "interview"
    },
    "graceful-change-for-intranet-communities": {
        "primary_persona": "laura",
        "secondary_personas": ["sue"],
        "pain_points": ["fast-changing-landscape", "digital-strategy"],
        "answers": ["how-do-we-improve-incrementally"],
        "concepts": ["shearing-layers"],
        "format": "how-to"
    },
    "how-was-your-last-site-redesign": {
        "primary_persona": "laura",
        "secondary_personas": ["sue"],
        "pain_points": ["digital-strategy"],
        "answers": ["how-can-i-make-it-better"],
        "concepts": ["ia-foundations"],
        "format": "thought-leadership"
    },
    "tell-better-stories-with-proportional-analysis": {
        "primary_persona": "laura",
        "secondary_personas": ["ben"],
        "pain_points": ["demonstrating-impact", "need-better-metrics"],
        "answers": ["how-do-i-communicate-this"],
        "concepts": ["modeling", "analysis"],
        "format": "how-to"
    },
    
    # IA Theory articles
    "leading-your-team-in-the-face-of-ai": {
        "primary_persona": "sara",
        "secondary_personas": ["laura"],
        "pain_points": ["ai-anxiety", "demonstrating-impact"],
        "answers": ["how-will-ai-change-my-world"],
        "concepts": ["pace-layers", "ai-strategy"],
        "format": "thought-leadership"
    },
    "ethical-ai-integration-with-the-aligned-groups-framework": {
        "primary_persona": "sara",
        "secondary_personas": ["laura"],
        "pain_points": ["ai-anxiety", "organizational-alignment"],
        "answers": ["how-do-we-do-ai-responsibly"],
        "concepts": ["ai-ethics", "alignment"],
        "format": "framework"
    },
    "it-takes-a-village-unlocking-ai-success-through-an-ai-center-of-excellence": {
        "primary_persona": "sara",
        "secondary_personas": ["laura"],
        "pain_points": ["ai-anxiety", "organizational-alignment"],
        "answers": ["how-do-we-organize-for-ai"],
        "concepts": ["ai-strategy", "governance"],
        "format": "framework"
    },
    "information-architecture-is-a-best-practice-now-so-bring-on-the-metrics": {
        "primary_persona": "sara",
        "secondary_personas": ["ben"],
        "pain_points": ["demonstrating-impact", "need-better-metrics"],
        "answers": ["whats-the-roi"],
        "concepts": ["metrics", "ia-foundations"],
        "format": "thought-leadership"
    },
    "otc": {
        "primary_persona": "sue",
        "secondary_personas": [],
        "pain_points": ["ia-understanding"],
        "answers": ["what-is-ia-really"],
        "concepts": ["otc", "ia-foundations"],
        "format": "framework"
    },
    "politics-of-classification-resmini": {
        "primary_persona": "sue",
        "secondary_personas": ["sara"],
        "pain_points": ["ai-anxiety", "ia-understanding"],
        "answers": ["how-does-ai-affect-ia"],
        "concepts": ["taxonomies", "ai-ethics"],
        "format": "thought-leadership"
    },
    "how-conceptual-models-avoid-failure-in-digital-projects": {
        "primary_persona": "ben",
        "secondary_personas": ["sue"],
        "pain_points": ["product-decisions", "organizational-alignment"],
        "answers": ["how-do-we-avoid-failure"],
        "concepts": ["modeling", "alignment"],
        "format": "thought-leadership"
    },
    "communicators-in-higher-education-are-pivotal-to-ethical-ai-integration": {
        "primary_persona": "sara",
        "secondary_personas": ["laura"],
        "pain_points": ["ai-anxiety"],
        "answers": ["how-do-we-do-ai-responsibly"],
        "concepts": ["ai-ethics"],
        "format": "thought-leadership"
    },
    "ethical-ai-beyond-application-to-integration": {
        "primary_persona": "sara",
        "secondary_personas": [],
        "pain_points": ["ai-anxiety"],
        "answers": ["how-do-we-do-ai-responsibly"],
        "concepts": ["ai-ethics"],
        "format": "thought-leadership"
    },
    "iac2023recap": {
        "primary_persona": "sue",
        "secondary_personas": [],
        "pain_points": ["skill-building"],
        "answers": ["what-is-happening-in-ia"],
        "concepts": ["ia-foundations"],
        "format": "case-study"
    },
    "ia-in-a-world-of-bullsht": {
        "primary_persona": "sue",
        "secondary_personas": ["sara"],
        "pain_points": ["ai-anxiety", "ia-understanding"],
        "answers": ["how-does-ai-affect-ia"],
        "concepts": ["ai-ethics", "ia-foundations"],
        "format": "thought-leadership"
    },
    "bring-innovation-back-to-agile-by-adding-information-architecture": {
        "primary_persona": "ben",
        "secondary_personas": ["sue"],
        "pain_points": ["product-decisions", "team-integration"],
        "answers": ["how-will-you-work-with-my-dev-team"],
        "concepts": ["blueprints", "agile"],
        "format": "thought-leadership"
    },
    "making-use-of-blueprints-to-improve-your-agile-projects": {
        "primary_persona": "ben",
        "secondary_personas": ["sue"],
        "pain_points": ["product-decisions", "team-integration"],
        "answers": ["how-will-you-work-with-my-dev-team"],
        "concepts": ["blueprints", "agile"],
        "format": "how-to"
    },
    "is-your-company-blindly-building-software": {
        "primary_persona": "ben",
        "secondary_personas": ["sara"],
        "pain_points": ["product-decisions", "organizational-alignment"],
        "answers": ["why-do-our-projects-fail"],
        "concepts": ["blueprints"],
        "format": "thought-leadership"
    },
    "rigorous-modeling-frameworks-for-deep-understanding": {
        "primary_persona": "sue",
        "secondary_personas": ["ben"],
        "pain_points": ["skill-building", "organizational-alignment"],
        "answers": ["how-do-we-get-clarity"],
        "concepts": ["modeling"],
        "format": "thought-leadership"
    },
    "information-architecture-and-incremental-website-improvement": {
        "primary_persona": "laura",
        "secondary_personas": ["sue"],
        "pain_points": ["fast-changing-landscape", "digital-strategy"],
        "answers": ["how-do-we-improve-incrementally"],
        "concepts": ["shearing-layers"],
        "format": "framework"
    },
    "fix-digital-strategy-with-information-architecture": {
        "primary_persona": "laura",
        "secondary_personas": ["sara"],
        "pain_points": ["digital-strategy"],
        "answers": ["whats-the-strategy"],
        "concepts": ["ia-foundations"],
        "format": "thought-leadership"
    },
    "four-objections-developers-have-about-information-architecture": {
        "primary_persona": "ben",
        "secondary_personas": ["sue"],
        "pain_points": ["team-integration"],
        "answers": ["how-is-ia-different-from-ux", "how-will-you-work-with-my-dev-team"],
        "concepts": ["ia-foundations", "agile"],
        "format": "thought-leadership"
    },
    "why-do-we-still-build-websites-like-its-1999": {
        "primary_persona": "laura",
        "secondary_personas": ["sue"],
        "pain_points": ["digital-strategy", "fast-changing-landscape"],
        "answers": ["whats-the-strategy"],
        "concepts": ["ia-foundations"],
        "format": "thought-leadership"
    },
    "good-web-design-creates-joyful-user-experiences": {
        "primary_persona": "sue",
        "secondary_personas": ["laura", "ben"],
        "pain_points": ["customer-delight"],
        "answers": ["how-do-we-delight-users"],
        "concepts": ["ux", "ia-foundations"],
        "format": "thought-leadership"
    },
}

# Compute document similarity for "related articles"
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
slugs = list(docs.keys())
texts = [docs[s] for s in slugs]
tfidf = vectorizer.fit_transform(texts)
sim_matrix = cosine_similarity(tfidf)

def get_related(slug, n=3):
    """Get top n related articles by cosine similarity."""
    idx = slugs.index(slug)
    sims = list(enumerate(sim_matrix[idx]))
    sims.sort(key=lambda x: x[1], reverse=True)
    # Skip self (index 0)
    return [slugs[i] for i, score in sims[1:n+1]]

# Build enriched data
enriched_articles = []
for article in meta["articles"]:
    slug = article["slug"]
    enrichment = ENRICHMENTS.get(slug, {})
    
    enriched = {
        "title": slug.replace("-", " ").title(),
        "slug": slug,
        "url": article["url"],
        "category": article["category"],
        "char_count": article["char_count"],
        "primary_persona": enrichment.get("primary_persona", "unknown"),
        "secondary_personas": enrichment.get("secondary_personas", []),
        "pain_points": enrichment.get("pain_points", []),
        "answers": enrichment.get("answers", []),
        "concepts": enrichment.get("concepts", []),
        "format": enrichment.get("format", "unknown"),
        "related_articles": get_related(slug, 3),
    }
    enriched_articles.append(enriched)

# Compute stats
persona_counts = {"sara": 0, "laura": 0, "ben": 0, "sue": 0}
for a in enriched_articles:
    p = a["primary_persona"]
    if p in persona_counts:
        persona_counts[p] += 1

concept_counts = {}
for a in enriched_articles:
    for c in a["concepts"]:
        concept_counts[c] = concept_counts.get(c, 0) + 1

pain_counts = {}
for a in enriched_articles:
    for p in a["pain_points"]:
        pain_counts[p] = pain_counts.get(p, 0) + 1

# Output
output = {
    "generated": meta["collected"],
    "article_count": len(enriched_articles),
    "personas": {
        "sara": {"name": "Sara - C-Level Executive", "count": persona_counts["sara"]},
        "laura": {"name": "Laura - VP Marketing Nonprofit", "count": persona_counts["laura"]},
        "ben": {"name": "Ben - Product Manager", "count": persona_counts["ben"]},
        "sue": {"name": "Sue - UX Lead", "count": persona_counts["sue"]},
    },
    "concept_counts": dict(sorted(concept_counts.items(), key=lambda x: -x[1])),
    "pain_counts": dict(sorted(pain_counts.items(), key=lambda x: -x[1])),
    "articles": enriched_articles,
}

os.makedirs("dashboard", exist_ok=True)
with open("dashboard/data.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Generated dashboard data for {len(enriched_articles)} articles")
print(f"\nPersona distribution:")
for p, data in output["personas"].items():
    print(f"  {data['name']}: {data['count']}")
print(f"\nTop concepts: {list(concept_counts.keys())[:8]}")
print(f"Top pain points: {list(pain_counts.keys())[:8]}")
