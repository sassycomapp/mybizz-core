"""Server module: server_dashboard/service.py

Dashboard data functions for Stage 1.3.
All functions return the standard Mybizz response envelope:
    {'success': True,  'data': ...}
    {'success': False, 'error': str}

Stub implementations are provided for Stage 1.3. Real queries will be
wired in Stage 1.7 (Analytics & Reporting) once bookings, invoices, and
time_entries tables are fully populated.
"""

import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import logging
from datetime import datetime, date

logger = logging.getLogger(__name__)


@anvil.server.callable
def get_dashboard_metrics() -> dict:
    """Return key metrics for the admin dashboard.

    Attempts to read live counts from available tables. Falls back to
    zero stubs for tables that do not yet exist (safe during phased build).

    Returns:
        dict: {
            'success': True,
            'data': {
                'revenue':      float  -- total invoiced this calendar month,
                'bookings':     int    -- confirmed bookings this calendar month,
                'customers':    int    -- total active contacts,
                'time_entries': float  -- total billable hours this calendar month,
                'currency':     str    -- system currency symbol (default 'R'),
            }
        }
    """
    logger.info("get_dashboard_metrics called")
    try:
        user = anvil.users.get_user()
        if not user:
            return {'success': False, 'error': 'Not authenticated'}

        revenue = _safe_revenue(user)
        bookings = _safe_bookings(user)
        customers = _safe_customers(user)
        time_entries = _safe_time_entries(user)
        currency = _safe_currency(user)

        return {
            'success': True,
            'data': {
                'revenue':      revenue,
                'bookings':     bookings,
                'customers':    customers,
                'time_entries': time_entries,
                'currency':     currency,
            },
        }
    except Exception:
        logger.error("get_dashboard_metrics: unexpected error", exc_info=True)
        return {'success': False, 'error': 'Could not load dashboard metrics.'}


@anvil.server.callable
def get_recent_activity() -> dict:
    """Return recent activity events for the dashboard activity feed.

    Returns an empty list at Stage 1.3. Will be populated in Phase 5
    once contact_events table is in place.

    Returns:
        dict: {'success': True, 'data': []}
    """
    logger.info("get_recent_activity called")
    try:
        user = anvil.users.get_user()
        if not user:
            return {'success': False, 'error': 'Not authenticated'}
        return {'success': True, 'data': []}
    except Exception:
        logger.error("get_recent_activity: unexpected error", exc_info=True)
        return {'success': False, 'error': 'Could not load recent activity.'}


@anvil.server.callable
def get_storage_usage() -> dict:
    """Return storage usage information for the dashboard storage widget.

    Returns stub values at Stage 1.3. Will be wired to Anvil storage
    APIs in a later stage.

    Returns:
        dict: {
            'success': True,
            'data': {
                'used_mb':  float,
                'limit_mb': float,
                'percent':  float,
            }
        }
    """
    logger.info("get_storage_usage called")
    try:
        user = anvil.users.get_user()
        if not user:
            return {'success': False, 'error': 'Not authenticated'}
        return {
            'success': True,
            'data': {
                'used_mb':  0.0,
                'limit_mb': 1000.0,
                'percent':  0.0,
            },
        }
    except Exception:
        logger.error("get_storage_usage: unexpected error", exc_info=True)
        return {'success': False, 'error': 'Could not load storage usage.'}


# -- Internal helpers (not callable) -----------------------------------------

def _safe_revenue(user) -> float:
    """Sum total_amount from invoice rows for the current calendar month.
    Returns 0.0 if the invoice table does not exist or has no rows."""
    try:
        invoice_table = getattr(app_tables, 'invoice', None)
        if invoice_table is None:
            return 0.0
        today = date.today()
        month_start = datetime(today.year, today.month, 1)
        total = 0.0
        for row in invoice_table.search(
            instance_id=user,
            status='paid',
            paid_at=q.greater_than_or_equal_to(month_start),
        ):
            total += row.get('total_amount') or 0.0
        return round(total, 2)
    except Exception:
        logger.warning("_safe_revenue: query failed", exc_info=True)
        return 0.0


def _safe_bookings(user) -> int:
    """Count confirmed bookings for the current calendar month.
    Returns 0 if the bookings table does not exist."""
    try:
        bookings_table = getattr(app_tables, 'bookings', None)
        if bookings_table is None:
            return 0
        today = date.today()
        month_start = datetime(today.year, today.month, 1)
        return len(list(bookings_table.search(
            instance_id=user,
            status='confirmed',
            start_datetime=q.greater_than_or_equal_to(month_start),
        )))
    except Exception:
        logger.warning("_safe_bookings: query failed", exc_info=True)
        return 0


def _safe_customers(user) -> int:
    """Count total active contacts.
    Returns 0 if the contacts table does not exist."""
    try:
        contacts_table = getattr(app_tables, 'contacts', None)
        if contacts_table is None:
            return 0
        return len(list(contacts_table.search(
            instance_id=user,
            status=q.any_of('Lead', 'Customer'),
        )))
    except Exception:
        logger.warning("_safe_customers: query failed", exc_info=True)
        return 0


def _safe_time_entries(user) -> float:
    """Sum billable hours from time_entries for the current calendar month.
    Returns 0.0 if the time_entries table does not exist."""
    try:
        te_table = getattr(app_tables, 'time_entries', None)
        if te_table is None:
            return 0.0
        today = date.today()
        month_start = datetime(today.year, today.month, 1)
        total = 0.0
        for row in te_table.search(
            instance_id=user,
            is_billable=True,
            start_time=q.greater_than_or_equal_to(month_start),
        ):
            total += row.get('duration_hours') or 0.0
        return round(total, 1)
    except Exception:
        logger.warning("_safe_time_entries: query failed", exc_info=True)
        return 0.0


def _safe_currency(user) -> str:
    """Read system currency symbol from the config table.
    Returns 'R' (ZAR) as the default if config is not yet set."""
    try:
        config_table = getattr(app_tables, 'config', None)
        if config_table is None:
            return 'R'
        row = config_table.get(instance_id=user, key='system_currency')
        if row:
            value = row.get('value') or {}
            return value.get('symbol', 'R')
        return 'R'
    except Exception:
        logger.warning("_safe_currency: query failed", exc_info=True)
        return 'R'
