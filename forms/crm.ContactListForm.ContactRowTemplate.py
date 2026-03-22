from ._anvil_designer import ContactRowTemplateTemplate
from anvil import *
import anvil.server
import m3.components as m3
from routing import router
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files

import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ContactRowTemplate(ContactRowTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
