from ._anvil_designer import HomePageTemplate
from anvil import *
import anvil.server
import anvil.users

from ...shared.navigation_helpers import navigate_to_dashboard


class HomePage(HomePageTemplate):
    """Public home page — entry point for the Mybizz app.

    Layout type: Custom Form (no layout wrapper).
    Key user flows:
        - Authenticated user -> routed to correct dashboard by role.
        - Unauthenticated visitor -> public home page displayed.
    Feature flag dependencies: none.
    """

    def __init__(self, **properties):
        """Route authenticated users immediately; render page for visitors."""
        user = anvil.users.get_user()
        if user:
            navigate_to_dashboard()
            return

        # Not logged in -- render the public home page
        self.init_components(**properties)
