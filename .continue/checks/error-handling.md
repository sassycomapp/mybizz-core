# Error Handling Check

Fires on every PR. Checks all Python files for correct exception handling patterns.

## Universal Rules
- No bare except: — named exceptions only
- Specific exceptions caught before general Exception
- No except block that passes silently without logging
- logger.error(exc_info=True) on all unexpected exceptions
- Traceback preserved: bare raise or raise X from e
- anvil.server.TimeoutError caught in all client server calls
- anvil.server.AnvilWrappedError caught in all client server calls
- No print() anywhere in server code — logger only

## Stage 1.2 — Authentication System

Look for these issues and fix them:

- `server_auth/service.py` — `authenticate_user` must catch `anvil.users.AuthenticationFailed` specifically before the general `Exception` catch — not just a bare `Exception` for all auth failures
- `server_auth/service.py` — `create_user` must catch `anvil.users.UserExists` specifically before the general `Exception` catch — not just a bare `Exception` for duplicate email
- `server_auth/service.py` — all four functions (`authenticate_user`, `create_user`, `reset_password`, `check_permission`) must log entry via `logger.info(...)` at the top of each function body
- `server_auth/rbac.py` — `require_role` and `require_permission` must log a `logger.warning(...)` when access is denied — include the function name being protected, not the user's role
- `LoginForm/__init__.py` — the login button handler must catch `anvil.server.AnvilWrappedError` and display a user-friendly message — not a raw exception traceback
- `LoginForm/__init__.py` — the login button handler must catch `anvil.server.TimeoutError` separately and display a timeout-specific message
- `PasswordResetForm/__init__.py` — the submit handler must catch `anvil.server.AnvilWrappedError` and `anvil.server.TimeoutError` separately

Pass if: all auth-specific Anvil exceptions (`AuthenticationFailed`, `UserExists`) are caught before the general `Exception` handler, all four service functions log entry, and all client handlers catch both `AnvilWrappedError` and `TimeoutError`.
