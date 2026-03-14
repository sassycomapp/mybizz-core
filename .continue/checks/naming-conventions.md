# Naming Conventions Check

Fires on every PR. Checks all files for correct Mybizz naming conventions.

## Universal Rules
- Form files live at client_code/{package}/{FormName}/__init__.py — no standalone FormName.py files
- Server modules live at server_code/{package}/service.py
- Component prefixes: txt_ TextBox, btn_ Button, lbl_ Text/Heading, dd_ DropdownMenu, cb_ Checkbox, rp_ RepeatingPanel, dg_ DataGrid, dp_ DatePicker, sw_ Switch, link_ Link, img_ Image, col_ ColumnPanel, lp_ LinearPanel, flow_ FlowPanel, grid_ GridPanel, menu_ Menu
- No tbl_ prefix on Data Tables — tables named without prefix (e.g. rate_limits not tbl_rate_limits)
- Server packages named server_{vertical} (e.g. server_auth, server_settings)
- Client packages named by vertical only (e.g. auth, settings)
- No numbered prefixes (NN_) in any filename or cross-reference

## Stage 1.2 — Authentication System

Look for these issues and fix them:

- Forms must be named exactly `LoginForm`, `SignupForm`, `PasswordResetForm` — PascalCase, no underscores, no abbreviations (e.g. `LoginFrm` or `login_form` are violations)
- Server module must be at `server_code/server_auth/service.py` — not `server_code/auth/service.py` or `server_code/server_auth/auth_service.py`
- RBAC module must be at `server_code/server_auth/rbac.py` — not `server_code/server_auth/permissions.py` or any other name
- `LoginForm/__init__.py` — email input must be named `txt_email`; password input must be named `txt_password`; submit button must be named `btn_login`
- `SignupForm/__init__.py` — email input `txt_email`, password input `txt_password`, confirm-password input `txt_confirm_password`, submit button `btn_signup`
- `PasswordResetForm/__init__.py` — email input `txt_email`, submit button `btn_reset`, back link `link_back_to_login`
- `server_auth/service.py` — function names must be exactly `authenticate_user`, `create_user`, `reset_password`, `check_permission` — no aliases or wrappers with different names exposed as callables
- `server_auth/rbac.py` — decorator names must be exactly `require_role` and `require_permission`
- Client package must be `client_code/auth/` — not `client_code/authentication/` or `client_code/login/`

Pass if: all three form names match exactly, all component names follow the `txt_`/`btn_`/`link_` prefix conventions, server module paths are exactly as specified, and all four service function names match exactly.

## Stage 1.4 — Settings & Configuration

Look for these issues and fix them:

- `SettingsForm/__init__.py` — the form file must be at `client_code/settings/SettingsForm/__init__.py` — flag if it exists as `client_code/settings/SettingsForm.py` (standalone file, not a folder)
- `server_settings/service.py` — the server module must be at `server_code/server_settings/service.py` — flag if it is at `server_code/settings/service.py` or any other path
- `SettingsForm/__init__.py` — tab button components must be named `btn_tab_business`, `btn_tab_email`, `btn_tab_payments`, `btn_tab_theme` — flag any tab button using a different prefix (e.g. `tab_business` without `btn_`) or a different naming pattern
- `SettingsForm/__init__.py` — tab panel components must be named `col_business`, `col_email`, `col_payments`, `col_theme` — flag any panel using a different prefix (e.g. `pnl_business` or `panel_business`)
- `SettingsForm/__init__.py` — gateway panel components must be named `col_stripe`, `col_paystack`, `col_paypal` — flag any gateway panel using a deprecated `pnl_` prefix or any other naming pattern
- `SettingsForm/__init__.py` — the logo file loader must be named `fu_logo`; the logo preview image must be named `img_logo_preview` — flag either component using a different prefix
- `SettingsForm/__init__.py` — the tab bar LinearPanel must be named `lp_tab_bar` — flag if it uses a different prefix or name
- `server_settings/service.py` — the module-level secret columns constant must be named `_PAYMENT_SECRET_COLUMNS` in `UPPER_SNAKE_CASE` with a leading underscore indicating module-private scope — flag if it uses a different casing or name

Pass if: `SettingsForm` is a folder at the correct path, all tab buttons use `btn_tab_*` names, all tab panels use `col_*` names, gateway panels use `col_*` names, `fu_logo` and `img_logo_preview` are correctly named, `lp_tab_bar` is correctly named, and `_PAYMENT_SECRET_COLUMNS` follows the naming convention.
