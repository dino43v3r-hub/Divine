from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path


INDEX_PATH = Path("reports/knowledge_retrieval_index.json")
AUDIT_PATH = Path("reports/review_rules_audit.json")
DAILY_DIGEST_PATH = Path("references/daily_research_digest.json")
PRIESTLY_LAYER_PATH = Path("research_documents/priestly_discernment_layer.json")
OUTPUT_PATH = Path("reports/divine_pattern_findings.md")

TOP_PATTERN_NAMES = [
    "Image Of God Pattern",
    "Cross And Reversal Pattern",
    "Creation-To-Consciousness Pattern",
    "Trinity-As-Behavior Pattern",
    "Providence And Contingency Pattern",
]


PATTERN_PROFILES = {
    "Image Of God Pattern": {
        "movement": "Mind -> Symbol -> Moral Agency -> Relationship -> Worship",
        "plain": "Human beings appear as meaning-making, morally accountable, relational persons. Christianity reads this through the image of God.",
        "theologian_judgment": "Theologians should judge this pattern by whether it protects the image of God in weak, wounded, disabled, poor, unborn, elderly, imprisoned, displaced, and overlooked people.",
        "evaluate": "Does this pattern protect human dignity before usefulness, intelligence, status, health, tribe, or performance?",
        "weakens_if": "It collapses human worth into ability, intelligence, productivity, or social value.",
    },
    "Cross And Reversal Pattern": {
        "movement": "Power -> Humility | Violence -> Forgiveness | Suffering -> Redemption | Death -> Resurrection",
        "plain": "The corpus repeatedly notices reversal: power judged by humility, suffering faced through truth, and hope shaped by the cross and resurrection.",
        "theologian_judgment": "Theologians should judge this pattern by whether it keeps the cross centered on Christ without romanticizing pain or asking victims to carry injustice quietly.",
        "evaluate": "Does this pattern tell the truth about harm while still inviting mercy, justice, and hope?",
        "weakens_if": "It romanticizes suffering, protects abusers, or asks victims to accept harm without justice.",
    },
    "Creation-To-Consciousness Pattern": {
        "movement": "Physical Order -> Life -> Consciousness -> Moral Awareness -> Worship",
        "plain": "The project sees layered movement from order and life toward mind, responsibility, meaning, and worship.",
        "theologian_judgment": "Theologians should judge this pattern by whether it honors creation as gift without turning science, intelligence, or consciousness into a ladder of superiority.",
        "evaluate": "Does this pattern create wonder and responsibility without pretending science mechanically proves worship?",
        "weakens_if": "It becomes a simple ladder from physics to God or ignores evolution, disability, animal life, or suffering in nature.",
    },
    "Trinity-As-Behavior Pattern": {
        "movement": "Father Creates -> Son Redeems -> Spirit Transforms",
        "plain": "The project sees Christian doctrine becoming practical: receive life as gift, follow Christ's redemption, and test transformation by the Spirit's fruit.",
        "theologian_judgment": "Theologians should judge this pattern by whether Father, Son, and Spirit remain distinct and united while the practical fruit stays accountable to Scripture, creed, and worship.",
        "evaluate": "Does this pattern preserve Father, Son, and Spirit while producing love, humility, holiness, unity, and service?",
        "weakens_if": "It turns the Trinity into vague symbolism, group emotion, authoritarian control, modalism, or tritheism.",
    },
    "Providence And Contingency Pattern": {
        "movement": "Stable Law -> Contingent Events -> Emergent Complexity -> Meaningful History",
        "plain": "The project sees order and contingency together: a world with stable patterns, real uncertainty, historical meaning, and possible providence.",
        "theologian_judgment": "Theologians should judge this pattern by whether it teaches trust, prayer, repentance, courage, and service while leaving room for grief, chance, mystery, and unfinished history.",
        "evaluate": "Does this pattern help a person act faithfully inside uncertainty without claiming to know every hidden cause?",
        "weakens_if": "It explains tragedy too neatly, blames victims, denies chance, or uses science language beyond its scope.",
    },
    "Holy Spirit Gifts Pattern": {
        "movement": "Presence -> Gift -> Service -> Fruit -> Communal Upbuilding",
        "plain": "The project notices gifts as possible Spirit-enabled service, truth, healing, wisdom, courage, and upbuilding.",
        "theologian_judgment": "Theologians should judge this pattern by whether gifts point to Christlike service, communal upbuilding, accountability, and fruit over time.",
        "evaluate": "Does this pattern produce truthful love, humility, accountability, justice, and fruit over time?",
        "weakens_if": "It treats spectacle, charisma, or intensity as proof of the Spirit.",
    },
    "Other Religious Comparative Witness": {
        "movement": "Longing -> Practice -> Wisdom -> Difference -> Humble Comparison",
        "plain": "The project sees resonances across traditions while keeping their real differences visible.",
        "theologian_judgment": "Theologians should judge this comparison by whether it honors other traditions honestly before making any Christian interpretation.",
        "evaluate": "Does this comparison honor the other tradition on its own terms before Christian interpretation?",
        "weakens_if": "It flattens other religions into hidden Christianity or uses them as props.",
    },
    "Science Analogy Guardrail": {
        "movement": "Observation -> Model -> Limit -> Humility -> Better Reasoning",
        "plain": "The project uses science as a guardrail for humility, precision, probability, causality, and model limits.",
        "theologian_judgment": "Theologians should judge this guardrail by whether it makes claims more careful without forcing science to do theology's work.",
        "evaluate": "Does this analogy make the claim more careful without pretending science proves theology?",
        "weakens_if": "It uses quantum, neuroscience, or complexity language as proof of God, prayer, consciousness, or miracles.",
    },
    "Mathematical Theophany Pattern": {
        "movement": "Order -> Symmetry -> Logic -> Beauty -> Wonder",
        "plain": "The project sees mathematical order and beauty as possible signs that can invite wonder and disciplined reasoning.",
        "theologian_judgment": "Theologians should judge this pattern by whether wonder remains humble and disciplined rather than becoming a shortcut proof.",
        "evaluate": "Does this pattern remain a humble sign-reading rather than a mathematical proof of God?",
        "weakens_if": "It ignores Platonist, formalist, constructivist, cognitive, cultural, or naturalistic explanations.",
    },
}

DAILY_PATTERN_EXTENSIONS = {
    "Image Of God Pattern": {
        "case_study": "A church praises usefulness and success while overlooking a disabled member, an elderly caregiver, or someone who cannot contribute visibly.",
        "theologian_panel": [
            "Irenaeus: Does this receive human life as made for communion with God?",
            "Aquinas: Is dignity grounded in God rather than usefulness?",
            "Bonhoeffer: Does this protect concrete neighbors instead of abstract humanity?",
            "Cone or Copeland: Does dignity language confront embodied and racialized harm?",
        ],
        "hard_objection": "Dignity language can be explained by social empathy, law, rights movements, and shared vulnerability without proving a divine pattern.",
        "confidence_language": "Pastorally useful with limits: strong for practice, still provisional as a pattern claim.",
        "faithful_response": "Honor one person before they are useful to you.",
        "interesting_not_true": "A recurring dignity signal is interesting, but it becomes responsible only when tested by Christ, Scripture, vulnerable people, and practice.",
    },
    "Cross And Reversal Pattern": {
        "case_study": "A harmed person is pressured to forgive quickly so others can feel peace, while truth, safety, and repair are still missing.",
        "theologian_panel": [
            "Augustine: Is peace being confused with avoidance?",
            "Luther: Is the cross exposing false power rather than baptizing it?",
            "Bonhoeffer: Has forgiveness become cheap grace without repentance?",
            "Cone or Williams: Does cross-language liberate the oppressed or ask them to endure more violence?",
        ],
        "hard_objection": "Christians have often used suffering language to silence victims, so careless versions of this pattern are spiritually dangerous.",
        "confidence_language": "Beautiful but risky: powerful with justice and protection, unsafe without them.",
        "faithful_response": "Tell the truth about harm without using mercy to erase justice.",
        "interesting_not_true": "Reversal is compelling, but beauty is not proof; the pattern must be judged by whether it follows Christ and protects the harmed.",
    },
    "Creation-To-Consciousness Pattern": {
        "case_study": "A student feels wonder studying life, consciousness, and the night sky, while also seeing animal suffering, ecological loss, disability, and death.",
        "theologian_panel": [
            "Athanasius: Is creation understood through the Word who gives and sustains life?",
            "Aquinas: Does natural order invite theology without replacing science?",
            "Polkinghorne: Is science respected before theological reflection begins?",
            "Disability theologians: Are consciousness and ability being used to rank persons?",
        ],
        "hard_objection": "Science, evolution, cognition, and culture can explain much of this movement without requiring a theological conclusion.",
        "confidence_language": "Promising but needs pressure: useful for wonder and stewardship, not mature as a proof claim.",
        "faithful_response": "Let wonder become care for a body, creature, or place.",
        "interesting_not_true": "Awe is interesting, but the pattern stays honest only when natural explanations and suffering remain visible.",
    },
    "Trinity-As-Behavior Pattern": {
        "case_study": "A church confesses orthodox doctrine while its common life is anxious, competitive, controlling, and unkind.",
        "theologian_panel": [
            "Gregory Nazianzen: Are Father, Son, and Spirit confessed without confusion or division?",
            "Augustine: Does doctrine train love rather than curiosity alone?",
            "Karl Barth: Does the pattern begin with God's self-revelation instead of human analogy?",
            "Zizioulas, Jennings, or Oduyoye: Does communion become concrete hospitality, justice, and belonging?",
        ],
        "hard_objection": "This can flatten the Trinity into behavior advice unless doctrine remains first and behavior is treated as fruit.",
        "confidence_language": "Developing evidence: fruitful as a practical test, risky if it becomes mere symbolism.",
        "faithful_response": "Test one belief by whether it produces humility, love, and service.",
        "interesting_not_true": "Practical fruit matters, but usefulness is not revelation; the pattern must remain accountable to Scripture, creed, and worship.",
    },
    "Providence And Contingency Pattern": {
        "case_study": "Someone loses a job, faces illness, or watches a plan collapse, and friends rush to explain what God must be doing.",
        "theologian_panel": [
            "Augustine: Does trust in providence become love of God rather than control?",
            "Calvin: Is God's care confessed with reverence instead of speculation?",
            "Karl Barth: Is providence read through Jesus Christ rather than bare events?",
            "Pastoral and trauma theologians: Is the claim safe for sufferers?",
        ],
        "hard_objection": "Psychology and history can explain many providence stories as ways humans survive uncertainty and impose meaning after the fact.",
        "confidence_language": "Pastorally useful with limits: strong as trust, weak as an explanation of hidden causes.",
        "faithful_response": "Act faithfully without explaining everything.",
        "interesting_not_true": "Meaning inside uncertainty is interesting, but the pattern should stop where grief, chance, and mystery require silence.",
    },
}

DEFAULT_DAILY_EXTENSION = {
    "case_study": "An ordinary person notices a recurring theme in life, faith, suffering, or culture.",
    "theologian_panel": [
        "A theologian should ask whether the pattern begins with Christ rather than recurrence.",
        "A pastoral reviewer should ask whether the pattern protects vulnerable people.",
    ],
    "hard_objection": "A rival explanation may account for the pattern without theology.",
    "confidence_language": "Promising but needs pressure: interesting enough to study, not strong enough to overclaim.",
    "faithful_response": "Let the pattern serve truth, love, humility, justice, and worship.",
    "interesting_not_true": "Interesting is not the same as true; the pattern remains secondary and provisional.",
}


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def confidence_phrase(tiers: Counter) -> str:
    if tiers.get("public_final_ready", 0):
        return "public final ready"
    if tiers.get("reviewed_evidence_ready", 0):
        return "ready for your evaluation"
    if tiers.get("developing_evidence", 0):
        return "developing evidence"
    return "candidate signal"


def make_pattern_rows(index: dict) -> list[dict]:
    rows = []
    documents = index.get("documents", [])
    for pattern, profile in PATTERN_PROFILES.items():
        matched = [doc for doc in documents if pattern in doc.get("patterns", [])]
        if not matched:
            continue
        tiers = Counter(doc.get("confidence_tier", "candidate_lead") for doc in matched)
        lanes = Counter(doc.get("lane", "unknown") for doc in matched)
        review_notes = sum(int(doc.get("review_note_count") or 0) for doc in matched)
        rows.append(
            {
                "pattern": pattern,
                "profile": profile,
                "documents": len(matched),
                "review_notes": review_notes,
                "tiers": tiers,
                "lanes": lanes,
                "examples": matched[:5],
                "status": confidence_phrase(tiers),
            }
        )
    rows.sort(
        key=lambda row: (
            row["tiers"].get("public_final_ready", 0),
            row["tiers"].get("reviewed_evidence_ready", 0),
            row["tiers"].get("developing_evidence", 0),
            row["documents"],
            row["review_notes"],
        ),
        reverse=True,
    )
    return rows


def format_counter(counter: Counter, limit: int = 4) -> str:
    if not counter:
        return "none recorded"
    return ", ".join(f"{name}: {count}" for name, count in counter.most_common(limit))


def format_counts(counts: dict, limit: int = 6) -> str:
    if not counts:
        return "none recorded"
    items = sorted(counts.items(), key=lambda item: (-int(item[1] or 0), item[0]))[:limit]
    return ", ".join(f"{name}: {int(count):,}" for name, count in items)


def daily_change_lines(digest: dict) -> list[str]:
    if not digest:
        return ["- No daily discovery digest was found."]

    lines = [
        f"- new candidate references: {int(digest.get('new_count', 0) or 0):,}",
        f"- new routed layers: {format_counts(digest.get('new_layer_counts', {}))}",
        f"- new provider mix: {format_counts(digest.get('new_provider_counts', {}))}",
        f"- new media candidates: {format_counts(digest.get('new_media_candidate_counts', {}))}",
        f"- new evidence labels: {format_counts(digest.get('new_automated_evidence_counts', {}))}",
    ]
    updated_at = digest.get("updated_at")
    if updated_at:
        lines.append(f"- latest collector update: {updated_at}")
    return lines


def newest_source_lines(digest: dict, limit: int = 5) -> list[str]:
    sources = digest.get("new_sources", []) if digest else []
    if not sources:
        return ["- No newest source titles were recorded in the latest digest."]

    lines = []
    for source in sources[:limit]:
        routes = ", ".join(source.get("layer_routes", [])) or "unrouted"
        label = source.get("automated_evidence_label", "unlabeled")
        year = source.get("year") or "n.d."
        provider = source.get("provider") or "unknown provider"
        lines.append(
            f"- {source.get('title', 'Untitled')} ({year}) | {provider} | {label} | routes: {routes}"
        )
    return lines


def daily_focus_row(rows: list[dict], generated_at: datetime) -> dict | None:
    if not rows:
        return None
    preferred_rows = [row for row in rows if row["pattern"] in TOP_PATTERN_NAMES]
    focus_pool = preferred_rows or rows
    return focus_pool[generated_at.date().toordinal() % len(focus_pool)]


def daily_extension(pattern: str) -> dict:
    extension = dict(DEFAULT_DAILY_EXTENSION)
    extension.update(DAILY_PATTERN_EXTENSIONS.get(pattern, {}))
    return extension


def build_report() -> str:
    generated_at = datetime.now(timezone.utc)
    generated = generated_at.strftime("%Y-%m-%d %H:%M UTC")
    index = read_json(INDEX_PATH)
    audit = read_json(AUDIT_PATH)
    digest = read_json(DAILY_DIGEST_PATH)
    priestly_layer = read_json(PRIESTLY_LAYER_PATH)
    rows = make_pattern_rows(index)
    focus_row = daily_focus_row(rows, generated_at)

    lines = [
        "# Divine Patterns Found",
        "",
        f"_Generated: {generated}_",
        "",
        "This report is intentionally simple: it shows the divine-pattern signals the system currently finds, explains why they surfaced, and leaves evaluation to you.",
        "",
        "The labels are not commands. They are reading aids:",
        "",
        "- `candidate signal`: interesting, but early.",
        "- `developing evidence`: enough structure to enter evidence testing.",
        "- `ready for your evaluation`: required research evidence-test controls are present, so the backend auto-promoted it to reviewed-evidence-ready.",
        "- `public final ready`: reviewed evidence plus public-final evidence-test boundaries are present, so the backend auto-promoted it for public-facing use.",
        "",
        "It is designed to change day to day when the collector, analyzer, and backend discover or re-index new material.",
        "",
        "Auto-promotion is staged: the evidence testing queue is the backlog; research evidence-test success becomes reviewed-evidence-ready; public-facing use requires the extra public-final evidence-test rules.",
        "",
    ]

    if priestly_layer:
        questions = priestly_layer.get("review_questions", [])[:4]
        restraints = priestly_layer.get("promotion_restraints", [])[:4]
        lines.extend(
            [
                "## Priestly Discernment Gate",
                "",
                priestly_layer.get(
                    "core_rule",
                    "Pattern claims must pass pastoral, ecclesial, sacramental, and spiritual-fruit review before public use.",
                ),
                "",
                "Before promoting any finding, ask:",
                "",
                *(f"- {question}" for question in questions),
                "",
                "Promotion restraints:",
                "",
                *(f"- {restraint}" for restraint in restraints),
                "",
            ]
        )

    if focus_row:
        profile = focus_row["profile"]
        extension = daily_extension(focus_row["pattern"])
        lines.extend(
            [
                "## Today's Pattern Focus",
                "",
                f"### {focus_row['pattern']}",
                "",
                f"**Status:** {focus_row['status']}",
                "",
                f"**Plain meaning:** {profile['plain']}",
                "",
                f"**Today case study:** {extension['case_study']}",
                "",
                "**Theologian panel:**",
                "",
                *(f"- {voice}" for voice in extension["theologian_panel"]),
                "",
                f"**Theologian judgment for ordinary readers:** {profile['theologian_judgment']}",
                "",
                f"**Hard objection:** {extension['hard_objection']}",
                "",
                f"**Common-person test:** {profile['evaluate']}",
                "",
                f"**Confidence in plain English:** {extension['confidence_language']}",
                "",
                f"**What would weaken it:** {profile['weakens_if']}",
                "",
                f"**Faithful response today:** {extension['faithful_response']}",
                "",
                f"**Why interesting is not the same as true:** {extension['interesting_not_true']}",
                "",
                f"**Why it surfaced:** {focus_row['documents']} indexed document(s), {focus_row['review_notes']} declared review note(s).",
                "",
            ]
        )

    lines.extend(
        [
            "## What Changed In The Latest Discovery Run",
            "",
            *daily_change_lines(digest),
            "",
            "Newest source leads:",
            "",
            *newest_source_lines(digest),
            "",
        ]
    )

    totals = audit.get("confidence_tier_totals", {})
    if totals:
        lines.extend(
            [
                "## Current Evidence Mix",
                "",
                f"- candidate leads: {int(totals.get('candidate_lead', 0)):,}",
                f"- developing evidence: {int(totals.get('developing_evidence', 0)):,}",
                f"- ready for your evaluation: {int(totals.get('reviewed_evidence_ready', 0)):,}",
                f"- public final ready: {int(totals.get('public_final_ready', 0)):,}",
                "",
            ]
        )

    lines.extend(["## Pattern Findings", ""])

    if not rows:
        lines.extend(
            [
                "No named divine-pattern signals were found in the current knowledge index.",
                "",
                "Run `python ai_knowledge_backend.py` first, then run this report again.",
                "",
            ]
        )
    for index_number, row in enumerate(rows, 1):
        profile = row["profile"]
        lines.extend(
            [
                f"### {index_number}. {row['pattern']}",
                "",
                f"**Status:** {row['status']}",
                "",
                f"**Pattern movement:** {profile['movement']}",
                "",
                f"**What the system sees:** {profile['plain']}",
                "",
                f"**Theologian judgment for ordinary readers:** {profile['theologian_judgment']}",
                "",
                f"**Why it surfaced:** {row['documents']} indexed document(s), {row['review_notes']} declared review note(s).",
                "",
                f"**Where it appears most:** {format_counter(row['lanes'])}",
                "",
                f"**Evidence tier mix:** {format_counter(row['tiers'])}",
                "",
                f"**Question for you:** {profile['evaluate']}",
                "",
                f"**What would weaken it:** {profile['weakens_if']}",
                "",
                "**Example source routes:**",
            ]
        )
        for example in row["examples"]:
            lines.append(
                f"- `{example.get('path', '')}` ({example.get('confidence_tier', 'candidate_lead')})"
            )
        lines.append("")

    lines.extend(
        [
            "## How To Read This",
            "",
            "You do not have to perform the review workflow. The system gives you the pattern, its status, why it surfaced, and the main question to evaluate.",
            "",
            "A good personal evaluation can be as simple as:",
            "",
            "- Does this pattern seem true to Scripture, reality, and lived experience?",
            "- Does it stay humble about what it can prove?",
            "- Does it produce truth, love, humility, justice, worship, patience, and faithful action?",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(build_report(), encoding="utf-8")
    print(f"Divine pattern findings saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
