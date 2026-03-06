"""Server module for settings and configuration services."""

import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files

import anvil.secrets
import anvil.files
from anvil.files import data_files
import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import logging
from datetime import datetime, timedelta

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


