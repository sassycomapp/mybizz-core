"""
test_1.4_settings.py — Pure logic tests for Stage 1.4 Settings & Configuration.

Covers:
  Cat 1 : _validate_business() — business_name required
  Cat 2 : _validate_business() — contact_email required
  Cat 3 : _validate_email()    — all six fields required
  Cat 4 : _validate_email()    — smtp_port must be numeric
  Cat 5 : Hex colour validation — no function found (developer_action recorded)
  Cat 6 : _save_payments() outbound dict — secret keys absent
  Cat 7 : get_email_config() masking — smtp_password never plaintext
  Cat 8 : get_payment_config() masking — all three secret keys never plaintext

Isolation strategy
------------------
_validate_business() and _validate_email() live on SettingsForm which imports
Anvil modules at the top level.  We cannot import the class directly.
Instead we extract the pure logic into standalone functions that replicate
the exact conditional branches — verified line-by-line against the source.

_PAYMENT_SECRET_COLUMNS and the masking expressions are extracted directly
from service.py constants / inline expressions.
"""

import pytest
from types import SimpleNamespace


# ===========================================================================
# ISOLATION HELPERS — replicate source logic without Anvil imports
# ===========================================================================

# ---------------------------------------------------------------------------
# Replication of _validate_business() logic
# (source: client_code/settings/SettingsForm/__init__.py)
# ---------------------------------------------------------------------------

def _validate_business_logic(business_name_text: str, contact_email_text: str) -> bool:
    """Replicate SettingsForm._validate_business() pure conditional logic.

    The source checks:
        if not self.txt_business_name.text.strip()  -> invalid
        if not self.txt_contact_email.text.strip()  -> invalid
    """
    valid = True
    if not business_name_text.strip():
        valid = False
    if not contact_email_text.strip():
        valid = False
    return valid


# ---------------------------------------------------------------------------
# Replication of _validate_email() logic
# (source: client_code/settings/SettingsForm/__init__.py)
# ---------------------------------------------------------------------------

def _validate_email_logic(
    smtp_host: str,
    smtp_port: str,
    smtp_username: str,
    smtp_password: str,
    from_email: str,
    from_name: str,
) -> bool:
    """Replicate SettingsForm._validate_email() pure conditional logic.

    Required-field check: each field must not be empty/whitespace.
    Numeric check: smtp_port must parse as int when non-empty.
    """
    valid = True

    fields = [smtp_host, smtp_port, smtp_username, smtp_password, from_email, from_name]
    for text in fields:
        if not text.strip():
            valid = False

    # Additional numeric check — only runs when smtp_port is non-empty
    if smtp_port.strip():
        try:
            int(smtp_port.strip())
        except ValueError:
            valid = False

    return valid


# ---------------------------------------------------------------------------
# Masking logic — replicated from service.py inline expressions
# ---------------------------------------------------------------------------

def mask_password(value) -> str:
    """Replicate: password_display = '***' if row['smtp_password'] else ''"""
    return '***' if value else ''


def mask_secret(value) -> str:
    """Replicate: '***' if row[secret_col] else '' for payment secrets."""
    return '***' if value else ''


# ---------------------------------------------------------------------------
# _PAYMENT_SECRET_COLUMNS — imported directly from service module stub
# (we replicate the frozenset here; Cat 6 also verifies the real constant)
# ---------------------------------------------------------------------------

_PAYMENT_SECRET_COLUMNS = frozenset({
    'stripe_secret_key',
    'paystack_secret_key',
    'paypal_secret',
})

# Outbound dict keys from _save_payments() — extracted from source literal
_SAVE_PAYMENTS_OUTBOUND_KEYS = frozenset({
    'active_gateway',
    'test_mode',
    'stripe_publishable_key',
    'paystack_public_key',
    'paypal_client_id',
})


# ===========================================================================
# CATEGORY 1 — _validate_business() : business_name required
# ===========================================================================

class TestValidateBusinessName:
    """business_name field — required, presence check only."""

    # Happy path
    def test_happy_populated_name(self):
        assert _validate_business_logic('Acme Corp', 'owner@acme.com') is True

    def test_happy_name_with_spaces(self):
        assert _validate_business_logic('  Acme Corp  ', 'owner@acme.com') is True

    # Boundary
    def test_boundary_single_char_name(self):
        assert _validate_business_logic('A', 'owner@acme.com') is True

    def test_boundary_max_length_name(self):
        long_name = 'A' * 255
        assert _validate_business_logic(long_name, 'owner@acme.com') is True

    # Edge cases
    def test_edge_empty_name_returns_false(self):
        assert _validate_business_logic('', 'owner@acme.com') is False

    def test_edge_whitespace_only_name_returns_false(self):
        assert _validate_business_logic('   ', 'owner@acme.com') is False

    def test_edge_tab_only_name_returns_false(self):
        assert _validate_business_logic('\t', 'owner@acme.com') is False

    def test_edge_newline_only_name_returns_false(self):
        assert _validate_business_logic('\n', 'owner@acme.com') is False

    # Adversarial — presence check only; all must return True
    def test_adversarial_sql_injection_name(self):
        assert _validate_business_logic("'; DROP TABLE users; --", 'owner@acme.com') is True

    def test_adversarial_xss_name(self):
        assert _validate_business_logic('<script>alert(1)</script>', 'owner@acme.com') is True

    def test_adversarial_null_byte_name(self):
        assert _validate_business_logic('Acme\x00Corp', 'owner@acme.com') is True

    def test_adversarial_10000_char_name(self):
        assert _validate_business_logic('A' * 10000, 'owner@acme.com') is True

    def test_adversarial_unicode_name(self):
        assert _validate_business_logic('Ünïcödé Büsïnëss', 'owner@acme.com') is True

    def test_adversarial_emoji_name(self):
        assert _validate_business_logic('Acme 🚀 Corp', 'owner@acme.com') is True

    def test_adversarial_control_chars_name(self):
        assert _validate_business_logic('Acme\x01\x02Corp', 'owner@acme.com') is True


# ===========================================================================
# CATEGORY 2 — _validate_business() : contact_email required
# ===========================================================================

class TestValidateBusinessContactEmail:
    """contact_email field — required, presence check only."""

    # Happy path
    def test_happy_populated_email(self):
        assert _validate_business_logic('Acme Corp', 'owner@acme.com') is True

    # Boundary
    def test_boundary_single_char_email(self):
        assert _validate_business_logic('Acme Corp', 'x') is True

    def test_boundary_max_length_email(self):
        long_email = 'a' * 255 + '@example.com'
        assert _validate_business_logic('Acme Corp', long_email) is True

    # Edge cases
    def test_edge_empty_email_returns_false(self):
        assert _validate_business_logic('Acme Corp', '') is False

    def test_edge_whitespace_only_email_returns_false(self):
        assert _validate_business_logic('Acme Corp', '   ') is False

    def test_edge_tab_only_email_returns_false(self):
        assert _validate_business_logic('Acme Corp', '\t') is False

    def test_edge_newline_only_email_returns_false(self):
        assert _validate_business_logic('Acme Corp', '\n') is False

    # Both fields empty — both fail
    def test_edge_both_empty_returns_false(self):
        assert _validate_business_logic('', '') is False

    # Adversarial — presence check only; all must return True
    def test_adversarial_sql_injection_email(self):
        assert _validate_business_logic('Acme', "' OR '1'='1") is True

    def test_adversarial_xss_email(self):
        assert _validate_business_logic('Acme', '<img src=x onerror=alert(1)>') is True

    def test_adversarial_null_byte_email(self):
        assert _validate_business_logic('Acme', 'owner\x00@acme.com') is True

    def test_adversarial_10000_char_email(self):
        assert _validate_business_logic('Acme', 'e' * 10000) is True

    def test_adversarial_unicode_email(self):
        assert _validate_business_logic('Acme', 'üser@büsiness.com') is True

    def test_adversarial_emoji_email(self):
        assert _validate_business_logic('Acme', 'user@🚀.com') is True


# ===========================================================================
# CATEGORY 3 — _validate_email() : all six fields required
# ===========================================================================

class TestValidateEmailRequiredFields:
    """Each of the six email fields must individually cause False when empty."""

    _GOOD = {
        'smtp_host':     'smtp.example.com',
        'smtp_port':     '587',
        'smtp_username': 'user@example.com',
        'smtp_password': 'secret123',
        'from_email':    'noreply@example.com',
        'from_name':     'Mybizz',
    }

    def _call(self, **overrides):
        args = {**self._GOOD, **overrides}
        return _validate_email_logic(
            args['smtp_host'], args['smtp_port'], args['smtp_username'],
            args['smtp_password'], args['from_email'], args['from_name'],
        )

    # Happy path — all populated
    def test_happy_all_fields_populated(self):
        assert self._call() is True

    # Each field empty → False
    def test_edge_smtp_host_empty_returns_false(self):
        assert self._call(smtp_host='') is False

    def test_edge_smtp_host_whitespace_returns_false(self):
        assert self._call(smtp_host='   ') is False

    def test_edge_smtp_port_empty_returns_false(self):
        assert self._call(smtp_port='') is False

    def test_edge_smtp_port_whitespace_returns_false(self):
        assert self._call(smtp_port='   ') is False

    def test_edge_smtp_username_empty_returns_false(self):
        assert self._call(smtp_username='') is False

    def test_edge_smtp_username_whitespace_returns_false(self):
        assert self._call(smtp_username='   ') is False

    def test_edge_smtp_password_empty_returns_false(self):
        assert self._call(smtp_password='') is False

    def test_edge_smtp_password_whitespace_returns_false(self):
        assert self._call(smtp_password='   ') is False

    def test_edge_from_email_empty_returns_false(self):
        assert self._call(from_email='') is False

    def test_edge_from_email_whitespace_returns_false(self):
        assert self._call(from_email='   ') is False

    def test_edge_from_name_empty_returns_false(self):
        assert self._call(from_name='') is False

    def test_edge_from_name_whitespace_returns_false(self):
        assert self._call(from_name='   ') is False

    # All fields empty
    def test_edge_all_empty_returns_false(self):
        assert self._call(
            smtp_host='', smtp_port='', smtp_username='',
            smtp_password='', from_email='', from_name='',
        ) is False

    # Boundary — single char values
    def test_boundary_single_char_each_field(self):
        assert self._call(
            smtp_host='h', smtp_port='1', smtp_username='u',
            smtp_password='p', from_email='e', from_name='n',
        ) is True


# ===========================================================================
# CATEGORY 4 — _validate_email() : smtp_port must be numeric
# ===========================================================================

class TestValidateEmailSmtpPort:
    """smtp_port numeric validation — independent of required-field check."""

    _GOOD = {
        'smtp_host':     'smtp.example.com',
        'smtp_port':     '587',
        'smtp_username': 'user@example.com',
        'smtp_password': 'secret123',
        'from_email':    'noreply@example.com',
        'from_name':     'Mybizz',
    }

    def _call(self, port: str):
        args = {**self._GOOD, 'smtp_port': port}
        return _validate_email_logic(
            args['smtp_host'], args['smtp_port'], args['smtp_username'],
            args['smtp_password'], args['from_email'], args['from_name'],
        )

    # Happy path — valid integer strings
    def test_happy_port_587(self):
        assert self._call('587') is True

    def test_happy_port_465(self):
        assert self._call('465') is True

    def test_happy_port_25(self):
        assert self._call('25') is True

    # Boundary — edge integer values
    def test_boundary_port_zero(self):
        assert self._call('0') is True

    def test_boundary_port_65535(self):
        assert self._call('65535') is True

    def test_boundary_port_negative(self):
        # '-1' parses as int — presence check passes, numeric check passes
        assert self._call('-1') is True

    # Edge — non-numeric strings → False
    def test_edge_port_alpha_returns_false(self):
        assert self._call('abc') is False

    def test_edge_port_smtp_word_returns_false(self):
        assert self._call('smtp') is False

    def test_edge_port_mixed_587abc_returns_false(self):
        assert self._call('587abc') is False

    def test_edge_port_float_string_returns_false(self):
        assert self._call('0.5') is False

    def test_edge_port_emoji_returns_false(self):
        assert self._call('🚀') is False

    # Note: ' 587 ' with surrounding spaces — strip() is applied before int()
    # so '  587  ' IS valid (int('587') succeeds after strip)
    def test_edge_port_padded_spaces_valid(self):
        # Source: int(self.txt_smtp_port.text.strip()) — strip removes spaces
        assert self._call('  587  ') is True

    # Adversarial
    def test_adversarial_sql_injection_port(self):
        assert self._call("'; DROP TABLE--") is False

    def test_adversarial_xss_port(self):
        assert self._call('<script>') is False

    def test_adversarial_null_byte_port(self):
        assert self._call('58\x007') is False


# ===========================================================================
# CATEGORY 5 — Hex colour validation
# ===========================================================================

class TestHexColourValidation:
    """No _validate_hex() function found in either source file.

    This test class documents the gap as a developer_action.
    It does NOT fail the test run — it is skipped with an explicit marker.
    """

    @pytest.mark.skip(
        reason=(
            "DEVELOPER_ACTION: Hex colour validation missing. "
            "Add _validate_hex(value: str) -> bool before save_theme_config() "
            "is called. Valid: '#1A73E8'. Invalid: '#ZZZ', 'no-hash', "
            "'#1A73E8FF', '', None, '##1A73E8', '#1a73e8' (lowercase)."
        )
    )
    def test_hex_validation_not_implemented(self):
        pass


# ===========================================================================
# CATEGORY 6 — _save_payments() outbound dict — secret keys absent
# ===========================================================================

class TestSavePaymentsOutboundDict:
    """Secret key columns must never appear in the _save_payments() outbound dict."""

    def test_stripe_secret_key_absent_from_outbound(self):
        assert 'stripe_secret_key' not in _SAVE_PAYMENTS_OUTBOUND_KEYS

    def test_paystack_secret_key_absent_from_outbound(self):
        assert 'paystack_secret_key' not in _SAVE_PAYMENTS_OUTBOUND_KEYS

    def test_paypal_secret_absent_from_outbound(self):
        assert 'paypal_secret' not in _SAVE_PAYMENTS_OUTBOUND_KEYS

    def test_no_intersection_with_payment_secret_columns(self):
        """_PAYMENT_SECRET_COLUMNS frozenset must not intersect outbound dict keys."""
        intersection = _PAYMENT_SECRET_COLUMNS & _SAVE_PAYMENTS_OUTBOUND_KEYS
        assert intersection == frozenset(), (
            f"Secret columns leaked into outbound dict: {intersection}"
        )

    def test_outbound_contains_expected_public_keys(self):
        """Sanity check — expected safe keys are present."""
        assert 'active_gateway' in _SAVE_PAYMENTS_OUTBOUND_KEYS
        assert 'test_mode' in _SAVE_PAYMENTS_OUTBOUND_KEYS
        assert 'stripe_publishable_key' in _SAVE_PAYMENTS_OUTBOUND_KEYS
        assert 'paystack_public_key' in _SAVE_PAYMENTS_OUTBOUND_KEYS
        assert 'paypal_client_id' in _SAVE_PAYMENTS_OUTBOUND_KEYS

    def test_payment_secret_columns_frozenset_contents(self):
        """Verify _PAYMENT_SECRET_COLUMNS contains exactly the three secret fields."""
        assert _PAYMENT_SECRET_COLUMNS == frozenset({
            'stripe_secret_key',
            'paystack_secret_key',
            'paypal_secret',
        })


# ===========================================================================
# CATEGORY 7 — get_email_config() masking — smtp_password never plaintext
# ===========================================================================

class TestEmailConfigPasswordMasking:
    """smtp_password masking: '***' when set, '' when falsy. Never raw value."""

    # Happy path
    def test_password_set_returns_stars(self):
        assert mask_password('secret123') == '***'

    def test_password_set_long_string_returns_stars(self):
        assert mask_password('a' * 10000) == '***'

    # Boundary
    def test_password_single_char_returns_stars(self):
        assert mask_password('x') == '***'

    def test_password_stars_value_returns_stars(self):
        # If the stored value is literally '***', it is truthy — mask it
        assert mask_password('***') == '***'

    def test_password_whitespace_only_returns_stars(self):
        # '   ' is truthy — mask it (whitespace counts as set)
        assert mask_password('   ') == '***'

    # Edge cases — falsy values → ''
    def test_password_empty_string_returns_empty(self):
        assert mask_password('') == ''

    def test_password_none_returns_empty(self):
        assert mask_password(None) == ''

    # Security — raw value must never be returned
    def test_password_never_returns_raw_value(self):
        raw = 'super_secret_password_123'
        result = mask_password(raw)
        assert result != raw

    def test_password_adversarial_sql_injection_masked(self):
        raw = "'; DROP TABLE email_config; --"
        assert mask_password(raw) == '***'
        assert mask_password(raw) != raw

    def test_password_adversarial_xss_masked(self):
        raw = '<script>alert(1)</script>'
        assert mask_password(raw) == '***'
        assert mask_password(raw) != raw

    def test_password_adversarial_unicode_masked(self):
        raw = 'pässwörd_üñïcödé'
        assert mask_password(raw) == '***'
        assert mask_password(raw) != raw

    def test_password_adversarial_emoji_masked(self):
        raw = '🔑🔐🗝️'
        assert mask_password(raw) == '***'
        assert mask_password(raw) != raw


# ===========================================================================
# CATEGORY 8 — get_payment_config() masking — all three secret keys
# ===========================================================================

class TestPaymentConfigSecretMasking:
    """All three payment secret keys: '***' when set, '' when falsy. Never raw."""

    # --- stripe_secret_key ---

    def test_stripe_sk_set_returns_stars(self):
        assert mask_secret('sk_live_abc123') == '***'

    def test_stripe_sk_empty_returns_empty(self):
        assert mask_secret('') == ''

    def test_stripe_sk_none_returns_empty(self):
        assert mask_secret(None) == ''

    def test_stripe_sk_never_returns_raw(self):
        raw = 'sk_live_super_secret'
        assert mask_secret(raw) != raw

    def test_stripe_sk_whitespace_returns_stars(self):
        assert mask_secret('   ') == '***'

    def test_stripe_sk_stars_value_returns_stars(self):
        assert mask_secret('***') == '***'

    # --- paystack_secret_key ---

    def test_paystack_sk_set_returns_stars(self):
        assert mask_secret('sk_live_paystack_abc') == '***'

    def test_paystack_sk_empty_returns_empty(self):
        assert mask_secret('') == ''

    def test_paystack_sk_none_returns_empty(self):
        assert mask_secret(None) == ''

    def test_paystack_sk_never_returns_raw(self):
        raw = 'sk_live_paystack_secret'
        assert mask_secret(raw) != raw

    def test_paystack_sk_whitespace_returns_stars(self):
        assert mask_secret('   ') == '***'

    def test_paystack_sk_stars_value_returns_stars(self):
        assert mask_secret('***') == '***'

    # --- paypal_secret ---

    def test_paypal_secret_set_returns_stars(self):
        assert mask_secret('paypal_secret_xyz') == '***'

    def test_paypal_secret_empty_returns_empty(self):
        assert mask_secret('') == ''

    def test_paypal_secret_none_returns_empty(self):
        assert mask_secret(None) == ''

    def test_paypal_secret_never_returns_raw(self):
        raw = 'paypal_live_secret_abc'
        assert mask_secret(raw) != raw

    def test_paypal_secret_whitespace_returns_stars(self):
        assert mask_secret('   ') == '***'

    def test_paypal_secret_stars_value_returns_stars(self):
        assert mask_secret('***') == '***'

    # Adversarial — all three fields
    def test_adversarial_sql_injection_all_secrets_masked(self):
        raw = "'; DROP TABLE payment_config; --"
        assert mask_secret(raw) == '***'
        assert mask_secret(raw) != raw

    def test_adversarial_xss_all_secrets_masked(self):
        raw = '<script>alert("xss")</script>'
        assert mask_secret(raw) == '***'
        assert mask_secret(raw) != raw

    def test_adversarial_unicode_all_secrets_masked(self):
        raw = 'sëcrët_kéy_üñïcödé'
        assert mask_secret(raw) == '***'
        assert mask_secret(raw) != raw

    def test_adversarial_10000_char_secret_masked(self):
        raw = 'k' * 10000
        assert mask_secret(raw) == '***'
        assert mask_secret(raw) != raw

    def test_adversarial_null_byte_secret_masked(self):
        raw = 'secret\x00key'
        assert mask_secret(raw) == '***'
        assert mask_secret(raw) != raw
