#!/usr/bin/env python3
"""Scrape TUG blog posts into corpus structure."""

import json
import os
import time
from datetime import datetime
from trafilatura import fetch_url, extract

BASE_URL = "https://understandinggroup.com"

# Articles discovered from index pages
ARTICLES = {
    "ia-practice": [
        "the-three-laws-of-good-project-roadmapping",
        "three-guidelines-for-making-useful-taxonomies",
        "reimagining-collaboration-a-playful-approach-to-facilitating-our-in-tension-alignment-workshop",
        "applying-a-service-design-lens-to-information-architecture-practice",
        "beyond-jargon-the-power-of-plain-language-in-information-architecture",
        "learn-about-the-three-core-tenets-of-information-architecture-with-dan-klyn",
        "help-your-product-managers-succeed-with-blueprints",
        "managing-conceptual-debt-using-modeling-to-gain-understanding-1",
        "model-play-session-2-relationships-of-books-within-your-home",
        "modeling-for-team-play-1-light-sources-in-your-home",
        "five-ways-to-tell-if-you-suffer-from-conceptual-debt",
        "intension-modeling-gains-alignment-1",
        "plain-language-model-amp-guide",
        "is-your-companys-complexity-essential-or-artificial",
        "dan-klyns-sermon-notes-for-wiad-bristol-2021",
        "talking-about-tugs-information-architecture-staycation-workshop",
        "talking-about-tugs-modeling-for-clarity-workshop",
        "graceful-change-for-intranet-communities",
        "how-was-your-last-site-redesign",
        "tell-better-stories-with-proportional-analysis",
    ],
    "ia-theory": [
        "leading-your-team-in-the-face-of-ai",
        "ethical-ai-integration-with-the-aligned-groups-framework",
        "it-takes-a-village-unlocking-ai-success-through-an-ai-center-of-excellence",
        "information-architecture-is-a-best-practice-now-so-bring-on-the-metrics",
        "otc",
        "politics-of-classification-resmini",
        "how-conceptual-models-avoid-failure-in-digital-projects",
        "communicators-in-higher-education-are-pivotal-to-ethical-ai-integration",
        "ethical-ai-beyond-application-to-integration",
        "iac2023recap",
        "ia-in-a-world-of-bullsht",
        "bring-innovation-back-to-agile-by-adding-information-architecture",
        "making-use-of-blueprints-to-improve-your-agile-projects",
        "is-your-company-blindly-building-software",
        "rigorous-modeling-frameworks-for-deep-understanding",
        "information-architecture-and-incremental-website-improvement",
        "fix-digital-strategy-with-information-architecture",
        "four-objections-developers-have-about-information-architecture",
        "why-do-we-still-build-websites-like-its-1999",
        "good-web-design-creates-joyful-user-experiences",
    ]
}

def scrape_article(category, slug):
    """Fetch and extract a single article."""
    url = f"{BASE_URL}/{category}/{slug}"
    print(f"  Fetching: {url}")
    
    html = fetch_url(url)
    if not html:
        print(f"  ERROR: Could not fetch {url}")
        return None
    
    text = extract(html, include_comments=False, include_tables=True)
    if not text:
        print(f"  ERROR: Could not extract text from {url}")
        return None
    
    return {
        "url": url,
        "category": category,
        "slug": slug,
        "text": text,
        "fetched_at": datetime.now().isoformat()
    }

def main():
    # Setup directories
    os.makedirs("raw", exist_ok=True)
    os.makedirs("processed", exist_ok=True)
    
    articles = []
    errors = []
    
    for category, slugs in ARTICLES.items():
        print(f"\n=== {category.upper()} ({len(slugs)} articles) ===")
        
        for slug in slugs:
            result = scrape_article(category, slug)
            
            if result:
                # Save raw text
                filename = f"{category}--{slug}.txt"
                with open(f"raw/{filename}", "w") as f:
                    f.write(result["text"])
                
                articles.append({
                    "url": result["url"],
                    "category": result["category"],
                    "slug": result["slug"],
                    "filename": filename,
                    "char_count": len(result["text"]),
                    "fetched_at": result["fetched_at"]
                })
                print(f"  ✓ Saved ({len(result['text'])} chars)")
            else:
                errors.append(f"{category}/{slug}")
            
            # Be polite
            time.sleep(0.5)
    
    # Save metadata
    metadata = {
        "name": "tug-blog",
        "description": "The Understanding Group blog posts on IA Practice and IA Theory",
        "source": BASE_URL,
        "collected": datetime.now().isoformat(),
        "document_count": len(articles),
        "categories": list(ARTICLES.keys()),
        "articles": articles,
        "errors": errors
    }
    
    with open("metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n=== COMPLETE ===")
    print(f"Scraped: {len(articles)} articles")
    print(f"Errors: {len(errors)}")
    if errors:
        print(f"Failed: {errors}")

if __name__ == "__main__":
    main()
