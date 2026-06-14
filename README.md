# Synthesize Data

Synthesize Data is a divine-pattern research prototype. It analyzes theology,
music lyrics, music notes, visual art, history, world languages, biblical Greek
and Hebrew, global text traditions, psychology, politics, science, technology,
culture, practical theology, pressure tests, and source metadata.

The current Trinitarian pattern lens is:

```text
Father creates and sustains order.
Son / Logos reveals meaning and redeems disorder.
Holy Spirit makes redemption present through communion and transformation.
```

The project also includes a mathematical theophany filter. It asks whether
mathematical order, pattern, symmetry, logic, infinity, and beauty may function
as cautious signs of divine self-disclosure, while requiring contrasting
evidence and alternative interpretations before any claim is strengthened.

## Run

```powershell
python divine_pattern_analyzer.py
```

Main reports are written to `reports/`.

## AI Knowledge Backend

The project now includes a first-pass backend shape for:

```text
MLLM + retrieval + knowledge graph + review rules
```

Build it locally with:

```powershell
python ai_knowledge_backend.py
```

The backend writes:

```text
reports/knowledge_retrieval_index.json
reports/knowledge_graph.json
reports/review_rules_audit.json
reports/multimodal_review_manifest.json
reports/ai_backend_report.txt
reports/combined_web_article.md
reports/combined_web_article.html
reports/published/final_book_report.md
```

The retrieval index is a local TF-IDF-style source index for RAG-style prompts
over text, captions, transcripts, and review notes. The knowledge graph connects
documents and media assets to source lanes, leading patterns, and review-rule
concepts. The review audit checks whether sources mention core claim controls
such as evidence, interpretation, discernment, analogy, practical use,
counter-reading, failure condition, and the boundary that machine labels route
attention rather than settle truth.

The multimodal manifest makes the backend MLLM-ready for image, video, and
audio assets. Media can enter the corpus directly, but uncaptioned or
untranscribed media is marked as needing MLLM or human review before it can
strengthen a claim. Sidecar files such as `image.jpg.md`, `image.md`,
`video.mp4.txt`, or `video.txt` can provide captions, transcripts, observations,
and reviewed-note counts.

The internet collector is also allowed to find videos, podcasts/audio, and
images/graphics as candidate leads for divine-pattern evaluation. These media
sources route into visual art, human stories, cultural inputs, theologians, and
pressure tests where appropriate. They remain `none_until_caption_transcript_or_human_review`
until a caption, transcript, direct image/video/audio observation, source
context, rights status, and counter-reading are recorded.

This is intentionally not a GAN/VAE backend. The project needs disciplined
reading, viewing, listening, and review more than synthetic pattern generation.
A future MLLM service can use these artifacts by retrieving source notes first,
inspecting queued media when needed, walking the graph to related claims and
pressure tests, then checking review-rule gaps before drafting or strengthening
a claim.

The combined report article merges the major generated reports into one readable
GitHub Markdown document and one HTML document:

```powershell
python build_combined_report_article.py
```

Read `reports/published/final_book_report.md` directly on GitHub. It is the
published synthesis. The other report files are build inputs and audit trails,
not the preferred reading experience.

## Cloud Reference Collection

```powershell
python internet_source_collector.py
python divine_pattern_analyzer.py
```

The collector stores metadata and summaries only. It does not copy full
copyrighted books, articles, or lyrics.

The collector also writes a daily candidate evaluation queue:

```text
research_documents/daily_evaluation_queue.md
```

This queue is intentionally cautious. It helps the analyzer see new material
from the internet, but all entries remain candidate leads until original-source
review, author/context checks, and counterarguments are added.

Daily candidates are also routed to likely review layers such as theologians,
visual art, history, world languages, biblical languages, all texts,
psychology, other religious texts, modern literature, human stories, deep
sources, and pressure tests. These routes are triage hints, not evidence
approval.

Media candidates are routed the same way. A podcast episode, video lecture,
documentary, interview, image archive, icon, painting, photograph, or museum
object may be queued for review, but the project must evaluate the actual media
before using it to strengthen a divine-pattern claim.

The analyzer also writes the next collector search plan:

```text
references/next_search_strategy.json
```

This file turns the report's own growth recommendations into priority lanes,
query modifiers, and suggested searches for the next daily run. The collector
reads it before searching, records the applied modifiers in
`references/daily_research_digest.json`, and uses it to pursue thinner lanes,
counter-readings, source packs, and pressure-test gaps instead of only repeating
the same broad query set.

The collector also assigns automated evidence labels:

```text
strong_scholarly_candidate
moderate_scholarly_candidate
weak_scholarly_candidate
do_not_strengthen_claim
```

These labels are based on scholarly metadata signals such as provider, DOI,
author/year metadata, source type, citation count when available, corroborating
routed sources, counterargument language, and overclaim risk. They estimate
evidence confidence; they do not declare absolute truth.

The collector can also auto-approve low-risk candidates for review routing with:

```text
AUTO_APPROVE_REVIEW_QUEUE
AUTO_APPROVE_MIN_SCORE
AUTO_APPROVE_OPEN_WEB
AUTO_APPROVE_WITH_WARNINGS
```

The GitHub workflow enables queue-only auto approval at score `7` and keeps
open-web or warning-bearing sources manual by default. Auto approval means
`auto_approved_for_review_queue`, not reviewed evidence; confidence remains
`none_until_human_review`.

### Broad Web Search

By default, the collector searches scholarly/indexed sources:

```text
Crossref
OpenAlex
Europe PMC
PubMed
Internet Archive
arXiv
```

OpenCitations is also used as a free/keyless DOI enrichment source. It does not
run broad keyword search; instead, it enriches DOI-based sources found by
Crossref, OpenAlex, Europe PMC, or PubMed with open citation/reference counts:

```text
ENABLE_OPENCITATIONS
OPENCITATIONS_ENRICHMENT_LIMIT
```

It can also search the broader web when repository secrets are configured.
The recommended limited-credit broader-web option is Tavily:

```text
TAVILY_API_KEY
TAVILY_DAILY_SEARCH_LIMIT
TAVILY_MAX_RESULTS
```

The default Tavily budget is `5` basic searches per UTC day, with `3` results
per search and no raw page content. Basic Tavily searches cost 1 credit each, so
this keeps the project around 5 credits per day. Usage is tracked in:

```text
references/tavily_usage.json
```

The five Tavily queries rotate across the research query set over time so one
topic does not consume the whole monthly allowance.

The fully-free broader-web software option is SearXNG:

```text
SEARXNG_BASE_URL
SEARXNG_BASE_URLS
```

`SEARXNG_BASE_URL` should point to a SearXNG instance with JSON results enabled,
for example a self-hosted instance. Public instances may disable JSON or rate
limit automation, so self-hosting is the most reliable free path. The collector
does not use a public SearXNG instance by default because those endpoints often
return `429 TOO MANY REQUESTS` during automated runs.

`SEARXNG_BASE_URLS` accepts a comma-separated list of SearXNG instances and
tries them in order. This lets the collector keep working when one public
instance returns rate limits:

```powershell
$env:SEARXNG_BASE_URLS="https://search.mdosch.de,https://your-searxng.example"
python internet_source_collector.py
```

To slow the collector down for free APIs, set:

```text
SEARCH_DELAY_SECONDS
SEARCH_REQUEST_TIMEOUT_SECONDS
ARXIV_REQUEST_TIMEOUT_SECONDS
```

Each provider can be toggled with `ENABLE_...` environment variables. For
example, this keeps the free scholarly/archive sources running but skips broad
SearXNG web search if public instances are rate-limiting:

```powershell
$env:ENABLE_SEARXNG="false"
python internet_source_collector.py
```

Paid or free-credit API options can also be configured:

```text
BING_SEARCH_API_KEY
BRAVE_SEARCH_API_KEY
```

Open-web results are stored as metadata and snippets only. They are scored more
cautiously than scholarly sources, and they need trusted-domain signals or
corroboration before they can strengthen a claim.

## GitHub

The GitHub Actions workflow is in:

```text
.github/workflows/daily-cloud-research.yml
```

It runs every day at 14:00 UTC, collects new reference metadata, updates the
daily evaluation queue, reruns the analyzer, rebuilds the AI knowledge backend,
opens a GitHub notification issue, and commits updated reports back to the
repository.

The workflow opts JavaScript-based GitHub Actions into Node.js 24 with:

```yaml
FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: "true"
```

This addresses GitHub's Node.js 20 deprecation warning for actions such as
`actions/checkout`, `actions/setup-python`, `actions/github-script`, and the
auto-commit action. The analyzer itself still uses Python 3.12.

## Project Areas

- `research_documents/`: theology, science, philosophy, and source notes
- `music_lyrics/`: lyric and genre motif analysis
- `music_notes/`: note, chord, interval, ratio, and tension analysis
- `cultural_inputs/`: art, politics, science, technology, economics, health, ecology, education, and community
- `visual_art/`: composition, symbol, beauty, image, gesture, and visual meaning notes
- `history_inputs/`: historical memory, conflict, era, power, reform, and repair notes
- `world_languages/`: translation, semantics, metaphor, grammar, and culture notes
- `biblical_languages/`: biblical Greek, Hebrew, Aramaic, lemma, syntax, and translation-range notes
- `all_texts/`: global sacred, philosophical, poetic, legal, oral, wisdom, ritual, and commentary text notes
- `psychology_inputs/`: perception, attachment, trauma, habit, identity, and transformation notes
- `other_religious_texts/`: comparative non-Christian sacred and wisdom-text notes
- `modern_literature/`: summarized literary comparison notes without copyrighted text copying
- `human_stories/`: privacy-preserving lived-experience and practical-witness notes
- `pattern_tests/`: counterexamples and pressure tests
- `deep_sources/`: stricter support for unresolved suffering and quantum/science claims
- `theologians/`: cross-era theologian sources and pattern-design material
- `references/`: collected source metadata
- `reports/`: generated findings

## Guardrails

- Treat patterns as research hypotheses, not proof.
- Preserve the distinction and unity of Father, Son, and Holy Spirit.
- Do not use quantum physics as vague proof of God.
- Do not treat mathematical order, symmetry, logic, infinity, or beauty as proof
  of divine self-disclosure; compare naturalistic, Platonist, formalist,
  constructivist, cognitive, cultural, and suffering-based alternatives.
- Do not rush unresolved suffering into easy resolution.
- Use source quality, counterarguments, and practical application checks.
- Treat language-family and text-tradition coverage as mapped, not universal,
  until source-specific notes and counter-readings are broad enough.
- Review routed cloud references before promoting them to strong evidence.
- Revise or weaken the pattern wherever pressure tests show it does not hold.

The current research roadmap is tracked in:

```text
research_documents/next_research_expansion_tracker.md
```

## Theologian Pattern Design

The project now includes a cross-era theologian lane in:

```text
theologians/
```

It groups theologian signals by era and concepts such as Trinity, creation,
Christology, Spirit, suffering, grace, church, and justice. The report is:

```text
reports/theologian_pattern_design_report.txt
```

The goal is not to flatten theologians into one voice. It is to use continuity,
development, and disagreement across eras to make pattern design more careful.

## Cross-Layer Reasoning

The analyzer now writes a dedicated synthesis report:

```text
reports/cross_layer_reasoning_report.txt
```

This report asks whether the app is seeing deeper context and movement across
visual symbol, history, language, original-language study, psychology, ethics,
practice, theology, and counter-readings. Word matches remain starting signals,
but stronger synthesis needs multiple lenses, meaning movement, and layer
convergence.

The report also tracks language-family and text-tradition coverage. This lets
the project explore all world languages over time without claiming universality
too early. Add translated notes, original-language observations, genre/context
notes, and counter-readings to `world_languages/` or `all_texts/`.

Comparative validation now also uses `other_religious_texts/`,
`modern_literature/`, and `human_stories/`. Recurrence across these lanes can
support a broad human pattern, but it does not by itself prove a distinct
Trinitarian claim.
