# Librarian Agent: Planning Document

## Project Vision

Build an AI agent — the Librarian Agent — that knows how to orchestrate the formal tools of information science to support information architects. The Librarian Agent is the first of two agents; the second is an Information Architect Agent that will eventually work alongside it. The Librarian handles analytical and organizational groundwork; the IA Agent handles design problems (navigation, labeling, search systems, content models).

The core thesis: LLMs are good at intuiting semantic relationships but do so as a black box. Information science has decades of rigorous, reproducible, auditable methods for the same tasks. Combining LLM judgment with formal IS tools — by teaching the LLM to orchestrate those tools — produces something better than either alone: auditable intermediate representations at each analytical stage.

-----

## Architecture Overview

### The Toolkit (Phase 1 — Built)

A Python package (`librarian-toolkit`) with six core tools:

- Corpus — Document ingestion, inventory, and statistical profiling
- TopicModeler — LDA topic discovery with coherence and similarity analysis
- DocumentClusterer — K-means, hierarchical, and density-based clustering
- VocabularyAnalyzer — TF-IDF term extraction, co-occurrence, controlled vocabulary support
- TaxonomyBuilder — Faceted classification construction, validation, SKOS export
- ConceptGraph — Co-occurrence networks, centrality, community detection

All tools return structured dicts suitable for LLM interpretation. The toolkit is tested and functional.

### The Skills (Phase 2 — In Progress)

Each analytical method becomes a Claude skill that encodes three layers:

1. Practice knowledge — When and why a trained professional uses this method, what the output means, what the pitfalls are
2. Tool interface — How to call the Python toolkit functions and interpret results
3. Collaboration protocols — When to hand off to other skills and what to pass them

Skills are not just API wrappers. They encode the professional judgment of an information scientist. Each skill acts as a domain expert at a deliberation table, and the Librarian Agent orchestrates the conversation between them.

### Multi-Agent Deliberation Pattern

The skills function as mini-agents that can converse with each other. Example deliberation flow:

> "Corpus Ingestion Skill has profiled this collection — 500 documents, moderate vocabulary diversity, healthcare domain. Topic Skill, what do you find? … Topic Skill found 8 topics but flags two as overlapping. Clustering Skill, do you see those as one group or two? … Clustering Skill says two subclusters with a shared bridge. Vocabulary Skill, what's the bridge term? … Graph Skill, show me the neighborhood around that bridge term…"

This makes the analytical process auditable and allows the human IA to intervene at any point.

### Shared Artifacts

The interface between agents is shared artifacts — taxonomies, ontologies, concept maps, controlled vocabularies, corpus analyses. These are formal, inspectable objects that both agents and the human can reason about.

-----

## Theoretical Foundation: Glushko's Organizing System Framework

The Librarian Agent's conceptual backbone is Robert Glushko's framework from *The Discipline of Organizing* (MIT Press, 4th Professional Edition).

Glushko defines an Organizing System as "an intentionally arranged collection of resources and the interactions they support."

Every organizing system involves:

1. Identifying resources to be organized
2. Describing and classifying those resources
3. Designing resource-based interactions
4. Maintaining resources and organization over time

### Why This Framework

Glushko's framework is the right abstraction for the Librarian Agent because:

- It unifies library science, computer science, cognitive science, and business perspectives under a single model. The Librarian Agent will encounter corpora from all of these domains.
- It makes the design decisions in any organizing system explicit. Rather than jumping straight to "run LDA," the agent first asks: what are the resources? What descriptions exist? What interactions are intended? What's the maintenance picture?
- It frames the fundamental tradeoff of **"organization on the way in" vs. "organization on the way out."** A corpus with rich metadata (organized on the way in) needs different treatment than a raw dump (requiring organization on the way out via search, clustering, and classification).

### How It Maps to the Librarian's Work

| Glushko Activity | Librarian Skill | What Happens |
|------------------|-----------------|--------------|
| Identifying resources | Ingestion Skill | Receive, examine, characterize what's in the collection |
| Describing resources | Vocabulary + Taxonomy Skills | Extract terms, build controlled vocabularies, propose categories |
| Classifying resources | Topic + Clustering Skills | Discover groupings, assign documents to categories |
| Designing interactions | IA Agent (future) | Navigation, search, labeling based on organizational structure |
| Maintaining over time | Governance protocols (future) | Taxonomy evolution, vocabulary updates, quality monitoring |

Source: Glushko, R.J. (ed.). *The Discipline of Organizing*, 4th Professional Edition. MIT Press / UC Berkeley. Available open-access at https://berkeley.pressbooks.pub/tdo4p/

Source: Glushko, R.J. (2013). "The Discipline of Organizing." *Bulletin of the American Society for Information Science and Technology*, 40(1).

-----

## The Ingestion Skill: First Skill to Build

### Why Ingestion Comes First

Every invocation of the Librarian Agent starts with a corpus that has to come from somewhere. Before the agent can advise anyone on what to do, it must receive, examine, and characterize the material. This is logically prior to all other skills.

The analogy: when a box of donated materials arrives at a library, or a new archival collection comes in for processing, the librarian doesn't dump it on a shelf. There is a discipline to receiving material.

### What a Librarian Does at Ingestion

**What do we have here?** Physical/digital inspection — how many items, what formats, what condition? Are there folders, labels, or naming conventions that suggest someone already organized this? Is there a finding aid or manifest? The digital equivalent: document count, file types, metadata fields present, folder structures, naming patterns.

**What's the provenance?** Where did this come from? Who created it, for what purpose? Was it curated or is it a raw dump? A carefully curated policy collection behaves differently under analysis than a web crawl, even at the same size.

**What's the scope and boundaries?** Is this everything, or a sample? What's included and excluded? What's obviously missing? Librarians processing archival collections are always attentive to what's *absent*, not just what's present.

**What's the condition?** Is text clean or noisy? Duplicates? Mixed languages? Inconsistent formatting? This is the preprocessing reality check.

**What are the resources, really?** Following Glushko: not just "500 documents" but what *kind* of resources. A 200-page report and a one-paragraph FAQ are both "documents" but are fundamentally different resources needing different treatment. The ingestion skill must characterize resource granularity and boundaries.

**What descriptions already exist?** What organization has been imposed "on the way in"? File names, folder structures, metadata fields, tags, categories — these are prior organizing decisions. They're clues about how the collection was intended to be used, and raw material for the Librarian's own work.

### Ingestion Skill Output: The Collection Record

The output of ingestion is a collection record — analogous to an archivist's finding aid. A structured description of:

- What's in the collection and how it's organized (if at all)
- What condition it's in
- What's known about its origins and purpose
- Statistical characterization (counts, lengths, vocabulary, distribution)
- What descriptions and metadata already exist
- What's missing or problematic
- Initial recommendations for what analytical methods are feasible

This collection record becomes the artifact all other skills reference.

-----

## The Three-Phase Workflow for Human Interaction

When the Librarian Agent works with a human information architect, it follows three phases. These are distinct from the ingestion skill (which produces the collection record). The three phases describe how the agent *advises* the human about what to do.

### Phase 1: The Reference Interview (Light Touch)

Drawn from library science practice. A reference librarian knows that **the first question asked is rarely the actual need**. It's what the person thinks will get the answer they need. The reference librarian is trained to get behind the initial question to find:

- Not just the task (what they want to find or do)
- But the need driving that task
- And the situation/context that created the need

Example: Someone says "organize these 500 documents into categories." The agent probes lightly — is this for navigation? Migration? Governance? Compliance? Search improvement? Each leads to fundamentally different analytical approaches.

Critical design constraint: Reference librarians can seem like gatekeepers. The agent should ask one or two clarifying questions at most, then move forward. It should be helpful, not an intake form.

### Phase 2: The Capabilities Briefing (Adapted Lab Report)

Key insight: **the corpus typically already exists and has been assembled for a reason.** The agent doesn't profile it in a vacuum. It presents a characterization oriented toward *what's possible given what we have*:

- "Here's your corpus and its characteristics"
- "Here are the kinds of analyses that are feasible at this scale"
- "Here's what would be straightforward vs. what would be harder"
- "Here's what additional information would unlock more options"

This is less "lab report" and more capabilities briefing. It respects the person's intelligence by showing them the landscape of options rather than just dumping statistics.

The briefing is built on top of the collection record from the Ingestion Skill.

### Phase 3: Collaborative Triage

The person triages, with the agent's help. The agent does not decide the path unilaterally; it helps the person see options and their tradeoffs:

- "Given what you're trying to accomplish and what this corpus looks like, here are two or three approaches."
- "This one is faster but less precise."
- "This one is more thorough but requires manual input."
- "This one would benefit from getting a domain expert to help define facets first."

This is solution architecture, co-designed. The output is a recommended approach with: what to do, what it'll take (resources, time, cost), and which other agents or skills to bring in.

-----

## Downstream Skills and Collaboration

### When Faceted Analysis Enters

Ranganathan's faceted classification (PMEST) and its modern descendants are powerful but belong downstream of ingestion and initial profiling. Facet discovery is substantive analytical work that may require:

- The Vocabulary Analyzer to surface candidate dimensions
- The Concept Graph to map how dimensions relate
- Potentially the IA Agent (future) to bring user mental models into the picture
- Object modeling or domain analysis that the Librarian works on with other agents

The Ingestion Skill should flag when faceted analysis would be valuable and note what raw materials exist for it (e.g., metadata fields that could serve as facets), but the actual facet modeling is collaborative work across multiple skills.

### Skill Collaboration Protocols

After ingestion and the three-phase human workflow, the Librarian dispatches work:

- Pre-existing categories found in metadata → route to Taxonomy Builder for validation against the corpus
- No pre-existing categories → route to Topic Modeler and Clustering for unsupervised discovery
- High vocabulary diversity → flag for Concept Graph to map the landscape
- Sparse metadata → recommend enrichment before proceeding
- Very small corpus (< 50 docs) → caution on LDA, prefer clustering
- Very large corpus (> 10K docs) → recommend sampling before exploratory analysis

-----

## Research Base and References

### Organizing Systems and Information Architecture

- Glushko, R.J. (ed.). *The Discipline of Organizing*, 4th Professional Edition. MIT Press / UC Berkeley. https://berkeley.pressbooks.pub/tdo4p/
- Glushko, R.J. (2013). "The Discipline of Organizing." *Bulletin of ASIS&T*, 40(1).
- Rosenfeld, L., Morville, P., & Arango, J. (2015). *Information Architecture: For the Web and Beyond*, 4th ed. O'Reilly Media.
- Beecher, F. (2009). "Content Analysis Heuristics." *Boxes and Arrows*. https://boxesandarrows.com/content-analysis-heuristics/
- Hide and Seek Digital. "Six Steps for Success Content Transformation." https://hideandseek.digital/articles/six-steps-to-a-successful-content-transformation

### Corpus Linguistics and Statistical Characterization

- Biber, D., Conrad, S., & Reppen, R. (1998). *Corpus Linguistics: Investigating Language Structure and Use*. Cambridge University Press.
- O'Keeffe, A., McCarthy, M.J., & Carter, R.A. (2007). *From Corpus to Classroom*. Cambridge University Press.
- Lu, X. (2014). *Computational Methods for Corpus Annotation and Analysis*. Springer. https://doi.org/10.1007/978-94-017-8645-4
- Evison, J. "What are the basics of analysing a corpus?" in *The Routledge Handbook of Corpus Linguistics*.
- Schweinberger, M. (2024). "What are Corpus Linguistics and Text Analysis?" SLAT7829. https://martinschweinberger.github.io/SLAT7829/
- Stansberry, K. (2018). "Corpus linguistics is not just for linguists." *Library Hi Tech*, 36(2). https://doi.org/10.1108/lht-12-2017-0271

### Content Analysis Methodology

- Berelson, B. (1952). *Content Analysis in Communication Research*. Free Press.
- Krippendorff, K. (2004). *Content Analysis: An Introduction to Its Methodology*, 2nd ed. Sage.
- Grimmer, J., & Stewart, B.M. (2013). "Text as Data." *Political Analysis*, 21(3).
- Neuendorf, K.A. (2002). *The Content Analysis Guidebook*. Sage.

### Classification Theory

- Ranganathan, S.R. (1933/1957). *Colon Classification*. Madras Library Association.
- Svenonius, E. (2000). *The Intellectual Foundation of Information Organization*. MIT Press.
- Hedden, H. "Faceted Classification and Faceted Taxonomies." Hedden Information Management. https://www.hedden-information.com/faceted-classification-and-faceted-taxonomies/
- Glushko, R.J. (ed.). "Faceted Classification" in *The Discipline of Organizing*, 4th ed. https://berkeley.pressbooks.pub/tdo4p/chapter/faceted-classification/
- Satija, M.P. & Singh, J. (2013). "Colon Classification: A Requiem." *DESIDOC Journal of Library & Information Technology*, 33(4), 265-276.

### Topic Modeling Evaluation

- Blei, D.M., Ng, A.Y., & Jordan, M.I. (2003). "Latent Dirichlet Allocation." *JMLR*, 3, 993-1022.
- Röder, M., Both, A., & Hinneburg, A. (2015). "Exploring the Space of Topic Coherence Measures." *WSDM '15*.
- Chang, J., et al. (2009). "Reading Tea Leaves: How Humans Interpret Topic Models." *NIPS '09*.
- Li, W., et al. (2021). "Selection of the Optimal Number of Topics for LDA Topic Model." *Entropy*, 23(10), 1280. https://pmc.ncbi.nlm.nih.gov/articles/PMC8534395/
- Kapadia, S. (2019/2025). "Evaluate Topic Models: Latent Dirichlet Allocation (LDA)." *Towards Data Science*. (Practical guide to coherence scoring with Gensim.)

-----

## Open Design Questions

1. **Skill communication format:** Should skills exchange a standardized JSON "corpus profile" object, or should each skill adapt its output to its consumer? Standardized is more robust; adapted is more efficient.

2. **How much autonomy for the agent?** The three-phase workflow puts the human in charge of triage. But in automated pipelines (no human in the loop), how much should the Librarian decide on its own?

3. **Non-text content:** Real IA corpora include images, PDFs with mixed content, structured data, video transcripts. How should the ingestion skill handle resources it can't directly analyze with text tools?

4. **Minimum viable analysis:** For a tiny corpus (5 docs), what's still worth computing? The skill needs graceful degradation, not just "corpus too small."

5. **Object modeling for facets:** When faceted analysis is warranted, how should the Librarian and other agents collaborate on the object modeling work? This may need its own skill or protocol.

6. **Skill packaging:** Each skill will be a Claude skill (.skill file). How should the toolkit Python code be bundled — as scripts within each skill, or as a shared library that all skills reference?

-----

## Next Steps

1. Draft the Ingestion Skill SKILL.md — encoding the practice knowledge described above, with references to the toolkit's Corpus tool
2. Test against sample corpora — verify the skill produces useful collection records
3. Draft the Corpus Briefing Skill — the human-facing skill that implements the three-phase workflow
4. Define the inter-skill communication protocol — the standardized artifact format that skills exchange
5. Build remaining skills — Topic Modeling, Clustering, Vocabulary, Taxonomy, Concept Graph, each with their own practice knowledge
6. Integration testing — end-to-end workflow from ingestion through taxonomy proposal
