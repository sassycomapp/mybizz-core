"""Server module: server_shared/encryption_service.py

Fernet symmetric encryption utilities for the Mybizz Vault.

These functions are internal server utilities only — never callable from
client code. All encryption uses the master encryption_key stored in
Anvil Secrets (set by Mybizz at provisioning via the IDE).

Usage:
    from server_shared.encryption_service import encrypt_value, decrypt_value

    ciphertext = encrypt_value('my-secret')
    plaintext  = decrypt_value(ciphertext)

Raises:
    RuntimeError: If encryption_key is not set in Anvil Secrets.
    cryptography.fernet.InvalidToken: If decryption fails (wrong key or
        corrupted ciphertext).
"""

import anvil.secrets
import logging
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

# Never expose or log this value. Retrieved fresh on each call so that
# provisioning the key mid-session takes effect without a server restart.
_SECRET_NAME = 'encryption_key'


def _get_cipher() -> Fernet:
    """Retrieve the encryption key from Anvil Secrets and return a Fernet cipher.

    Returns:
        Fernet: Initialised cipher instance ready for encrypt/decrypt.

    Raises:
        RuntimeError: If encryption_key is not present in Anvil Secrets.
    """
    try:
        key = anvil.secrets.get_secret(_SECRET_NAME)
    except Exception:
        logger.error(
            "encryption_service: encryption_key not found in Anvil Secrets. "
            "Set this via the Anvil IDE before using the Vault.",
            exc_info=True,
        )
        raise RuntimeError(
            "Vault encryption key is not configured. "
            "Contact your Mybizz administrator."
        )
    return Fernet(key.encode())


def encrypt_value(plaintext: str) -> str:
    """Encrypt a plaintext string using Fernet symmetric encryption.

    Args:
        plaintext: The string to encrypt. Must not be empty.

    Returns:
        str: URL-safe base64-encoded ciphertext string.

    Raises:
        ValueError: If plaintext is empty or not a string.
        RuntimeError: If encryption_key is not set in Anvil Secrets.
    """
    if not isinstance(plaintext, str) or not plaintext:
        raise ValueError("encrypt_value: plaintext must be a non-empty string")
    cipher = _get_cipher()
    return cipher.encrypt(plaintext.encode()).decode()


def decrypt_value(ciphertext: str) -> str:
    """Decrypt a Fernet ciphertext string back to plaintext.

    Args:
        ciphertext: The encrypted string produced by encrypt_value().

    Returns:
        str: The original plaintext string.

    Raises:
        ValueError: If ciphertext is empty or not a string.
        RuntimeError: If encryption_key is not set in Anvil Secrets.
        cryptography.fernet.InvalidToken: If the ciphertext is invalid or
            was encrypted with a different key.
    """
    if not isinstance(ciphertext, str) or not ciphertext:
        raise ValueError("decrypt_value: ciphertext must be a non-empty string")
    cipher = _get_cipher()
    return cipher.decrypt(ciphertext.encode()).decode()
