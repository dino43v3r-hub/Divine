# External Review Protocol

Type: peer review and advisory protocol
Source status: proposed review lane

This protocol defines how outside reviewers should pressure-test the Divine
Pattern Project. The goal is not approval theater. The goal is to find
overclaims, missing sources, unfair comparisons, and harm risks before the
project speaks too confidently.

## Reviewer Roles

### Biblical Scholar

Primary questions:

- Does the claim respect original context, genre, canon, and translation?
- Are Scripture anchors direct, inferred, analogical, or disputed?
- Are Jewish and historical-critical counter-readings visible where needed?

### Theologian Or Historical Theologian

Primary questions:

- Does the claim preserve orthodox boundaries around Trinity, incarnation,
  creation, sin, grace, resurrection, and new creation?
- Are Christian disagreements represented fairly?
- Does the claim confuse doctrine with a symbolic pattern?

### Scientist Or Philosopher Of Science

Primary questions:

- Does the project use science inside the source's actual domain?
- Are probability, causality, quantum theory, neuroscience, and AI claims kept
  narrow?
- Is analogy being mistaken for proof?

### Comparative Religion Scholar Or Cultural Expert

Primary questions:

- Is each tradition being read on its own terms before Christian comparison?
- Are internal counter-readings included?
- Does the project avoid treating other traditions as props for Christian
  claims?

### Pastoral Care, Trauma, Or Ethics Reviewer

Primary questions:

- Could this claim be used to excuse harm, control, denial, or passivity?
- Does it protect victims and vulnerable people?
- Does it preserve lament and justice where repair is incomplete?

## Review Packet

Each reviewer should receive:

- `reports/published/final_book_report.md`,
- `research_documents/claim_ledger.md`,
- `research_documents/research_governance_workflow.md`,
- `research_documents/weakened_claims_register.md`,
- `research_documents/does_not_prove_boundaries.json`,
- the source pack or lane file relevant to their review role.

## Reviewer Output Template

```text
Reviewer role:
Reviewed claim or source lane:
Date:

Strongest supported claim:
Most serious overclaim:
Missing primary source:
Missing counter-reading:
Analogy/proof confusion:
Failure condition not faced:
Pastoral or ethical harm risk:
Recommended confidence change:
Required revision before publication:
```

## Decision Rules

If a reviewer identifies an unresolved overclaim, the relevant claim should move
down one confidence tier until revised.

If a reviewer identifies possible pastoral harm, the claim should be marked
`do_not_strengthen_claim` until the ethical harm audit is updated.

If reviewers disagree, preserve the disagreement in the report. Do not average
the disagreement into a cleaner conclusion.

## Publication Rule

Public-facing reports should include a short external-review status:

- not yet externally reviewed,
- reviewed with revisions required,
- reviewed with major unresolved objections,
- reviewed and ready for cautious use.

No external review status should imply theological certainty.
