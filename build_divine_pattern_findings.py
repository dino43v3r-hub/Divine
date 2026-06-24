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


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def confidence_phrase(tiers: Counter) -> str:
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
        "- `developing evidence`: enough structure to consider carefully.",
        "- `ready for your evaluation`: enough controls are present that you can weigh it directly.",
        "",
        "It is designed to change day to day when the collector, analyzer, and backend discover or re-index new material.",
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
                f"**Theologian judgment for ordinary readers:** {profile['theologian_judgment']}",
                "",
                f"**Common-person test:** {profile['evaluate']}",
                "",
                f"**What would weaken it:** {profile['weakens_if']}",
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
