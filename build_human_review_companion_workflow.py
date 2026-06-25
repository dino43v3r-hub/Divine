from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path


QUEUE_PATH = Path("reports/evidence_testing_queue.json")
OUTPUT_MD_PATH = Path("reports/human_review_companion_workflow.md")
OUTPUT_JSON_PATH = Path("reports/human_review_companion_workflow.json")

DAILY_LIMIT = 5
FLAGSHIP_PATTERN = "Image Of God Pattern"

REVIEW_QUESTIONS = [
    "What does the source actually say?",
    "What evidence, if any, does it provide?",
    "What Christian interpretation is being proposed?",
    "What rival explanation could also fit?",
    "What would weaken, narrow, or reject this claim?",
    "Could this be pastorally harmful, especially for someone wounded by religious authority?",
    "Does this need ecclesial, pastoral, theological, source, or tradition-aware review before public use?",
    "Is this analogy-only, developing evidence, reviewed-ready, public-final-ready, or blocked?",
    "Should this source affect confidence? Why or why not?",
]


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def patterns(item: dict) -> list[str]:
    values = item.get("patterns", [])
    return values if isinstance(values, list) else []


def tier_rank(tier: str) -> int:
    return {
        "public_final_ready": 5,
        "reviewed_evidence_ready": 4,
        "developing_evidence": 3,
        "candidate_lead": 2,
        "media_pending_review": 1,
    }.get(tier, 0)


def select_daily_items(queue: dict, limit: int = DAILY_LIMIT) -> list[dict]:
    source_check_items = queue.get("machine_source_check_items", [])
    gap_items = queue.get("items", [])

    combined = []
    for item in source_check_items:
        copy = dict(item)
        copy["workflow_type"] = "source_check_machine_draft"
        copy.setdefault("missing_rules", [])
        combined.append(copy)
    for item in gap_items:
        copy = dict(item)
        copy["workflow_type"] = "missing_review_fields"
        combined.append(copy)

    def score(item: dict) -> tuple[int, int, int, int, str]:
        item_patterns = patterns(item)
        flagship = 1 if FLAGSHIP_PATTERN in item_patterns else 0
        tier = tier_rank(item.get("confidence_tier", ""))
        source_check = 1 if item.get("workflow_type") == "source_check_machine_draft" else 0
        pattern_count = len(item_patterns)
        return flagship, tier, source_check, pattern_count, item.get("path", "")

    deduped = {}
    for item in sorted(combined, key=score, reverse=True):
        path = item.get("path")
        if path and path not in deduped:
            deduped[path] = item
    return list(deduped.values())[:limit]


def field_list(item: dict, key: str) -> str:
    values = item.get(key, [])
    if not values:
        return "none visible"
    return ", ".join(values)


def build_markdown(queue: dict, selected: list[dict]) -> str:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    source_check_count = int(queue.get("machine_source_check_count", 0) or 0)
    queue_count = int(queue.get("queue_count", 0) or 0)

    lines = [
        "# Human Review Companion Workflow",
        "",
        f"_Generated: {generated}_",
        "",
        "This is today's small review packet. It turns the large source-check backlog into five human-sized tasks.",
        "",
        "Machine-drafted fields organize review work only. They should not raise confidence until the original source or primary artifact has been checked directly.",
        "",
        "## Daily Packet",
        "",
        f"- Source-check backlog: {source_check_count:,}",
        f"- Missing-field queue: {queue_count:,}",
        f"- Today's selected tasks: {len(selected):,}",
        f"- Flagship priority: {FLAGSHIP_PATTERN}",
        "",
    ]

    if not selected:
        lines.extend(
            [
                "No review tasks were found. Rebuild the backend and evidence testing queue, then run this workflow again.",
                "",
            ]
        )
        return "\n".join(lines) + "\n"

    for index, item in enumerate(selected, 1):
        item_patterns = ", ".join(patterns(item)) or "none detected"
        lines.extend(
            [
                f"## Review Form {index}: {item.get('title') or item.get('path')}",
                "",
                f"- Path: `{item.get('path', '')}`",
                f"- Lane: {item.get('lane', 'unknown')}",
                f"- Current tier: {item.get('confidence_tier', 'candidate_lead')}",
                f"- Workflow type: {item.get('workflow_type', 'source_check')}",
                f"- Related patterns: {item_patterns}",
                f"- Machine-drafted fields present: {field_list(item, 'machine_drafted_rules')}",
                f"- Missing research fields: {field_list(item, 'missing_research_test_rules')}",
                f"- Missing public-final fields: {field_list(item, 'missing_public_final_rules')}",
                f"- Next gate: {item.get('next_gate', 'source_check')}",
                "",
                "Reviewer answers:",
                "",
            ]
        )
        for question_index, question in enumerate(REVIEW_QUESTIONS, 1):
            lines.extend([f"{question_index}. {question}", "", "   Answer:", ""])
        lines.extend(
            [
                "Decision:",
                "",
                "- Confidence effect: none / weakens / remains candidate / developing evidence / reviewed-ready / public-final-ready",
                "- Required follow-up:",
                "- Reviewer initials/date:",
                "",
            ]
        )

    return "\n".join(lines) + "\n"


def main() -> None:
    queue = read_json(QUEUE_PATH)
    selected = select_daily_items(queue)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_queue": QUEUE_PATH.as_posix(),
        "daily_limit": DAILY_LIMIT,
        "flagship_pattern": FLAGSHIP_PATTERN,
        "items": selected,
    }
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    OUTPUT_MD_PATH.write_text(build_markdown(queue, selected), encoding="utf-8")
    print(f"Human review companion workflow saved to: {OUTPUT_MD_PATH}")
    print(f"Human review companion workflow JSON saved to: {OUTPUT_JSON_PATH}")


if __name__ == "__main__":
    main()
