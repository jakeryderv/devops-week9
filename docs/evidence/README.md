# Week 9 supporting evidence

The report source is `../evidence-template.md`. `commands/` contains actual command output with capture times and exit codes. `transcripts/` provides readable browser views of selected output; excerpts link to the complete logs. `screenshots/` is reserved for the ten milestone screenshots and supplemental browser evidence.

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
