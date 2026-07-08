# Bhasad

AI-powered YouTube channel automation, static website deployment, and business planning workspace for `bhasad.org`.

## What This Repo Does

- Updates YouTube video descriptions from `scripts/descriptions.json`.
- Deploys the static website in `index.html` through GitHub Pages.
- Runs content validation, secret scanning, and lightweight security checks.
- Keeps the Bhasad operating plan, publishing calendar, and issue templates in version control.

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/validate_content.py
python scripts/security_audit.py
python scripts/update_yt_desc.py --descriptions scripts/descriptions.json --dry-run
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts\validate_content.py
python scripts\security_audit.py
python scripts\update_yt_desc.py --descriptions scripts\descriptions.json --dry-run
```

## YouTube Setup

Add these GitHub Actions secrets before running the live YouTube workflow:

- `YT_CLIENT_ID`
- `YT_CLIENT_SECRET`
- `YT_REFRESH_TOKEN`

See [docs/youtube-setup.md](docs/youtube-setup.md) for the OAuth flow.

## Automation

- `.github/workflows/yt-desc.yml` updates YouTube descriptions manually or when `scripts/descriptions.json` changes.
- `.github/workflows/deploy.yml` validates content and deploys the static site to GitHub Pages.
- `.github/workflows/audit.yml` runs scheduled and manual repo audits.

## Operating Rules

- Keep public content English-only.
- Keep credentials out of git.
- Use dry runs before live YouTube updates.
- Use `docs/business-plan-bhasad-kpihub.md` as the business control center.
