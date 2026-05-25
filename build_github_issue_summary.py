from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path


REPORT_PATHS = [
    Path("reports/disciplined_theological_assistant_report.txt"),
    Path("reports/divine_pattern_summary_report.txt"),
    Path("reports/top_five_divine_patterns_report.txt"),
    Path("reports/cloud_research_findings_report.txt"),
    Path("reports/divine_pattern_research_report.txt"),
    Path("reports/divine_pattern_candidates_report.txt"),
    Path("reports/divine_pattern_test_report.txt"),
    Path("reports/deep_source_review_report.txt"),
    Path("reports/theologian_pattern_design_report.txt"),
    Path("reports/cross_layer_reasoning_report.txt"),
    Path("reports/music_note_patterns_report.txt"),
    Path("reports/music_lyric_patterns_report.txt"),
    Path("reports/cultural_pattern_relationships_report.txt"),
    Path("research_documents/daily_evaluation_queue.md"),
]


OUTPUT_PATH = Path("reports/github_issue_summary.md")


def read_preview(path: Path, max_lines: int = 18):
    if not path.exists():
        return f"`{path}` was not generated."

    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    preview = "\n".join(lines[:max_lines])
    if len(lines) > max_lines:
        preview += f"\n\n_Full report has {len(lines):,} lines. Open the linked report above to read everything._"
    return preview


def report_link(path: Path):
    repository = os.getenv("GITHUB_REPOSITORY", "").strip()
    server_url = os.getenv("GITHUB_SERVER_URL", "https://github.com").strip()
    branch = os.getenv("GITHUB_REF_NAME", "main").strip()

    if repository:
        return f"{server_url}/{repository}/blob/{branch}/{path.as_posix()}"

    return path.as_posix()


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Daily Cloud Research Results",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This issue was created automatically by the Synthesize Data workflow.",
        "Full reports are committed in the repository under `reports/`.",
        "",
        "## Full Reports",
        "",
        "| Report | Read full file |",
        "| --- | --- |",
    ]

    for path in REPORT_PATHS:
        status = "available" if path.exists() else "missing"
        lines.append(f"| `{path.name}` | [{status}]({report_link(path)}) |")

    lines.extend(
        [
            "",
            "## Quick Highlights",
            "",
            "The sections below are only short previews. Use the links above for the full reports.",
            "",
        ]
    )

    for path in REPORT_PATHS:
        lines.extend(
            [
                f"## {path}",
                "",
                "```text",
                read_preview(path),
                "```",
                "",
            ]
        )

    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Issue summary saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
