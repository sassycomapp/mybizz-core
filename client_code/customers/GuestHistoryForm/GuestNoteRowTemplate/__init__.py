from ._anvil_designer import GuestNoteRowTemplateTemplate
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


class GuestNoteRowTemplate(GuestNoteRowTemplateTemplate):
  def __init__(self, **properties):
    self.item = properties.get('item')
    self.init_components(**properties)

    self.lbl_note.text = self.item['note']