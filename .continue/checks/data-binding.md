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

## Stage 1.4 — Settings & Configuration

Look for these issues and fix them:

- `SettingsForm/__init__.py` — `SettingsForm` does not use `self.item` data binding; all field population is done manually in `load_*` methods by direct assignment to component `.text` and `.selected_value` properties — confirm no `self.item` is set before `init_components()` (it is not needed here) and that no Write Back bindings are configured in the Designer for this form
- `SettingsForm/__init__.py` — `load_business_profile` populates fields by direct assignment (e.g. `self.txt_business_name.text = data.get('business_name', '')`); confirm that `_save_business` reads values back from the component properties (e.g. `self.txt_business_name.text`) rather than from `self.item` — flag if `self.item` is referenced in any save method
- `SettingsForm/__init__.py` — `_validate_business` and `_validate_email` use `_set_field_error` to set `role='outlined-error'` and clear the text, and `_clear_field_error` to reset to `role='outlined'`; confirm `_clear_field_error` is called for every field that passes validation, not only for fields that fail — flag if a field that previously had an error is not reset on a subsequent valid submission
- `SettingsForm/__init__.py` — `_validate_email` checks `txt_smtp_port` for non-empty and then separately checks that the value parses as an integer; confirm the integer check only runs when the field is non-empty (i.e. it is inside the `if self.txt_smtp_port.text.strip():` branch) — flag if the `int()` conversion can be attempted on an empty string

Pass if: `SettingsForm` uses no `self.item` data binding (manual load/save pattern throughout), all save methods read from component properties not `self.item`, `_clear_field_error` is called for every field that passes validation, and the port integer check is guarded by a non-empty check.
