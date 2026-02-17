# Credentials

## Handling Instructions
- When any droid encounters or generates credentials, append them here with date, owner, purpose, and environment.
- Do not place secrets in client-side code or repos; keep them here and in secured env variables only.
- If an entry already exists, confirm it and update the "Last Updated" timestamp.

## Anvil Uplink / API Keys
- Name: Uplink (server)
- Purpose: Local Anvil Uplink connection
- Owner: MyBizz Ops
- Environment: Local
- Last Updated: 2026-02-02
- Value: **Stored in environment variable `ANVIL_UPLINK_KEY`**
- Setup: `export ANVIL_UPLINK_KEY=<value>` (Linux/Mac) or `$env:ANVIL_UPLINK_KEY="<value>"` (Windows PowerShell)

## GitHub / SCM Tokens
- Pending — add token/name, purpose, environment, owner, last updated, and value.

## Database / Storage Credentials
- Pending — add DB/storage endpoint, username, environment, owner, last updated, and value.

## Email / SMTP Services
- Pending — add service name, purpose, environment, owner, last updated, and value.

## Third-Party Integrations (Stripe/Paystack/etc.)
- Pending — add integration name, purpose, environment, owner, last updated, and value.

## IDE / Local Tool Licenses
- Pending — add tool name, scope, environment, owner, last updated, and value.

## OpenRouter
- Name: OpenRouter API Key
- Purpose: AI/ML API access
- Owner: MyBizz Ops
- Environment: Local/Development
- Last Updated: 2026-02-02
- Value: **Stored in environment variable `OPENROUTER_API_KEY`**
- Setup: `export OPENROUTER_API_KEY=<value>` (Linux/Mac) or `$env:OPENROUTER_API_KEY="<value>"` (Windows PowerShell)