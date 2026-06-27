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
