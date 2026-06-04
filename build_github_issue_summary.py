from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path


PUBLISHED_ARTICLE_PATH = Path("reports/published/final_book_report.md")


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
        "# Daily Divine Pattern Research Article",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "This issue was created automatically by the Synthesize Data workflow.",
        "The workflow now publishes one synthesized reading article instead of a wall of generated reports.",
        "",
        "## Published Article",
        "",
        f"[Read `{PUBLISHED_ARTICLE_PATH.as_posix()}`]({report_link(PUBLISHED_ARTICLE_PATH)})",
        "",
        "## Preview",
        "",
        "```text",
        read_preview(PUBLISHED_ARTICLE_PATH, max_lines=80),
        "```",
    ]

    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Issue summary saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
