# Data Integrity Check

Fires on every PR. Checks all server modules for correct Data Tables access patterns.

## Universal Rules
- Every Data Tables search includes instance_id filter where applicable
- No row deletion without explicit confirmation pattern
- All table column access uses only columns defined in anvil.yaml
- app_tables access only in server modules — never in client code
- tbl_audit_log access always wrapped in silent try/except — table may not exist
- No direct table manipulation in client code — all access via @anvil.server.callable

## Stage 1.2 — Authentication System

Look for these issues and fix them:

- `users` table — confirm the following columns exist in `anvil.yaml` before any code accesses them: `role` (string), `permissions` (simpleObject), `account_status` (string), `last_login` (datetime) — flag if any column is accessed in code but absent from the schema
- `server_auth/service.py` — `create_user` must write `role='customer'` and `account_status='active'` as defaults when creating a new user row; no other defaults are acceptable for a new signup
- `server_auth/service.py` — `authenticate_user` must update `last_login` on the users row after every successful authentication
- `server_auth/service.py` — `check_permission` must read the `permissions` simpleObject from the users row — never from a client-supplied parameter
- `server_auth/rbac.py` — `require_role` must read the `role` column from the users row returned by `anvil.users.get_user()` — never from a client-supplied value
- `rate_limits` table — confirm the table exists in `anvil.yaml` with columns: `identifier` (string), `count` (number), `reset_time` (datetime), `last_request` (datetime); flag if `check_rate_limit` in `server_shared/utilities.py` references columns not present in the schema

Pass if: all new `users` columns are present in `anvil.yaml`, `create_user` writes correct defaults, `last_login` is updated on auth, and `rate_limits` table schema matches what `check_rate_limit` accesses.
