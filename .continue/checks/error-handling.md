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

## Stage 1.4 — Settings & Configuration

Look for these issues and fix them:

- `server_settings/service.py` — `test_email_connection` must catch `smtplib.SMTPAuthenticationError` specifically before `smtplib.SMTPException`, and `smtplib.SMTPException` before `socket.error`, and `socket.error` before `tables.TableError`, and `tables.TableError` before the general `Exception` — flag any ordering that catches a broader exception before a narrower one
- `server_settings/service.py` — `test_email_connection` must log `logger.warning(...)` with `exc_info=True` for `SMTPAuthenticationError`, `SMTPException`, and `socket.error` — flag if any of these three are caught without a warning log
- `server_settings/service.py` — `save_payment_config` contains a defensive `assert` that secret columns are not in the write dict; if this assert fires it will raise `AssertionError` which is not caught — confirm this is intentional (hard fail on programmer error) and that no production code path can trigger it
- `server_settings/service.py` — all eight `@anvil.server.callable` functions must log `logger.info(...)` at entry — flag any callable that does not have an entry log call as its first statement after the authentication check
- `SettingsForm/__init__.py` — `_save_email` calls `int(self.txt_smtp_port.text.strip())` without a try/except; this conversion is guarded by `_validate_email()` which is called first — confirm `_validate_email` always runs before `_save_email` proceeds to the conversion, and that no code path reaches the `int()` call with a non-numeric string
- `SettingsForm/__init__.py` — all four `load_*` methods display an `alert(...)` on `result['success'] == False`; confirm no raw exception traceback or internal server error message is shown to the user — the message shown must be `result['error']` only

Pass if: `test_email_connection` catches exceptions in narrowest-to-broadest order with warning logs on all SMTP/socket exceptions, all eight callables log entry, `_validate_email` always precedes the `int()` conversion in `_save_email`, and all client error displays show only `result['error']` strings.
