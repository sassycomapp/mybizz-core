"""Server module: server_shared/vault_service.py

Mybizz Vault — encrypted client secrets store.

All secrets are encrypted at rest using Fernet symmetric encryption via
encryption_service.py. The encryption_key lives in Anvil Secrets and is
never accessible from client code.

Access control: Owner role only. All callable functions enforce this.
Plaintext values never leave this module — they are decrypted in memory
and used immediately or returned only to other server functions.

Internal convention:
    Secret names beginning with '_' are reserved for system use (e.g.
    '_totp_secret'). These are never returned by list_vault_secrets() and
    are never accessible via the public callable functions. They are read
    and written only by the specific server functions that need them
    (e.g. vault_totp_service.py).

Public callable functions (Owner only):
    set_vault_secret(name, value)   — add or update a secret
    delete_vault_secret(name)       — permanently delete a secret
    list_vault_secrets()            — list secret names only (no values)

Internal server functions (not callable):
    get_vault_secret(name)          — decrypt and return a secret value
    _require_owner()                — enforce Owner role; raise if not
    _is_reserved(name)              — True if name is a system-reserved entry
"""

import anvil.server
import anvil.users
import anvil.tables as tables
from anvil.tables import app_tables
import logging
from datetime import datetime

from .encryption_service import encrypt_value, decrypt_value

logger = logging.getLogger(__name__)

# Prefix that marks a vault entry as system-reserved.
# Reserved entries are hidden from list_vault_secrets() and cannot be
# read, written, or deleted via the public callable functions.
_RESERVED_PREFIX = '_'


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _require_owner() -> object:
    """Return the current user if they are the Owner; raise otherwise.

    Returns:
        The authenticated users row.

    Raises:
        Exception: If the user is not authenticated or does not hold the
            Owner role. Generic message — does not reveal role structure.
    """
    user = anvil.users.get_user()
    if not user:
        raise Exception("Access denied: authentication required")
    if user.get('role') != 'owner':
        raise Exception("Access denied: insufficient permissions")
    return user


def _is_reserved(name: str) -> bool:
    """Return True if the secret name is system-reserved.

    Reserved names begin with '_'. They are not accessible via the public
    callable functions and are never listed in list_vault_secrets().

    Args:
        name: The secret name to check.

    Returns:
        bool: True if reserved, False if available for Owner use.
    """
    return isinstance(name, str) and name.startswith(_RESERVED_PREFIX)


def _validate_name(name: str) -> None:
    """Validate a user-supplied secret name.

    Args:
        name: The secret name to validate.

    Raises:
        ValueError: If the name is empty, not a string, or reserved.
    """
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Secret name must be a non-empty string")
    if _is_reserved(name):
        raise ValueError(
            f"Secret name '{name}' is reserved for system use"
        )


# ---------------------------------------------------------------------------
# Internal server function — not callable from client
# ---------------------------------------------------------------------------

def get_vault_secret(name: str) -> str:
    """Retrieve and decrypt a secret value from the vault table.

    This function is for internal server use only. It is not decorated
    with @anvil.server.callable and cannot be called from client code.
    It does not enforce the Owner role — callers are trusted server
    functions that have already validated their own access context.

    Reserved names (beginning with '_') ARE accessible here — this is
    intentional. System functions such as vault_totp_service.py use this
    to retrieve '_totp_secret' and similar entries.

    Args:
        name: The exact secret name to retrieve.

    Returns:
        str: The decrypted plaintext value.

    Raises:
        Exception: If no secret with that name exists in the vault.
        RuntimeError: If the encryption key is not configured.
        cryptography.fernet.InvalidToken: If the stored value is corrupt.
    """
    if not isinstance(name, str) or not name.strip():
        raise ValueError("get_vault_secret: name must be a non-empty string")

    row = app_tables.vault.get(name=name)
    if row is None:
        raise Exception(
            f"Vault secret '{name}' not found. "
            "Configure it in the Vault before use."
        )

    logger.debug("get_vault_secret: decrypting secret", extra={"name": name})
    return decrypt_value(row['value'])


# ---------------------------------------------------------------------------
# Callable functions — Owner role only
# ---------------------------------------------------------------------------

@anvil.server.callable
def set_vault_secret(name: str, value: str) -> dict:
    """Add a new secret or update an existing one in the vault.

    Encrypts the value before writing. Creates a new row if the name does
    not exist; updates the existing row if it does. Reserved names
    (beginning with '_') cannot be set via this function.

    Args:
        name:  The secret name. Must be non-empty and not reserved.
        value: The plaintext secret value. Must be non-empty.

    Returns:
        dict: {'success': True, 'data': None}
              {'success': False, 'error': str}
    """
    logger.info("set_vault_secret called", extra={"name": name})
    try:
        user = _require_owner()
        _validate_name(name)

        if not isinstance(value, str) or not value.strip():
            return {'success': False, 'error': "Secret value must be non-empty"}

        ciphertext = encrypt_value(value)
        now        = datetime.now()
        row        = app_tables.vault.get(name=name)

        if row is None:
            app_tables.vault.add_row(
                name=name,
                value=ciphertext,
                created_at=now,
                updated_at=now,
                updated_by=user,
            )
            logger.info("set_vault_secret: created new entry", extra={"name": name})
        else:
            row.update(
                value=ciphertext,
                updated_at=now,
                updated_by=user,
            )
            logger.info("set_vault_secret: updated existing entry", extra={"name": name})

        return {'success': True, 'data': None}

    except AssertionError:
        raise
    except ValueError as exc:
        logger.warning("set_vault_secret: validation error", extra={"name": name})
        return {'success': False, 'error': str(exc)}
    except RuntimeError as exc:
        # Encryption key not configured — surface clearly
        logger.error("set_vault_secret: encryption error", exc_info=True)
        return {'success': False, 'error': str(exc)}
    except Exception:
        logger.error("set_vault_secret: unexpected error", exc_info=True)
        return {'success': False, 'error': "Could not save secret. Please try again."}


@anvil.server.callable
def delete_vault_secret(name: str) -> dict:
    """Permanently delete a secret from the vault.

    The deleted value is unrecoverable. Reserved names cannot be deleted
    via this function.

    Args:
        name: The exact secret name to delete.

    Returns:
        dict: {'success': True, 'data': None}
              {'success': False, 'error': str}
    """
    logger.info("delete_vault_secret called", extra={"name": name})
    try:
        _require_owner()
        _validate_name(name)

        row = app_tables.vault.get(name=name)
        if row is None:
            return {'success': False, 'error': f"Secret '{name}' not found"}

        row.delete()
        logger.info("delete_vault_secret: deleted", extra={"name": name})
        return {'success': True, 'data': None}

    except AssertionError:
        raise
    except ValueError as exc:
        logger.warning("delete_vault_secret: validation error", extra={"name": name})
        return {'success': False, 'error': str(exc)}
    except Exception:
        logger.error("delete_vault_secret: unexpected error", exc_info=True)
        return {'success': False, 'error': "Could not delete secret. Please try again."}


@anvil.server.callable
def list_vault_secrets() -> dict:
    """Return a list of all non-reserved secret names in the vault.

    Values are never returned. Reserved entries (names beginning with '_')
    are excluded — they are invisible to the Owner in the UI.

    Returns:
        dict: {'success': True, 'data': [str, ...]}
              {'success': False, 'error': str}
    """
    logger.info("list_vault_secrets called")
    try:
        _require_owner()

        names = [
            row['name']
            for row in app_tables.vault.search()
            if not _is_reserved(row['name'])
        ]

        logger.debug(
            "list_vault_secrets: returning names",
            extra={"count": len(names)},
        )
        return {'success': True, 'data': sorted(names)}

    except AssertionError:
        raise
    except Exception:
        logger.error("list_vault_secrets: unexpected error", exc_info=True)
        return {'success': False, 'error': "Could not load vault secrets."}
