from ._anvil_designer import AdminLayoutTemplate
from anvil import *
import anvil.server
import anvil.users


# Navigation structure for the Consulting & Services vertical.
# Each entry is (nav_attr_name, label, icon, navigate_to_form).
# Dividers are plain strings.
_NAV_STRUCTURE = [
    ('nav_dashboard', 'Dashboard',    'fa:tachometer',  'DashboardForm'),
    'Sales & Operations',
    ('nav_bookings',  'Bookings',     'fa:calendar',    'BookingListForm'),
    ('nav_services',  'Services',     'fa:briefcase',   'ServiceManagementForm'),
    'Customers & Marketing',
    ('nav_contacts',   'Contacts',    'fa:users',         'ContactListForm'),
    ('nav_campaigns',  'Campaigns',   'fa:envelope',      'EmailCampaignListForm'),
    ('nav_broadcasts', 'Broadcasts',  'fa:bullhorn',      'EmailBroadcastForm'),
    ('nav_segments',   'Segments',    'fa:filter',        'SegmentManagerForm'),
    ('nav_tasks',      'Tasks',       'fa:check-square',  'TaskListForm'),
    'Content & Website',
    ('nav_blog',   'Blog',   'fa:pencil', 'BlogListForm'),
    ('nav_pages',  'Pages',  'fa:file',   'PageEditorForm'),
    'Finance & Reports',
    ('nav_invoices',  'Invoices',     'fa:file-text',   'InvoiceListForm'),
    ('nav_payments',  'Payments',     'fa:credit-card', 'PaymentListForm'),
    ('nav_reports',   'Reports',      'fa:bar-chart',   'ReportsForm'),
    ('nav_analytics', 'Analytics',    'fa:line-chart',  'AnalyticsForm'),
    ('nav_time',      'Time Entries', 'fa:clock-o',     'TimeTrackerForm'),
    ('nav_expenses',  'Expenses',     'fa:money',       'ExpenseListForm'),
    'Settings',
    ('nav_settings', 'Settings', 'fa:cog',  'SettingsForm'),
    ('nav_vault',    'Vault',    'fa:lock', 'VaultForm'),  # owner only
]


class AdminLayout(AdminLayoutTemplate):
    """Programmatic layout for the admin area.

    Layout type: Custom layout - all components built in code.
    Navigation destinations: see _NAV_STRUCTURE above.
    Key user flows: top-level navigation for all admin/staff roles.
    Feature flag dependencies: none (C&S single vertical).
    M3 component choices: NavigationLink-style Link components created
    programmatically and stored as self.nav_* attributes. Sidebar is a
    ColumnPanel (self.sidebar_panel) built in code. Content panel
    (self.content_panel) hosts the active content form.
    """

    def __init__(self, **properties):
        """Authenticate, build sidebar, then initialise components."""
        user = anvil.users.get_user()
        if not user:
            open_form('LoginForm')
            return

        role = user.get('role', '')
        if role not in ('owner', 'manager', 'admin', 'staff'):
            open_form('LoginForm')
            return

        self.init_components(**properties)
        self._user = user
        self._nav_links = {}  # attr_name -> Link instance
        self._build_sidebar()

    # -- Layout construction --------------------------------------------------

    def _build_sidebar(self) -> None:
        """Build the sidebar ColumnPanel with branding, nav links, and logout."""
        lbl_brand = Label(
            text='Mybizz',
            bold=True,
            font_size=18,
            foreground='theme:On Primary',
            spacing_above='small',
            spacing_below='small',
        )
        self.sidebar_panel.add_component(lbl_brand)

        self.build_navigation()

        self.sidebar_panel.add_component(Label(text='', spacing_above='large'))
        lbl_logout = Link(
            text='Sign out',
            foreground='theme:On Surface Variant',
            spacing_above='small',
            spacing_below='small',
        )
        lbl_logout.set_event_handler('click', self._logout_click)
        self.sidebar_panel.add_component(lbl_logout)

    def build_navigation(self) -> None:
        """Create all navigation Link components and add them to the sidebar.

        Links are stored as self.nav_* attributes so content forms can call
        set_active_link() to highlight the current destination.
        navigate_to is implemented via a click handler that calls open_form()
        with the target form name string. No external click handlers are added
        by content forms - navigation is self-contained in this layout.
        nav_vault is hidden unless the current user role is 'owner'.
        """
        role = self._user.get('role', '') if hasattr(self, '_user') else ''

        for entry in _NAV_STRUCTURE:
            if isinstance(entry, str):
                # Divider / group label
                lbl = Label(
                    text=entry,
                    bold=True,
                    font_size=11,
                    foreground='theme:On Surface Variant',
                    spacing_above='medium',
                    spacing_below='none',
                )
                self.sidebar_panel.add_component(lbl)
                continue

            attr_name, label, icon, form_name = entry

            nav_link = Link(
                text=label,
                icon=icon,
                foreground='theme:On Surface',
                spacing_above='none',
                spacing_below='none',
            )

            # Vault is owner-only
            if attr_name == 'nav_vault':
                nav_link.visible = (role == 'owner')

            # Capture loop variables explicitly to avoid closure issues
            nav_link.set_event_handler(
                'click',
                lambda e, fn=form_name, a=attr_name: self._nav_click(fn, a),
            )

            setattr(self, attr_name, nav_link)
            self._nav_links[attr_name] = nav_link
            self.sidebar_panel.add_component(nav_link)

    # -- Navigation helpers ---------------------------------------------------

    def _nav_click(self, form_name: str, attr_name: str) -> None:
        """Handle a navigation link click: highlight link and open target form."""
        self.set_active_link(attr_name)
        open_form(form_name)

    def set_active_link(self, attr_name: str) -> None:
        """Highlight the named link and clear all others.

        Args:
            attr_name: The nav_* attribute name to mark as active,
                       e.g. 'nav_dashboard'.
        """
        for name, link in self._nav_links.items():
            link.bold = (name == attr_name)
            link.foreground = (
                'theme:Primary' if name == attr_name
                else 'theme:On Surface'
            )

    # -- Logout ---------------------------------------------------------------

    def _logout_click(self, **event_args) -> None:
        """Sign the user out and return to the public home page."""
        anvil.users.logout()
        open_form('HomePage')
