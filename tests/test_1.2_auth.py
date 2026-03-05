"""Stage 1.2 Authentication — pure logic tests.

Tests run locally with pytest — no Anvil imports.
"""

from __future__ import annotations

from datetime import datetime, timedelta
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_module(name: str, relative_path: str):
    module_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    if spec and spec.loader:
        spec.loader.exec_module(module)
    return module


server_validation = _load_module(
    "server_validation", "server_code/server_auth/validation.py"
)
client_validation = _load_module(
    "client_validation", "client_code/auth/validation.py"
)


# ── Server auth validation helpers ──────────────────────────────────────────

def test_normalize_email_none():
    assert server_validation.normalize_email(None) == ""


def test_normalize_email_strips_and_lowercases():
    assert server_validation.normalize_email("  Test@Example.COM ") == "test@example.com"


def test_is_valid_email_happy_path():
    assert server_validation.is_valid_email("user@example.com") is True
    assert server_validation.is_valid_email("user.name+tag@sub.example.co") is True


def test_is_valid_email_invalid_formats():
    assert server_validation.is_valid_email("") is False
    assert server_validation.is_valid_email("no-at-symbol") is False
    assert server_validation.is_valid_email("user@") is False
    assert server_validation.is_valid_email("user@example") is False
    assert server_validation.is_valid_email("user@.com") is False
    assert server_validation.is_valid_email("t" + chr(0) + "st@example.com") is False


def test_validate_password_strength_valid_boundary():
    is_valid, message = server_validation.validate_password_strength("Aa1aaaaa")
    assert is_valid is True
    assert message == ""


def test_validate_password_strength_too_short():
    is_valid, message = server_validation.validate_password_strength("Aa1aaaa")
    assert is_valid is False
    assert message == "Password must be at least 8 characters"


def test_validate_password_strength_missing_upper():
    is_valid, message = server_validation.validate_password_strength("aa1aaaaa")
    assert is_valid is False
    assert message == "Password must contain an uppercase letter"


def test_validate_password_strength_missing_lower():
    is_valid, message = server_validation.validate_password_strength("AA1AAAAA")
    assert is_valid is False
    assert message == "Password must contain a lowercase letter"


def test_validate_password_strength_missing_number():
    is_valid, message = server_validation.validate_password_strength("Aaaaaaaa")
    assert is_valid is False
    assert message == "Password must contain a number"


def test_evaluate_rate_limit_no_record_allows():
    now = datetime.now()
    status = server_validation.evaluate_rate_limit(None, now, limit=10, window_minutes=1)
    assert status['allowed'] is True
    assert status['reset'] is False
    assert status['count'] == 0
    assert status['reset_time'] > now


def test_evaluate_rate_limit_boundary_allows():
    now = datetime.now()
    record = {'count': 9, 'reset_time': now + timedelta(minutes=1)}
    status = server_validation.evaluate_rate_limit(record, now, limit=10, window_minutes=1)
    assert status['allowed'] is True
    assert status['reset'] is False


def test_evaluate_rate_limit_limit_reached_denies():
    now = datetime.now()
    record = {'count': 10, 'reset_time': now + timedelta(minutes=1)}
    status = server_validation.evaluate_rate_limit(record, now, limit=10, window_minutes=1)
    assert status['allowed'] is False
    assert status['reset'] is False


def test_evaluate_rate_limit_expired_resets():
    now = datetime.now()
    record = {'count': 5, 'reset_time': now - timedelta(minutes=1)}
    status = server_validation.evaluate_rate_limit(record, now, limit=10, window_minutes=1)
    assert status['allowed'] is True
    assert status['reset'] is True
    assert status['count'] == 0
    assert status['reset_time'] > now


def test_evaluate_rate_limit_no_reset_time():
    now = datetime.now()
    record = {'count': 10, 'reset_time': None}
    status = server_validation.evaluate_rate_limit(record, now, limit=10, window_minutes=1)
    assert status['allowed'] is False


# ── Client auth validation helpers ──────────────────────────────────────────

def test_client_is_basic_email_happy_path():
    assert client_validation.is_basic_email("user@example.com") is True
    assert client_validation.is_basic_email(" user@example.com ") is True


def test_client_is_basic_email_edge_cases():
    assert client_validation.is_basic_email("") is False
    assert client_validation.is_basic_email(None) is False
    assert client_validation.is_basic_email("no-at") is False


def test_client_is_basic_email_adversarial():
    assert client_validation.is_basic_email("user@example.com\n") is True
    assert client_validation.is_basic_email("user@example.com" + chr(0)) is True


def test_client_is_non_empty():
    assert client_validation.is_non_empty("value") is True
    assert client_validation.is_non_empty("   ") is False
    assert client_validation.is_non_empty("") is False
    assert client_validation.is_non_empty(None) is False


def test_client_validate_password_strength_valid():
    is_valid, message = client_validation.validate_password_strength("Aa1aaaaa")
    assert is_valid is True
    assert message == ""


def test_client_validate_password_strength_missing_upper():
    is_valid, message = client_validation.validate_password_strength("aa1aaaaa")
    assert is_valid is False
    assert message == "Password must include an uppercase letter."


def test_client_validate_password_strength_missing_lower():
    is_valid, message = client_validation.validate_password_strength("AA1AAAAA")
    assert is_valid is False
    assert message == "Password must include a lowercase letter."


def test_client_validate_password_strength_missing_number():
    is_valid, message = client_validation.validate_password_strength("Aaaaaaaa")
    assert is_valid is False
    assert message == "Password must include a number."


def test_client_validate_password_strength_too_short():
    is_valid, message = client_validation.validate_password_strength("Aa1aaaa")
    assert is_valid is False
    assert message == "Password must be at least 8 characters."
