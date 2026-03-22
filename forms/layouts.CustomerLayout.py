from ._anvil_designer import CustomerLayoutTemplate
from anvil import *
import anvil.server
import anvil.users


# Navigation structure for the customer portal.
_CUSTOMER_NAV = [
    ('nav_my_dashboard', 'My Dashboard', 'fa:home',        'ClientPortalForm'),
    ('nav_my_bookings',  'My Bookings',  'fa:calendar',    'BookingListForm'),
    ('nav_my_invoices',  'My Invoices',  'fa:file-text',   'InvoiceListForm'),
    ('nav_my_reviews',   'My Reviews',   'fa:star',        'ReviewSubmissionForm'),
    ('nav_support',      'Support',      'fa:life-ring',   'TicketSubmissionForm'),
    ('nav_account',      'Account',      'fa:user-circle', 'LoginForm'),
]


class CustomerLayout(CustomerLayoutTemplate):
    """Programmatic layout for the customer portal.

    Layout type: Custom layout - all components built in code.
    Navigation destinations: see _CUSTOMER_NAV above.
    Key user flows: customer self-service - bookings, invoices, reviews, support.
    Feature flag dependencies: none (C&S single vertical).
    M3 component choices: Link components created programmatically and stored
    as self.nav_* attributes. Sidebar is self.sidebar_panel (ColumnPanel).
    Content panel is self.content_panel.
    """

    def __init__(self, **properties):
        """Authenticate as customer, build sidebar, initialise components."""
        user = anvil.users.get_user()
        if not user:
            open_form('LoginForm')
            return

        self.init_components(**properties)
        self._user = user
        self._nav_links = {}
        self._build_sidebar()

    # -- Layout construction --------------------------------------------------

    def _build_sidebar(self) -> None:
        """Build the sidebar with branding, nav links, and logout."""
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
        """Create all customer navigation Link components."""
        for attr_name, label, icon, form_name in _CUSTOMER_NAV:
            nav_link = Link(
                text=label,
                icon=icon,
                foreground='theme:On Surface',
                spacing_above='none',
                spacing_below='none',
            )
            nav_link.set_event_handler(
                'click',
                lambda e, fn=form_name, a=attr_name: self._nav_click(fn, a),
            )
            setattr(self, attr_name, nav_link)
            self._nav_links[attr_name] = nav_link
            self.sidebar_panel.add_component(nav_link)

    # -- Navigation helpers ---------------------------------------------------

    def _nav_click(self, form_name: str, attr_name: str) -> None:
        """Highlight link and open target form."""
        self.set_active_link(attr_name)
        open_form(form_name)

    def set_active_link(self, attr_name: str) -> None:
        """Highlight the named link and clear all others.

        Args:
            attr_name: The nav_* attribute name to mark as active.
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
