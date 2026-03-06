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
