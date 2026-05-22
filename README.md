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

## Run

```powershell
python divine_pattern_analyzer.py
```

Main reports are written to `reports/`.

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

### Broad Web Search

By default, the collector searches scholarly/indexed sources:

```text
Crossref
OpenAlex
arXiv
```

It can also search the broader web when repository secrets are configured.
The fully-free option is SearXNG:

```text
SEARXNG_BASE_URL
```

`SEARXNG_BASE_URL` should point to a SearXNG instance with JSON results enabled,
for example a self-hosted instance. Public instances may disable JSON or rate
limit automation, so self-hosting is the most reliable free path.

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
daily evaluation queue, reruns the analyzer, opens a GitHub notification issue,
and commits updated reports back to the repository.

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
- Do not rush unresolved suffering into easy resolution.
- Use source quality, counterarguments, and practical application checks.

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
