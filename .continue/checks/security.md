# Security Check

Fires on every PR. Checks all server modules and client forms for security violations.

## Universal Rules
- No Data Tables access from client code — server functions only
- instance_id never accepted as a client parameter
- No hardcoded secrets, keys, or passwords in any file
- All @anvil.server.callable functions validate inputs before any other action
- Rate limiting applied before authentication attempts
- Password reset always returns identical message regardless of email existence (enumeration prevention)
- No internal exception messages leaked to client — generic user-facing messages only
- Server Uplink key never committed to any source file

## Stage 1.2 — Authentication System

Look for these issues and fix them:

- `server_auth/service.py` — `authenticate_user` must not accept `instance_id` as a parameter; user identity must be derived from `anvil.users.get_user()` server-side only
- `server_auth/service.py` — `reset_password` must return an identical response regardless of whether the email exists in the users table — no enumeration via message or timing differences
- `server_auth/service.py` — `create_user` must validate password strength (min 8 chars, 1 uppercase, 1 lowercase, 1 digit) before calling any Anvil signup function
- `server_auth/rbac.py` — `require_role` and `require_permission` decorators must raise `Exception('Access denied')` only — never include the specific role name or permission name in the error string returned to the client
- `server_auth/rbac.py` — both decorators must call `anvil.users.get_user()` server-side — never accept role or permission claims from client-supplied parameters
- `server_auth/service.py` — `authenticate_user` must call `check_rate_limit` from `server_shared/utilities.py` before attempting authentication; must return `{'success': False, 'error': 'Rate limit exceeded...'}` if limit is hit
- `LoginForm/__init__.py` — no password value may be stored in `self.item` or any form attribute after the authentication call completes
- `LoginForm/__init__.py` — failed login must return the same user-facing message for wrong email and wrong password — no enumeration
- `SignupForm/__init__.py` — password field must be cleared immediately after the server call returns — no raw password persists in form state
- `PasswordResetForm/__init__.py` — must display the same success message regardless of whether the email is registered

Pass if: all auth server functions derive identity from `anvil.users` only, `reset_password` and `authenticate_user` return identical messages for all invalid inputs, passwords are never stored in form state after use, and `require_role`/`require_permission` raise only generic error strings.
