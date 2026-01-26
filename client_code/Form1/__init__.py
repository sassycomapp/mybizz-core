from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import m3.components as m3
from routing import router
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import stripe.checkout
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import Slot  # Add this import

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Create the slot using your existing slot_1 component
    self.slot_1 = Slot(self.slot_1, 0, {})  # Target=itself, insert at index 0

    # Define the slots dictionary so the designer recognizes it
    self.slots = {"slot_1": self.slot_1}

    # Any code you write here will run before the form opens.

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    pass
