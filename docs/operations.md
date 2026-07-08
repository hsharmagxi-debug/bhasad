# Operations

## Local Checks

```bash
python scripts/validate_content.py
python scripts/security_audit.py
python scripts/update_yt_desc.py --descriptions scripts/descriptions.json --dry-run
```

## Add a Video Description

1. Open `scripts/descriptions.json`.
2. Add the YouTube video ID as the key.
3. Add the final English description as the value.
4. Run a dry run.
5. Commit and push.

## Deploy the Website

Run local checks:

```bash
scripts/deploy.sh --dry-run
```

Push to `main`. GitHub Pages deploys after validation passes.

## Weekly Review

- Review YouTube backlog and content schedule.
- Check GitHub Actions.
- Update the business plan with new learnings.
- Convert high-value ideas into GitHub issues.
