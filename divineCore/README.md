# Divine Core

Divine Core is a modular reasoning foundation. It stores structured theology, ecclesial wisdom, and source-profile data for later review and use by application-specific composers.

## Daily Expansion Drafts

The daily expansion workflow creates draft profiles only. It runs `createDailySourceDraft.js`, selects the next undrafted source from `sourceExpansionQueue.json`, and writes one safe structured draft under `divineCore/drafts/`.

Drafts are not active source profiles. They require human review before moving into active folders such as `theologians`, `confessions`, `liturgy`, or future source collections.

The draft process uses empty arrays and concise review prompts. It must not include quotations, copyrighted text, or final user-facing prose.

This protects:

- theology quality by requiring human review
- JSON quality through validation before pull request creation
- app stability by keeping drafts isolated from application behavior
- composer safety by keeping Divine Core as reasoning data, not final prose

## Versioned Source Profiles

Versioned source profiles use `schemaVersion: "1.0"` and
`profileType: "source-profile"`. Their contract is defined by
`schemas/source-profile.schema.json` and separates five reasoning layers:

1. `sourceObservations` records what a source appears to argue, emphasize,
   assume, or repeatedly present. An observation is not a Divine Core
   conclusion.
2. `interpretiveSynthesis` cautiously relates observations while retaining
   ambiguities, alternate readings, and counterevidence.
3. `divineCoreAssessment` records provisional and revisable theological
   reasoning under the Divine Core Constitution.
4. `scripturalDoctrinalEvaluation` tests the profile through Scripture,
   canonical context, and accountable Christian doctrine.
5. `provenanceAndReview` records the reviewed scope, bibliographic details when
   known, evidence locations, and independent human-review metadata.

Scripture is the governing written authority. Patristic and other theological
sources are subordinate witnesses. Neither a maturity label nor human review
makes a source doctrinally authoritative or determines theological confidence.

## Profile Maturity

`profileMaturity` describes the content that is actually present:

- `scaffold`: generated structure with little or no substantive evidence. It
  may be inspected but contributes no affirmative theological confidence.
- `developing`: contains some substantive content but remains incomplete. It
  may suggest questions or explicitly tentative relationships.
- `evidence-ready`: contains source observations, provenance, interpretive
  distinctions, and scriptural or doctrinal evaluation sufficient for a
  qualified Divine Core assessment.
- `evaluated`: contains a recorded Divine Core assessment with contributions,
  cautions, and unresolved tensions. The assessment remains revisable and
  subordinate to Scripture.

The stored maturity is checked against a separately derived maturity. A stored
value above the derived value fails validation. A lower stored value passes
with a conservative-state warning. Human review never enters the maturity
calculation and never authorizes or prevents Divine Core reasoning.

Reasoning language must follow the evidence rather than the label. Scaffolds
identify research needs, developing profiles support tentative questions,
evidence-ready profiles support qualified assessment, and evaluated profiles
provide revisable reasoning inputs. Confidence arises from evidence quality,
Scriptural faithfulness, doctrinal coherence, provenance, counterevidence, and
unresolved tensions.

## Human Review

`provenanceAndReview.humanReview` records `not-reviewed`, `reviewed`, or
`reviewed-with-concerns`, together with reviewers, comments, and a review time.
This is visible stewardship and correction metadata only. It does not control
reasoning eligibility, maturity, confidence, doctrinal status, publication, or
ecclesial approval. A profile may be evaluated and not reviewed; a reviewed
scaffold remains a scaffold.

Run structural and semantic validation with:

```powershell
node divineCore/validateSourceProfiles.js
node divineCore/testSourceProfiles.js
```

The legacy `status`, `reasoningMethod`, `patternRecognition`, `composerHints`,
and `reviewNotes` fields remain temporarily for compatibility. The transitional
`status: "draft"` field does not control maturity or reasoning behavior.
