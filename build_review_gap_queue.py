from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path


AUDIT_PATH = Path("reports/review_rules_audit.json")
OUTPUT_MD_PATH = Path("reports/review_gap_queue.md")
OUTPUT_JSON_PATH = Path("reports/review_gap_queue.json")

PRIORITY_RULES = [
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
    review_notes = int(document.get("review_note_count") or 0)
    pattern_count = len(document.get("patterns", []))
    return priority_missing, pattern_count, review_notes


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
                "missing_rules": missing,
                "machine_drafted_rules": sorted(machine_drafted),
                "fill_prompts": {
                    rule: RULE_PROMPTS.get(rule, f"Fill missing review control: {rule}")
                    for rule in missing
                },
            }
        )
    queue.sort(key=priority_score, reverse=True)
    return queue


def build_markdown(audit: dict, queue: list[dict]) -> str:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    missing_counts = Counter()
    for item in queue:
        missing_counts.update(item["missing_rules"])

    lines = [
        "# Review Gap Fill Queue",
        "",
        f"_Generated: {generated}_",
        "",
        "This report explains why the book report says fields are missing. A field is missing when a source does not explicitly separate that review control in a way the audit can detect.",
        "",
        "The goal is not to hide the gap. The goal is to let the system fill structured review companions over time so the Divine Pattern findings become easier for you to evaluate.",
        "",
        "## Why Things Are Missing",
        "",
        "- Many files are candidate notes or imported source leads, not full source reviews.",
        "- Many files contain useful summaries but do not use explicit labels like `Interpretation:` or `Failure condition:`.",
        "- Auto-imported cloud candidates are intentionally cautious: they can route attention, but they should not strengthen claims by themselves.",
        "- The audit only counts controls it can see clearly.",
        "",
        "## How To Fill The Gap",
        "",
        "For each queued source, add or generate a structured review companion with these fields:",
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
        "The system can draft these fields, but it labels them as machine-drafted until the source is directly checked.",
        "",
        "## Missing Field Counts In This Queue",
        "",
    ]
    for rule in PRIORITY_RULES:
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
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_audit": AUDIT_PATH.as_posix(),
        "queue_count": len(queue),
        "items": queue,
    }
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    OUTPUT_MD_PATH.write_text(build_markdown(audit, queue), encoding="utf-8")
    print(f"Review gap queue saved to: {OUTPUT_MD_PATH}")
    print(f"Review gap queue JSON saved to: {OUTPUT_JSON_PATH}")


if __name__ == "__main__":
    main()
