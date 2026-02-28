# Corpus Profiling: What the Numbers Mean

Statistical characterization of a corpus is not just data collection. Each metric tells you something about what analytical methods will work and what pitfalls to expect.

## Document Count

| Range | Implications |
|-------|--------------|
| < 20 | Manual review feasible. Statistical methods unreliable. |
| 20-50 | Clustering works. LDA marginal. Manual validation essential. |
| 50-500 | Sweet spot for most methods. LDA viable. |
| 500-5,000 | Full toolkit available. Consider sampling for exploration. |
| 5,000-50,000 | Sampling recommended for initial exploration. Batch processing needed. |
| > 50,000 | Distributed processing. Strategic sampling. Incremental analysis. |

## Length Distribution

**Why it matters:** Documents of vastly different lengths behave differently under analysis. A 50-page whitepaper and a 2-paragraph news brief are not equivalent units.

| Pattern | What it suggests |
|---------|------------------|
| Tight distribution (low std) | Homogeneous collection. Methods will work consistently. |
| Wide distribution (high std) | Heterogeneous. May need to segment by length or type. |
| Many very short docs (< 100 chars) | Stubs, fragments, or metadata records. Flag for review. |
| Few very long docs | Outliers may dominate topic models. Consider segmentation. |
| Bimodal distribution | Two different document types mixed. Segment before analysis. |

**Rule of thumb:** If std > mean, you have high heterogeneity.

## Vocabulary Metrics

### Unique Terms

Raw count of distinct word types after basic normalization.

| Range | Interpretation |
|-------|----------------|
| < 1,000 | Small vocabulary. Specialized domain or small corpus. |
| 1,000-10,000 | Typical for focused domain corpus. |
| 10,000-50,000 | Rich vocabulary. General domain or large corpus. |
| > 50,000 | Very large or very diverse. Watch for noise. |

### Type-Token Ratio (TTR)

Unique terms ÷ total tokens. Measures vocabulary diversity.

| TTR | Interpretation |
|-----|----------------|
| > 0.5 | High diversity. Small corpus or very varied content. |
| 0.2-0.5 | Moderate diversity. Typical for domain-specific content. |
| 0.1-0.2 | Repetitive vocabulary. Technical/specialized domain. |
| < 0.1 | Very repetitive. May indicate boilerplate or templates. |

**Caution:** TTR decreases with corpus size. Compare only corpora of similar size.

### Hapax Legomena

Words appearing exactly once.

| Hapax % | Interpretation |
|---------|----------------|
| > 50% | Many rare terms. OCR errors? Proper nouns? Misspellings? |
| 30-50% | Normal range for natural text. |
| < 30% | Controlled vocabulary or templated content. |

High hapax count suggests either noise (errors) or rich terminology (technical domain). Investigate before proceeding.

## Vocabulary Richness Assessment

Combine metrics into an overall assessment:

| Richness | Characteristics | Implications |
|----------|-----------------|--------------|
| **Low** | TTR < 0.1, few unique terms, repetitive | Controlled vocabulary exists. Taxonomy extraction promising. |
| **Moderate** | TTR 0.1-0.3, reasonable term diversity | Standard methods work. Good baseline for analysis. |
| **High** | TTR > 0.3, many unique terms, high hapax | May need vocabulary normalization. Watch for noise. |

## Format Distribution

What file types are present?

| Pattern | What it suggests |
|---------|------------------|
| Single format (.txt, .md) | Pre-processed or homogeneous source. Clean. |
| Mixed documents (.pdf, .docx, .txt) | Extraction quality will vary. Check for errors. |
| Web formats (.html, .htm) | May contain navigation/boilerplate. Extraction critical. |
| Structured data (.json, .xml, .csv) | Different treatment needed. May not be "documents." |

## Language Detection

| Finding | Implications |
|---------|--------------|
| Single language | Standard methods apply. |
| Mixed languages | Segment by language before analysis, or use multilingual models. |
| Wrong language detected | Check for OCR errors, code snippets, or metadata pollution. |

## Quality Flags

### Duplicates

| Duplicate % | Action |
|-------------|--------|
| 0-1% | Normal. Ignore. |
| 1-10% | Deduplicate before analysis. |
| > 10% | Investigate source. Web crawl? Version copies? |

Duplicates will inflate topic coherence artificially.

### Stubs (< 100 characters)

May be:
- Incomplete documents
- Metadata-only records
- Navigation pages or redirects
- Errors in extraction

Review manually. Often exclude from analysis but keep in inventory.

### Encoding Issues

Non-UTF8, mojibake, or garbled text. Fix before analysis or exclude.

## Feasibility Assessment

Based on profiling, assess what methods are viable:

### Topic Modeling (LDA/NMF)

| Criterion | Minimum | Ideal |
|-----------|---------|-------|
| Document count | 50 | 200+ |
| Avg doc length | 100 tokens | 300+ tokens |
| Vocabulary richness | Moderate | Moderate-High |
| Homogeneity | Low-Moderate | Low-Moderate |

**Red flags:** Very short docs, very small corpus, extreme heterogeneity.

### Clustering

| Criterion | Minimum | Ideal |
|-----------|---------|-------|
| Document count | 20 | 100+ |
| Avg doc length | 50 tokens | 200+ tokens |

More forgiving than topic modeling. Works on smaller corpora.

### Taxonomy Extraction

Best when:
- Prior categories exist in metadata
- Folder structure suggests organization
- Vocabulary is controlled/consistent

Harder when:
- No prior organization
- High vocabulary diversity
- Heterogeneous document types

### Faceted Analysis

Look for:
- Multiple metadata fields present
- Orthogonal dimensions evident (e.g., date + topic + author)
- User questions that cross-cut categories

## Red Flags Summary

| Flag | Risk |
|------|------|
| < 20 documents | Statistical methods unreliable |
| Std > 2× mean length | High heterogeneity, segment first |
| > 50% hapax | Noise or extreme specialization |
| > 10% duplicates | Inflated coherence, dedupe first |
| > 20% stubs | Collection may be incomplete |
| Mixed languages | Segment or use multilingual approach |
| No metadata | Limited facet options |

## Communicating Results

The Capabilities Briefing should present profiling results in terms of **what's possible**, not raw statistics:

**Don't say:** "TTR is 0.08, hapax ratio 32%, mean length 4,200 chars"

**Say:** "This is a focused, technical collection with consistent vocabulary — good candidate for topic modeling. The 200-page reports and 2-page briefs should probably be analyzed separately."

The human IA needs to understand the landscape of options, not pass a statistics exam.
