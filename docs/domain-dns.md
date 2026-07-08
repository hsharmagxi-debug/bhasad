# bhasad.org DNS Setup

GitHub Pages is configured to use `bhasad.org` for this repository, but the domain registrar/DNS provider must point the domain to GitHub Pages before HTTPS can be enabled.

## Current DNS Observed

As of the last verification, `bhasad.org` and `www.bhasad.org` were still pointing to Squarespace records.

## Required Apex Records

Set these `A` records for `bhasad.org`:

```text
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

If the DNS provider supports IPv6, also set these `AAAA` records:

```text
2606:50c0:8000::153
2606:50c0:8001::153
2606:50c0:8002::153
2606:50c0:8003::153
```

## Required WWW Record

Set this CNAME:

```text
www.bhasad.org -> hsharmagxi-debug.github.io
```

## After DNS Propagates

1. Open the GitHub Pages settings for `hsharmagxi-debug/bhasad`.
2. Confirm the custom domain is `bhasad.org`.
3. Wait for certificate issuance.
4. Enable "Enforce HTTPS".
