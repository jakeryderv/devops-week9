# Week 9 supporting evidence

The submission PDF is `../week9-evidence.pdf`, with source in `../evidence-template.md`. `commands/` contains actual command output with capture times and exit codes. `transcripts/` provides readable browser views of selected output; excerpts link to the complete logs. `screenshots/` contains the ten milestone screenshots and supplemental browser evidence. The command-output screenshots are browser captures of the original saved transcripts; the GitHub screenshots are captures of the live repository, PR, and Actions pages.

No `.env` contents are included. The baseline image is `helpdesk:week9-before`; the hardened image is `helpdesk:week9-after`. Scan counts reflect the captured scan and may change with new image versions or vulnerability data. Non-root hardening does not claim to fix the reported package CVEs.

## Repeat the validation

From the repository root, after installing `requirements.txt` into `.venv`:

```bash
python3 docs/evidence/capture-command.py repeat-tests .venv/bin/python -m pytest -v
docker compose up -d --build
docker cp docs/evidence/verify-app.py week9-web-1:/tmp/week9-smoke.py
python3 docs/evidence/capture-command.py repeat-app docker compose exec -T web python /tmp/week9-smoke.py
```

The application check creates one test request and changes its status from Open to Closed using Streamlit's AppTest interface against the running PostgreSQL database. `verify-policy.py` requires PyYAML, Git, and Docker; it checks both the passing inputs and the failing tracked-file/root-image cases without tracking the real `.env`.

To save another command, run `python3 docs/evidence/capture-command.py NAME COMMAND [ARGS...]`. Never pass secrets as command arguments: both the command and its combined stdout/stderr are saved.

## Browser evidence sources

Captured with an isolated Playwright Chromium session on October 30, 2026. GitHub code and checks were publicly viewable without transferring browser credentials.

| Image | Source |
| --- | --- |
| `01-baseline.png` | `transcripts/01-baseline.html` |
| `02-env.png` | `transcripts/02-env.html` |
| `03-dependabot.png` | GitHub branch `security/week9-devsecops`, `.github/dependabot.yml` |
| `04-scout.png` | `transcripts/04-scout.html` |
| `05-recommendations.png` | `transcripts/05-recommendations.html` |
| `06-dockerfile.png` | GitHub branch `security/week9-devsecops`, `Dockerfile` |
| `07-uid.png` | `transcripts/07-uid.html` |
| `08-workflow.png` | GitHub branch `security/week9-devsecops`, `.github/workflows/security.yml` |
| `09-security-checks.png` | <https://github.com/jakeryderv/devops-week9/actions/runs/41086244268> |
| `10-pull-request.png` | <https://github.com/jakeryderv/devops-week9/pull/2/checks> |
| `pr-files.png` | <https://github.com/jakeryderv/devops-week9/pull/2/files> |
| `app-running.png` | <http://localhost:8501> after hardening |
| `security-workflow-full.png` | Supplemental full workflow view on GitHub |

The PDF includes the ten milestones, a supporting changed-files view, and all four reflections. The raw command logs preserve baseline timing even though the screenshots of those transcripts were captured later.

## Rebuild the PDF

Install ReportLab into a separate document environment, then run:

```bash
python3 docs/evidence/build-report.py
pdfinfo docs/week9-evidence.pdf
pdftoppm -png docs/week9-evidence.pdf /tmp/week9-evidence-page
```

Inspect the rendered pages after changing the report. The builder fails if a required screenshot is missing or the Markdown still contains pending screenshot markers.
