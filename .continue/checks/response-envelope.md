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
