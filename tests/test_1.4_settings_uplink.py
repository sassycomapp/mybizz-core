"""
Uplink integration tests -- Stage 1.4 Settings & Configuration
Test file: test_1.4_settings_uplink.py

Covers all @anvil.server.callable functions in server_settings/service.py:
  - get_business_profile
  - save_business_profile
  - get_email_config
  - save_email_config
  - get_payment_config
  - save_payment_config
  - get_theme_config
  - save_theme_config

Safety rules:
  - All config tables hold at most one row -- never deleted.
  - Pre-test state captured before every test; restored after regardless of outcome.
  - Sentinel prefix TEST_ used for all test data written to string fields.
  - Unauthenticated tests call functions without logging in.
"""

import os
import pytest
import anvil.server
import anvil.users

# ---------------------------------------------------------------------------
# Uplink connection
# ---------------------------------------------------------------------------

UPLINK_KEY = os.environ.get("ANVIL_UPLINK_KEY")
if not UPLINK_KEY:
    raise RuntimeError(
        "ANVIL_UPLINK_KEY environment variable is not set. "
        "Set it before running these tests."
    )

anvil.server.connect(UPLINK_KEY)


# ---------------------------------------------------------------------------
# Helpers -- state capture / restore
# ---------------------------------------------------------------------------

def _capture_single_row_state(table_name):
    """Return the current row of a single-row config table as a plain dict,
    or None if the table is empty."""
    result = anvil.server.call("test_helper_capture_row", table_name)
    return result.get("data")


def _restore_single_row_state(table_name, state):
    """Restore a single-row config table to its captured state."""
    anvil.server.call("test_helper_restore_row", table_name, state)


# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------

def login_as_owner():
    email = os.environ.get("TEST_OWNER_EMAIL")
    password = os.environ.get("TEST_OWNER_PASSWORD")
    if not email or not password:
        pytest.skip("TEST_OWNER_EMAIL / TEST_OWNER_PASSWORD not set")
    anvil.users.login_with_email(email, password)


def logout():
    try:
        anvil.users.logout()
    except Exception:
        pass


@pytest.fixture
def authenticated():
    login_as_owner()
    yield
    logout()


@pytest.fixture
def unauthenticated():
    logout()
    yield
    logout()


# ===========================================================================
# get_business_profile
# ===========================================================================

class TestGetBusinessProfile:

    def test_gbp_happy_path_row_exists(self, authenticated):
        """T001 -- Authenticated, row exists -> success, all fields returned."""
        state = _capture_single_row_state("business_profile")
        try:
            anvil.server.call("save_business_profile", {
                "business_name": "TEST_Happy Corp",
                "tagline": "TEST_tagline",
            })
            result = anvil.server.call("get_business_profile")
            assert result["success"] is True
            data = result["data"]
            assert isinstance(data, dict)
            expected_keys = [
                "business_name", "tagline", "description", "logo",
                "contact_email", "phone", "address_line_1", "address_line_2",
                "city", "country", "postal_code", "website_url",
                "social_facebook", "social_instagram", "social_x",
                "social_linkedin", "updated_at",
            ]
            for key in expected_keys:
                assert key in data, f"Missing key: {key}"
        finally:
            _restore_single_row_state("business_profile", state)

    def test_gbp_empty_table(self, authenticated):
        """T002 -- Authenticated, table empty -> success, empty dict returned."""
        state = _capture_single_row_state("business_profile")
        try:
            anvil.server.call("test_helper_clear_row", "business_profile")
            result = anvil.server.call("get_business_profile")
            assert result["success"] is True
            assert result["data"] == {}
        finally:
            _restore_single_row_state("business_profile", state)

    def test_gbp_unauthenticated(self, unauthenticated):
        """T003 -- Unauthenticated -> failure, 'Not authenticated'."""
        result = anvil.server.call("get_business_profile")
        assert result["success"] is False
        assert "Not authenticated" in result["error"]

    def test_gbp_logo_returned_as_url_string(self, authenticated):
        """T004 -- logo field returned as URL string or None, never raw media object."""
        state = _capture_single_row_state("business_profile")
        try:
            result = anvil.server.call("get_business_profile")
            assert result["success"] is True
            logo_value = result["data"].get("logo")
            assert logo_value is None or isinstance(logo_value, str), (
                f"logo should be str or None, got {type(logo_value)}"
            )
        finally:
            _restore_single_row_state("business_profile", state)


# ===========================================================================
# save_business_profile
# ===========================================================================

class TestSaveBusinessProfile:

    def test_sbp_happy_path_valid_data(self, authenticated):
        """T005 -- Authenticated, valid data -> success, row written correctly."""
        state = _capture_single_row_state("business_profile")
        try:
            data = {
                "business_name": "TEST_Valid Corp",
                "tagline": "TEST_We test things",
                "description": "TEST_A valid description",
                "contact_email": "test@example.com",
                "phone": "+1-555-0100",
                "address_line_1": "TEST_123 Main St",
                "address_line_2": "",
                "city": "TEST_Testville",
                "country": "TEST_Testland",
                "postal_code": "TEST_12345",
                "website_url": "https://test.example.com",
                "social_facebook": "",
                "social_instagram": "",
                "social_x": "",
                "social_linkedin": "",
            }
            result = anvil.server.call("save_business_profile", data)
            assert result["success"] is True
            fetched = anvil.server.call("get_business_profile")
            assert fetched["success"] is True
            assert fetched["data"]["business_name"] == "TEST_Valid Corp"
            assert fetched["data"]["city"] == "TEST_Testville"
        finally:
            _restore_single_row_state("business_profile", state)

    def test_sbp_no_existing_row(self, authenticated):
        """T006 -- Authenticated, no existing row -> success, new row created."""
        state = _capture_single_row_state("business_profile")
        try:
            anvil.server.call("test_helper_clear_row", "business_profile")
            result = anvil.server.call("save_business_profile", {
                "business_name": "TEST_Brand New Corp",
            })
            assert result["success"] is True
            fetched = anvil.server.call("get_business_profile")
            assert fetched["success"] is True
            assert fetched["data"]["business_name"] == "TEST_Brand New Corp"
        finally:
            _restore_single_row_state("business_profile", state)

    def test_sbp_unauthenticated(self, unauthenticated):
        """T007 -- Unauthenticated -> failure, 'Not authenticated'."""
        result = anvil.server.call("save_business_profile", {"business_name": "TEST_X"})
        assert result["success"] is False
        assert "Not authenticated" in result["error"]

    def test_sbp_adversarial_sql_injection(self, authenticated):
        """T008 -- SQL injection string in business_name -> stored safely as plain string."""
        state = _capture_single_row_state("business_profile")
        try:
            injection = "TEST_'; DROP TABLE business_profile; --"
            result = anvil.server.call("save_business_profile", {"business_name": injection})
            assert result["success"] is True
            fetched = anvil.server.call("get_business_profile")
            assert fetched["success"] is True
            assert fetched["data"]["business_name"] == injection
        finally:
            _restore_single_row_state("business_profile", state)

    def test_sbp_adversarial_xss(self, authenticated):
        """T009 -- XSS string in business_name -> stored safely as plain string."""
        state = _capture_single_row_state("business_profile")
        try:
            xss = "TEST_<script>alert('xss')</script>"
            result = anvil.server.call("save_business_profile", {"business_name": xss})
            assert result["success"] is True
            fetched = anvil.server.call("get_business_profile")
            assert fetched["success"] is True
            assert fetched["data"]["business_name"] == xss
        finally:
            _restore_single_row_state("business_profile", state)

    def test_sbp_adversarial_oversized_description(self, authenticated):
        """T010 -- 10000-char string in description -> stored safely without exception."""
        state = _capture_single_row_state("business_profile")
        try:
            long_desc = "TEST_" + ("A" * 9995)
            assert len(long_desc) == 10000
            result = anvil.server.call("save_business_profile", {"description": long_desc})
            assert result["success"] is True
            fetched = anvil.server.call("get_business_profile")
            assert fetched["success"] is True
            assert fetched["data"]["description"] == long_desc
        finally:
            _restore_single_row_state("business_profile", state)

    def test_sbp_logo_none_does_not_overwrite(self, authenticated):
        """T011 -- logo_file=None -> existing logo column value not modified."""
        state = _capture_single_row_state("business_profile")
        try:
            anvil.server.call("save_business_profile", {"business_name": "TEST_Logo Test"})
            before = anvil.server.call("get_business_profile")
            logo_before = before["data"].get("logo")
            result = anvil.server.call("save_business_profile",
                                       {"business_name": "TEST_Logo Test Updated"},
                                       None)
            assert result["success"] is True
            after = anvil.server.call("get_business_profile")
            logo_after = after["data"].get("logo")
            assert logo_before == logo_after, (
                f"logo changed when logo_file=None: before={logo_before}, after={logo_after}"
            )
        finally:
            _restore_single_row_state("business_profile", state)


# ===========================================================================
# get_email_config
# ===========================================================================

class TestGetEmailConfig:

    def test_gec_password_masked_when_set(self, authenticated):
        """T012 -- smtp_password set -> returned as '***', never plaintext."""
        state = _capture_single_row_state("email_config")
        try:
            anvil.server.call("save_email_config", {
                "smtp_host": "TEST_smtp.example.com",
                "smtp_port": 587,
                "smtp_username": "TEST_user",
                "smtp_password": "TEST_supersecret",
                "from_email": "test@example.com",
                "from_name": "TEST_Sender",
            })
            result = anvil.server.call("get_email_config")
            assert result["success"] is True
            assert result["data"]["smtp_password"] == "***", (
                "smtp_password must be masked as '***' when set"
            )
            assert "TEST_supersecret" not in str(result["data"]), (
                "Plaintext password must never appear in response"
            )
        finally:
            _restore_single_row_state("email_config", state)

    def test_gec_password_empty_when_not_set(self, authenticated):
        """T013 -- smtp_password empty or None -> returned as ''."""
        state = _capture_single_row_state("email_config")
        try:
            anvil.server.call("save_email_config", {
                "smtp_host": "TEST_smtp.example.com",
                "smtp_port": 587,
                "smtp_username": "TEST_user",
                "smtp_password": "",
                "from_email": "test@example.com",
                "from_name": "TEST_Sender",
            })
            result = anvil.server.call("get_email_config")
            assert result["success"] is True
            assert result["data"]["smtp_password"] == "", (
                "smtp_password should be '' when not set"
            )
        finally:
            _restore_single_row_state("email_config", state)

    def test_gec_empty_table(self, authenticated):
        """T014 -- Authenticated, table empty -> success, empty dict."""
        state = _capture_single_row_state("email_config")
        try:
            anvil.server.call("test_helper_clear_row", "email_config")
            result = anvil.server.call("get_email_config")
            assert result["success"] is True
            assert result["data"] == {}
        finally:
            _restore_single_row_state("email_config", state)

    def test_gec_unauthenticated(self, unauthenticated):
        """T015 -- Unauthenticated -> failure, 'Not authenticated'."""
        result = anvil.server.call("get_email_config")
        assert result["success"] is False
        assert "Not authenticated" in result["error"]


# ===========================================================================
# save_email_config
# ===========================================================================

class TestSaveEmailConfig:

    def test_sec_happy_path_valid_data(self, authenticated):
        """T016 -- Authenticated, valid data -> success, configured set to False."""
        state = _capture_single_row_state("email_config")
        try:
            data = {
                "smtp_host": "TEST_smtp.example.com",
                "smtp_port": 587,
                "smtp_username": "TEST_user@example.com",
                "smtp_password": "TEST_password123",
                "from_email": "TEST_from@example.com",
                "from_name": "TEST_Sender Name",
            }
            result = anvil.server.call("save_email_config", data)
            assert result["success"] is True
            fetched = anvil.server.call("get_email_config")
            assert fetched["success"] is True
            assert fetched["data"]["configured"] is False, (
                "configured must be False after save_email_config"
            )
        finally:
            _restore_single_row_state("email_config", state)

    def test_sec_configured_reset_to_false(self, authenticated):
        """T017 -- Row already has configured=True -> reset to False after save."""
        state = _capture_single_row_state("email_config")
        try:
            anvil.server.call("test_helper_set_email_configured_true")
            before = anvil.server.call("get_email_config")
            assert before["data"].get("configured") is True
            result = anvil.server.call("save_email_config", {
                "smtp_host": "TEST_smtp.example.com",
                "smtp_port": 587,
                "smtp_username": "TEST_user",
                "smtp_password": "TEST_pw",
                "from_email": "TEST_from@example.com",
                "from_name": "TEST_Name",
            })
            assert result["success"] is True
            after = anvil.server.call("get_email_config")
            assert after["data"]["configured"] is False, (
                "configured must be reset to False after save even if it was True"
            )
        finally:
            _restore_single_row_state("email_config", state)

    def test_sec_unauthenticated(self, unauthenticated):
        """T018 -- Unauthenticated -> failure, 'Not authenticated'."""
        result = anvil.server.call("save_email_config", {"smtp_host": "TEST_x"})
        assert result["success"] is False
        assert "Not authenticated" in result["error"]


# ===========================================================================
# get_payment_config
# ===========================================================================

class TestGetPaymentConfig:

    def test_gpc_all_secret_keys_masked(self, authenticated):
        """T019 -- All three secret keys set -> each returned as '***', never plaintext."""
        state = _capture_single_row_state("payment_config")
        try:
            anvil.server.call("test_helper_set_payment_secrets",
                              "TEST_stripe_sk", "TEST_paystack_sk", "TEST_paypal_sk")
            result = anvil.server.call("get_payment_config")
            assert result["success"] is True
            data = result["data"]
            assert data["stripe_secret_key"] == "***"
            assert data["paystack_secret_key"] == "***"
            assert data["paypal_secret"] == "***"
            response_str = str(data)
            for secret in ("TEST_stripe_sk", "TEST_paystack_sk", "TEST_paypal_sk"):
                assert secret not in response_str, (
                    f"Plaintext secret '{secret}' must never appear in response"
                )
        finally:
            _restore_single_row_state("payment_config", state)

    def test_gpc_empty_secret_keys_returned_as_empty_string(self, authenticated):
        """T020 -- Secret keys empty or None -> each returned as ''."""
        state = _capture_single_row_state("payment_config")
        try:
            anvil.server.call("test_helper_set_payment_secrets", "", "", "")
            result = anvil.server.call("get_payment_config")
            assert result["success"] is True
            data = result["data"]
            assert data["stripe_secret_key"] == ""
            assert data["paystack_secret_key"] == ""
            assert data["paypal_secret"] == ""
        finally:
            _restore_single_row_state("payment_config", state)

    def test_gpc_unauthenticated(self, unauthenticated):
        """T021 -- Unauthenticated -> failure, 'Not authenticated'."""
        result = anvil.server.call("get_payment_config")
        assert result["success"] is False
        assert "Not authenticated" in result["error"]


# ===========================================================================
# save_payment_config
# ===========================================================================

class TestSavePaymentConfig:

    def test_spc_happy_path_non_secret_data(self, authenticated):
        """T022 -- Authenticated, valid non-secret data -> success, row written."""
        state = _capture_single_row_state("payment_config")
        try:
            data = {
                "active_gateway": "stripe",
                "test_mode": True,
                "stripe_publishable_key": "TEST_pk_test_abc123",
                "stripe_connected": False,
                "paystack_public_key": "TEST_pk_paystack_abc",
                "paystack_connected": False,
                "paypal_client_id": "TEST_paypal_client_abc",
                "paypal_connected": False,
            }
            result = anvil.server.call("save_payment_config", data)
            assert result["success"] is True
            fetched = anvil.server.call("get_payment_config")
            assert fetched["success"] is True
            assert fetched["data"]["active_gateway"] == "stripe"
            assert fetched["data"]["stripe_publishable_key"] == "TEST_pk_test_abc123"
        finally:
            _restore_single_row_state("payment_config", state)

    def test_spc_stripe_secret_key_not_written(self, authenticated):
        """T023 -- stripe_secret_key in data dict -> column value in DB unchanged."""
        state = _capture_single_row_state("payment_config")
        try:
            before_secrets = anvil.server.call("test_helper_get_raw_payment_secrets")
            original_stripe_sk = before_secrets.get("stripe_secret_key", "")
            result = anvil.server.call("save_payment_config", {
                "active_gateway": "stripe",
                "stripe_secret_key": "TEST_INJECTED_STRIPE_SK",
            })
            assert result["success"] is True
            after_secrets = anvil.server.call("test_helper_get_raw_payment_secrets")
            assert after_secrets.get("stripe_secret_key") == original_stripe_sk, (
                "stripe_secret_key must not be modified by save_payment_config"
            )
        finally:
            _restore_single_row_state("payment_config", state)

    def test_spc_paystack_secret_key_not_written(self, authenticated):
        """T024 -- paystack_secret_key in data dict -> column value in DB unchanged."""
        state = _capture_single_row_state("payment_config")
        try:
            before_secrets = anvil.server.call("test_helper_get_raw_payment_secrets")
            original_paystack_sk = before_secrets.get("paystack_secret_key", "")
            result = anvil.server.call("save_payment_config", {
                "active_gateway": "paystack",
                "paystack_secret_key": "TEST_INJECTED_PAYSTACK_SK",
            })
            assert result["success"] is True
            after_secrets = anvil.server.call("test_helper_get_raw_payment_secrets")
            assert after_secrets.get("paystack_secret_key") == original_paystack_sk, (
                "paystack_secret_key must not be modified by save_payment_config"
            )
        finally:
            _restore_single_row_state("payment_config", state)

    def test_spc_paypal_secret_not_written(self, authenticated):
        """T025 -- paypal_secret in data dict -> column value in DB unchanged."""
        state = _capture_single_row_state("payment_config")
        try:
            before_secrets = anvil.server.call("test_helper_get_raw_payment_secrets")
            original_paypal_sk = before_secrets.get("paypal_secret", "")
            result = anvil.server.call("save_payment_config", {
                "active_gateway": "paypal",
                "paypal_secret": "TEST_INJECTED_PAYPAL_SK",
            })
            assert result["success"] is True
            after_secrets = anvil.server.call("test_helper_get_raw_payment_secrets")
            assert after_secrets.get("paypal_secret") == original_paypal_sk, (
                "paypal_secret must not be modified by save_payment_config"
            )
        finally:
            _restore_single_row_state("payment_config", state)

    def test_spc_unauthenticated(self, unauthenticated):
        """T026 -- Unauthenticated -> failure, 'Not authenticated'."""
        result = anvil.server.call("save_payment_config", {"active_gateway": "stripe"})
        assert result["success"] is False
        assert "Not authenticated" in result["error"]


# ===========================================================================
# get_theme_config
# ===========================================================================

class TestGetThemeConfig:

    def test_gtc_happy_path_row_exists(self, authenticated):
        """T027 -- Authenticated, row exists -> success, all fields returned."""
        state = _capture_single_row_state("theme_config")
        try:
            anvil.server.call("save_theme_config", {
                "primary_color": "#TEST01",
                "accent_color": "#TEST02",
                "font_family": "TEST_Roboto",
                "header_style": "TEST_solid",
            })
            result = anvil.server.call("get_theme_config")
            assert result["success"] is True
            data = result["data"]
            for key in ["primary_color", "accent_color", "font_family",
                        "header_style", "updated_at"]:
                assert key in data, f"Missing key: {key}"
            assert data["primary_color"] == "#TEST01"
            assert data["font_family"] == "TEST_Roboto"
        finally:
            _restore_single_row_state("theme_config", state)

    def test_gtc_empty_table(self, authenticated):
        """T028 -- Authenticated, table empty -> success, empty dict."""
        state = _capture_single_row_state("theme_config")
        try:
            anvil.server.call("test_helper_clear_row", "theme_config")
            result = anvil.server.call("get_theme_config")
            assert result["success"] is True
            assert result["data"] == {}
        finally:
            _restore_single_row_state("theme_config", state)

    def test_gtc_unauthenticated(self, unauthenticated):
        """T029 -- Unauthenticated -> failure, 'Not authenticated'."""
        result = anvil.server.call("get_theme_config")
        assert result["success"] is False
        assert "Not authenticated" in result["error"]


# ===========================================================================
# save_theme_config
# ===========================================================================

class TestSaveThemeConfig:

    def test_stc_happy_path_valid_data(self, authenticated):
        """T030 -- Authenticated, valid data -> success, row written correctly."""
        state = _capture_single_row_state("theme_config")
        try:
            data = {
                "primary_color": "#TEST_AA",
                "accent_color": "#TEST_BB",
                "font_family": "TEST_Inter",
                "header_style": "TEST_gradient",
            }
            result = anvil.server.call("save_theme_config", data)
            assert result["success"] is True
            fetched = anvil.server.call("get_theme_config")
            assert fetched["success"] is True
            assert fetched["data"]["primary_color"] == "#TEST_AA"
            assert fetched["data"]["font_family"] == "TEST_Inter"
            assert fetched["data"]["header_style"] == "TEST_gradient"
            assert "updated_at" in fetched["data"]
        finally:
            _restore_single_row_state("theme_config", state)

    def test_stc_unauthenticated(self, unauthenticated):
        """T031 -- Unauthenticated -> failure, 'Not authenticated'."""
        result = anvil.server.call("save_theme_config", {"primary_color": "#TEST_CC"})
        assert result["success"] is False
        assert "Not authenticated" in result["error"]


# ===========================================================================
# Teardown -- disconnect Uplink
# ===========================================================================

def pytest_sessionfinish(session, exitstatus):
    try:
        anvil.server.disconnect()
    except Exception:
        pass
