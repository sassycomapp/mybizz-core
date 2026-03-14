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

## Stage 1.4 — Settings & Configuration

Look for these issues and fix them:

- `server_settings/service.py` — `get_business_profile` reads from `app_tables.business_profile` without an `instance_id` filter; confirm this table is single-row-per-instance by design and that no cross-tenant rows can exist — flag if the table has an `instance_id` column that is not being filtered
- `server_settings/service.py` — `get_email_config`, `get_payment_config`, and `get_theme_config` all use `list(app_tables.<table>.search())` and take `rows[0]` — confirm each of these tables (`email_config`, `payment_config`, `theme_config`) is defined as single-row-per-instance in `anvil.yaml` and has no `instance_id` column that would require filtering
- `server_settings/service.py` — `save_business_profile` writes an `updated_at` datetime field; confirm the `business_profile` table has an `updated_at` column of type `datetime` in `anvil.yaml`
- `server_settings/service.py` — `save_email_config` always sets `configured = False` on every save; confirm the `email_config` table has a `configured` column of type `bool` and a `configured_at` column of type `datetime` in `anvil.yaml`
- `server_settings/service.py` — `save_payment_config` writes `stripe_connected`, `paystack_connected`, and `paypal_connected` boolean columns; confirm all three exist in `anvil.yaml` for the `payment_config` table
- `server_settings/service.py` — `test_email_connection` updates `configured = True` and `configured_at = now` on the `email_config` row after a successful SMTP send; confirm neither field is written anywhere else that could bypass the live-test requirement
- `server_settings/service.py` — `create_initial_config` writes to `app_tables.config` using `key` and `value` columns; confirm the `config` table has columns `key` (string), `value` (simpleObject), `category` (string), `updated_at` (datetime), and `updated_by` (link to users) in `anvil.yaml`

Pass if: all four settings tables (`business_profile`, `email_config`, `payment_config`, `theme_config`) are confirmed single-row-per-instance in `anvil.yaml`, all columns accessed in `service.py` exist in the schema, `configured` is only set to `True` by `test_email_connection`, and `create_initial_config` columns match the `config` table schema.
