"""Pure validation helpers for authentication.

This module contains logic with no Anvil dependencies for local testing.
"""

from __future__ import annotations

from datetime import datetime, timedelta
import re
from typing import Optional, Tuple, Dict, Any


def normalize_email(email: Optional[str]) -> str:
    """Strip whitespace and lowercase an email string."""
    return (email or "").strip().lower()


def is_valid_email(email: str) -> bool:
    """Return True if email matches a basic RFC-5321 pattern."""
    if not email:
        return False
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_password_strength(password: Optional[str]) -> Tuple[bool, str]:
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


def evaluate_rate_limit(
    record: Optional[Dict[str, Any]],
    now: datetime,
    limit: int,
    window_minutes: int,
) -> Dict[str, Any]:
    """Evaluate whether a request is allowed within the rate-limit window.

    Args:
        record: Dict with keys like 'count' and 'reset_time', or None.
        now: Current datetime for evaluation.
        limit: Maximum allowed attempts within the window.
        window_minutes: Rolling window duration in minutes.

    Returns:
        dict: {
            'allowed': bool,
            'reset': bool,
            'count': int,
            'reset_time': datetime | None,
        }
    """
    if not record:
        return {
            'allowed': True,
            'reset': False,
            'count': 0,
            'reset_time': now + timedelta(minutes=window_minutes),
        }

    reset_time = record.get('reset_time')
    if reset_time and now > reset_time:
        return {
            'allowed': True,
            'reset': True,
            'count': 0,
            'reset_time': now + timedelta(minutes=window_minutes),
        }

    count = record.get('count') or 0
    return {
        'allowed': count < limit,
        'reset': False,
        'count': count,
        'reset_time': reset_time,
    }
