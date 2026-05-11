from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from pathlib import Path


REPORT_PATHS = [
    Path("reports/cloud_research_findings_report.txt"),
    Path("reports/divine_pattern_research_report.txt"),
    Path("reports/divine_pattern_test_report.txt"),
    Path("reports/deep_source_review_report.txt"),
]


def read_preview(path: Path, max_lines: int = 45):
    if not path.exists():
        return f"{path}: not found"

    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    preview = "\n".join(lines[:max_lines])
    if len(lines) > max_lines:
        preview += f"\n\n[Trimmed. Full report has {len(lines):,} lines.]"
    return preview


def require_env(name: str):
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def build_message():
    to_address = require_env("EMAIL_TO")
    from_address = require_env("EMAIL_FROM")
    subject = os.getenv("EMAIL_SUBJECT", "Daily Cloud Research Results")

    sections = [
        "Daily Cloud Research Results",
        "============================",
        "",
        "This is an automated summary from the Synthesize Data divine-pattern research workflow.",
        "Full reports are committed back to the GitHub repository.",
        "",
    ]

    for path in REPORT_PATHS:
        sections.extend(
            [
                "",
                str(path),
                "-" * len(str(path)),
                read_preview(path),
            ]
        )

    message = EmailMessage()
    message["To"] = to_address
    message["From"] = from_address
    message["Subject"] = subject
    message.set_content("\n".join(sections))

    for path in REPORT_PATHS:
        if path.exists():
            message.add_attachment(
                path.read_bytes(),
                maintype="text",
                subtype="plain",
                filename=path.name,
            )

    return message


def main():
    smtp_server = require_env("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = require_env("SMTP_USERNAME")
    smtp_password = require_env("SMTP_PASSWORD")

    message = build_message()

    with smtplib.SMTP(smtp_server, smtp_port, timeout=60) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(message)

    print(f"Email sent to {message['To']}")


if __name__ == "__main__":
    main()
