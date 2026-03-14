# Response Envelope Check

Fires on every PR. Checks all @anvil.server.callable functions for correct envelope pattern.

## Universal Rules
- Every @anvil.server.callable must return exactly:
  {'success': True, 'data': x} on success
  {'success': False, 'error': str} on failure
- No bare returns from callable functions
- No extra top-level keys beyond success, data, error
- Client code always checks result['success'] before accessing result['data']
- No callable function returns None

## Stage 1.2 — Authentication System

Look for these issues and fix them:

- `server_auth/service.py` — `authenticate_user` must return `{'success': True, 'data': {'user_id': ..., 'role': ...}}` on success and `{'success': False, 'error': 'Invalid credentials'}` on failure — no other shape permitted
- `server_auth/service.py` — `create_user` must return `{'success': True, 'data': {'user_id': ...}}` on success and `{'success': False, 'error': str(e)}` on failure
- `server_auth/service.py` — `reset_password` must return `{'success': True, 'data': {'message': 'If that email is registered, a reset link has been sent.'}}` on both found and not-found paths — identical envelope in both cases
- `server_auth/service.py` — `check_permission` must return `{'success': True, 'data': {'has_permission': bool}}` — not a bare boolean
- `server_auth/rbac.py` — decorator-wrapped functions that raise on access denial must still be called via a `@anvil.server.callable` outer function that catches the exception and returns `{'success': False, 'error': 'Access denied'}`

Pass if: all four functions in `server_auth/service.py` return the exact envelope shape above, and access-denied paths always produce `{'success': False, 'error': 'Access denied'}` rather than raising unhandled exceptions to the client.

## Stage 1.4 — Settings & Configuration

Look for these issues and fix them:

- `server_settings/service.py` — `get_business_profile` must return `{'success': True, 'data': {}}` when no row exists — not `{'success': True, 'data': None}` or a bare empty response
- `server_settings/service.py` — `save_business_profile` must return `{'success': True, 'data': None}` on success — not `{'success': True}` without a `data` key
- `server_settings/service.py` — `get_email_config`, `get_payment_config`, and `get_theme_config` must each return `{'success': True, 'data': {}}` when no row exists — not `None` or a missing `data` key
- `server_settings/service.py` — `save_email_config`, `save_payment_config`, and `save_theme_config` must each return `{'success': True, 'data': None}` on success — flag any that return `{'success': True}` without the `data` key
- `server_settings/service.py` — `test_email_connection` must return `{'success': True, 'data': '<message string>'}` on success and `{'success': False, 'error': '<exception message>'}` on failure — flag if the success path returns the message under any key other than `data`
- `SettingsForm/__init__.py` — all eight `anvil.server.call(...)` return values must be checked for `result['success']` before accessing `result['data']` — flag any call site that accesses `result['data']` without first checking `result['success']`

Pass if: all eight server functions return the exact `{'success': bool, 'data'/'error': ...}` envelope, empty-row paths return `{'success': True, 'data': {}}`, save functions return `{'success': True, 'data': None}`, `test_email_connection` returns the message under `data`, and all client call sites check `result['success']` before accessing `result['data']`.
