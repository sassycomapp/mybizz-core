"""
Auth UI Helper Functions

Pure display/formatting functions for auth-related UI operations.
All business logic and validation live in server_code/server_auth/.

M3-compliant utilities for displaying user information and handling
role-based navigation.
"""

import anvil.users
from anvil import open_form
from typing import Optional


def navigate_by_role() -> None:
    """Route the current user to the correct dashboard by role.

    Reads the authenticated user from the Anvil Users service and opens
    the appropriate form. Falls back to LoginForm if no user is found or
    the role is unrecognised.
    """
    user = anvil.users.get_user()
    if not user:
        open_form('LoginForm')
        return
    role = user.get('role')
    if role in ['owner', 'manager', 'admin', 'staff']:
        open_form('DashboardForm')
        return
    if role == 'customer':
        open_form('ClientPortalForm')
        return
    open_form('LoginForm')


def require_auth() -> bool:
    """Redirect to LoginForm if the current user is not authenticated.

    Returns:
        bool: True if a user is authenticated, False if redirected to login.
    """
    if not anvil.users.get_user():
        open_form('LoginForm')
        return False
    return True


def format_user_display_name(user: Optional[dict]) -> str:
    """Format a user's display name from a user row.

    Args:
        user: User row from the users table, or None.

    Returns:
        str: Formatted display name. Falls back to email username, then 'User'.

    Example:
        >>> format_user_display_name({'first_name': 'Jane', 'last_name': 'Smith'})
        'Jane Smith'
    """
    if not user:
        return "Guest"
    first_name = user.get('first_name', '')
    last_name = user.get('last_name', '')
    if first_name and last_name:
        return f"{first_name} {last_name}"
    if first_name:
        return first_name
    if last_name:
        return last_name
    email = user.get('email', '')
    return email.split('@')[0] if email else "User"


def get_user_initials(user: Optional[dict]) -> str:
    """Get up to two uppercase initials for avatar display.

    Args:
        user: User row from the users table, or None.

    Returns:
        str: One or two uppercase characters, or '?' if user is None.

    Example:
        >>> get_user_initials({'first_name': 'Jane', 'last_name': 'Smith'})
        'JS'
    """
    if not user:
        return "?"
    first_name = user.get('first_name', '')
    last_name = user.get('last_name', '')
    email = user.get('email', '')
    if first_name and last_name:
        return f"{first_name[0]}{last_name[0]}".upper()
    if first_name:
        return first_name[0:2].upper()
    if email:
        return email[0:2].upper()
    return "U"


def format_role_display(role: str) -> str:
    """Format a user role string for human-readable display.

    Args:
        role: Role string from the users table (e.g. 'owner', 'manager').

    Returns:
        str: Title-cased role label.

    Example:
        >>> format_role_display('owner')
        'Owner'
    """
    role_map = {
        'owner': 'Owner',
        'manager': 'Manager',
        'admin': 'Admin',
        'staff': 'Staff',
        'customer': 'Customer',
    }
    return role_map.get(role, role.title())


def format_account_status(status: str) -> str:
    """Format an account status string for human-readable display.

    Args:
        status: Status string from the users table
                (e.g. 'active', 'suspended').

    Returns:
        str: Title-cased status label.

    Example:
        >>> format_account_status('active')
        'Active'
    """
    status_map = {
        'active': 'Active',
        'inactive': 'Inactive',
        'suspended': 'Suspended',
        'pending': 'Pending Verification',
        'deleted': 'Deleted',
    }
    return status_map.get(status, status.title())


def format_last_login(last_login_time) -> str:
    """Format a last-login datetime as a human-readable relative string.

    Args:
        last_login_time: datetime of last login, or None.

    Returns:
        str: Relative time string (e.g. '2 hours ago', 'Just now', 'Never').

    Example:
        >>> format_last_login(None)
        'Never'
    """
    if not last_login_time:
        return "Never"
    from datetime import datetime
    diff = datetime.now() - last_login_time
    if diff.days > 365:
        years = diff.days // 365
        return f"{years} year{'s' if years > 1 else ''} ago"
    if diff.days > 30:
        months = diff.days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    if diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    if diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    return "Just now"


__all__ = [
    'navigate_by_role',
    'require_auth',
    'format_user_display_name',
    'get_user_initials',
    'format_role_display',
    'format_account_status',
    'format_last_login',
]