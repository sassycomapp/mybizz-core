"""Navigation helper functions for the Mybizz Consulting & Services app.

All functions are pure client-side utilities. No server calls are made here.
Business logic and RBAC enforcement live in server_code/server_auth/.
"""

import anvil.users
from anvil import open_form


# Roles that have access to the admin area
_ADMIN_ROLES = ('owner', 'manager', 'admin', 'staff')


def require_auth() -> bool:
    """Redirect to LoginForm if the current user is not authenticated.

    Returns:
        bool: True if a user is authenticated, False if redirected to login.
    """
    if not anvil.users.get_user():
        open_form('LoginForm')
        return False
    return True


def require_admin() -> bool:
    """Redirect to LoginForm if the current user does not hold an admin role.

    Checks for owner, manager, admin, or staff. Customers and unauthenticated
    visitors are both redirected to LoginForm.

    Returns:
        bool: True if the user holds an admin role, False if redirected.
    """
    user = anvil.users.get_user()
    if not user:
        open_form('LoginForm')
        return False
    if user.get('role') not in _ADMIN_ROLES:
        open_form('LoginForm')
        return False
    return True


def navigate_to_dashboard() -> None:
    """Route the current user to the correct dashboard by role.

    - owner / manager / admin / staff -> AdminLayout (which opens DashboardForm)
    - customer -> ClientPortalForm
    - unauthenticated -> LoginForm
    """
    user = anvil.users.get_user()
    if not user:
        open_form('LoginForm')
        return
    role = user.get('role', '')
    if role in _ADMIN_ROLES:
        open_form('DashboardForm')
        return
    if role == 'customer':
        open_form('ClientPortalForm')
        return
    open_form('LoginForm')


__all__ = [
    'require_auth',
    'require_admin',
    'navigate_to_dashboard',
]
