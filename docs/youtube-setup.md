# YouTube Data API Setup

Use this once to connect GitHub Actions to the YouTube channel.

## Google Cloud

1. Create or select a Google Cloud project.
2. Enable YouTube Data API v3.
3. Create OAuth 2.0 credentials.
4. Choose Desktop app as the app type.
5. Download the credentials JSON locally. Do not commit it.

## Refresh Token

Run the local helper and approve access with the YouTube channel owner account:

```bash
python scripts/get_youtube_refresh_token.py --credentials /path/to/credentials.json
```

The helper prints the values needed by GitHub Actions:

- client ID
- client secret
- refresh token

The updater expects these environment variables:

```bash
export YT_CLIENT_ID="..."
export YT_CLIENT_SECRET="..."
export YT_REFRESH_TOKEN="..."
```

Then test:

```bash
python scripts/update_yt_desc.py --descriptions scripts/descriptions.json --dry-run
```

Run live only after `scripts/descriptions.json` contains real video IDs:

```bash
python scripts/update_yt_desc.py --descriptions scripts/descriptions.json
```

## GitHub Secrets

Add these repository secrets in GitHub:

- `YT_CLIENT_ID`
- `YT_CLIENT_SECRET`
- `YT_REFRESH_TOKEN`

The GitHub workflow defaults to dry-run mode unless manually dispatched with `dry_run` set to `false`.
