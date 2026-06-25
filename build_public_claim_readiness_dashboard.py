from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path


AUDIT_PATH = Path("reports/review_rules_audit.json")
INDEX_PATH = Path("reports/knowledge_retrieval_index.json")
QUEUE_PATH = Path("reports/evidence_testing_queue.json")
OUTPUT_MD_PATH = Path("reports/public_claim_readiness_dashboard.md")
OUTPUT_JSON_PATH = Path("reports/public_claim_readiness_dashboard.json")

FLAGSHIP_PATTERN = "Image Of God Pattern"

RESEARCH_TEST_RULES = [
    "evidence",
    "interpretation",
    "discernment",
    "analogy",
    "practical_use",
    "counter_reading",
    "failure_condition",
    "pastoral_safety",
    "ecclesial_review",
    "liturgical_grounding",
    "promotion_restraint",
    "machine_label_boundary",
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

BLOCKER_LABELS = {
    "evidence": "source-specific evidence",
    "counter_reading": "rival explanation",
    "practical_use": "practical-use boundary",
    "pastoral_safety": "pastoral safety",
    "ecclesial_review": "ecclesial review",
    "liturgical_grounding": "liturgical grounding",
    "promotion_restraint": "promotion restraint",
    "machine_label_boundary": "machine-label boundary",
    "scripture_anchor": "Scripture anchor",
    "doctrinal_fit": "doctrinal fit",
    "no_unresolved_pastoral_harm": "pastoral harm clearance",
    "no_abuse_enabling_language": "abuse-language clearance",
    "no_science_overclaim": "science-overclaim guardrail",
    "no_comparative_flattening": "comparative-flattening guardrail",
    "does_not_prove_boundary": "does-not-prove boundary",
    "plain_language_public_summary": "plain-language public summary",
    "final_promotion_restraint": "final promotion restraint",
}


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def document_patterns(document: dict) -> list[str]:
    patterns = document.get("patterns", [])
    return patterns if isinstance(patterns, list) else []


def most_common(counter: Counter, limit: int = 5) -> str:
    if not counter:
        return "none"
    return ", ".join(f"{name}: {count}" for name, count in counter.most_common(limit))


def confidence_rank(tier: str) -> int:
    return {
        "public_final_ready": 4,
        "reviewed_evidence_ready": 3,
        "developing_evidence": 2,
        "candidate_lead": 1,
    }.get(tier, 0)


def next_action_for_missing(missing: Counter) -> str:
    if not missing:
        return "No visible blocker remains in the audit. Confirm with human review before public use."
    for rule in [
        "scripture_anchor",
        "doctrinal_fit",
        "no_unresolved_pastoral_harm",
        "no_abuse_enabling_language",
        "does_not_prove_boundary",
        "pastoral_safety",
        "ecclesial_review",
        "liturgical_grounding",
        "promotion_restraint",
        "evidence",
        "counter_reading",
        "practical_use",
        "machine_label_boundary",
    ]:
        if missing.get(rule, 0):
            label = BLOCKER_LABELS.get(rule, rule.replace("_", " "))
            return f"Review the next source for {label}."
    rule, _count = missing.most_common(1)[0]
    label = BLOCKER_LABELS.get(rule, rule.replace("_", " "))
    return f"Review the next source for {label}."


def choose_next_source(pattern: str, queue_items: list[dict]) -> dict:
    pattern_items = [
        item for item in queue_items if pattern in document_patterns(item)
    ]
    pool = pattern_items or queue_items
    if not pool:
        return {}

    def score(item: dict) -> tuple[int, int, int, str]:
        tier = confidence_rank(item.get("confidence_tier", ""))
        public_gaps = len(item.get("missing_public_final_rules", []))
        research_gaps = len(item.get("missing_research_test_rules", []))
        return tier, -public_gaps, -research_gaps, item.get("path", "")

    return sorted(pool, key=score, reverse=True)[0]


def build_rows(audit: dict, index: dict, queue: dict) -> list[dict]:
    docs = audit.get("documents", [])
    indexed_docs = index.get("documents", [])
    queue_items = queue.get("items", [])

    all_patterns = set()
    for document in docs + indexed_docs:
        all_patterns.update(document_patterns(document))

    rows = []
    for pattern in sorted(all_patterns):
        pattern_docs = [
            document for document in docs if pattern in document_patterns(document)
        ]
        if not pattern_docs:
            pattern_docs = [
                document
                for document in indexed_docs
                if pattern in document_patterns(document)
            ]

        tiers = Counter(
            document.get("confidence_tier", "candidate_lead")
            for document in pattern_docs
        )
        lanes = Counter(document.get("lane", "unknown") for document in pattern_docs)
        missing = Counter()
        for document in pattern_docs:
            machine_drafted = set(document.get("machine_drafted_rules", []))
            for rule in document.get("missing_rules", []):
                if rule not in machine_drafted:
                    missing[rule] += 1

        next_source = choose_next_source(pattern, queue_items)
        rows.append(
            {
                "pattern": pattern,
                "is_flagship": pattern == FLAGSHIP_PATTERN,
                "documents": len(pattern_docs),
                "tiers": dict(tiers),
                "lanes": dict(lanes),
                "top_blockers": dict(missing.most_common(8)),
                "next_action": next_action_for_missing(missing),
                "next_source": next_source,
            }
        )

    rows.sort(
        key=lambda row: (
            row["is_flagship"],
            row["tiers"].get("public_final_ready", 0),
            row["tiers"].get("reviewed_evidence_ready", 0),
            row["tiers"].get("developing_evidence", 0),
            row["documents"],
        ),
        reverse=True,
    )
    return rows


def build_markdown(audit: dict, rows: list[dict]) -> str:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    totals = audit.get("confidence_tier_totals", {})
    public_ready = int(totals.get("public_final_ready", 0) or 0)

    lines = [
        "# Public Claim Readiness Dashboard",
        "",
        f"_Generated: {generated}_",
        "",
        "This dashboard is a steering report. It shows which pattern families are closest to public-safe use and which review controls are still blocking promotion.",
        "",
        "Machine labels route attention; they do not decide truth. Human source-check, Scripture, doctrine, pastoral safety, ecclesial review, and promotion restraint still govern public claims.",
        "",
        "## Snapshot",
        "",
        f"- Candidate leads: {int(totals.get('candidate_lead', 0) or 0):,}",
        f"- Developing evidence: {int(totals.get('developing_evidence', 0) or 0):,}",
        f"- Ready for human confidence review: {int(totals.get('reviewed_evidence_ready', 0) or 0):,}",
        f"- Public-final ready: {public_ready:,}",
        "",
    ]

    if public_ready:
        lines.append("At least one source is public-final ready in the audit. Human review should still confirm the wording before publication.")
    else:
        lines.append("No source is public-final ready yet. The public-facing posture should remain patient, clear, and non-final.")
    lines.extend(
        [
            "",
            f"## Flagship Track: {FLAGSHIP_PATTERN}",
            "",
            "This is the recommended first pattern to move toward public-final review because it currently has the strongest reviewed-readiness signal.",
            "",
        ]
    )

    flagship = next((row for row in rows if row["pattern"] == FLAGSHIP_PATTERN), None)
    if flagship:
        lines.extend(format_pattern_section(flagship, include_heading=False))
    else:
        lines.extend(["No flagship-row data was found in the current audit.", ""])

    lines.extend(["## Pattern Readiness", ""])
    for row in rows:
        if row["pattern"] == FLAGSHIP_PATTERN:
            continue
        lines.extend(format_pattern_section(row, include_heading=True))

    return "\n".join(lines) + "\n"


def format_pattern_section(row: dict, include_heading: bool) -> list[str]:
    tiers = Counter(row.get("tiers", {}))
    lanes = Counter(row.get("lanes", {}))
    blockers = Counter(row.get("top_blockers", {}))
    next_source = row.get("next_source", {})
    lines = []
    if include_heading:
        lines.extend([f"### {row['pattern']}", ""])
    lines.extend(
        [
            f"- Documents: {row['documents']:,}",
            f"- Tier mix: {most_common(tiers)}",
            f"- Main lanes: {most_common(lanes)}",
            f"- Top blockers: {most_common(blockers)}",
            f"- Next action: {row['next_action']}",
        ]
    )
    if next_source:
        missing = next_source.get("missing_rules") or next_source.get("missing_public_final_rules") or next_source.get("missing_research_test_rules") or []
        lines.extend(
            [
                f"- Next source: `{next_source.get('path', '')}`",
                f"- Source gate: {next_source.get('next_gate', 'source_check')}",
                f"- Source missing: {', '.join(missing[:8]) or 'none visible'}",
            ]
        )
    lines.append("")
    return lines


def main() -> None:
    audit = read_json(AUDIT_PATH)
    index = read_json(INDEX_PATH)
    queue = read_json(QUEUE_PATH)
    rows = build_rows(audit, index, queue)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_audit": AUDIT_PATH.as_posix(),
        "source_index": INDEX_PATH.as_posix(),
        "source_queue": QUEUE_PATH.as_posix(),
        "flagship_pattern": FLAGSHIP_PATTERN,
        "patterns": rows,
    }
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    OUTPUT_MD_PATH.write_text(build_markdown(audit, rows), encoding="utf-8")
    print(f"Public claim readiness dashboard saved to: {OUTPUT_MD_PATH}")
    print(f"Public claim readiness dashboard JSON saved to: {OUTPUT_JSON_PATH}")


if __name__ == "__main__":
    main()
