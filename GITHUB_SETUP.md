# GitHub Setup

This project is ready to upload to GitHub.

## What Is Already Set Up

- `.github/workflows/daily-cloud-research.yml`
  - runs every day at 14:00 UTC
  - can also be run manually from the GitHub Actions tab
  - runs `internet_source_collector.py`
  - runs `divine_pattern_analyzer.py`
  - builds a GitHub issue summary
  - creates a daily notification issue
  - commits updated references and reports back to the repository
  - opts JavaScript-based GitHub Actions into Node.js 24 with `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24`

- `internet_source_collector.py`
  - collects metadata from Crossref, OpenAlex, and arXiv
  - stores metadata and summaries only
  - avoids copying full copyrighted text

- `references/references.json`
  - stores collected reference metadata

- `reports/cloud_research_findings_report.txt`
  - summarizes collected sources

- `research_documents/cloud_references_summary.md`
  - lets the main analyzer include reference metadata in divine-pattern reports

## Option 1: GitHub Website Upload

1. Go to GitHub and create a new repository.
2. Choose **Add file -> Upload files**.
3. Upload this whole project folder.
4. Commit the upload.
5. Go to the **Actions** tab.
6. Enable workflows if GitHub asks.
7. Open **Daily Cloud Research**.
8. Click **Run workflow**.

## Option 2: GitHub Desktop

1. Install GitHub Desktop.
2. Choose **File -> Add local repository**.
3. Select this folder:

   `C:\Users\mgerdin\OneDrive - alamo.edu\Documents\Compiler`

4. Publish the repository to GitHub.
5. Open the repository on GitHub and run the workflow from the **Actions** tab.

## GitHub Actions Node.js 24

GitHub is deprecating Node.js 20 for JavaScript-based actions. The workflow sets
this environment variable:

```yaml
FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: "true"
```

This opts actions such as `actions/checkout`, `actions/setup-python`,
`actions/github-script`, and `stefanzweifel/git-auto-commit-action` into the
Node.js 24 runtime ahead of GitHub's default switch. Keep
`python-version: "3.12"` for the analyzer; that setting is separate from the
GitHub Actions Node.js runtime.

## Option 3: Command Line Later

If Git is installed later, run:

```powershell
git init
git add .
git commit -m "Initial divine pattern research system"
git branch -M main
git remote add origin https://github.com/YOUR-USER/YOUR-REPO.git
git push -u origin main
```

## Important Guardrails

The collector stores source metadata, URLs, tags, and short summaries. It should
not store full copyrighted articles, books, or song lyrics.

The cloud workflow grows references over time, but findings should still be
reviewed before treating them as strong evidence.
