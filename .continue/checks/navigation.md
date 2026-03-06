# Navigation Check

Fires on every PR. Checks all forms for correct navigation patterns.

## Universal Rules
- open_form() used only in auth forms and startup — all other navigation via navigate_to
- NavigationLinks use navigate_to property — no manual click handlers
- navigate_by_role() used after every successful login — no hardcoded form targets
- require_auth() called in __init__ of every non-auth form before init_components()
- open_form() in __init__ always followed immediately by return

## Stage 1.2 — Authentication System

Look for these issues and fix them:

- `client_code/auth/LoginForm/__init__.py` — after a successful login, navigation must call `navigate_by_role()` from `client_code/shared/navigation_helpers.py` — never hardcode `open_form('DashboardForm')` or any specific form name
- `client_code/auth/LoginForm/__init__.py` — `open_form('LoginForm')` must not appear anywhere inside `LoginForm` itself
- Startup form `__init__.py` — must call `anvil.users.get_user()` and branch to `navigate_by_role()` if a user is logged in, or remain on the startup/home form if not — this check must appear before `self.init_components(**properties)` and be followed immediately by `return`
- `client_code/auth/SignupForm/__init__.py` — after successful signup, must navigate to `LoginForm` via `open_form('LoginForm')` followed immediately by `return` — no further form logic after the navigation call
- `client_code/auth/PasswordResetForm/__init__.py` — must contain a `link_back_to_login` component that navigates to `LoginForm` via `open_form('LoginForm')` — not a NavigationLink (auth forms have no NavigationDrawerLayout)
- No `@router.route` decorator on `LoginForm`, `SignupForm`, or `PasswordResetForm` — auth forms use `open_form()` navigation, not the Routing dependency

Pass if: post-login navigation uses `navigate_by_role()` only, the startup form routes by role before `init_components()`, all `open_form()` calls in auth forms are immediately followed by `return`, and no auth form uses `@router.route`.
