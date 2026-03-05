"""Server module for Stage 1.2 authentication services.

Provides callable server functions for user authentication, account creation,
password reset, permission checking, and user info retrieval.

All functions return the standard Mybizz response envelope:
    {'success': True, 'data': ...}
    {'success': False, 'error': str}

Internal helpers (_log_auth_event, _check_rate_limit, etc.) are not callable
from client code and have no @anvil.server.callable decorator.
"""

import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import logging
from datetime import datetime, timedelta
import re
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


# ── Pure helpers ──────────────────────────────────────────────────────────────

def _normalize_email(email: Optional[str]) -> str:
    """Strip whitespace and lowercase an email string."""
    return (email or "").strip().lower()


def _is_valid_email(email: str) -> bool:
    """Return True if email matches a basic RFC-5321 pattern."""
    if not email:
        return False
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def _validate_password_strength(password: Optional[str]) -> Tuple[bool, str]:
    """Check password meets minimum strength requirements.

    Args:
        password: Candidate password string.

    Returns:
        Tuple[bool, str]: (is_valid, error_message).
                          error_message is empty when is_valid is True.
    """
    password = password or ""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain an uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain a lowercase letter"
    if not re.search(r"[0-9]", password):
        return False, "Password must contain a number"
    return True, ""


# ── Callable server functions ─────────────────────────────────────────────────

@anvil.server.callable
def authenticate_user(email: str, password: str) -> dict:
    """Authenticate a user via email and password.

    Checks the rate limit before attempting login. On success, updates
    last_login and resets the rate limit counter. On failure, increments
    the counter and logs the event.

    Args:
        email: The user's email address.
        password: The user's plaintext password.

    Returns:
        dict: {'success': True, 'data': {'role': str, 'email': str}}
              {'success': False, 'error': str}
    """
    logger.info("authenticate_user called", extra={"email": _normalize_email(email)})
    identifier = _normalize_email(email)
    try:
        if not identifier or not password:
            return {'success': False, 'error': 'Email and password are required'}

        if not _check_rate_limit(identifier):
            return {
                'success': False,
                'error': 'Too many login attempts. Please try again in a minute.',
            }

        user = anvil.users.login_with_email(identifier, password)
        user['last_login'] = datetime.now()
        _reset_rate_limit(identifier)
        _log_auth_event('login_success', user=user)
        logger.info("authenticate_user succeeded", extra={"email": identifier})

        return {
            'success': True,
            'data': {
                'role': user.get('role'),
                'email': user.get('email'),
            },
        }

    except anvil.users.TooManyPasswordFailures:
        _log_auth_event('login_failure_locked', user=None)
        logger.warning(
            "authenticate_user: too many failures", extra={"email": identifier}
        )
        return {
            'success': False,
            'error': (
                'Too many failed attempts. '
                'Please reset your password via the forgot-password link.'
            ),
        }
    except anvil.users.AuthenticationFailed:
        _increment_rate_limit(identifier)
        _log_auth_event('login_failure', user=None)
        logger.info(
            "authenticate_user: invalid credentials", extra={"email": identifier}
        )
        return {'success': False, 'error': 'Invalid email or password'}
    except Exception:
        logger.error(
            "authenticate_user: unexpected error",
            exc_info=True,
            extra={"email": identifier},
        )
        return {'success': False, 'error': 'Sign in failed. Please try again.'}


@anvil.server.callable
def create_user(email: str, password: str, business_name: str) -> dict:
    """Create a new owner account and initialise configuration.

    Validates inputs, checks for an existing account, creates the user via
    the Anvil Users service, sets role/status fields, and calls
    create_initial_config.

    Args:
        email: The new user's email address.
        password: The new user's plaintext password.
        business_name: The name of the business being registered.

    Returns:
        dict: {'success': True, 'data': {'email': str}}
              {'success': False, 'error': str}

    Note on get_user_by_email: context7 did not return a confirmed signature
    for anvil.users.get_user_by_email(). The pre-existence check below uses
    a try/except guard so that if the function is unavailable the duplicate
    check is skipped and UserExists from signup_with_email still catches the
    duplicate.
    ⚠️ NEEDS HUMAN REVIEW — confirm anvil.users.get_user_by_email() is
    available in this Anvil runtime version before relying on it.
    """
    logger.info("create_user called", extra={"email": _normalize_email(email)})
    identifier = _normalize_email(email)
    try:
        if not business_name or not business_name.strip():
            return {'success': False, 'error': 'Business name is required'}
        if not _is_valid_email(identifier):
            return {'success': False, 'error': 'Invalid email format'}

        is_valid, message = _validate_password_strength(password)
        if not is_valid:
            return {'success': False, 'error': message}

        # Pre-existence check — guarded because get_user_by_email availability
        # is not confirmed by context7 for this runtime.
        try:
            existing = anvil.users.get_user_by_email(identifier)
            if existing:
                return {
                    'success': False,
                    'error': 'An account with this email already exists',
                }
        except AttributeError:
            # get_user_by_email not available — UserExists below will catch it
            logger.debug(
                "create_user: get_user_by_email unavailable, skipping pre-check"
            )

        user = anvil.users.signup_with_email(identifier, password)
        user['role'] = 'owner'
        user['account_status'] = 'active'
        user['permissions'] = {}
        user['created_at'] = datetime.now()

        # Import at call site to avoid module-level circular imports.
        from ..server_settings import service as settings_service
        settings_service.create_initial_config(business_name.strip())

        _log_auth_event('account_created', user=user)
        logger.info("create_user succeeded", extra={"email": identifier})
        return {'success': True, 'data': {'email': identifier}}

    except anvil.users.UserExists:
        logger.info(
            "create_user: email already exists", extra={"email": identifier}
        )
        return {'success': False, 'error': 'An account with this email already exists'}
    except Exception:
        logger.error(
            "create_user: unexpected error",
            exc_info=True,
            extra={"email": identifier},
        )
        return {'success': False, 'error': 'Account creation failed. Please try again.'}


@anvil.server.callable
def reset_password(email: str) -> dict:
    """Request a password reset email.

    Always returns a success envelope with an identical message regardless of
    whether the email is registered (OWASP A07:2021 — prevents enumeration).

    Args:
        email: The email address to send the reset link to.

    Returns:
        dict: {'success': True, 'data': {'message': str}} — always.
    """
    logger.info("reset_password called")
    identifier = _normalize_email(email)
    message = "If that email is registered, a reset link has been sent."
    try:
        if _is_valid_email(identifier):
            anvil.users.send_password_reset_email(identifier)
        _log_auth_event('password_reset_requested', user=None)
        logger.info("reset_password completed")
        return {'success': True, 'data': {'message': message}}
    except Exception:
        logger.warning("reset_password: send failed", exc_info=True)
        # Return success regardless — enumeration prevention.
        return {'success': True, 'data': {'message': message}}


@anvil.server.callable
def check_permission(permission_name: str) -> dict:
    """Check whether the current user holds a named permission.

    Owner role always returns True. Customer role always returns False.
    All other roles consult the permissions simpleObject on the user row.

    Args:
        permission_name: The permission key to check (e.g. 'bookings.manage').

    Returns:
        dict: {'success': True, 'data': {'has_permission': bool}}
              {'success': False, 'error': str}
    """
    logger.info(
        "check_permission called", extra={"permission": permission_name}
    )
    try:
        user = anvil.users.get_user()
        if not user:
            return {'success': False, 'error': 'Not authenticated'}
        if not permission_name:
            return {'success': False, 'error': 'Permission name is required'}

        role = user.get('role')
        if role == 'owner':
            has_permission = True
        elif role == 'customer':
            has_permission = False
        else:
            permissions = user.get('permissions') or {}
            has_permission = bool(permissions.get(permission_name, False))

        return {'success': True, 'data': {'has_permission': has_permission}}
    except Exception:
        logger.error(
            "check_permission: unexpected error",
            exc_info=True,
            extra={"permission": permission_name},
        )
        return {'success': False, 'error': 'Permission check failed.'}


@anvil.server.callable
def get_current_user_info() -> dict:
    """Return basic profile information for the currently authenticated user.

    Returns:
        dict: {'success': True, 'data': {'email', 'role', 'permissions', 'account_status'}}
              {'success': False, 'error': str}
    """
    logger.info("get_current_user_info called")
    try:
        user = anvil.users.get_user()
        if not user:
            return {'success': False, 'error': 'Not authenticated'}

        return {
            'success': True,
            'data': {
                'email': user.get('email'),
                'role': user.get('role'),
                'permissions': user.get('permissions') or {},
                'account_status': user.get('account_status'),
            },
        }
    except Exception:
        logger.error("get_current_user_info: unexpected error", exc_info=True)
        return {'success': False, 'error': 'Could not retrieve user info.'}


# ── Internal helpers (not callable from client) ───────────────────────────────

def _log_auth_event(event_type: str, user=None) -> None:
    """Write an authentication event to the audit_log table if it exists.

    Wrapped in a silent try/except — the audit_log table may not yet exist
    in Anvil.works during early development stages.

    Args:
        event_type: Short string identifying the event (e.g. 'login_success').
        user: The Anvil user row, or None for anonymous events.
    """
    try:
        audit_table = getattr(app_tables, 'audit_log', None)
        if audit_table is None:
            return
        ip_address = None
        try:
            request = anvil.server.request
            if request:
                ip_address = request.origin
        except Exception:
            ip_address = None
        audit_table.add_row(
            timestamp=datetime.now(),
            event_type=event_type,
            description=f"Auth event: {event_type}",
            user=user,
            ip_address=ip_address,
        )
    except Exception:
        logger.warning(
            "_log_auth_event: write failed",
            exc_info=True,
            extra={"event_type": event_type},
        )


def _check_rate_limit(
    identifier: str, limit: int = 10, window_minutes: int = 1
) -> bool:
    """Return True if the identifier is within the allowed rate limit.

    Fails open (returns True) if the rate_limits table does not exist or
    if any unexpected error occurs, so that a missing table never blocks login.

    Args:
        identifier: Normalised email address or IP string.
        limit: Maximum allowed attempts within the window.
        window_minutes: Rolling window duration in minutes.

    Returns:
        bool: True if the request is allowed, False if rate-limited.
    """
    try:
        rate_table = getattr(app_tables, 'rate_limits', None)
        if rate_table is None:
            return True

        record = rate_table.get(identifier=identifier)
        now = datetime.now()
        if not record:
            return True

        reset_time = record.get('reset_time')
        if reset_time and now > reset_time:
            record['count'] = 0
            record['reset_time'] = now + timedelta(minutes=window_minutes)
            record['last_request'] = now
            return True

        count = record.get('count') or 0
        return count < limit
    except Exception:
        logger.warning(
            "_check_rate_limit: check failed — failing open",
            exc_info=True,
            extra={"identifier": identifier},
        )
        return True


def _increment_rate_limit(
    identifier: str, window_minutes: int = 1
) -> None:
    """Increment the rate limit counter for the identifier.

    Creates a new record if none exists. Resets the window if it has expired.

    Args:
        identifier: Normalised email address or IP string.
        window_minutes: Rolling window duration in minutes.
    """
    try:
        rate_table = getattr(app_tables, 'rate_limits', None)
        if rate_table is None:
            return

        now = datetime.now()
        record = rate_table.get(identifier=identifier)
        if not record:
            rate_table.add_row(
                identifier=identifier,
                count=1,
                reset_time=now + timedelta(minutes=window_minutes),
                last_request=now,
            )
            return

        reset_time = record.get('reset_time')
        if reset_time and now > reset_time:
            record['count'] = 1
            record['reset_time'] = now + timedelta(minutes=window_minutes)
        else:
            record['count'] = (record.get('count') or 0) + 1
        record['last_request'] = now
    except Exception:
        logger.warning(
            "_increment_rate_limit: update failed",
            exc_info=True,
            extra={"identifier": identifier},
        )


def _reset_rate_limit(
    identifier: str, window_minutes: int = 1
) -> None:
    """Reset the rate limit counter for the identifier to zero.

    Args:
        identifier: Normalised email address or IP string.
        window_minutes: Rolling window duration in minutes.
    """
    try:
        rate_table = getattr(app_tables, 'rate_limits', None)
        if rate_table is None:
            return

        now = datetime.now()
        record = rate_table.get(identifier=identifier)
        if record:
            record['count'] = 0
            record['reset_time'] = now + timedelta(minutes=window_minutes)
            record['last_request'] = now
    except Exception:
        logger.warning(
            "_reset_rate_limit: update failed",
            exc_info=True,
            extra={"identifier": identifier},
        )