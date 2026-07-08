# Bhasad Automation Instructions

## Mission

This repo manages the Bhasad website, YouTube description automation, publishing operations, and business planning.

## Rules

- Public-facing content must be English-only.
- Do not commit credentials, OAuth tokens, API keys, exports, or `.env` files.
- Prefer dry-run commands before live automation.
- Keep the `bhasad.org` link present in the website and YouTube footer.
- Keep scripts deterministic and safe for GitHub Actions.

## Common Commands

```bash
python scripts/validate_content.py
python scripts/security_audit.py
python scripts/update_yt_desc.py --descriptions scripts/descriptions.json --dry-run
```

## Repo Map

- `index.html`: static landing page.
- `scripts/descriptions.json`: video ID to description mapping.
- `scripts/update_yt_desc.py`: YouTube description updater.
- `scripts/validate_content.py`: English-only and brand-link validation.
- `scripts/security_audit.py`: lightweight repo safety scan.
- `docs/business-plan-bhasad-kpihub.md`: business and content operating plan.
