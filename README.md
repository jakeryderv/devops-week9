# SDI 4213 Week 9 - DevSecOps Individual Exercise

This repository continues the **Help Desk / Service Request Tracker** used in Week 7. The application and Docker Compose stack are already functional. Your Week 9 task is to improve the security of the software delivery workflow.

## Week 9 focus
You will practice:
- secret and `.env` hygiene
- Dependabot configuration
- Docker image vulnerability scanning with Docker Scout
- interpreting CVE findings and recommendations
- running the application container as a non-root user
- adding automated security policy checks to GitHub Actions
- documenting security evidence with screenshots

## Baseline application
The stack contains:
- Streamlit web application
- PostgreSQL database
- Adminer database interface
- named PostgreSQL volume

## Before you begin
Copy `.env.example` to `.env` and replace the sample password with a local development password. Never commit `.env`.

Windows PowerShell:
```powershell
Copy-Item .env.example .env
```

macOS/Linux:
```bash
cp .env.example .env
```

## Run tests
```bash
python -m pytest -v
```

## Start the application
```bash
docker compose up -d --build
docker compose ps
```

Web app: http://localhost:8501
Adminer: http://localhost:8080

## Assignment
Follow `docs/Week9_Individual_Exercise.docx`.

## Important
Never put a real password, token, cloud credential, SSH key, or API key into this repository or into your screenshot evidence.

## Week 9 security controls

- `.env` is excluded from Git and the Docker build context; `.env.example` contains placeholders only.
- Dependabot checks pip and GitHub Actions dependencies weekly.
- The application image runs as `appuser` (UID 10001), with a writable `/app` for the SQLite fallback.
- `Security Checks` rejects a tracked `.env` or an image that runs as UID 0 on pull requests and pushes to `main`.
- PostgreSQL 18 stores its data in the named volume mounted at `/var/lib/postgresql`.

The submission PDF is [docs/week9-evidence.pdf](docs/week9-evidence.pdf), with editable source in [docs/evidence-template.md](docs/evidence-template.md).
Saved commands and outputs are in [docs/evidence/commands](docs/evidence/commands).
Docker Scout findings describe package vulnerabilities; passing the non-root policy does not mean the image has no CVEs.

To repeat the main security checks:

```bash
docker build -t helpdesk:week9-after .
docker run --rm --entrypoint id helpdesk:week9-after -u
docker scout cves helpdesk:week9-after
```
