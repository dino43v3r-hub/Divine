from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re


REPORT_PATHS = [
    Path("reports/divine_pattern_findings.md"),
    Path("reports/published/final_book_report.md"),
    Path("reports/combined_web_article.md"),
]

OUTPUT_MD_PATH = Path("reports/public_language_overclaim_filter.md")
OUTPUT_JSON_PATH = Path("reports/public_language_overclaim_filter.json")

MAX_CONTEXT_CHARS = 190

RULES = [
    {
        "id": "proof_language",
        "severity": "high",
        "pattern": r"\b(proves?|proof|demonstrates?|confirms?|establishes?)\b",
        "why": "Pattern evidence should not be presented as proof of God, doctrine, providence, or divine action.",
    },
    {
        "id": "certainty_language",
        "severity": "medium",
        "pattern": r"\b(certainly|undeniably|irrefutably|without doubt|must mean|clearly shows)\b",
        "why": "Public language should preserve confidence tiers and leave room for mystery and rival explanations.",
    },
    {
        "id": "science_overclaim",
        "severity": "high",
        "pattern": r"\b(quantum|neuroscience|mathematics|physics|biology|evolution|probability|complexity)\b.{0,90}\b(proves?|proof|confirms?|demonstrates?|shows God|divine action)\b",
        "why": "Science, math, and psychology can illuminate analogies, but they should not be used as theological proof.",
    },
    {
        "id": "suffering_risk",
        "severity": "high",
        "pattern": r"\b(suffering|trauma|abuse|victim|grief|tragedy|harm)\b.{0,100}\b(good|gift|necessary|meant to|God wanted|redemptive)\b",
        "why": "Suffering-related claims need lament, protection, justice, repair, and pastoral harm checks.",
    },
    {
        "id": "comparative_flattening",
        "severity": "medium",
        "pattern": r"\b(all religions|every tradition|really means|hidden Christianity|points to Christianity)\b",
        "why": "Comparative claims should honor other traditions on their own terms before Christian interpretation.",
    },
    {
        "id": "private_revelation_risk",
        "severity": "high",
        "pattern": r"\b(God told me|God revealed through this pattern|the pattern reveals God's will|divine message)\b",
        "why": "The project is not a private revelation engine; claims remain under Scripture, creed, Church witness, and review.",
    },
]

SAFE_CONTEXT_PATTERNS = [
    r"\bdoes\s+not\s+prove\b",
    r"\bdo\s+not\s+prove\b",
    r"\bdid\s+not\s+prove\b",
    r"\bcannot\s+prove\b",
    r"\bcan\s+not\s+prove\b",
    r"\bnot\s+proof\b",
    r"\bno\s+proof\b",
    r"\bnot\s+a\s+proof\b",
    r"\bwithout\s+pretending\b.{0,80}\bprove",
    r"\bmust\s+not\s+be\s+treated\s+as\s+proof\b",
    r"\bmust\s+not\s+exceed\b",
    r"\bnot\s+be\s+used\s+as\b.{0,80}\bproof\b",
    r"\bnot\b.{0,80}\bas\s+proof\b",
    r"\bnot\b.{0,80}\bproof\b",
    r"\bdo\s+not\b.{0,100}\bproof\b",
    r"\breject\b.{0,90}\bas\s+proof\b",
    r"\bshould\s+not\b.{0,90}\bproof\b",
    r"\bno\s+mathematical\s+proof\b",
    r"\bwhat\s+this\s+does\s+not\s+prove\b",
    r"\bdoes-not-prove\b",
    r"\bwhat\s+would\s+weaken\b.{0,120}\bproof\b",
    r"\bweakens?\b.{0,120}\bproof\b",
    r"\bmisuse\s+risk\b.{0,140}\bproof\b",
    r"\bguardrail\b.{0,140}\bproof\b",
    r"\brequired\s+revision\b.{0,140}\bproof\b",
    r"\bwhy\s+it\s+fails\b.{0,140}\bproves?\b",
    r"\bpattern\s+claim\s+under\s+test\b.{0,140}\bproves?\b",
    r"\bshortcut\s+proof\b",
    r"\bproof-language\s+must\s+not\b",
]


def is_safe_boundary_language(rule_id: str, context: str) -> bool:
    lowered = context.lower()
    if rule_id in {"certainty_language", "suffering_risk", "comparative_flattening", "private_revelation_risk"}:
        return False
    return any(re.search(pattern, lowered, flags=re.IGNORECASE) for pattern in SAFE_CONTEXT_PATTERNS)


def read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def line_number_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def context_for(text: str, start: int, end: int) -> str:
    left = max(0, start - MAX_CONTEXT_CHARS // 2)
    right = min(len(text), end + MAX_CONTEXT_CHARS // 2)
    context = re.sub(r"\s+", " ", text[left:right]).strip()
    return context


def scan_report(path: Path) -> list[dict]:
    text = read(path)
    if not text:
        return []
    findings = []
    for rule in RULES:
        regex = re.compile(rule["pattern"], flags=re.IGNORECASE | re.DOTALL)
        for match in regex.finditer(text):
            context = context_for(text, match.start(), match.end())
            if is_safe_boundary_language(rule["id"], context):
                continue
            findings.append(
                {
                    "path": path.as_posix(),
                    "line": line_number_for_offset(text, match.start()),
                    "rule_id": rule["id"],
                    "severity": rule["severity"],
                    "matched_text": match.group(0)[:160],
                    "context": context,
                    "why": rule["why"],
                }
            )
    findings.sort(key=lambda item: (item["path"], item["line"], item["rule_id"]))
    return findings


def build_markdown(findings: list[dict]) -> str:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    severity_counts = {}
    for item in findings:
        severity_counts[item["severity"]] = severity_counts.get(item["severity"], 0) + 1

    lines = [
        "# Public Language Overclaim Filter",
        "",
        f"_Generated: {generated}_",
        "",
        "This report flags wording that may need human review before public use. A flag is not a verdict; it is a request to check confidence, pastoral safety, and public-final boundaries.",
        "",
        "## Summary",
        "",
        f"- Files scanned: {len(REPORT_PATHS):,}",
        f"- Flags found: {len(findings):,}",
        f"- High severity: {severity_counts.get('high', 0):,}",
        f"- Medium severity: {severity_counts.get('medium', 0):,}",
        "",
    ]

    if not findings:
        lines.extend(["No overclaim flags were found in the scanned public reports.", ""])
        return "\n".join(lines) + "\n"

    lines.extend(["## Flags", ""])
    for index, item in enumerate(findings, 1):
        lines.extend(
            [
                f"### {index}. {item['rule_id']} ({item['severity']})",
                "",
                f"- File: `{item['path']}`",
                f"- Line: {item['line']}",
                f"- Why check it: {item['why']}",
                f"- Matched wording: `{item['matched_text']}`",
                f"- Context: {item['context']}",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    findings = []
    for path in REPORT_PATHS:
        findings.extend(scan_report(path))
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "reports_scanned": [path.as_posix() for path in REPORT_PATHS],
        "rules": [{key: rule[key] for key in ("id", "severity", "why")} for rule in RULES],
        "findings": findings,
    }
    OUTPUT_JSON_PATH.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    OUTPUT_MD_PATH.write_text(build_markdown(findings), encoding="utf-8")
    print(f"Public language overclaim filter saved to: {OUTPUT_MD_PATH}")
    print(f"Public language overclaim filter JSON saved to: {OUTPUT_JSON_PATH}")


if __name__ == "__main__":
    main()
