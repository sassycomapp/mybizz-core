from ._anvil_designer import DashboardFormTemplate
from anvil import *
import anvil.server
import anvil.users
import logging

logger = logging.getLogger(__name__)


# Metric card definitions: (attr_suffix, label, stub_value, period_text)
_METRICS = [
    ('revenue',      'Revenue',      'R 0',  'This month'),
    ('bookings',     'Bookings',     '0',    'This month'),
    ('customers',    'Customers',    '0',    'Total'),
    ('time_entries', 'Time Entries', '0 hr', 'This month'),
]


class DashboardForm(DashboardFormTemplate):
    """Main admin dashboard — content form hosted inside AdminLayout.

    Layout type: Content form (no layout wrapper of its own).
    Key user flows: view revenue, bookings, customer, and time-entry metrics.
    Feature flag dependencies: none.
    M3 component choices: all components built programmatically.
    Metric cards use ColumnPanel containers with Label/Heading children.
    """

    def __init__(self, **properties):
        """Require auth, build metric cards, load stub data."""
        from ...shared.navigation_helpers import require_auth
        if not require_auth():
            return

        self.init_components(**properties)
        self._metric_value_labels = {}
        self._build_ui()
        self._load_metrics()

    # -- UI construction ------------------------------------------------------

    def _build_ui(self) -> None:
        """Build page title and the four metric cards."""
        # Page title
        lbl_title = Label(
            text='Dashboard',
            bold=True,
            font_size=24,
            foreground='theme:On Surface',
            spacing_above='small',
            spacing_below='medium',
        )
        self.content_panel.add_component(lbl_title)

        # Horizontal panel for metric cards
        lp_metrics = LinearPanel(direction='left-to-right', spacing='small')
        self.content_panel.add_component(lp_metrics)

        for suffix, label, stub, period in _METRICS:
            card_col = ColumnPanel(
                background='theme:Surface Variant',
                spacing_above='small',
                spacing_below='small',
            )

            lbl_card_label = Label(
                text=label,
                bold=True,
                font_size=12,
                foreground='theme:On Surface Variant',
                spacing_above='small',
                spacing_below='none',
            )
            lbl_value = Label(
                text=stub,
                bold=True,
                font_size=28,
                foreground='theme:Primary',
                spacing_above='none',
                spacing_below='none',
            )
            lbl_period = Label(
                text=period,
                font_size=11,
                foreground='theme:On Surface Variant',
                spacing_above='none',
                spacing_below='small',
            )

            card_col.add_component(lbl_card_label)
            card_col.add_component(lbl_value)
            card_col.add_component(lbl_period)
            lp_metrics.add_component(card_col)

            # Store value label so _load_metrics() can update it
            self._metric_value_labels[suffix] = lbl_value

    # -- Data loading ---------------------------------------------------------

    def _load_metrics(self) -> None:
        """Call server for dashboard metrics and update card values."""
        try:
            result = anvil.server.call('get_dashboard_metrics')
        except anvil.server.TimeoutError:
            logger.warning("DashboardForm: get_dashboard_metrics timed out")
            return
        except Exception:
            logger.error(
                "DashboardForm: get_dashboard_metrics failed", exc_info=True
            )
            return

        if not result.get('success'):
            logger.warning(
                "DashboardForm: metrics returned failure: %s",
                result.get('error'),
            )
            return

        data = result.get('data', {})
        currency = data.get('currency', 'R')

        lbl = self._metric_value_labels.get('revenue')
        if lbl:
            lbl.text = f"{currency} {data.get('revenue', 0):,.2f}"

        lbl = self._metric_value_labels.get('bookings')
        if lbl:
            lbl.text = str(data.get('bookings', 0))

        lbl = self._metric_value_labels.get('customers')
        if lbl:
            lbl.text = str(data.get('customers', 0))

        lbl = self._metric_value_labels.get('time_entries')
        if lbl:
            lbl.text = f"{data.get('time_entries', 0)} hr"
