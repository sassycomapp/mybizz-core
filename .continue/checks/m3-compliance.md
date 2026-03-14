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

## Stage 1.4 — Settings & Configuration

Look for these issues and fix them:

- `SettingsForm/__init__.py` — the form uses a manual tab pattern (four `btn_tab_*` buttons + four `col_*` panels toggled by `_activate_tab`); the active tab button must use `role='filled'` and inactive tab buttons must use `role='outlined'` — flag if any tab button uses `role='filled-button'` (wrong role name for this pattern) or has no role set
- `SettingsForm/__init__.py` — `self.lp_tab_bar.orientation = 'horizontal'` is set in code because it cannot be set in the Designer; confirm `lp_tab_bar` is a `LinearPanel` component — flag if a `FlowPanel` or `ColumnPanel` is used instead
- `SettingsForm/__init__.py` — `self.txt_smtp_password.hide_text = True` is set in `__init__`; confirm no `type='password'` assignment is attempted anywhere in the file (M3 does not support this in code)
- `SettingsForm/__init__.py` — all TextBox components used for data entry (`txt_business_name`, `txt_contact_email`, `txt_smtp_host`, `txt_smtp_port`, `txt_smtp_username`, `txt_smtp_password`, `txt_from_email`, `txt_from_name`, `txt_primary_color`, `txt_accent_color`) must use `role='outlined'` as their default state — flag any that have no role or use a different role
- `SettingsForm/__init__.py` — `_set_field_error` sets `role='outlined-error'` and clears the text; `_clear_field_error` resets to `role='outlined'` — confirm no field is left in `outlined-error` state after a successful save (i.e. `_clear_field_error` is called for all validated fields that pass)
- `SettingsForm/__init__.py` — `dd_active_gateway` and `dd_font_family` and `dd_header_style` are `DropdownMenu` components; confirm all three have `role='outlined'` set (either in Designer or in code)
- `SettingsForm/__init__.py` — `img_logo_preview` is an `Image` component; confirm it uses the `img_` prefix as required for multi-image forms

Pass if: tab buttons use `role='filled'`/`role='outlined'` (not `filled-button`), `lp_tab_bar` is a `LinearPanel`, `hide_text = True` is used instead of `type='password'`, all data-entry TextBoxes default to `role='outlined'`, error fields are cleared after successful validation, and all three DropdownMenus have `role='outlined'`.
