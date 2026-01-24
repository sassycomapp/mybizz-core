from ._anvil_designer import HomePageTemplate
from anvil import *
import anvil.server
import anvil.users

# Import your startup logic module (optional, structured apps only)
from .. import startup


class HomePage(HomePageTemplate):
  def __init__(self, **properties):
    # Initialize UI components
    self.init_components(**properties)

    # Initialize application logic ONCE
    # (routing, auth decisions, layout selection)
    startup.initialize_app_once()