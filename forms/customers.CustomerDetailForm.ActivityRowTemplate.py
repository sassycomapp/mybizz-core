from ._anvil_designer import ActivityRowTemplateTemplate
from anvil import *
import m3.components as m3
from routing import router
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files

import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ActivityRowTemplate(ActivityRowTemplateTemplate):
  def __init__(self, **properties):
    self.item = properties.get('item')
    self.init_components(**properties)

    # Generic display for different activity types
    self.lbl_number.text = self.item.get('number', 'N/A')
    self.lbl_number.bold = True

    if self.item.get('date'):
      self.lbl_date.text = f"•  {self.item['date'].strftime('%b %d, %Y')}"
    else:
      self.lbl_date.text = ""

    if self.item.get('amount'):
      self.lbl_amount.text = f"•  ${self.item['amount']:.2f}"
    else:
      self.lbl_amount.text = ""

    self.lbl_status.text = f"•  {self.item.get('status', 'Unknown').capitalize()}"