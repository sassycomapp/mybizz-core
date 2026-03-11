"""Server module f"""

import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import logging
import smtplib
import socket
from email.mime.text import MIMEText
from datetime import datetime

logger = logging.getLogger(__name__)


def create_initial_config(business_name: str, user=None) -> dict:
  """Create minimal config rows for a newly created client instance.

    Args:
        business_name: The name of the business being registered.
        user: Optional user row to attribute updates.

    Returns:
        dict: {'success': True, 'data': {'key': str}}

    Raises:
        ValueError: If business_name is missing or empty.
        RuntimeError: If a Data Tables write fails.
    """
  if not business_name or not business_name.strip():
    raise ValueError("Business name is required")

  owner = user or anvil.users.get_user()
  now = datetime.now()
  key = 'business_profile'
  value = {'business_name': business_name.strip()}

  try:
    existing = app_tables.config.get(key=key)
    if existing:
      existing['value'] = value
      existing['category'] = 'system'
      existing['updated_at'] = now
      if owner:
        existing['updated_by'] = owner
    else:
      app_tables.config.add_row(
        key=key,
        value=value,
        category='system',
        updated_at=now,
        updated_by=owner,
      )
    logger.info("create_initial_config succeeded", extra={"key": key})
    return {'success': True, 'data': {'key': key}}
  except tables.TableError as exc:
    logger.error("create_initial_config table error", exc_info=True)
    raise RuntimeError("Failed to create initial config") from exc
  except Exception as exc:
    logger.error("create_initial_config unexpected error", exc_info=True)
    raise RuntimeError("Failed to create initial config") from exc


# ---------------------------------------------------------------------------
# Business profile
# ---------------------------------------------------------------------------

@anvil.server.callable
def get_business_profile() -> dict:
  """Return all business_profile fields as a plain dict.

    The logo media object is converted to a URL string so it can be safely
    passed to the client and assigned to an Image component's source property.

    Returns:
        dict: {'success': True, 'data': {field: value, ...}}
              {'success': False, 'error': str}
    """
  logger.info("get_business_profile called")
  user = anvil.users.get_user()
  if user is None:
    return {'success': False, 'error': 'Not authenticated'}

  try:
    rows = list(app_tables.business_profile.search())
    row  = rows[0] if rows else None

    if row is None:
      logger.debug("get_business_profile: no row found, returning empty dict")
      return {'success': True, 'data': {}}

    logo = row['logo']
    # Convert media object to URL string; pass None if no logo stored
    logo_url = logo.url if logo is not None else None

    data = {
      'business_name':  row['business_name'],
      'tagline':        row['tagline'],
      'description':    row['description'],
      'logo':           logo_url,
      'contact_email':  row['contact_email'],
      'phone':          row['phone'],
      'address_line_1': row['address_line_1'],
      'address_line_2': row['address_line_2'],
      'city':           row['city'],
      'country':        row['country'],
      'postal_code':    row['postal_code'],
      'website_url':    row['website_url'],
      'social_facebook':  row['social_facebook'],
      'social_instagram': row['social_instagram'],
      'social_x':         row['social_x'],
      'social_linkedin':  row['social_linkedin'],
      'updated_at':     row['updated_at'],
    }
    logger.debug("get_business_profile: returning profile")
    return {'success': True, 'data': data}

  except tables.TableError as exc:
    logger.error("get_business_profile table error", exc_info=True)
    return {'success': False, 'error': str(exc)}
  except Exception as exc:
    logger.error("get_business_profile unexpected error", exc_info=True)
    return {'success': False, 'error': 'An unexpected error occurred'}


@anvil.server.callable
def save_business_profile(data: dict, logo_file=None) -> dict:
  """Create or update the business_profile row.

    Args:
        data:      Dict of business profile fields to write.
        logo_file: Optional Anvil media object uploaded from the client.
                   When provided, written to the logo media column.

    Returns:
        dict: {'success': True, 'data': None}
              {'success': False, 'error': str}
    """
  logger.info("save_business_profile called")
  user = anvil.users.get_user()
  if user is None:
    return {'success': False, 'error': 'Not authenticated'}

  try:
    now  = datetime.now()
    rows = list(app_tables.business_profile.search())
    row  = rows[0] if rows else None

    fields = {
      'business_name':    data.get('business_name', ''),
      'tagline':          data.get('tagline', ''),
      'description':      data.get('description', ''),
      'contact_email':    data.get('contact_email', ''),
      'phone':            data.get('phone', ''),
      'address_line_1':   data.get('address_line_1', ''),
      'address_line_2':   data.get('address_line_2', ''),
      'city':             data.get('city', ''),
      'country':          data.get('country', ''),
      'postal_code':      data.get('postal_code', ''),
      'website_url':      data.get('website_url', ''),
      'social_facebook':  data.get('social_facebook', ''),
      'social_instagram': data.get('social_instagram', ''),
      'social_x':         data.get('social_x', ''),
      'social_linkedin':  data.get('social_linkedin', ''),
      'updated_at':       now,
    }

    if logo_file is not None:
      fields['logo'] = logo_file

    if row is None:
      logger.debug("save_business_profile: creating new row")
      app_tables.business_profile.add_row(**fields)
    else:
      logger.debug("save_business_profile: updating existing row")
      row.update(**fields)

    logger.info("save_business_profile: saved successfully")
    return {'success': True, 'data': None}

  except tables.TableError as exc:
    logger.error("save_business_profile table error", exc_info=True)
    return {'success': False, 'error': str(exc)}
  except Exception as exc:
    logger.error("save_business_profile unexpected error", exc_info=True)
    return {'success': False, 'error': 'An unexpected error occurred'}


# ---------------------------------------------------------------------------
# Email configuration
# ---------------------------------------------------------------------------

@anvil.server.callable
def get_email_config() -> dict:
  """Return email_config fields. smtp_password is never returned in plaintext.

    Returns '***' if smtp_password is set, '' if not set.

    Returns:
        dict: {'success': True, 'data': {field: value, ...}}
              {'success': False, 'error': str}
    """
  logger.info("get_email_config called")
  user = anvil.users.get_user()
  if user is None:
    return {'success': False, 'error': 'Not authenticated'}

  try:
    rows = list(app_tables.email_config.search())
    row  = rows[0] if rows else None

    if row is None:
      logger.debug("get_email_config: no row found, returning empty dict")
      return {'success': True, 'data': {}}

      # Never return smtp_password plaintext — mask it
    password_display = '***' if row['smtp_password'] else ''

    data = {
      'email_provider':  row['email_provider'],
      'smtp_host':       row['smtp_host'],
      'smtp_port':       row['smtp_port'],
      'smtp_username':   row['smtp_username'],
      'smtp_password':   password_display,
      'from_email':      row['from_email'],
      'from_name':       row['from_name'],
      'configured':      row['configured'],
      'configured_at':   row['configured_at'],
    }
    logger.debug("get_email_config: returning config")
    return {'success': True, 'data': data}

  except tables.TableError as exc:
    logger.error("get_email_config table error", exc_info=True)
    return {'success': False, 'error': str(exc)}
  except Exception as exc:
    logger.error("get_email_config unexpected error", exc_info=True)
    return {'success': False, 'error': 'An unexpected error occurred'}


@anvil.server.callable
def save_email_config(data: dict) -> dict:
  """Create or update the email_config row.

    Always sets configured = False. Only test_email_connection() may set
    configured = True, ensuring the saved credentials have been verified.

    Args:
        data: Dict containing smtp_host, smtp_port, smtp_username,
              smtp_password, from_email, from_name.

    Returns:
        dict: {'success': True, 'data': None}
              {'success': False, 'error': str}
    """
  logger.info("save_email_config called")
  user = anvil.users.get_user()
  if user is None:
    return {'success': False, 'error': 'Not authenticated'}

  try:
    rows = list(app_tables.email_config.search())
    row  = rows[0] if rows else None

    fields = {
      'smtp_host':     data.get('smtp_host', ''),
      'smtp_port':     data.get('smtp_port'),
      'smtp_username': data.get('smtp_username', ''),
      'smtp_password': data.get('smtp_password', ''),
      'from_email':    data.get('from_email', ''),
      'from_name':     data.get('from_name', ''),
      # Always reset configured — must re-test after any save
      'configured':    False,
    }

    if row is None:
      logger.debug("save_email_config: creating new row")
      app_tables.email_config.add_row(**fields)
    else:
      logger.debug("save_email_config: updating existing row")
      row.update(**fields)

    logger.info("save_email_config: saved successfully")
    return {'success': True, 'data': None}

  except tables.TableError as exc:
    logger.error("save_email_config table error", exc_info=True)
    return {'success': False, 'error': str(exc)}
  except Exception as exc:
    logger.error("save_email_config unexpected error", exc_info=True)
    return {'success': False, 'error': 'An unexpected error occurred'}


@anvil.server.callable
def test_email_connection() -> dict:
  """Send a real test email using the stored SMTP credentials.

    Reads smtp_host, smtp_port, smtp_username, smtp_password from
    email_config and sends a plain-text test message to the logged-in
    user's email address.

    On success: sets configured = True and configured_at = now.
    On failure: returns the exact exception message string.

    Returns:
        dict: {'success': True, 'data': 'Test email sent successfully to <email>'}
              {'success': False, 'error': <exact exception message>}
    """
  logger.info("test_email_connection called")
  user = anvil.users.get_user()
  if user is None:
    return {'success': False, 'error': 'Not authenticated'}

  try:
    rows = list(app_tables.email_config.search())
    row  = rows[0] if rows else None

    if row is None:
      return {'success': False, 'error': 'No email configuration found. Save your settings first.'}

    smtp_host     = row['smtp_host']
    smtp_port     = row['smtp_port']
    smtp_username = row['smtp_username']
    smtp_password = row['smtp_password']
    from_email    = row['from_email']
    from_name     = row['from_name']
    to_email      = user['email']

    if not all([smtp_host, smtp_port, smtp_username, smtp_password, from_email]):
      return {'success': False, 'error': 'Email configuration is incomplete. Please fill in all fields.'}

    logger.debug("test_email_connection: connecting to SMTP",
                 extra={'smtp_host': smtp_host, 'smtp_port': smtp_port})

    msg = MIMEText(
      "This is a test email from Mybizz.\n\n"
            "Your SMTP configuration is working correctly."
        )
        msg['Subject'] = 'Mybizz — SMTP Test'
        msg['From']    = f"{from_name} <{from_email}>" if from_name else from_email
        msg['To']      = to_email

        with smtplib.SMTP(smtp_host, int(smtp_port), timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_username, smtp_password)
            server.sendmail(from_email, [to_email], msg.as_string())

        # Mark as configured only after a successful send
        now = datetime.now()
        row.update(configured=True, configured_at=now)

        logger.info("test_email_connection: test email sent",
                    extra={'to_email': to_email})
        return {'success': True, 'data': f'Test email sent successfully to {to_email}'}

    except smtplib.SMTPAuthenticationError as exc:
        logger.warning("test_email_connection: authentication failed", exc_info=True)
        return {'success': False, 'error': f'Authentication failed: {exc.smtp_error.decode(errors="replace").strip()}'}
    except smtplib.SMTPException as exc:
        logger.warning("test_email_connection: SMTP error", exc_info=True)
        return {'success': False, 'error': str(exc)}
    except socket.error as exc:
        logger.warning("test_email_connection: socket error", exc_info=True)
        return {'success': False, 'error': str(exc)}
    except tables.TableError as exc:
        logger.error("test_email_connection: table error updating configured flag", exc_info=True)
        return {'success': False, 'error': str(exc)}
    except Exception as exc:
        logger.error("test_email_connection: unexpected error", exc_info=True)
        return {'success': False, 'error': 'An unexpected error occurred'}


# ---------------------------------------------------------------------------
# Payment configuration
# ---------------------------------------------------------------------------

# Columns that must NEVER be written by save_payment_config.
# Secret keys are managed exclusively via The Vault (Stage 1.5).
_PAYMENT_SECRET_COLUMNS = frozenset({
    'stripe_secret_key',
    'paystack_secret_key',
    'paypal_secret',
})


@anvil.server.callable
def get_payment_config() -> dict:
    """Return payment_config fields. Secret keys are never returned in plaintext.

    Returns '***' for each secret key if set, '' if not set.

    Returns:
        dict: {'success': True, 'data': {field: value, ...}}
              {'success': False, 'error': str}
    """
    logger.info("get_payment_config called")
    user = anvil.users.get_user()
    if user is None:
        return {'success': False, 'error': 'Not authenticated'}

    try:
        rows = list(app_tables.payment_config.search())
        row  = rows[0] if rows else None

        if row is None:
            logger.debug("get_payment_config: no row found, returning empty dict")
            return {'success': True, 'data': {}}

        # Mask all three secret keys — never return plaintext to client
        stripe_sk_display   = '***' if row['stripe_secret_key']   else ''
        paystack_sk_display = '***' if row['paystack_secret_key'] else ''
        paypal_sk_display   = '***' if row['paypal_secret']       else ''

        data = {
            'active_gateway':         row['active_gateway'],
            'stripe_publishable_key': row['stripe_publishable_key'],
            'stripe_secret_key':      stripe_sk_display,
            'stripe_connected':       row['stripe_connected'],
            'stripe_connected_at':    row['stripe_connected_at'],
            'paystack_public_key':    row['paystack_public_key'],
            'paystack_secret_key':    paystack_sk_display,
            'paystack_connected':     row['paystack_connected'],
            'paystack_connected_at':  row['paystack_connected_at'],
            'paypal_client_id':       row['paypal_client_id'],
            'paypal_secret':          paypal_sk_display,
            'paypal_connected':       row['paypal_connected'],
            'paypal_connected_at':    row['paypal_connected_at'],
            'test_mode':              row['test_mode'],
            'configured_at':          row['configured_at'],
        }
        logger.debug("get_payment_config: returning config")
        return {'success': True, 'data': data}

    except tables.TableError as exc:
        logger.error("get_payment_config table error", exc_info=True)
        return {'success': False, 'error': str(exc)}
    except Exception as exc:
        logger.error("get_payment_config unexpected error", exc_info=True)
        return {'success': False, 'error': 'An unexpected error occurred'}


@anvil.server.callable
def save_payment_config(data: dict) -> dict:
    """Create or update the payment_config row.

    Secret key columns (stripe_secret_key, paystack_secret_key, paypal_secret)
    are explicitly excluded from all write operations regardless of what is
    present in the data dict. These columns are managed exclusively via
    The Vault (Stage 1.5).

    Args:
        data: Dict of payment config fields. Secret key fields are ignored
              even if present.

    Returns:
        dict: {'success': True, 'data': None}
              {'success': False, 'error': str}
    """
    logger.info("save_payment_config called")
    user = anvil.users.get_user()
    if user is None:
        return {'success': False, 'error': 'Not authenticated'}

    try:
        now  = datetime.now()
        rows = list(app_tables.payment_config.search())
        row  = rows[0] if rows else None

        # Build write dict from the explicit safe-column list only.
        # _PAYMENT_SECRET_COLUMNS are never written here under any circumstances.
        fields = {
            'active_gateway':         data.get('active_gateway', ''),
            'test_mode':              bool(data.get('test_mode', True)),
            'stripe_publishable_key': data.get('stripe_publishable_key', ''),
            'stripe_connected':       bool(data.get('stripe_connected', False)),
            'paystack_public_key':    data.get('paystack_public_key', ''),
            'paystack_connected':     bool(data.get('paystack_connected', False)),
            'paypal_client_id':       data.get('paypal_client_id', ''),
            'paypal_connected':       bool(data.get('paypal_connected', False)),
            'configured_at':          now,
        }

        # Defensive assertion — secret columns must not be in the write dict
        assert not (_PAYMENT_SECRET_COLUMNS & set(fields)), (
            "Secret key columns leaked into save_payment_config write dict"
        )

        if row is None:
            logger.debug("save_payment_config: creating new row")
            app_tables.payment_config.add_row(**fields)
        else:
            logger.debug("save_payment_config: updating existing row")
            row.update(**fields)

        logger.info("save_payment_config: saved successfully")
        return {'success': True, 'data': None}

    except tables.TableError as exc:
        logger.error("save_payment_config table error", exc_info=True)
        return {'success': False, 'error': str(exc)}
    except Exception as exc:
        logger.error("save_payment_config unexpected error", exc_info=True)
        return {'success': False, 'error': 'An unexpected error occurred'}


# ---------------------------------------------------------------------------
# Theme configuration
# ---------------------------------------------------------------------------

@anvil.server.callable
def get_theme_config() -> dict:
    """Return all theme_config fields as a plain dict.

    Returns:
        dict: {'success': True, 'data': {field: value, ...}}
              {'success': False, 'error': str}
    """
    logger.info("get_theme_config called")
    user = anvil.users.get_user()
    if user is None:
        return {'success': False, 'error': 'Not authenticated'}

    try:
        rows = list(app_tables.theme_config.search())
        row  = rows[0] if rows else None

        if row is None:
            logger.debug("get_theme_config: no row found, returning empty dict")
            return {'success': True, 'data': {}}

        data = {
            'primary_color': row['primary_color'],
            'accent_color':  row['accent_color'],
            'font_family':   row['font_family'],
            'header_style':  row['header_style'],
            'updated_at':    row['updated_at'],
        }
        logger.debug("get_theme_config: returning config")
        return {'success': True, 'data': data}

    except tables.TableError as exc:
        logger.error("get_theme_config table error", exc_info=True)
        return {'success': False, 'error': str(exc)}
    except Exception as exc:
        logger.error("get_theme_config unexpected error", exc_info=True)
        return {'success': False, 'error': 'An unexpected error occurred'}


@anvil.server.callable
def save_theme_config(data: dict) -> dict:
    """Create or update the theme_config row.

    Args:
        data: Dict containing primary_color, accent_color,
              font_family, header_style.

    Returns:
        dict: {'success': True, 'data': None}
              {'success': False, 'error': str}
    """
    logger.info("save_theme_config called")
    user = anvil.users.get_user()
    if user is None:
        return {'success': False, 'error': 'Not authenticated'}

    try:
        now  = datetime.now()
        rows = list(app_tables.theme_config.search())
        row  = rows[0] if rows else None

        fields = {
            'primary_color': data.get('primary_color', ''),
            'accent_color':  data.get('accent_color', ''),
            'font_family':   data.get('font_family', ''),
            'header_style':  data.get('header_style', ''),
            'updated_at':    now,
        }

        if row is None:
            logger.debug("save_theme_config: creating new row")
            app_tables.theme_config.add_row(**fields)
        else:
            logger.debug("save_theme_config: updating existing row")
            row.update(**fields)

        logger.info("save_theme_config: saved successfully")
        return {'success': True, 'data': None}

    except tables.TableError as exc:
        logger.error("save_theme_config table error", exc_info=True)
        return {'success': False, 'error': str(exc)}
    except Exception as exc:
        logger.error("save_theme_config unexpected error", exc_info=True)
        return {'success': False, 'error': 'An unexpected error occurred'}


# POLISH COMPLETE — server_settings service module



