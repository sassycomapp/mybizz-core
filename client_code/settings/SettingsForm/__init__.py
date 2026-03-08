from ._anvil_designer import SettingsFormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files

import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class SettingsForm(SettingsFormTemplate):
  """Main settings form with tabbed interface"""

  def __init__(self, **properties):
