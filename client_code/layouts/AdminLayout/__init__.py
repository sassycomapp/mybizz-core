from ._anvil_designer import AdminLayoutTemplate
from anvil import *
import anvil.server
from routing import router
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files

import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class AdminLayout(AdminLayoutTemplate):
  def __init__(self, **properties):
    # Authentication check
    user = anvil.users.get_user()
    if not user:
      alert("Please log in to access this area.")
      open_form('public.LoginPage')
      return

    # Role check (admin, manager, or owner)
    if not self.is_admin_user(user):
      alert("Access denied. Admin privileges required.")
      open_form('public.HomePage')
      return

    # Set up Form properties and Data Bindings.
    self.init_components(**properties)

    # Initialize UI
    self.setup_header()
    self.setup_sidebar()
    self.load_user_data(user)

  def is_admin_user(self, user):
    """Check if user has admin role"""
    if not user:
      return False
    role = user.get('role', 'guest')
    return role in ['admin', 'manager', 'owner']

  def is_owner_or_manager(self, user):
    """Check if user has elevated privileges"""
    if not user:
      return False
    role = user.get('role', 'guest')
    return role in ['owner', 'manager']

  def setup_header(self):
    """Configure header appearance"""
    self.lbl_logo.text = "MyBusiness"  # Or load from business settings
    self.lbl_logo.foreground = "#FFFFFF"
    self.lbl_logo.font_size = 20
    self.lbl_logo.bold = True

    self.lbl_notifications.text = "🔔"
    self.lbl_notifications.font_size = 18
    self.lbl_notifications.foreground = "#FFFFFF"

  def setup_sidebar(self):
    """Configure sidebar appearance and role-based visibility"""
    user = anvil.users.get_user()

    # Sidebar styling
    self.sidebar_panel.background = "#2C3E50"
    self.sidebar_panel.foreground = "#ECF0F1"

    # Set all group headers clickable
    self.lbl_sales_header.text = "▼ Sales"
    self.lbl_marketing_header.text = "▼ Marketing"
    self.lbl_content_header.text = "▼ Content"
    self.lbl_finance_header.text = "▼ Finance"
    self.lbl_settings_header.text = "▼ Settings"

    # Role-based visibility
    show_restricted = self.is_owner_or_manager(user)
    self.lbl_finance_header.visible = show_restricted
    self.panel_finance_items.visible = show_restricted
    self.lbl_settings_header.visible = show_restricted
    self.panel_settings_items.visible = show_restricted

    # Initially expand all visible groups
    self.panel_sales_items.visible = True
    self.panel_marketing_items.visible = True
    self.panel_content_items.visible = True
    if show_restricted:
      self.panel_finance_items.visible = True
      self.panel_settings_items.visible = True

  def load_user_data(self, user):
    """Load and display user information"""
    user_name = user.get('name', user.get('email', 'User'))
    self.link_user_menu.text = f"{user_name} ▼"
    self.link_user_menu.foreground = "#FFFFFF"

  def update_breadcrumbs(self, *crumbs):
    """Update breadcrumb navigation
    Args:
      *crumbs: Tuples of (text, click_handler) or (text, None) for current page
    """
    self.breadcrumbs_panel.clear()

    for i, crumb in enumerate(crumbs):
      text, handler = crumb

      if handler:
        # Clickable breadcrumb
        link = Link(text=text, foreground="#3498DB")
        link.set_event_handler('click', handler)
        self.breadcrumbs_panel.add_component(link)
      else:
        # Current page (not clickable)
        label = Label(text=text, foreground="#7F8C8D")
        self.breadcrumbs_panel.add_component(label)

      # Add separator if not last item
      if i < len(crumbs) - 1:
        separator = Label(text=" / ", foreground="#BDC3C7")
        self.breadcrumbs_panel.add_component(separator)

  def highlight_link(self, target_link):
    """Highlight active navigation link"""
    # List all navigation links
    all_links = [
      self.link_dashboard,
      self.link_bookings, self.link_products, self.link_orders,
      self.link_rooms, self.link_services, self.link_memberships,
      self.link_contacts, self.link_campaigns, self.link_broadcasts,
      self.link_segments, self.link_tasks, self.link_lead_capture,
      self.link_referrals, self.link_reviews,
      self.link_blog, self.link_pages, self.link_media,
      self.link_payments, self.link_invoices, self.link_transactions, self.link_reports,
      self.link_business, self.link_branding, self.link_features,
      self.link_users, self.link_integrations,
      self.link_support
    ]

    # Reset all links
    for link in all_links:
      link.bold = False
      link.foreground = "#ECF0F1"

    # Highlight target
    if target_link:
      target_link.bold = True
      target_link.foreground = "#3498DB"

  def toggle_group(self, header_label, panel, arrow_down="▼", arrow_right="►"):
    """Toggle collapsible group"""
    panel.visible = not panel.visible

    # Update arrow
    current_text = header_label.text
    if panel.visible:
      header_label.text = current_text.replace(arrow_right, arrow_down)
    else:
      header_label.text = current_text.replace(arrow_down, arrow_right)

  # === HEADER EVENTS ===

  def lbl_logo_click(self, **event_args):
    """Go to dashboard"""
    open_form('admin.Dashboard')

  def lbl_notifications_click(self, **event_args):
    """Show notifications"""
    alert("Notifications feature coming soon!")

  def link_user_menu_click(self, **event_args):
    """Show user menu"""
    alert("User menu feature coming soon!")

  # === GROUP HEADER EVENTS ===

  def lbl_sales_header_click(self, **event_args):
    """Toggle sales group"""
    self.toggle_group(self.lbl_sales_header, self.panel_sales_items)

  def lbl_marketing_header_click(self, **event_args):
    """Toggle marketing group"""
    self.toggle_group(self.lbl_marketing_header, self.panel_marketing_items)

  def lbl_content_header_click(self, **event_args):
    """Toggle content group"""
    self.toggle_group(self.lbl_content_header, self.panel_content_items)

  def lbl_finance_header_click(self, **event_args):
    """Toggle finance group"""
    self.toggle_group(self.lbl_finance_header, self.panel_finance_items)

  def lbl_settings_header_click(self, **event_args):
    """Toggle settings group"""
    self.toggle_group(self.lbl_settings_header, self.panel_settings_items)

  # === NAVIGATION LINK EVENTS ===

  @handle("link_dashboard", "click")
  def link_dashboard_click(self, **event_args):
    """Navigate to dashboard"""
    open_form('admin.Dashboard')

  # SALES GROUP
  @handle("link_bookings", "click")
  def link_bookings_click(self, **event_args):
    """Navigate to bookings"""
    open_form('admin.BookingsList')

  @handle("link_products", "click")
  def link_products_click(self, **event_args):
    """Navigate to products"""
    open_form('admin.ProductsList')

  @handle("link_orders", "click")
  def link_orders_click(self, **event_args):
    """Navigate to orders"""
    open_form('admin.OrdersList')

  @handle("link_rooms", "click")
  def link_rooms_click(self, **event_args):
    """Navigate to rooms"""
    open_form('admin.RoomsList')

  @handle("link_services", "click")
  def link_services_click(self, **event_args):
    """Navigate to services"""
    open_form('admin.ServicesList')

  @handle("link_memberships", "click")
  def link_memberships_click(self, **event_args):
    """Navigate to memberships"""
    open_form('admin.MembershipsList')

  # MARKETING GROUP
  @handle("link_contacts", "click")
  def link_contacts_click(self, **event_args):
    """Navigate to contacts"""
    open_form('admin.ContactsList')

  @handle("link_campaigns", "click")
  def link_campaigns_click(self, **event_args):
    """Navigate to campaigns"""
    open_form('admin.CampaignsList')

  @handle("link_broadcasts", "click")
  def link_broadcasts_click(self, **event_args):
    """Navigate to broadcasts"""
    open_form('admin.BroadcastsList')

  @handle("link_segments", "click")
  def link_segments_click(self, **event_args):
    """Navigate to segments"""
    open_form('admin.SegmentsList')

  @handle("link_tasks", "click")
  def link_tasks_click(self, **event_args):
    """Navigate to tasks"""
    open_form('admin.TasksList')

  @handle("link_lead_capture", "click")
  def link_lead_capture_click(self, **event_args):
    """Navigate to lead capture"""
    open_form('admin.LeadCaptureList')

  @handle("link_referrals", "click")
  def link_referrals_click(self, **event_args):
    """Navigate to referrals"""
    open_form('admin.ReferralsList')

  @handle("link_reviews", "click")
  def link_reviews_click(self, **event_args):
    """Navigate to reviews"""
    open_form('admin.ReviewsList')

  # CONTENT GROUP
  @handle("link_blog", "click")
  def link_blog_click(self, **event_args):
    """Navigate to blog"""
    open_form('admin.BlogPostsList')

  @handle("link_pages", "click")
  def link_pages_click(self, **event_args):
    """Navigate to pages"""
    open_form('admin.PagesList')

  @handle("link_media", "click")
  def link_media_click(self, **event_args):
    """Navigate to media"""
    open_form('admin.MediaLibrary')

  # FINANCE GROUP
  @handle("link_payments", "click")
  def link_payments_click(self, **event_args):
    """Navigate to payments"""
    open_form('admin.PaymentsList')

  @handle("link_invoices", "click")
  def link_invoices_click(self, **event_args):
    """Navigate to invoices"""
    open_form('admin.InvoicesList')

  @handle("link_transactions", "click")
  def link_transactions_click(self, **event_args):
    """Navigate to transactions"""
    open_form('admin.TransactionsList')
  
  @handle("link_reports", "click")
  def link_reports_click(self, **event_args):
    """Navigate to financial reports"""
    open_form('admin.FinancialReports')
  
  # SETTINGS GROUP
  @handle("link_business", "click")
  def link_business_click(self, **event_args):
    """Navigate to business settings"""
    open_form('admin.BusinessSettings')
  
  @handle("link_branding", "click")
  def link_branding_click(self, **event_args):
    """Navigate to branding settings"""
    open_form('admin.BrandingSettings')
  
  @handle("link_features", "click")
  def link_features_click(self, **event_args):
    """Navigate to feature toggles"""
    open_form('admin.FeatureToggles')
  
  @handle("link_users", "click")
  def link_users_click(self, **event_args):
    """Navigate to user management"""
    open_form('admin.UserManagement')
  
  @handle("link_integrations", "click")
  def link_integrations_click(self, **event_args):
    """Navigate to integrations"""
    open_form('admin.IntegrationsList')
  
  # BOTTOM LINKS
  @handle("link_support", "click")
  def link_support_click(self, **event_args):
    """Navigate to support"""
    open_form('admin.Support')
  
  @handle("link_logout", "click")
  def link_logout_click(self, **event_args):
    """Logout and redirect"""
    anvil.users.logout()
    alert("You have been logged out.", title="Logged Out")
    open_form('public.HomePage')

  @handle("link_home", "click")
  def link_home_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  @handle("link_about", "click")
  def link_about_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  @handle("link_contact", "click")
  def link_contact_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass
