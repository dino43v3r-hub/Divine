# Synthesize Data

Synthesize Data is a divine-pattern research prototype. It analyzes theology,
music lyrics, music notes, art, politics, science, technology, culture,
practical theology, pressure tests, and source metadata.

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

## GitHub

The GitHub Actions workflow is in:

```text
.github/workflows/weekly-cloud-research.yml
```

It collects new reference metadata, reruns the analyzer, and commits updated
reports back to the repository.

## Project Areas

- `research_documents/`: theology, science, philosophy, and source notes
- `music_lyrics/`: lyric and genre motif analysis
- `music_notes/`: note, chord, interval, ratio, and tension analysis
- `cultural_inputs/`: art, politics, science, technology, economics, health, ecology, education, and community
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
