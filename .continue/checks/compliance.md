# Compliance Check

Fires on every PR. Checks all forms and server modules for regulatory compliance.

## Universal Rules
- SignupForm must include visible links to Terms & Conditions and Privacy Policy (GDPR/POPIA/CCPA §1.1)
- No personal data logged in plain text — email addresses in logs must be normalised only
- audit_log table write attempted for all auth events — silent fail if table absent
- Password reset always returns identical message regardless of email validity (OWASP A07:2021)
- No user enumeration possible via timing or message differences in auth responses
- instance_id enforced server-side — never derived from client input

## Stage 1.2 — Authentication System

Look for these issues and fix them:

- `SignupForm/__init__.py` — must contain a visible `link_terms` component linking to the Terms & Conditions page and a visible `link_privacy` component linking to the Privacy Policy page — both must be present and visible at all times (GDPR/POPIA/CCPA requirement per policy_security_compliance.md §1.1)
- `SignupForm/__init__.py` — must contain a `cb_agree_terms` Checkbox that the user must check before the signup button is enabled — flag if the signup server call can be triggered without the checkbox being checked
- `server_auth/service.py` — `authenticate_user` must attempt to write an entry to `audit_log` on every login attempt (success and failure) — the write must be wrapped in a silent `try/except` so a missing `audit_log` table does not break authentication
- `server_auth/service.py` — `create_user` must attempt to write an entry to `audit_log` on every new account creation — silent `try/except` required
- `server_auth/service.py` — no email address or password may appear in plain text in any log entry — log only normalised identifiers (e.g. email domain only, or a hash) if logging user identity
- `server_auth/service.py` — `reset_password` must return an identical response for registered and unregistered emails — flag any code path that produces a different message, status code, or timing for the two cases

Pass if: `SignupForm` contains visible Terms and Privacy links, the agree-terms checkbox gates the signup call, `audit_log` writes are present and silently fail-safe, no plain-text emails appear in logs, and `reset_password` returns identical responses for all email inputs.
