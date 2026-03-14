# Code Quality Check

Fires on every PR. Checks all Python files for code quality standards.

## Universal Rules
- Every non-trivial function has a docstring with Args, Returns, Raises
- Type hints on all public server functions
- Event handlers contain zero logic — call private methods only
- open_form() in __init__ always followed immediately by return
- self.item set BEFORE self.init_components(**properties) in every form
- No TODOs or placeholder stubs in any file
- logger = logging.getLogger(__name__) at module top in all server modules
- logger.info at entry of every @anvil.server.callable function
- No unused imports in any file

## Stage 1.2 — Authentication System

Look for these issues and fix them:

- `server_auth/service.py` — all four functions (`authenticate_user`, `create_user`, `reset_password`, `check_permission`) must have docstrings with Args, Returns, and Raises sections
- `server_auth/rbac.py` — `require_role` and `require_permission` must have docstrings documenting the `allowed_roles` / `permission_name` parameter and what exception is raised on denial
- `server_auth/service.py` — all four public functions must have type hints on all parameters and return type annotated as `dict`
- `LoginForm/__init__.py` — `btn_login_click` handler must contain zero logic — it must call a private method (e.g. `self._handle_login()`) that contains the logic
- `SignupForm/__init__.py` — `btn_signup_click` handler must contain zero logic — it must call a private method
- `PasswordResetForm/__init__.py` — `btn_reset_click` handler must contain zero logic — it must call a private method
- `server_auth/service.py` — password validation logic must be extracted to a standalone pure function (e.g. `validate_password_strength(password: str) -> tuple[bool, str]`) so it can be unit-tested without Anvil
- `server_auth/rbac.py` — no module-level mutable state (no global dicts or lists that accumulate data across requests)

Pass if: all four service functions have complete docstrings and type hints, all three form button handlers delegate to private methods, and password validation is a standalone testable function.

## Stage 1.4 — Settings & Configuration

Look for these issues and fix them:

- `server_settings/service.py` — all eight `@anvil.server.callable` functions must have docstrings with Args, Returns, and Raises sections — flag any that have a docstring missing one of these three sections
- `server_settings/service.py` — all eight callable functions must have type hints on all parameters and return type annotated as `-> dict` — flag any function missing parameter or return type annotations
- `SettingsForm/__init__.py` — all four tab button click handlers (`btn_tab_business_click`, `btn_tab_email_click`, `btn_tab_payments_click`, `btn_tab_theme_click`) must contain zero logic — each must call only `self._activate_tab(...)` — flag any handler that contains inline logic beyond a single method call
- `SettingsForm/__init__.py` — all four save button click handlers (`btn_save_business_click`, `btn_save_email_click`, `btn_save_payments_click`, `btn_save_theme_click`) must contain zero logic — each must call only the corresponding private `_save_*` method — flag any handler that contains inline logic
- `SettingsForm/__init__.py` — `btn_test_email_click` must contain zero logic — it must call only `self._test_email()` — flag if the handler contains inline logic
- `SettingsForm/__init__.py` — `dd_active_gateway_change` must contain zero logic — it must call only `self._show_gateway_panel(...)` — flag if the handler contains inline logic
- `server_settings/service.py` — `_PAYMENT_SECRET_COLUMNS` is a module-level constant defined as a `frozenset`; confirm it is named in `UPPER_SNAKE_CASE` and is not reassigned anywhere in the module
- `server_settings/service.py` — `create_initial_config` is not decorated with `@anvil.server.callable`; confirm this is intentional (called internally from signup flow only) and that no client code calls it directly

Pass if: all eight callable functions have complete docstrings and type hints, all six event handlers in `SettingsForm` delegate entirely to private methods, `_PAYMENT_SECRET_COLUMNS` is a module-level frozenset constant, and `create_initial_config` has no `@anvil.server.callable` decorator.
