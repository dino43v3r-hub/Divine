from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path


QUEUE_PATH = Path("reports/review_gap_queue.json")
OUTPUT_JSON_PATH = Path("research_documents/machine_drafted_review_companions.json")
OUTPUT_MD_PATH = Path("research_documents/machine_drafted_review_companions.md")

FIELD_DRAFTS = {
    "evidence": "Machine-drafted placeholder: identify what the source actually supports before using it as evidence.",
    "interpretation": "Machine-drafted placeholder: state the possible Christian theological reading separately from the source evidence.",
    "discernment": "Machine-drafted placeholder: name what still needs prayerful, communal, and accountable testing.",
    "analogy": "Machine-drafted placeholder: mark whether this is analogy, comparison, or sign-reading rather than proof.",
    "practical_use": "Machine-drafted placeholder: describe possible faithful practice without coercion, denial, or overclaiming.",
    "counter_reading": "Machine-drafted placeholder: name a rival explanation that could account for the same signal.",
    "failure_condition": "Machine-drafted placeholder: state what would weaken, narrow, or reject the claim.",
    "pastoral_safety": "Machine-drafted placeholder: test whether the claim would be safe in pastoral crisis and whether it protects vulnerable people first.",
    "ecclesial_review": "Machine-drafted placeholder: name the pastoral, theological, source, harm-safety, or tradition-aware reviewers needed before public use.",
    "liturgical_grounding": "Machine-drafted placeholder: relate any public or devotional use to worship, sacrament, prayer, and the Church's discernment without reducing them to symbols.",
    "promotion_restraint": "Machine-drafted placeholder: state why the claim should remain research-only, analogy-only, developing, reviewed-ready, or blocked.",
    "machine_label_boundary": "Machine-drafted placeholder: machine labels route attention; they do not settle truth or confidence.",
}


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def build_companions(queue_payload: dict) -> list[dict]:
    companions = []
    for item in queue_payload.get("items", []):
        missing_rules = item.get("missing_rules", [])
        if not missing_rules:
            continue
        companions.append(
            {
                "path": item.get("path", ""),
                "title": item.get("title", ""),
                "lane": item.get("lane", ""),
                "confidence_tier_at_draft_time": item.get("confidence_tier", ""),
                "draft_status": "machine_drafted_not_source_checked",
                "confidence_effect": "does_not_raise_confidence",
                "machine_drafted_fields": {
                    rule: FIELD_DRAFTS.get(
                        rule,
                        f"Machine-drafted placeholder: fill missing review control `{rule}`.",
                    )
                    for rule in missing_rules
                },
            }
        )
    return companions


def build_markdown(companions: list[dict]) -> str:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Machine-Drafted Review Companions",
        "",
        f"_Generated: {generated}_",
        "",
        "These companions fill missing review fields with machine-drafted placeholders so the project can track complete review coverage without pretending the source has been human/source checked.",
        "",
        "Rule: machine-drafted fields do not raise confidence. They only show what still needs to be checked or refined.",
        "",
        "## Companion Records",
        "",
    ]
    for index, item in enumerate(companions[:80], 1):
        lines.extend(
            [
                f"### {index}. {item.get('title') or item.get('path')}",
                "",
                f"- Path: `{item.get('path', '')}`",
                f"- Draft status: {item.get('draft_status', '')}",
                f"- Confidence effect: {item.get('confidence_effect', '')}",
                "",
            ]
        )
        for rule, draft in item.get("machine_drafted_fields", {}).items():
            lines.append(f"- {rule}: {draft}")
        lines.append("")

    if len(companions) > 80:
        lines.append(f"_Additional companion records are stored in `{OUTPUT_JSON_PATH.as_posix()}`._")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    queue_payload = read_json(QUEUE_PATH)
    companions = build_companions(queue_payload)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_queue": QUEUE_PATH.as_posix(),
        "policy": "Machine-drafted fields fill review coverage but do not raise confidence unless source checked.",
        "companion_count": len(companions),
        "companions": companions,
    }
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    OUTPUT_MD_PATH.write_text(build_markdown(companions), encoding="utf-8")
    print(f"Machine-drafted companions saved to: {OUTPUT_JSON_PATH}")
    print(f"Machine-drafted companion summary saved to: {OUTPUT_MD_PATH}")


if __name__ == "__main__":
    main()
