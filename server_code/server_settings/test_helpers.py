"""
Test helper server functions for Stage 1.4 Uplink integration tests.

IMPORTANT: These functions are for automated testing only.
They must never be called from production client code.
They provide controlled state manipulation for single-row config tables.

Covered tables: business_profile, email_config, payment_config, theme_config.
"""

import anvil.server
import anvil.users
import anvil.tables as tables
from anvil.tables import app_tables
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Table column maps -- defines which columns to capture/restore per table.
# Media columns (logo) are excluded from capture/restore -- they cannot be
# round-tripped as plain dicts over Uplink. The logo column is left
# untouched by restore; its pre-test value is preserved by never deleting
# the row.
# ---------------------------------------------------------------------------

_TABLE_COLUMNS = {
    "business_profile": [
        "business_name", "tagline", "description",
        "contact_email", "phone",
        "address_line_1", "address_line_2", "city", "country", "postal_code",
        "website_url", "social_facebook", "social_instagram",
        "social_x", "social_linkedin", "updated_at",
    ],
    "email_config": [
        "email_provider", "smtp_host", "smtp_port", "smtp_username",
        "smtp_password", "from_email", "from_name", "configured", "configured_at",
    ],
    "payment_config": [
        "active_gateway",
        "stripe_publishable_key", "stripe_secret_key", "stripe_connected", "stripe_connected_at",
        "paystack_public_key", "paystack_secret_key", "paystack_connected", "paystack_connected_at",
        "paypal_client_id", "paypal_secret", "paypal_connected", "paypal_connected_at",
        "test_mode", "configured_at",
    ],
    "theme_config": [
        "primary_color", "accent_color", "font_family", "header_style", "updated_at",
    ],
}


def _get_table(table_name: str):
    """Return the app_tables reference for the given table name."""
    mapping = {
        "business_profile": app_tables.business_profile,
        "email_config": app_tables.email_config,
        "payment_config": app_tables.payment_config,
        "theme_config": app_tables.theme_config,
    }
    if table_name not in mapping:
        raise ValueError(f"test_helper: unknown table '{table_name}'")
    return mapping[table_name]


@anvil.server.callable
def test_helper_capture_row(table_name: str) -> dict:
    """Capture the current state of a single-row config table.

    Returns the row as a plain dict (media columns excluded), or None
    if the table is empty.

    Args:
        table_name: One of business_profile, email_config,
                    payment_config, theme_config.

    Returns:
        dict: {'data': {col: value, ...}} or {'data': None}
    """
    logger.debug("test_helper_capture_row: %s", table_name)
    tbl = _get_table(table_name)
    cols = _TABLE_COLUMNS[table_name]
    rows = list(tbl.search())
    if not rows:
        return {"data": None}
    row = rows[0]
    state = {col: row[col] for col in cols}
    return {"data": state}


@anvil.server.callable
def test_helper_restore_row(table_name: str, state: dict) -> dict:
    """Restore a single-row config table to a previously captured state.

    If state is None the table was empty before the test; any row written
    during the test is deleted. If state is a dict the row is updated back
    to that state (or a new row is created if none exists).

    Media columns (logo) are never touched by this function.

    Args:
        table_name: One of business_profile, email_config,
                    payment_config, theme_config.
        state: Dict from test_helper_capture_row, or None.

    Returns:
        dict: {'success': True}
    """
    logger.debug("test_helper_restore_row: %s", table_name)
    tbl = _get_table(table_name)
    rows = list(tbl.search())
    row = rows[0] if rows else None

    if state is None:
        # Table was empty before test -- delete any row that was created
        if row is not None:
            row.delete()
            logger.debug("test_helper_restore_row: deleted test row from %s", table_name)
    else:
        # Restore to captured state
        if row is None:
            tbl.add_row(**state)
            logger.debug("test_helper_restore_row: re-created row in %s", table_name)
        else:
            row.update(**state)
            logger.debug("test_helper_restore_row: restored row in %s", table_name)

    return {"success": True}


@anvil.server.callable
def test_helper_clear_row(table_name: str) -> dict:
    """Delete the single row from a config table (for empty-table edge case tests).

    The caller is responsible for restoring state via test_helper_restore_row.

    Args:
        table_name: One of business_profile, email_config,
                    payment_config, theme_config.

    Returns:
        dict: {'success': True}
    """
    logger.debug("test_helper_clear_row: %s", table_name)
    tbl = _get_table(table_name)
    rows = list(tbl.search())
    for row in rows:
        row.delete()
    return {"success": True}


@anvil.server.callable
def test_helper_set_email_configured_true() -> dict:
    """Force email_config.configured = True for testing reset behaviour.

    Creates a minimal row if none exists.

    Returns:
        dict: {'success': True}
    """
    logger.debug("test_helper_set_email_configured_true called")
    rows = list(app_tables.email_config.search())
    if rows:
        rows[0].update(configured=True)
    else:
        app_tables.email_config.add_row(
            smtp_host="TEST_smtp.example.com",
            smtp_port=587,
            smtp_username="TEST_user",
            smtp_password="TEST_pw",
            from_email="TEST_from@example.com",
            from_name="TEST_Name",
            configured=True,
        )
    return {"success": True}


@anvil.server.callable
def test_helper_set_payment_secrets(
    stripe_sk: str,
    paystack_sk: str,
    paypal_sk: str,
) -> dict:
    """Write raw secret key values directly to payment_config for masking tests.

    This bypasses save_payment_config intentionally -- it is the only way to
    populate secret columns for get_payment_config masking verification.
    Creates a minimal row if none exists.

    Args:
        stripe_sk: Value to write to stripe_secret_key.
        paystack_sk: Value to write to paystack_secret_key.
        paypal_sk: Value to write to paypal_secret.

    Returns:
        dict: {'success': True}
    """
    logger.debug("test_helper_set_payment_secrets called")
    rows = list(app_tables.payment_config.search())
    fields = {
        "stripe_secret_key": stripe_sk,
        "paystack_secret_key": paystack_sk,
        "paypal_secret": paypal_sk,
    }
    if rows:
        rows[0].update(**fields)
    else:
        app_tables.payment_config.add_row(
            active_gateway="",
            stripe_publishable_key="",
            stripe_connected=False,
            paystack_public_key="",
            paystack_connected=False,
            paypal_client_id="",
            paypal_connected=False,
            test_mode=True,
            **fields,
        )
    return {"success": True}


@anvil.server.callable
def test_helper_get_raw_payment_secrets() -> dict:
    """Return the raw (unmasked) secret key values from payment_config.

    Used by secret-boundary tests to verify save_payment_config does not
    overwrite secret columns.

    Returns:
        dict: {
            'stripe_secret_key': str,
            'paystack_secret_key': str,
            'paypal_secret': str,
        }
    """
    logger.debug("test_helper_get_raw_payment_secrets called")
    rows = list(app_tables.payment_config.search())
    if not rows:
        return {
            "stripe_secret_key": "",
            "paystack_secret_key": "",
            "paypal_secret": "",
        }
    row = rows[0]
    return {
        "stripe_secret_key": row["stripe_secret_key"] or "",
        "paystack_secret_key": row["paystack_secret_key"] or "",
        "paypal_secret": row["paypal_secret"] or "",
    }
