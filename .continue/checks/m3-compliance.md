# M3 Compliance Check

Fires on every PR. Checks all form files for M3 component compliance.

## Universal Rules
- No legacy Label component — Text or Heading only
- No Anvil Extras components where M3 alternatives exist
- No hardcoded colours — theme: prefix only
- All form inputs use role='outlined'
- Error states use role='outlined-error'
- Maximum 1 filled button per screen
- Button hierarchy: filled → outlined → text
- Auth forms use BlankLayout (Custom Form) — no NavigationDrawerLayout
- NavigationLinks use navigate_to property — no click handlers
- No XYPanel for layout
- txt_password.hide_text = True set in __init__ for all password fields — type='password' not supported in M3

## Stage 1.2 — Authentication System

Look for these issues and fix them:

- `LoginForm/__init__.py` — form must use `BlankLayout` (Custom Form with no NavigationDrawerLayout parent) — flag if any layout wrapper is present
- `SignupForm/__init__.py` — form must use `BlankLayout` — flag if any layout wrapper is present
- `PasswordResetForm/__init__.py` — form must use `BlankLayout` — flag if any layout wrapper is present
- `LoginForm/__init__.py` — the email field must be named `txt_email` and the password field `txt_password`; confirm `txt_password.hide_text = True` is set in `__init__` (M3 does not support `type='password'` in code)
- `SignupForm/__init__.py` — all text input fields must use `role='outlined'`; confirm no field uses `role='filled'` or has no role set
- `SignupForm/__init__.py` — the submit button must use `role='filled-button'`; any secondary action (e.g. "Back to login") must use `role='outlined'` or `role='text-button'` — never a second `filled-button`
- `LoginForm/__init__.py` — the submit button must use `role='filled-button'`; the "Forgot password?" link must be a `Link` component (`link_forgot_password`) — not a second button
- `PasswordResetForm/__init__.py` — the submit button must use `role='filled-button'`; a back/cancel action must use `role='outlined'` or `role='text-button'`
- All three forms — no `Label` component present anywhere; all text uses `Text` or `Heading` components only

Pass if: all three auth forms use BlankLayout, all inputs use `role='outlined'`, `txt_password.hide_text = True` is set in code, no `Label` components are present, and button hierarchy is correct (max 1 filled-button per form).
