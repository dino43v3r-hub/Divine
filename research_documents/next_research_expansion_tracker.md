# Next Research Expansion Tracker

Type: research roadmap
Source status: human-maintained tracker

This tracker turns the recurring next-action list into concrete status checks.
The project has first-pass coverage for each item, but several lanes still need
deeper primary sources, actual source review, and counter-readings before the
pattern can be treated as strong.

## 1. Theologian Source Material Across Eras

Status: second-pass expanded, needs primary-text checking.

Current coverage:

- Patristic, medieval, Reformation, modern, and contemporary theologian lanes
  exist in `theologians/`.
- `theologians/cross_era_primary_source_expansion.md` adds named source works
  and interpretive cautions.
- `theologians/source_specific_theologian_review_notes.md` adds source-specific
  review notes for Irenaeus, Athanasius, Basil, Augustine, Aquinas, Luther,
  Calvin, Barth, Bonhoeffer, Moltmann, Cone, Coakley, and Jennings.

Next depth work:

- Check the source-specific notes against primary texts and page/section
  references.
- Track agreement, disagreement, and pressure points rather than flattening them
  into one voice.

## 2. Cross-Layer Synthesis Notes

Status: second-pass expanded across all requested lanes.

Current coverage:

- Visual art: `visual_art/composition_symbol_pressure_notes.md`
- History: `history_inputs/empire_reform_memory_pressure_notes.md`
- World languages: `world_languages/language_family_expansion_notes.md`
- Biblical Greek/Hebrew: `biblical_languages/greek_hebrew_source_expansion_notes.md`
- All texts: `all_texts/text_tradition_expansion_notes.md`
- Psychology: `psychology_inputs/trauma_attachment_repair_notes.md`
- Added case-study and limits notes in visual art, history, world languages,
  biblical languages, all texts, and psychology.

Next depth work:

- Replace framework notes with source-specific examples and counter-readings.
- Keep separating actual source evidence from broad category maps.

## 3. Language-Family And Text-Tradition Coverage

Status: mapped and sampled, not universal.

Current coverage:

- Reports now map 16 language families and 12 text traditions.
- The summary explicitly says mapped coverage is a research agenda, not proof of
  universality.
- `world_languages/source_specific_language_sampling_notes.md` and
  `all_texts/comparative_text_case_notes.md` define the next sampling method.

Next depth work:

- Add actual translated source notes across families and traditions.
- Include translator choices, genre, colonial context, oral tradition context,
  and rival interpretation.

## 4. Harder Unresolved-Suffering Case Studies

Status: expanded again.

Current coverage:

- Added war-survivor, dementia, and generational-poverty pressure tests.
- Added moral-injury and ecological-loss pressure tests.
- Existing tests cover child loss, chronic illness, spiritual abuse, injustice,
  unanswered prayer, and no-resolution suffering.

Next depth work:

- Add case studies where no visible repair occurs.
- Include pastoral, clinical, social, economic, and justice-centered readings.

## 5. Qualified Quantum/Science References And Counterarguments

Status: source-review map and counterargument matrix added, still needs deeper citation review.

Current coverage:

- `deep_sources/qualified_science_reference_review_notes.md` names qualified
  physics, quantum, philosophy-of-science, and counterargument sources.
- `deep_sources/science_counterargument_matrix.md` defines allowed conclusions
  and counterarguments for order, mathematics, quantum theory, fine-tuning, and
  consciousness.
- Reports mark science claims as source-supported but still not proof.

Next depth work:

- Add source-specific notes for each named work.
- Track what each source actually supports and what it explicitly does not
  support.

## 6. Daily Cloud Reference Review

Status: checklist added, routed daily triage active, automated evidence scoring active, first review log started.

Current coverage:

- `research_documents/cloud_reference_review_checklist.md` defines review
  labels and required checks.
- Daily candidates remain candidate leads until reviewed.
- `internet_source_collector.py` now adds `layer_routes`, `primary_layer`, and
  layer-specific review prompts to each candidate so new material is triaged
  toward theologians, visual art, history, world languages, biblical languages,
  all texts, psychology, other religious texts, modern literature, human
  stories, deep sources, pressure tests, and cultural lanes.
- `internet_source_collector.py` now assigns machine evidence labels from
  scholarly metadata, DOI/stable identifiers, author/year metadata, source
  type, citation count when available, routed corroboration, counterargument
  language, and overclaim risk.
- Broad web search is supported through optional `SEARXNG_BASE_URL`,
  `BING_SEARCH_API_KEY`, and `BRAVE_SEARCH_API_KEY` secrets. SearXNG is the
  preferred free path when a reliable instance with JSON enabled is available.
  Open-web results are scored more cautiously than scholarly/indexed sources and
  require trusted-domain signals or corroboration before strengthening claims.
- `research_documents/daily_cloud_reference_review_log.md` starts reviewing
  routed queue items with cautious labels.

Next depth work:

- Review the newest queue entries one by one.
- Let automated labels shape confidence, but do not treat them as absolute
  truth. Promote only claim-scoped conclusions that have strong scholarly
  support, corroboration, and no unresolved overclaim warning.
- Convert high-quality routed candidates into source-specific notes in the
  appropriate layer folder.

## 7. Refine Only Where The Pattern Survives Pressure

Status: active method.

Current coverage:

- Pressure-test reports now distinguish confidence from hold-under-friction.
- Comparative validation distinguishes shared human recurrence from distinct
  Trinitarian claims.

Next depth work:

- Treat failures and underdeveloped hold assessments as revision points.
- Keep adding rival explanations, misuse cases, unresolved suffering, and
  non-Christian comparisons before strengthening claims.
