"""Server module: server_shared/vault_totp_service.py

TOTP step-up authentication for Vault access.

Implements Google Authenticator-compatible TOTP (RFC 6238) as a step-up
challenge that fires every time VaultForm is opened. This is separate from
app-level login — the user is already authenticated; this confirms physical
possession of their TOTP device before Vault contents are accessible.

The TOTP secret is stored in the vault table as a reserved entry named
'_totp_secret', encrypted at rest via Fernet. It is never returned to
client code and never appears in list_vault_secrets().

Flow:
    1. Owner opens VaultForm
    2. Client calls get_vault_totp_uri() — returns a setup URI if first
       time, or indicates TOTP is already configured
    3. Owner enters the 6-digit code from their Authenticator app
    4. Client calls verify_vault_totp(token) — server validates the token
       against the stored secret using pyotp with a ±1 window
    5. On success, the server returns a short-lived session token
    6. All subsequent Vault callable functions validate this session token
       before executing

Session token:
    A Fernet-encrypted string containing the user's email and an expiry
    timestamp. Stored in memory on the client only — never persisted.
    Valid for VAULT_SESSION_TTL_SECONDS from the moment of issue.
    Each Vault callable that requires a verified session calls
    require_vault_session(session_token) before doing any work.

TOTP secret name reserved in vault table: '_totp_secret'
TOTP issuer name shown in Authenticator app: 'Mybizz Vault'
"""

import anvil.server
import anvil.users
import anvil.email
import anvil.tables as tables
from anvil.tables import app_tables
import logging
import pyotp
from datetime import datetime, timedelta
import json

from .encryption_service import encrypt_value, decrypt_value
from .vault_service import get_vault_secret, _require_owner

logger = logging.getLogger(__name__)

# Reserved vault entry name for the TOTP secret
_TOTP_SECRET_NAME = '_totp_secret'

# Session token validity window in seconds
VAULT_SESSION_TTL_SECONDS = 300  # 5 minutes

# TOTP issuer label shown in Google Authenticator
_TOTP_ISSUER = 'Mybizz Vault'

# Allowed TOTP window — accepts current code ±1 interval (±30 seconds)
# to compensate for minor clock skew between server and device
_TOTP_WINDOW = 1


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_totp_secret() -> str:
    """Retrieve the plaintext TOTP secret from the vault.

    Returns:
        str: The base32 TOTP secret.

    Raises:
        Exception: If '_totp_secret' has not been initialised in the vault.
    """
    return get_vault_secret(_TOTP_SECRET_NAME)


def _store_totp_secret(secret: str, user) -> None:
    """Encrypt and store a new TOTP secret in the vault.

    Args:
        secret: The base32 TOTP secret to store.
        user:   The Owner users row (written to updated_by).
    """
    now        = datetime.now()
    ciphertext = encrypt_value(secret)
    row        = app_tables.vault.get(name=_TOTP_SECRET_NAME)

    if row is None:
        app_tables.vault.add_row(
            name=_TOTP_SECRET_NAME,
            value=ciphertext,
            created_at=now,
            updated_at=now,
            updated_by=user,
        )
    else:
        row.update(value=ciphertext, updated_at=now, updated_by=user)


def _issue_session_token(user_email: str) -> str:
    """Issue a short-lived Fernet session token for a verified Vault session.

    The token encodes the user's email and an expiry timestamp. It is
    encrypted with the same Fernet key used by the Vault, making it
    tamper-proof. It is never persisted — the client holds it in memory
    for the duration of the VaultForm session.

    Args:
        user_email: The authenticated Owner's email address.

    Returns:
        str: Encrypted session token string.
    """
    expiry  = datetime.now() + timedelta(seconds=VAULT_SESSION_TTL_SECONDS)
    payload = json.dumps({
        'email':  user_email,
        'expiry': expiry.isoformat(),
    })
    return encrypt_value(payload)


def _validate_session_token(session_token: str, user_email: str) -> bool:
    """Validate a Vault session token.

    Decrypts the token, checks that the email matches the current user,
    and confirms the token has not expired.

    Args:
        session_token: The token issued by verify_vault_totp().
        user_email:    The current user's email for binding check.

    Returns:
        bool: True if the token is valid and unexpired, False otherwise.
    """
    try:
        payload = json.loads(decrypt_value(session_token))
        if payload.get('email') != user_email:
            logger.warning("_validate_session_token: email mismatch")
            return False
        expiry = datetime.fromisoformat(payload['expiry'])
        if datetime.now() > expiry:
            logger.info("_validate_session_token: token expired")
            return False
        return True
    except Exception:
        logger.warning(
            "_validate_session_token: validation failed", exc_info=True
        )
        return False


def _send_vault_access_notification(user) -> None:
    """Send an email notification to the Owner on every Vault access.

    Fires after a successful TOTP verification. If the Owner receives a
    notification they did not trigger, they know immediately that
    unauthorised access has occurred.

    Failures are logged and silently swallowed — a notification failure
    must never block Vault access.

    Args:
        user: The authenticated Owner users row.
    """
    try:
        email   = user.get('email', '')
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        anvil.email.send(
            to=email,
            subject='Mybizz Vault accessed',
            text=(
                f"Your Mybizz Vault was accessed at {now_str}.\n\n"
                "If you did not open the Vault at this time, please change "
                "your password immediately and contact support."
            ),
        )
        logger.info(
            "_send_vault_access_notification: sent",
            extra={"email": email},
        )
    except Exception:
        logger.warning(
            "_send_vault_access_notification: send failed — access not blocked",
            exc_info=True,
        )


# ---------------------------------------------------------------------------
# Callable functions
# ---------------------------------------------------------------------------

@anvil.server.callable
def get_vault_totp_setup() -> dict:
    """Return TOTP setup information for first-time Vault configuration.

    Generates a new TOTP secret if one does not already exist, stores it
    encrypted in the vault, and returns a provisioning URI suitable for
    display as a QR code in the client.

    If TOTP is already configured, returns is_configured=True with no URI
    so the client shows the entry form rather than the setup QR code.

    Returns:
        dict: {
            'success': True,
            'data': {
                'is_configured': bool,
                'uri': str | None,   # otpauth:// URI for QR code, or None
                'secret': str | None # base32 secret for manual entry, or None
            }
        }
        dict: {'success': False, 'error': str}
    """
    logger.info("get_vault_totp_setup called")
    try:
        user = _require_owner()

        # Check if _totp_secret already exists
        existing = app_tables.vault.get(name=_TOTP_SECRET_NAME)
        if existing:
            return {
                'success': True,
                'data': {
                    'is_configured': True,
                    'uri':           None,
                    'secret':        None,
                },
            }

        # Generate a new TOTP secret and store it
        secret = pyotp.random_base32()
        _store_totp_secret(secret, user)

        totp = pyotp.TOTP(secret)
        uri  = totp.provisioning_uri(
            name=user.get('email', 'owner'),
            issuer_name=_TOTP_ISSUER,
        )

        logger.info("get_vault_totp_setup: new secret generated and stored")
        return {
            'success': True,
            'data': {
                'is_configured': False,
                'uri':           uri,
                'secret':        secret,  # for manual entry fallback
            },
        }

    except AssertionError:
        raise
    except Exception:
        logger.error("get_vault_totp_setup: unexpected error", exc_info=True)
        return {'success': False, 'error': "Could not set up Vault authentication."}


@anvil.server.callable
def verify_vault_totp(token: str) -> dict:
    """Verify a TOTP token and issue a Vault session token on success.

    Validates the 6-digit token against the stored TOTP secret using a
    ±1 interval window to tolerate minor clock skew. On success, sends
    the Owner an email notification and returns a session token that
    authorises access to Vault callable functions for
    VAULT_SESSION_TTL_SECONDS.

    Args:
        token: The 6-digit TOTP code from the Owner's Authenticator app.

    Returns:
        dict: {
            'success': True,
            'data': {
                'session_token': str,   # pass to all subsequent Vault calls
                'ttl_seconds':   int,   # how long the token is valid for
            }
        }
        dict: {'success': False, 'error': str}
    """
    logger.info("verify_vault_totp called")
    try:
        user = _require_owner()

        if not token or not str(token).strip():
            return {'success': False, 'error': "Authentication code is required"}

        secret     = _get_totp_secret()
        totp       = pyotp.TOTP(secret)
        is_valid   = totp.verify(str(token).strip(), valid_window=_TOTP_WINDOW)

        if not is_valid:
            logger.warning(
                "verify_vault_totp: invalid token",
                extra={"email": user.get('email')},
            )
            return {'success': False, 'error': "Invalid authentication code. Please try again."}

        # Valid — issue session token and notify
        session_token = _issue_session_token(user.get('email'))
        _send_vault_access_notification(user)

        logger.info(
            "verify_vault_totp: verified, session issued",
            extra={"email": user.get('email')},
        )
        return {
            'success': True,
            'data': {
                'session_token': session_token,
                'ttl_seconds':   VAULT_SESSION_TTL_SECONDS,
            },
        }

    except AssertionError:
        raise
    except Exception:
        logger.error("verify_vault_totp: unexpected error", exc_info=True)
        return {'success': False, 'error': "Authentication failed. Please try again."}


def require_vault_session(session_token: str) -> None:
    """Assert that the session token is valid for the current Owner.

    Called at the top of every Vault callable that requires a verified
    TOTP session. Raises an exception if the token is missing, expired,
    or does not match the current user.

    This function is not decorated with @anvil.server.callable — it is
    an internal guard for other server functions to call directly.

    Args:
        session_token: The token returned by verify_vault_totp().

    Raises:
        Exception: If the session is invalid, expired, or the user is
            not the Owner.
    """
    user = _require_owner()
    if not session_token:
        raise Exception("Vault session required. Please authenticate first.")
    if not _validate_session_token(session_token, user.get('email')):
        raise Exception(
            "Vault session has expired. Please re-authenticate to continue."
        )
