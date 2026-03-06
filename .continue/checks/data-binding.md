# Data Binding Check

Fires on every PR. Checks all form files for correct data binding patterns.

## Universal Rules
- self.item set BEFORE self.init_components(**properties) in every form
- Write-back enabled in Designer for all input components bound to self.item (cannot be verified in code — flag for human review if new forms added)
- No manual change handlers where Write Back handles it
- refresh_data_bindings() called only where self.item is modified in place
- validate_form() returns bool and is called before every server call
- Invalid field state: role='outlined-error'
- Valid field reset: role='outlined'

## Stage 1.2 — Authentication System

Look for these issues and fix them:

- `LoginForm/__init__.py` — `self.item` must be set to a dict (e.g. `{'email': '', 'password': ''}`) before `self.init_components(**properties)` is called — flag if `self.item` is absent or set after `init_components`
- `SignupForm/__init__.py` — `self.item` must be set before `self.init_components(**properties)` — flag if absent or set after
- `PasswordResetForm/__init__.py` — `self.item` must be set before `self.init_components(**properties)` — flag if absent or set after
- `LoginForm/__init__.py` — `validate_form()` must be called inside the login handler before the `anvil.server.call` — flag if the server call is made without prior validation
- `SignupForm/__init__.py` — `validate_form()` must be called inside the signup handler before the `anvil.server.call` — flag if the server call is made without prior validation; confirm password and confirm-password fields are compared in `validate_form()` before the call
- `SignupForm/__init__.py` — the confirm-password field (`txt_confirm_password`) must be set to `role='outlined-error'` and show an error placeholder if the passwords do not match — not just a generic alert
- All three forms — no manual `change` event handlers on input fields where Write Back is configured — flag any handler that manually copies a field value into `self.item`

Pass if: `self.item` is set before `init_components()` in all three forms, `validate_form()` is called before every server call, password mismatch is shown inline via `outlined-error` role, and no manual change handlers duplicate Write Back behaviour.
