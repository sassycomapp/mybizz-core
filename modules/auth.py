import anvil.server
"""
Auth Package

M3-compliant authentication module.

Contains:
    - LoginForm: User login
    - SignupForm: New account registration
    - PasswordResetForm: Password reset request
    - ui_helpers: Display formatting utilities

Architecture:
    UI Forms → server_code/server_auth/ (business logic)
"""

from .ui_helpers import (
    format_user_display_name,
    get_user_initials,
    format_role_display,
    format_last_login,
    format_account_status
)

__all__ = [
    'format_user_display_name',
    'get_user_initials',
    'format_role_display',
    'format_last_login',
    'format_account_status'
]
