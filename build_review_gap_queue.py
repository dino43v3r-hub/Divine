from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path


AUDIT_PATH = Path("reports/review_rules_audit.json")
OUTPUT_MD_PATH = Path("reports/review_gap_queue.md")
OUTPUT_JSON_PATH = Path("reports/review_gap_queue.json")
EVIDENCE_TESTING_MD_PATH = Path("reports/evidence_testing_queue.md")
EVIDENCE_TESTING_JSON_PATH = Path("reports/evidence_testing_queue.json")

RESEARCH_TEST_RULES = [
    "pastoral_safety",
    "ecclesial_review",
    "liturgical_grounding",
    "promotion_restraint",
    "interpretation",
    "analogy",
    "failure_condition",
    "discernment",
    "machine_label_boundary",
    "evidence",
    "counter_reading",
    "practical_use",
]

PUBLIC_FINAL_RULES = [
    "scripture_anchor",
    "doctrinal_fit",
    "no_unresolved_pastoral_harm",
    "no_abuse_enabling_language",
    "no_science_overclaim",
    "no_comparative_flattening",
    "does_not_prove_boundary",
    "plain_language_public_summary",
    "final_promotion_restraint",
]

PRIORITY_RULES = RESEARCH_TEST_RULES + PUBLIC_FINAL_RULES

RULE_PROMPTS = {
    "evidence": "What does this source actually support, without theological inflation?",
    "interpretation": "What Christian theological reading is being proposed from that evidence?",
    "discernment": "What still needs prayerful, communal, accountable testing?",
    "analogy": "Is this only an analogy, comparison, or sign-reading rather than proof?",
    "practical_use": "What faithful action, repair, worship, justice, or humility could this shape?",
    "counter_reading": "What rival explanation could explain the same signal without the Divine Pattern claim?",
    "failure_condition": "What would weaken, narrow, or reject this claim?",
    "pastoral_safety": "Would this claim be safe beside a hospital bed, at a funeral, in confession, or with someone harmed by religious authority?",
    "ecclesial_review": "What pastoral, theological, source, harm-safety, or tradition-aware review is needed before public use?",
    "liturgical_grounding": "How does this remain accountable to baptism, Eucharist, confession, anointing, funerals, the church year, or daily prayer without reducing worship to symbolism?",
    "promotion_restraint": "Why should this stay research-only, analogy-only, developing, reviewed-ready, or blocked rather than being overpromoted?",
    "machine_label_boundary": "What should the machine label not be allowed to settle?",
    "scripture_anchor": "What Scripture text or biblical theme anchors, limits, or corrects this claim?",
    "doctrinal_fit": "How does this fit with Christ, creed, Trinity, creation, sin, redemption, Church witness, and orthodox doctrine?",
    "no_unresolved_pastoral_harm": "What pastoral harm risk has been checked, and what risk would still block public use?",
    "no_abuse_enabling_language": "Could this wording protect abusers, pressure victims, excuse coercion, or silence lament?",
    "no_science_overclaim": "Does this avoid using science, math, probability, or psychology as proof beyond its proper scope?",
    "no_comparative_flattening": "If another tradition appears, has it been represented on its own terms before Christian comparison?",
    "does_not_prove_boundary": "What does this evidence not prove, even if the pattern is interesting or useful?",
    "plain_language_public_summary": "How can this be stated plainly for ordinary readers without inflating confidence?",
    "final_promotion_restraint": "Why is this ready, or not ready, to shape a public-facing claim?",
}


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def priority_score(document: dict) -> tuple[int, int, int]:
    missing = set(document.get("missing_rules", []))
    priority_missing = sum(1 for rule in PRIORITY_RULES[:4] if rule in missing)
    public_final_missing = sum(1 for rule in PUBLIC_FINAL_RULES if rule in missing)
    review_notes = int(document.get("review_note_count") or 0)
    pattern_count = len(document.get("patterns", []))
    return priority_missing, public_final_missing, pattern_count, review_notes


def next_gate(document: dict, missing: list[str]) -> str:
    missing_set = set(missing)
    if any(rule in missing_set for rule in RESEARCH_TEST_RULES):
        return "research_evidence_test"
    if document.get("confidence_tier") == "reviewed_evidence_ready" and any(
        rule in missing_set for rule in PUBLIC_FINAL_RULES
    ):
        return "public_final_evidence_test"
    if any(rule in missing_set for rule in PUBLIC_FINAL_RULES):
        return "public_final_evidence_test_after_research_gate"
    return "source_check"


def build_queue(audit: dict) -> list[dict]:
    documents = audit.get("documents", [])
    queue = []
    for document in documents:
        machine_drafted = set(document.get("machine_drafted_rules", []))
        missing = [
            rule for rule in document.get("missing_rules", []) if rule not in machine_drafted
        ]
        if not missing:
            continue
        queue.append(
            {
                "path": document.get("path", ""),
                "title": document.get("title", ""),
                "lane": document.get("lane", ""),
                "confidence_tier": document.get("confidence_tier", "candidate_lead"),
                "patterns": document.get("patterns", []),
                "review_note_count": int(document.get("review_note_count") or 0),
                "next_gate": next_gate(document, missing),
                "missing_rules": missing,
                "missing_research_test_rules": [
                    rule for rule in missing if rule in RESEARCH_TEST_RULES
                ],
                "missing_public_final_rules": [
                    rule for rule in missing if rule in PUBLIC_FINAL_RULES
                ],
                "machine_drafted_rules": sorted(machine_drafted),
                "fill_prompts": {
                    rule: RULE_PROMPTS.get(rule, f"Fill missing review control: {rule}")
                    for rule in missing
                },
            }
        )
    queue.sort(key=priority_score, reverse=True)
    return queue


def build_machine_source_check_queue(audit: dict) -> list[dict]:
    queue = []
    for document in audit.get("documents", []):
        machine_rules = document.get("machine_drafted_rules", [])
        if not machine_rules:
            continue
        if document.get("machine_drafted_confidence_effect") == "source_checked_can_inform_confidence":
            continue
        queue.append(
            {
                "path": document.get("path", ""),
                "title": document.get("title", ""),
                "lane": document.get("lane", ""),
                "confidence_tier": document.get("confidence_tier", "candidate_lead"),
                "patterns": document.get("patterns", []),
                "machine_drafted_rules": sorted(machine_rules),
                "source_check_prompt": (
                    "Read the original source or primary artifact directly, replace any generic machine-drafted fields "
                    "with source-specific notes, and only then mark whether the companion can inform confidence."
                ),
            }
        )
    queue.sort(key=lambda item: (item["confidence_tier"] != "candidate_lead", item["path"]))
    return queue


def build_markdown(audit: dict, queue: list[dict], machine_source_check_queue: list[dict]) -> str:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    missing_counts = Counter()
    for item in queue:
        missing_counts.update(item["missing_rules"])

    lines = [
        "# Evidence Testing Queue",
        "",
        f"_Generated: {generated}_",
        "",
        "This is the project's source-by-source testing backlog. It explains which sources still need research evidence testing before they can strengthen a claim, and which reviewed sources still need public-use testing before they can become final public evidence.",
        "",
        "The goal is not to hide the gap. The goal is to make every promotion traceable: candidate source -> evidence testing queue -> source-specific review -> reviewed_evidence_ready -> public-use testing -> public_final_ready.",
        "",
        "## Testing Gates",
        "",
        "- `research_evidence_test`: checks evidence, interpretation, discernment, analogy, practical use, counter-reading, failure condition, pastoral safety, ecclesial review, liturgical grounding, promotion restraint, and machine-label boundary.",
        "- `public_final_evidence_test`: checks Scripture anchor, doctrinal fit, pastoral harm clearance, abuse-language risk, science overclaim, comparative flattening, does-not-prove boundary, plain-language public summary, and final promotion restraint.",
        "- Machine-drafted fields may organize this testing, but they do not raise confidence until the original source has been checked directly.",
        "",
        "## Why Sources Are Queued",
        "",
        "- Many files are candidate notes or imported source leads, not full source reviews.",
        "- Many files contain useful summaries but do not use explicit labels like `Interpretation:` or `Failure condition:`.",
        "- Auto-imported cloud candidates are intentionally cautious: they can route attention, but they should not strengthen claims by themselves.",
        "- The audit only counts controls it can see clearly.",
        "",
        "## How To Test A Source",
        "",
        "For each queued source, read the original source or source note, then add a structured review companion with the relevant missing fields.",
        "",
        "Research evidence test fields:",
        "",
        "- Evidence",
        "- Interpretation",
        "- Discernment",
        "- Analogy",
        "- Practical use",
        "- Counter-reading",
        "- Failure condition",
        "- Pastoral safety",
        "- Ecclesial review",
        "- Liturgical grounding",
        "- Promotion restraint",
        "- Machine-label boundary",
        "",
        "Public-final evidence test fields:",
        "",
        "- Scripture anchor",
        "- Doctrinal fit",
        "- No unresolved pastoral harm",
        "- No abuse-enabling language",
        "- No science overclaim",
        "- No comparative flattening",
        "- Does-not-prove boundary",
        "- Plain-language public summary",
        "- Final promotion restraint",
        "",
        "Passing the research test can move a source toward `reviewed_evidence_ready`. Passing both the research test and the public-final test can move a source toward `public_final_ready`.",
        "",
        "## Missing Test Counts In This Queue",
        "",
    ]
    for rule in RESEARCH_TEST_RULES:
        lines.append(f"- {rule}: {missing_counts.get(rule, 0)}")
    lines.extend(["", "Public-final test gaps:", ""])
    for rule in PUBLIC_FINAL_RULES:
        lines.append(f"- {rule}: {missing_counts.get(rule, 0)}")

    coverage = audit.get("rule_coverage", {})
    if coverage:
        lines.extend(["", "## Companion Coverage Already Created", ""])
        for rule in PRIORITY_RULES:
            values = coverage.get(rule, {})
            lines.append(
                f"- {rule}: {int(values.get('review_companion', 0)):,} reviewed companion; {int(values.get('machine_drafted', 0)):,} machine-drafted; {int(values.get('missing', 0)):,} still missing"
            )

    lines.extend(
        [
            "",
            "## Machine-Drafted Source-Check Queue",
            "",
            f"- Items requiring source-check before trust: {len(machine_source_check_queue):,}",
            "- Rule: machine-drafted fields organize work only; they do not raise confidence until the original source has been checked directly.",
            "",
        ]
    )
    for index, item in enumerate(machine_source_check_queue[:25], 1):
        patterns = ", ".join(item["patterns"]) or "none detected"
        lines.extend(
            [
                f"### M{index}. {item['title'] or item['path']}",
                "",
                f"- Path: `{item['path']}`",
                f"- Lane: {item['lane']}",
                f"- Current tier: {item['confidence_tier']}",
                f"- Patterns: {patterns}",
                f"- Machine-drafted rules: {', '.join(item['machine_drafted_rules'])}",
                f"- Source-check prompt: {item['source_check_prompt']}",
                "",
            ]
        )

    lines.extend(
        [
            "",
            "## Highest Priority Sources",
            "",
        ]
    )

    if not queue:
        lines.extend(
            [
                "No still-missing review fields remain. Existing gaps are covered by machine-drafted companions and should be source-checked over time if confidence needs to rise.",
                "",
            ]
        )

    for index, item in enumerate(queue[:40], 1):
        patterns = ", ".join(item["patterns"]) or "none detected"
        lines.extend(
            [
                f"### {index}. {item['title'] or item['path']}",
                "",
                f"- Path: `{item['path']}`",
                f"- Lane: {item['lane']}",
                f"- Current tier: {item['confidence_tier']}",
                f"- Next gate: {item['next_gate']}",
                f"- Patterns: {patterns}",
                f"- Missing: {', '.join(item['missing_rules'])}",
                "",
                "Fill prompts:",
            ]
        )
        for rule, prompt in item["fill_prompts"].items():
            lines.append(f"- {rule}: {prompt}")
        lines.append("")

    return "\n".join(lines) + "\n"


def main() -> None:
    audit = read_json(AUDIT_PATH)
    queue = build_queue(audit)
    machine_source_check_queue = build_machine_source_check_queue(audit)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_audit": AUDIT_PATH.as_posix(),
        "legacy_paths": {
            "markdown": OUTPUT_MD_PATH.as_posix(),
            "json": OUTPUT_JSON_PATH.as_posix(),
        },
        "evidence_testing_paths": {
            "markdown": EVIDENCE_TESTING_MD_PATH.as_posix(),
            "json": EVIDENCE_TESTING_JSON_PATH.as_posix(),
        },
        "queue_count": len(queue),
        "machine_source_check_count": len(machine_source_check_queue),
        "machine_source_check_items": machine_source_check_queue,
        "items": queue,
    }
    json_text = json.dumps(payload, indent=2, sort_keys=True)
    markdown_text = build_markdown(audit, queue, machine_source_check_queue)
    OUTPUT_JSON_PATH.write_text(json_text, encoding="utf-8")
    EVIDENCE_TESTING_JSON_PATH.write_text(json_text, encoding="utf-8")
    OUTPUT_MD_PATH.write_text(markdown_text, encoding="utf-8")
    EVIDENCE_TESTING_MD_PATH.write_text(markdown_text, encoding="utf-8")
    print(f"Review gap queue saved to: {OUTPUT_MD_PATH}")
    print(f"Review gap queue JSON saved to: {OUTPUT_JSON_PATH}")
    print(f"Evidence testing queue saved to: {EVIDENCE_TESTING_MD_PATH}")
    print(f"Evidence testing queue JSON saved to: {EVIDENCE_TESTING_JSON_PATH}")


if __name__ == "__main__":
    main()
