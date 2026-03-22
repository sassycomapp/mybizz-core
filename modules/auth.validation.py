"""Pure validation helpers for authentication forms.

No Anvil imports — safe for local pytest.
"""

from __future__ import annotations

import re
from typing import Optional, Tuple


def is_basic_email(email: Optional[str]) -> bool:
    """Basic email check used by auth forms.

    Requires non-empty string containing '@' after trimming whitespace.
    """
    email_text = (email or "").strip()
    return bool(email_text) and "@" in email_text


def is_non_empty(value: Optional[str]) -> bool:
    """Return True if value is a non-empty string after trimming."""
    return bool((value or "").strip())


def validate_password_strength(password: str) -> Tuple[bool, str]:
    """Check password meets minimum strength requirements.

    Args:
        password: The candidate password string.

    Returns:
        tuple: (bool, str) — (is_valid, error_message).
               error_message is empty string when is_valid is True.
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if not re.search(r'[A-Z]', password):
        return False, "Password must include an uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must include a lowercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must include a number."
    return True, ""
