# Evidence Testing Queue

_Generated: 2026-06-25 16:18 UTC_

This is the project's source-by-source testing backlog. It explains which sources still need research evidence testing before they can strengthen a claim, and which reviewed sources still need public-use testing before they can become final public evidence.

The goal is not to hide the gap. The goal is to make every promotion traceable: candidate source -> evidence testing queue -> source-specific review -> reviewed_evidence_ready -> public-use testing -> public_final_ready.

## Testing Gates

- `research_evidence_test`: checks evidence, interpretation, discernment, analogy, practical use, counter-reading, failure condition, pastoral safety, ecclesial review, liturgical grounding, promotion restraint, and machine-label boundary.
- `public_final_evidence_test`: checks Scripture anchor, doctrinal fit, pastoral harm clearance, abuse-language risk, science overclaim, comparative flattening, does-not-prove boundary, plain-language public summary, and final promotion restraint.
- Machine-drafted fields may organize this testing, but they do not raise confidence until the original source has been checked directly.

## Why Sources Are Queued

- Many files are candidate notes or imported source leads, not full source reviews.
- Many files contain useful summaries but do not use explicit labels like `Interpretation:` or `Failure condition:`.
- Auto-imported cloud candidates are intentionally cautious: they can route attention, but they should not strengthen claims by themselves.
- The audit only counts controls it can see clearly.

## How To Test A Source

For each queued source, read the original source or source note, then add a structured review companion with the relevant missing fields.

Research evidence test fields:

- Evidence
- Interpretation
- Discernment
- Analogy
- Practical use
- Counter-reading
- Failure condition
- Pastoral safety
- Ecclesial review
- Liturgical grounding
- Promotion restraint
- Machine-label boundary

Public-final evidence test fields:

- Scripture anchor
- Doctrinal fit
- No unresolved pastoral harm
- No abuse-enabling language
- No science overclaim
- No comparative flattening
- Does-not-prove boundary
- Plain-language public summary
- Final promotion restraint

Passing the research test can move a source toward `reviewed_evidence_ready`. Passing both the research test and the public-final test can move a source toward `public_final_ready`.

## Missing Test Counts In This Queue

- pastoral_safety: 573
- ecclesial_review: 574
- liturgical_grounding: 572
- promotion_restraint: 573
- interpretation: 0
- analogy: 0
- failure_condition: 0
- discernment: 0
- machine_label_boundary: 170
- evidence: 101
- counter_reading: 43
- practical_use: 33

Public-final test gaps:

- scripture_anchor: 1026
- doctrinal_fit: 1028
- no_unresolved_pastoral_harm: 1029
- no_abuse_enabling_language: 1029
- no_science_overclaim: 982
- no_comparative_flattening: 1023
- does_not_prove_boundary: 1013
- plain_language_public_summary: 1028
- final_promotion_restraint: 1029

## Companion Coverage Already Created

- pastoral_safety: 3 reviewed companion; 407 machine-drafted; 572 still missing
- ecclesial_review: 2 reviewed companion; 449 machine-drafted; 572 still missing
- liturgical_grounding: 2 reviewed companion; 429 machine-drafted; 570 still missing
- promotion_restraint: 2 reviewed companion; 441 machine-drafted; 571 still missing
- interpretation: 993 reviewed companion; 2 machine-drafted; 0 still missing
- analogy: 976 reviewed companion; 0 machine-drafted; 0 still missing
- failure_condition: 932 reviewed companion; 1 machine-drafted; 0 still missing
- discernment: 598 reviewed companion; 0 machine-drafted; 0 still missing
- machine_label_boundary: 0 reviewed companion; 2 machine-drafted; 170 still missing
- evidence: 0 reviewed companion; 2 machine-drafted; 101 still missing
- counter_reading: 0 reviewed companion; 1 machine-drafted; 43 still missing
- practical_use: 0 reviewed companion; 0 machine-drafted; 33 still missing
- scripture_anchor: 1 reviewed companion; 0 machine-drafted; 1,026 still missing
- doctrinal_fit: 1 reviewed companion; 0 machine-drafted; 1,028 still missing
- no_unresolved_pastoral_harm: 1 reviewed companion; 0 machine-drafted; 1,029 still missing
- no_abuse_enabling_language: 1 reviewed companion; 0 machine-drafted; 1,029 still missing
- no_science_overclaim: 1 reviewed companion; 0 machine-drafted; 982 still missing
- no_comparative_flattening: 1 reviewed companion; 0 machine-drafted; 1,023 still missing
- does_not_prove_boundary: 1 reviewed companion; 0 machine-drafted; 1,013 still missing
- plain_language_public_summary: 1 reviewed companion; 0 machine-drafted; 1,028 still missing
- final_promotion_restraint: 1 reviewed companion; 0 machine-drafted; 1,029 still missing

## Machine-Drafted Source-Check Queue

- Items requiring source-check before trust: 451
- Rule: machine-drafted fields organize work only; they do not raise confidence until the original source has been checked directly.

### M1. Global Text Exploration Framework

- Path: `all_texts/global_text_exploration_framework.md`
- Lane: all_texts
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M2. Text-Tradition Counter-Reading Map

- Path: `all_texts/text_tradition_counterreading_map.md`
- Lane: all_texts
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M3. Text Tradition Expansion Notes

- Path: `all_texts/text_tradition_expansion_notes.md`
- Lane: all_texts
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M4. Expanded Lexeme Balance Notes

- Path: `biblical_languages/expanded_lexeme_balance_notes.md`
- Lane: biblical_languages
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M5. Biblical Greek And Hebrew: Depth Checks

- Path: `biblical_languages/greek_hebrew_depth_checks.md`
- Lane: biblical_languages
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M6. Greek Hebrew Source Expansion Notes

- Path: `biblical_languages/greek_hebrew_source_expansion_notes.md`
- Lane: biblical_languages
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M7. Source-Specific Biblical-Language Counter-Readings

- Path: `biblical_languages/source_specific_counterreadings.md`
- Lane: biblical_languages
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M8. Source-Specific Lexeme Review Notes

- Path: `biblical_languages/source_specific_lexeme_review_notes.md`
- Lane: biblical_languages
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M9. Art Beauty Symbol

- Path: `cultural_inputs/art_beauty_symbol.md`
- Lane: cultural_inputs
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M10. Cultural Practice Balance Notes

- Path: `cultural_inputs/cultural_practice_balance_notes.md`
- Lane: cultural_inputs
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M11. Ecology Creation Care

- Path: `cultural_inputs/ecology_creation_care.md`
- Lane: cultural_inputs
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M12. Economics Work Dignity

- Path: `cultural_inputs/economics_work_dignity.md`
- Lane: cultural_inputs
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M13. Education Formation Wisdom

- Path: `cultural_inputs/education_formation_wisdom.md`
- Lane: cultural_inputs
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M14. Family Community Belonging

- Path: `cultural_inputs/family_community_belonging.md`
- Lane: cultural_inputs
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M15. Health Suffering Healing

- Path: `cultural_inputs/health_suffering_healing.md`
- Lane: cultural_inputs
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M16. Politics Justice Repair

- Path: `cultural_inputs/politics_justice_repair.md`
- Lane: cultural_inputs
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M17. Science Order Humility

- Path: `cultural_inputs/science_order_humility.md`
- Lane: cultural_inputs
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M18. Technology Ai Responsibility

- Path: `cultural_inputs/technology_ai_responsibility.md`
- Lane: cultural_inputs
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M19. Math And Physics Theorem Inventory For Pattern Testing

- Path: `deep_sources/math_physics_theorem_inventory.md`
- Lane: deep_sources
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M20. Math, Statistics, And Logic Congruence Filters

- Path: `deep_sources/math_statistics_logic_congruence_filters.md`
- Lane: deep_sources
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M21. Qualified Science Reference Review Notes

- Path: `deep_sources/qualified_science_reference_review_notes.md`
- Lane: deep_sources
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M22. Quantum And Science Claim-Limit Source Pairs

- Path: `deep_sources/quantum_claim_limits_source_pairs.md`
- Lane: deep_sources
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M23. Quantum Science Source Framework

- Path: `deep_sources/quantum_science_source_framework.md`
- Lane: deep_sources
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M24. Unresolved Suffering Source Framework

- Path: `deep_sources/unresolved_suffering_source_framework.md`
- Lane: deep_sources
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.

### M25. Case Study History Pressure Notes

- Path: `history_inputs/case_study_history_pressure_notes.md`
- Lane: history_inputs
- Current tier: candidate_lead
- Patterns: none detected
- Machine-drafted rules: ecclesial_review, liturgical_grounding, pastoral_safety, promotion_restraint
- Source-check prompt: Read the original source or primary artifact directly, replace any generic machine-drafted fields with source-specific notes, and only then mark whether the companion can inform confidence.


## Highest Priority Sources

### 1. Book Review: A More Profound Alleluia: Theology and Worship in Harmony

- Path: `research_documents/auto_imported_cloud_candidates/book_review_a_more_profound_alleluia_theology_and_worship_in_harmony_ee1c835b96b7.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 2. Book Review: A Study in Methodology

- Path: `research_documents/auto_imported_cloud_candidates/book_review_a_study_in_methodology_e88ec6efdfaf.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 3. Book Review: An Essay on Theological Method

- Path: `research_documents/auto_imported_cloud_candidates/book_review_an_essay_on_theological_method_ff441bcf058d.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 4. Book Review: Comparative Religion . An Introductory and Historical Survey

- Path: `research_documents/auto_imported_cloud_candidates/book_review_comparative_religion_an_introductory_and_historical_survey_e156e2b49cb8.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 5. Book Review: ‘Going Forth’

- Path: `research_documents/auto_imported_cloud_candidates/book_review_going_forth_d9656294612c.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 6. Book Review: Hymns in Christian Worship

- Path: `research_documents/auto_imported_cloud_candidates/book_review_hymns_in_christian_worship_65976d57e64f.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 7. Book Review: Let God be God

- Path: `research_documents/auto_imported_cloud_candidates/book_review_let_god_be_god_b99d94a38385.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 8. Book Review: Liturgy of the Ordinary: Sacred Practices in Everyday Life

- Path: `research_documents/auto_imported_cloud_candidates/book_review_liturgy_of_the_ordinary_sacred_practices_in_everyday_life_661657c6dee3.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 9. Book Review: The God of Love and Human Dignity: Essays in honour of George M. Newlands

- Path: `research_documents/auto_imported_cloud_candidates/book_review_the_god_of_love_and_human_dignity_essays_in_honour_of_george_m_newla_fb256b700a32.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 10. Book Review: The Identity of Anglican Worship

- Path: `research_documents/auto_imported_cloud_candidates/book_review_the_identity_of_anglican_worship_a2f57d80c584.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 11. Book Review: The Torah's Vision of Worship

- Path: `research_documents/auto_imported_cloud_candidates/book_review_the_torah_s_vision_of_worship_d562a8a235f8.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 12. Book Review: To Relieve the Human Condition: Bioethics, Technology, and the Body

- Path: `research_documents/auto_imported_cloud_candidates/book_review_to_relieve_the_human_condition_bioethics_technology_and_the_body_984c2d03d738.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 13. Book Review: Visual Faith

- Path: `research_documents/auto_imported_cloud_candidates/book_review_visual_faith_01090f22266f.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 14. Book Review: Worship

- Path: `research_documents/auto_imported_cloud_candidates/book_review_worship_028544e6278f.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 15. Chance, Divine Action, and the Natural Order of Things

- Path: `research_documents/auto_imported_cloud_candidates/chance_divine_action_and_the_natural_order_of_things_310bffe1b9c3.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 16. Church Unity and Social Contexts: The Ecumenical Debate on Ecclesiology and Ethics

- Path: `research_documents/auto_imported_cloud_candidates/church_unity_and_social_contexts_the_ecumenical_debate_on_ecclesiology_and_ethic_1f58a5ac9f62.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 17. Comparative Theology after Religion?

- Path: `research_documents/auto_imported_cloud_candidates/comparative_theology_after_religion_d8cbba3fe76f.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 18. Comparative Theology and Interreligious Dialogue

- Path: `research_documents/auto_imported_cloud_candidates/comparative_theology_and_interreligious_dialogue_62f8629a337d.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 19. CONCLUSION

- Path: `research_documents/auto_imported_cloud_candidates/conclusion_cce9a6cdef65.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 20. Consciousness and agency in Plotinus

- Path: `research_documents/auto_imported_cloud_candidates/consciousness_and_agency_in_plotinus_7534cf22283f.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 21. Contingency and Providence: Aristotle and Augustine

- Path: `research_documents/auto_imported_cloud_candidates/contingency_and_providence_aristotle_and_augustine_bedaec80430e.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 22. Deaf in the Image of the Deaf God

- Path: `research_documents/auto_imported_cloud_candidates/deaf_in_the_image_of_the_deaf_god_425c4fd721f3.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 23. Decolonising epistemology within a (southern) African context: Teaching and learning towards transformation at Stellenbosch University

- Path: `research_documents/auto_imported_cloud_candidates/decolonising_epistemology_within_a_southern_african_context_teaching_and_learnin_cff558f3b889.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 24. Diaries

- Path: `research_documents/auto_imported_cloud_candidates/diaries_605ef7d823e9.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 25. Disability as a Boundary Object

- Path: `research_documents/auto_imported_cloud_candidates/disability_as_a_boundary_object_37f5fbf79062.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 26. Discerning Providence: How the Reign of God in Liberation Theology Explicates Divine Struggle as a Feature of Providence

- Path: `research_documents/auto_imported_cloud_candidates/discerning_providence_how_the_reign_of_god_in_liberation_theology_explicates_div_aadf3f3571eb.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 27. Energy Ethics: a Literature Review

- Path: `research_documents/auto_imported_cloud_candidates/energy_ethics_a_literature_review_0fc320c1ce06.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 28. Enrique Dussel and Liberation Theology

- Path: `research_documents/auto_imported_cloud_candidates/enrique_dussel_and_liberation_theology_cd1bb05694a6.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 29. Environmental Care in Islam: A Quranic Perspective

- Path: `research_documents/auto_imported_cloud_candidates/environmental_care_in_islam_a_quranic_perspective_1f86e7fbefd3.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 30. Epistemic Injustice: Power and the Ethics of Knowing - Miranda Fricker

- Path: `research_documents/auto_imported_cloud_candidates/epistemic_injustice_power_and_the_ethics_of_knowing_miranda_fricker_db681ec337c1.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 31. Epistemology

- Path: `research_documents/auto_imported_cloud_candidates/epistemology_4698c4ff9497.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 32. Eternity

- Path: `research_documents/auto_imported_cloud_candidates/eternity_7884cf7f71ae.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 33. Falsification: On the Role of the Empirical in J. G. Fichte’s Transcendental Method

- Path: `research_documents/auto_imported_cloud_candidates/falsification_on_the_role_of_the_empirical_in_j_g_fichte_s_transcendental_method_c5fcb239b4ef.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 34. God Meets us in Our Suffering: Hope and Encouragement for Those Journeying Through Cancer

- Path: `research_documents/auto_imported_cloud_candidates/god_meets_us_in_our_suffering_hope_and_encouragement_for_those_journeying_throug_2e5667a72c64.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 35. God’s Suffering in the Hindu-Christian Gaze

- Path: `research_documents/auto_imported_cloud_candidates/god_s_suffering_in_the_hindu_christian_gaze_07e12cf7bd24.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 36. II. Popular Theology

- Path: `research_documents/auto_imported_cloud_candidates/ii_popular_theology_1696923f29e6.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 37. In Case of Spiritual Emergency

- Path: `research_documents/auto_imported_cloud_candidates/in_case_of_spiritual_emergency_492543555b16.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 38. Incarnational Speech

- Path: `research_documents/auto_imported_cloud_candidates/incarnational_speech_1949cfd9863d.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 39. Introduction

- Path: `research_documents/auto_imported_cloud_candidates/introduction_1a5716b94e03.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

### 40. Introduction: On Theological Hermeneutics and Theological Method

- Path: `research_documents/auto_imported_cloud_candidates/introduction_on_theological_hermeneutics_and_theological_method_c5b75fd47a3c.md`
- Lane: research_documents
- Current tier: developing_evidence
- Next gate: research_evidence_test
- Patterns: none detected
- Missing: pastoral_safety, ecclesial_review, liturgical_grounding, promotion_restraint, scripture_anchor, doctrinal_fit, no_unresolved_pastoral_harm, no_abuse_enabling_language, no_science_overclaim, no_comparative_flattening, does_not_prove_boundary, plain_language_public_summary, final_promotion_restraint

Fill prompts:
- pastoral_safety: Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?
- ecclesial_review: What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?
- liturgical_grounding: How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?
- promotion_restraint: Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?
- scripture_anchor: What Scripture text or biblical theme anchors, limits, or corrects this claim?
- doctrinal_fit: How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?
- no_unresolved_pastoral_harm: What pastoral harm risk has been checked, and what risk would still block public use?
- no_abuse_enabling_language: Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?
- no_science_overclaim: Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?
- no_comparative_flattening: If another tradition appears, has it been represented on its own terms before Christian comparison?
- does_not_prove_boundary: What does this evidence not prove, even if the pattern is interesting or useful?
- plain_language_public_summary: How can this be stated plainly for ordinary readers without inflating confidence?
- final_promotion_restraint: Why is this ready, or not ready, to shape a public-facing claim?

