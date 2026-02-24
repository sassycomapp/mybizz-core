---
description: "04_architecture_specification.md - Mybizz Architecture Specification"
globs: ["**/*"]
alwaysApply: true
---

# Mybizz Platform V1.x - Architecture Specification

**Document Version:** 11.0  
**Date:** January 26, 2026  
**Status:** Active Specification  
**Compliance:** 100% Anvil.works native architecture + Material Design 3  
**UI Theme:** Material Design 3 (Dependency ID: 4UK6WHQ6UX7AKELK)  
**Target Scale:** 100 clients maximum (V1.x)  
**Architecture Model:** Single master_template with Anvil packages (Open Verticals)

---

## 1. System Overview

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Mybizz V1.x Platform                           │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │              Mybizz Founder Account (Platform Owner)             │  │
│  │                                                                  │  │
│  │  ┌────────────────────────────────────────────────────────────┐ │  │
│  │  │  master_template_dev (Primary Development Workspace)       │ │  │
│  │  │                                                            │ │  │
│  │  │  ├─ client_code/          (Client-side packages)          │ │  │
│  │  │  │  ├─ auth/              Login, signup forms             │ │  │
│  │  │  │  ├─ dashboard/         Main dashboard                  │ │  │
│  │  │  │  ├─ bookings/          Booking calendar, forms         │ │  │
│  │  │  │  ├─ products/          Product catalog, shop           │ │  │
│  │  │  │  ├─ customers/         CRM functionality               │ │  │
│  │  │  │  ├─ marketing/         Email campaigns, lead capture   │ │  │
│  │  │  │  ├─ blog/              Blog posts, content             │ │  │
│  │  │  │  ├─ settings/          All configuration               │ │  │
│  │  │  │  └─ shared/            Reusable components             │ │  │
│  │  │  │                                                        │ │  │
│  │  │  └─ server_code/          (Server-side packages)          │ │  │
│  │  │     ├─ server_auth/              Authentication service          │ │  │
│  │  │     ├─ server_bookings/          Booking business logic          │ │  │
│  │  │     ├─ server_products/          Product/inventory service       │ │  │
│  │  │     ├─ server_customers/         Customer service                │ │  │
│  │  │     ├─ server_marketing/         Email campaigns, Brevo API      │ │  │
│  │  │     ├─ server_payments/          Stripe, Paystack integrations   │ │  │
│  │  │     ├─ server_emails/            Zoho email service              │ │  │
│  │  │     ├─ server_analytics/         Basic reporting                 │ │  │
│  │  │     └─ server_shared/            Utilities, validators           │ │  │
│  │  │                                                            │ │  │
│  │  │  ALL FEATURES IN ONE APP (Open Verticals Architecture)    │ │  │
│  │  └────────────────────────────────────────────────────────────┘ │  │
│  │                             ↓                                    │  │
│  │                    Tested & Published as                         │  │
│  │                             ↓                                    │  │
│  │  ┌────────────────────────────────────────────────────────────┐ │  │
│  │  │  master_template (V1.0, V1.1, V1.2... published versions) │ │  │
│  │  │  - Published dependency (frozen snapshot)                 │ │  │
│  │  │  - Versioned releases                                     │ │  │
│  │  │  - Pull-based updates (clients choose when)               │ │  │
│  │  └────────────────────────────────────────────────────────────┘ │  │
│  │                                                                  │  │
│  │  ┌────────────────────────────────────────────────────────────┐ │  │
│  │  │  Mybizz_management (Separate - Mybizz Internal Tools)     │ │  │
│  │  │  - Clone of master_template + management features         │ │  │
│  │  │  - Client provisioning                                    │ │  │
│  │  │  - Multi-client monitoring                                │ │  │
│  │  │  - Billing automation                                     │ │  │
│  │  │  - Update distribution                                    │ │  │
│  │  │  NOT included in master_template (security isolation)     │ │  │
│  │  └────────────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│                 ↓ Consumed by 100 Client Instances ↓                   │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  Client Instance 1: client_yogastudio (Subscriber A's Account)  │  │
│  │                                                                  │  │
│  │  ├─ Depends on: master_template (e.g., V1.2)                   │  │
│  │  ├─ Anvil Data Tables (Client's business data)                 │  │
│  │  │  ├─ tbl_config          (feature toggles, branding)         │  │
│  │  │  ├─ tbl_business_profile                                    │  │
│  │  │  ├─ tbl_users            (staff, customers)                 │  │
│  │  │  ├─ tbl_bookings         (appointments, reservations)       │  │
│  │  │  ├─ tbl_products         (if e-commerce enabled)            │  │
│  │  │  ├─ tbl_orders           (if e-commerce enabled)            │  │
│  │  │  ├─ tbl_customers        (CRM data)                         │  │
│  │  │  ├─ tbl_invoices         (billing records)                  │  │
│  │  │  └─ ... (all feature data)                                  │  │
│  │  │                                                              │  │
│  │  └─ Client owns & controls: Data, theme, features enabled      │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  [... up to 100 client instances for V1.x]                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Architectural Principles

**1. Single App Architecture**
- ONE master_template contains all features
- Organized using Anvil packages (client_code/, server_code/)
- NO separate modular apps
- Simpler to develop, test, and maintain

**2. Open Verticals Philosophy**
- All 4 verticals available to ALL clients
- Clients activate features via toggles
- Examples:
  - Yoga studio (Hospitality) + sells products (E-commerce) + memberships
  - Consultant (Services) + sells courses (E-commerce) + blog
- Maximum flexibility, no vertical lock

**3. Dependency-Based Code Sharing**
- All functionality resides in master_template
- Client instances import (not duplicate) code
- Updates available via Anvil's dependency system
- Pull-based updates (clients control timing)

**4. Complete Data Isolation**
- Each client operates in separate Anvil account
- Zero shared database or resources
- No cross-tenant data access possible
- Client owns 100% of their data

**5. Configuration-Driven Behavior**
- Feature toggles (not vertical selection)
- Branding via theme config
- All business logic adapts to enabled features

**6. Stateless Master Template**
- Master template contains zero client data
- All state lives in client instance Data Tables
- Master template queries client data via `app_tables` (in client's environment)

**7. Security-First Design**
- RBAC enforced on all server functions
- Sensitive data encrypted at rest
- GDPR/POPIA compliance built-in
- Anvil-native security patterns

---

## 2. Component Architecture

### 2.1 Master Template Package Structure

**App:** master_template_dev → master_template (published)  
**Organization:** Anvil packages (feature-based)

```
master_template/
│
├─ client_code/                    # CLIENT PACKAGES
│  │
│  ├─ auth/                        # Authentication
│  │  ├─ LoginForm
│  │  ├─ SignupForm
│  │  └─ PasswordResetForm
│  │
│  ├─ dashboard/                   # Main Dashboard
│  │  ├─ DashboardForm
│  │  ├─ MetricsPanel
│  │  └─ ActivityFeed
│  │
│  ├─ bookings/                    # Booking Management
│  │  ├─ BookingCalendarForm
│  │  ├─ BookingListForm
│  │  ├─ BookingDetailForm
│  │  └─ AvailabilitySettings
│  │
│  ├─ products/                    # E-commerce
│  │  ├─ ProductListForm
│  │  ├─ ProductEditorForm
│  │  ├─ ShoppingCartForm
│  │  └─ CheckoutForm
│  │
│  ├─ customers/                   # CRM
│  │  ├─ ContactListForm
│  │  ├─ ContactDetailForm
│  │  ├─ ContactEditorForm
│  │  └─ SegmentManagerForm
│  │
│  ├─ marketing/                   # Marketing Tools
│  │  ├─ MarketingDashboardForm
│  │  ├─ EmailCampaignListForm
│  │  ├─ EmailCampaignEditorForm
│  │  ├─ EmailBroadcastForm
│  │  ├─ LeadCaptureEditorForm
│  │  ├─ ReviewRequestForm
│  │  ├─ ReferralProgramForm
│  │  └─ TaskListForm
│  │
│  ├─ blog/                        # Blog System
│  │  ├─ BlogListForm
│  │  ├─ BlogPostForm
│  │  └─ BlogEditorForm
│  │
│  ├─ settings/                    # Configuration
│  │  ├─ SettingsForm
│  │  ├─ BusinessProfileSettings
│  │  ├─ FeatureActivationSettings
│  │  ├─ ThemeCustomizationSettings
│  │  └─ UserPermissionsSettings
│  │
│  └─ shared/                      # Reusable Components
│     ├─ Layouts/
│     │  ├─ AdminLayout           # Admin sidebar layout
│     │  ├─ CustomerLayout        # Customer portal layout
│     │  ├─ BlankLayout           # Login, signup (no nav)
│     │  └─ ErrorLayout           # Error pages
│     │
│     └─ components/
│        ├─ MetricCard
│        ├─ ActivityTimeline
│        └─ ConfirmationDialog
│
└─ server_code/                    # SERVER PACKAGES
   │
   ├─ server_auth/                 # Authentication Service
   │  ├─ service.py
   │  └─ rbac.py
   │
   ├─ server_bookings/             # Booking Service
   │  ├─ booking_service.py
   │  ├─ calendar_service.py
   │  └─ availability_service.py
   │
   ├─ server_products/             # Product Service
   │  ├─ product_service.py
   │  ├─ order_service.py
   │  └─ inventory_service.py
   │
   ├─ server_customers/            # Customer Service
   │  ├─ contact_service.py
   │  ├─ segment_service.py
   │  └─ timeline_service.py
   │
   ├─ server_marketing/            # Marketing Service
   │  ├─ campaign_service.py
   │  ├─ broadcast_service.py
   │  ├─ task_service.py
   │  ├─ lead_capture_service.py
   │  ├─ referral_service.py
   │  ├─ review_service.py
   │  └─ brevo_integration.py
   │
   ├─ server_payments/             # Payment Integrations
   │  ├─ stripe_service.py
   │  ├─ paystack_service.py
   │  └─ invoice_service.py
   │
   ├─ server_emails/               # Email Service
   │  └─ zoho_integration.py
   │
   ├─ server_analytics/            # Analytics Service
   │  └─ reporting_service.py
   │
   └─ server_shared/               # Shared Utilities
      ├─ utilities.py
      ├─ validators.py
      ├─ encryption.py
      └─ config.py
```

### 2.2 Navigation Architecture

**Mybizz uses Material Design 3 NavigationDrawerLayout + NavigationLink for navigation.**

#### M3 Navigation Pattern

**Core Components:**
1. **NavigationDrawerLayout** - M3 pre-built layout with navigation drawer, top app bar, and content panel
2. **NavigationLink** - M3 component for navigation items with `navigate_to` property (internal SPA navigation)
3. **Routing Dependency (Optional)** - For public pages requiring URLs (Dependency: `3PIDO5P3H4VPEMPL`)

**Two Navigation Systems:**
- **M3 NavigationLink:** Internal admin/customer navigation (NO URLs, SPA only)
- **Routing Dependency:** Public pages with shareable URLs (blog, products, landing pages)

**Reference:** `Docs/Anvil_Methods/anvil_cop_m3_navigation_routing.md` for complete implementation patterns

#### Layout Forms

**4 Layout Forms provide consistent structure:**

1. **AdminLayout** - NavigationDrawerLayout template with 20+ navigation destinations
2. **CustomerLayout** - NavigationDrawerLayout template with 9 navigation destinations  
3. **BlankLayout** - No layout (Login, Signup, Password Reset)
4. **ErrorLayout** - Minimal layout (error pages with back-to-home link)

#### AdminLayout Navigation

**M3 Implementation:**

```python
from m3.components import NavigationLink

class AdminLayout(NavigationDrawerLayoutTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.build_navigation()
  
  def build_navigation(self):
    """Configure NavigationLinks - NO click handlers needed"""
    config = anvil.server.call('get_config')
    features = config['features']
    
    # NavigationLinks set navigate_to property in Designer
    # Code only handles feature-based visibility
    
    # Always visible
    self.nav_dashboard.visible = True
    self.nav_contacts.visible = True
    self.nav_settings.visible = True
    
    # Sales & Operations (conditional visibility)
    self.nav_bookings.visible = features.get('bookings_enabled', False)
    self.nav_products.visible = features.get('ecommerce_enabled', False)
    self.nav_orders.visible = features.get('ecommerce_enabled', False)
    self.nav_rooms.visible = features.get('hospitality_enabled', False)
    self.nav_services.visible = features.get('services_enabled', False)
    self.nav_memberships.visible = features.get('memberships_enabled', False)
    
    # Customers & Marketing (conditional visibility)
    self.nav_campaigns.visible = features.get('marketing_enabled', False)
    self.nav_broadcasts.visible = features.get('marketing_enabled', False)
    self.nav_segments.visible = features.get('marketing_enabled', False)
    self.nav_tasks.visible = features.get('marketing_enabled', False)
    
    # Content & Website (conditional visibility)
    self.nav_blog.visible = features.get('blog_enabled', False)
    self.nav_pages.visible = True
    self.nav_media.visible = True
    
    # Finance & Reports (always visible)
    self.nav_invoices.visible = True
    self.nav_payments.visible = True
    self.nav_reports.visible = True
    self.nav_analytics.visible = True
```

**AdminLayout Navigation Groups:**

- Dashboard (always visible)
- Sales & Operations
  - Bookings (if bookings_enabled)
  - Products (if ecommerce_enabled)
  - Orders (if ecommerce_enabled)
  - Rooms (if hospitality_enabled)
  - Services (if services_enabled)
  - Memberships (if memberships_enabled)
- Customers & Marketing
  - Contacts (always visible)
  - Campaigns (if marketing_enabled)
  - Broadcasts (if marketing_enabled)
  - Segments (if marketing_enabled)
  - Tasks (if marketing_enabled)
- Content & Website
  - Blog (if blog_enabled)
  - Pages (always visible)
  - Media (always visible)
- Finance & Reports
  - Invoices (always visible)
  - Payments (always visible)
  - Reports (always visible)
  - Analytics (always visible)
- Settings (always visible)

**NavigationLink Configuration (in Designer):**

```
Each NavigationLink requires:
- name: nav_{destination} (e.g., nav_dashboard, nav_bookings)
- text: Display label (e.g., "Dashboard", "Bookings")
- icon: FontAwesome icon (e.g., 'fa:dashboard', 'fa:calendar')
- navigate_to: Form name (e.g., 'DashboardForm', 'BookingListForm')
- selected: False (default, set True to highlight active)

NO click handlers needed - navigate_to property handles navigation automatically.
```

#### CustomerLayout Navigation

**M3 Implementation:**

```python
from m3.components import NavigationLink

class CustomerLayout(NavigationDrawerLayoutTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.build_navigation()
  
  def build_navigation(self):
    """Configure customer portal NavigationLinks"""
    user = anvil.users.get_user()
    config = anvil.server.call('get_config')
    features = config['features']
    
    # Always visible
    self.nav_my_dashboard.visible = True
    self.nav_payment_methods.visible = True
    self.nav_invoices.visible = True
    self.nav_support.visible = True
    self.nav_account.visible = True
    
    # Activity-based visibility
    has_bookings = anvil.server.call('user_has_bookings', user)
    has_orders = anvil.server.call('user_has_orders', user)
    is_member = anvil.server.call('user_is_member', user)
    
    self.nav_my_bookings.visible = has_bookings or features.get('bookings_enabled', False)
    self.nav_my_orders.visible = has_orders or features.get('ecommerce_enabled', False)
    self.nav_my_membership.visible = is_member or features.get('memberships_enabled', False)
    self.nav_my_reviews.visible = features.get('reviews_enabled', False)
```

**CustomerLayout Navigation Structure:**

- My Dashboard (always visible)
- My Bookings (if has bookings OR bookings_enabled)
- My Orders (if has orders OR ecommerce_enabled)
- My Membership (if is_member OR memberships_enabled)
- Payment Methods (always visible)
- Invoices (always visible)
- My Reviews (if reviews_enabled)
- Support Tickets (always visible)
- Account Settings (always visible)
- Logout (always visible)

#### Navigation Helpers

```python
# client_code/shared/navigation_helpers.py
from anvil import open_form
import anvil.users

def require_auth():
  """Check authentication, redirect to login if needed"""
  user = anvil.users.get_user()
  if not user:
    open_form('LoginForm')
    return None
  return user

def require_admin():
  """Check admin role"""
  user = require_auth()
  if not user or user['role'] not in ['owner', 'manager', 'admin']:
    open_form('ErrorForm', error='Access denied')
    return None
  return user

def navigate_to_dashboard():
  """Navigate to appropriate dashboard based on role"""
  user = anvil.users.get_user()
  if not user:
    open_form('LoginForm')
    return
  
  if user['role'] in ['owner', 'manager', 'admin', 'staff']:
    open_form('DashboardForm')  # Opens with AdminLayout
  else:
    open_form('CustomerDashboardForm')  # Opens with CustomerLayout

def highlight_active_nav(layout, active_form):
  """Highlight the active NavigationLink"""
  if not layout:
    return
  
  # AdminLayout NavigationLinks
  if hasattr(layout, 'nav_dashboard'):
    layout.nav_dashboard.selected = (active_form == 'DashboardForm')
    layout.nav_bookings.selected = (active_form == 'BookingListForm')
    layout.nav_products.selected = (active_form == 'ProductListForm')
    # etc. for all NavigationLinks
```

#### M3 Navigation Best Practices

**DO:**
- Use NavigationDrawerLayout for 8+ navigation destinations
- Set `navigate_to` property on all NavigationLinks in Designer
- Use feature-based visibility in `build_navigation()` method
- Use `selected` property to highlight active NavigationLink
- Use `open_form()` only for programmatic navigation (not menu clicks)

**DON'T:**
- Use custom layouts instead of NavigationDrawerLayout
- Use Link components with click handlers for internal navigation
- Manually call `open_form()` in NavigationLink click handlers
- Use Routing for internal admin navigation (use M3 NavigationLink instead)
- Hardcode navigation visibility - always check features/permissions

**Note on Routing:** Routing IS required for public pages (blog, products, landing pages) but NOT for internal admin navigation. See anvil_cop_m3_navigation_routing.md for usage guidelines.

#### Mobile Responsiveness

NavigationDrawerLayout automatically handles mobile responsiveness:

- **Desktop/Tablet:** Navigation drawer visible as persistent sidebar
- **Mobile:** Navigation drawer collapses to modal overlay (hamburger menu)
- **Automatic:** No code required - M3 handles responsive behavior

#### Navigation Layout Properties

```python
# Access layout properties from content form
class DashboardForm(DashboardFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    AdminLayout(content=self)
    
    # Access layout
    layout = self.get_layout()
    
    # Configure layout properties
    layout.show_sidesheet = False  # Optional side panel (default: False)
    layout.navigation_drawer_vertical_align = "top"  # or "center"
    layout.content_padding = 24  # Spacing around content (pixels)
```

---

### 2.3 CRM & Marketing System Architecture

**Purpose:** Integrated customer relationship management and email marketing

#### CRM Data Model

**Core Tables:**

```
tbl_contacts                        # Customer database
├─ first_name, last_name, email, phone
├─ company, address
├─ status (lead/customer/inactive)
├─ source (website/referral/manual)
├─ tags (JSON array)
├─ total_spent, total_transactions
├─ average_order_value
├─ lifecycle_stage (new/active/at_risk/lost)
├─ last_contact_date
└─ client_id (link to Users)

tbl_contact_events                  # Activity timeline
├─ contact_id (link to tbl_contacts)
├─ event_type (booking/order/email/note)
├─ event_date
├─ description
└─ metadata (JSON)

tbl_email_campaigns                 # Email sequences
├─ campaign_name, campaign_type
├─ trigger_type (booking_created/lead_captured)
├─ sequence_emails (JSON array of emails)
├─ status (active/paused)
└─ client_id

tbl_contact_campaigns               # Campaign enrollment
├─ contact_id
├─ campaign_id
├─ sequence_day (current position)
├─ status (active/completed)
└─ enrolled_date

tbl_segments                        # Custom segments
├─ segment_name, segment_type
├─ filter_criteria (JSON)
├─ contact_count (cached)
└─ client_id

tbl_tasks                           # Task management
├─ contact_id
├─ task_title, task_type
├─ due_date, completed_date
├─ status (pending/completed)
├─ auto_generated (boolean)
└─ client_id
```

#### Integration Points

**Bookings Integration:**
```python
# In server_code/server_bookings/service.py
@anvil.server.callable
def create_booking(booking_data):
    # ... create booking ...
    
    # Integrate with CRM
    from server_code.server_customers import contact_service
    contact_service.update_contact_from_transaction(
        email=booking_data['customer_email'],
        transaction_type='booking',
        transaction_id=booking.get_id(),
        amount=booking_data['total_amount']
    )
    
    # Check for campaign enrollment
    from server_code.server_marketing import campaign_service
    campaign_service.check_campaign_triggers(
        contact_email=booking_data['customer_email'],
        trigger_type='booking_created'
    )
```

#### Background Tasks

**Scheduled Tasks:**

```python
# 1. Update Lifecycle Stages (Daily 2am)
@anvil.server.background_task
def update_lifecycle_stages():
    for contact in app_tables.tbl_contacts.search():
        days_since_contact = (now - contact['last_contact_date']).days
        
        if days_since_contact <= 30 and transactions > 0:
            lifecycle = 'Active'
        elif 90 < days_since_contact <= 180:
            lifecycle = 'At Risk'
        elif days_since_contact > 180:
            lifecycle = 'Lost'
        
        if contact['lifecycle_stage'] != lifecycle:
            contact['lifecycle_stage'] = lifecycle

# 2. Process Email Campaigns (Hourly)
@anvil.server.background_task
def process_email_campaigns():
    enrollments = app_tables.tbl_contact_campaigns.search(status='Active')
    
    for enrollment in enrollments:
        if should_send_next_email(enrollment):
            send_campaign_email(
                contact=enrollment['contact_id'],
                campaign=enrollment['campaign_id'],
                sequence_day=enrollment['sequence_day']
            )
            enrollment['sequence_day'] += 1

# 3. Generate Auto-Tasks (Daily 3am)
@anvil.server.background_task
def create_automated_tasks():
    # Check upcoming bookings (7 days out)
    bookings = app_tables.tbl_bookings.search(
        start_datetime > now,
        start_datetime < now + timedelta(days=8)
    )
    
    for booking in bookings:
        if not task_exists(booking, 'send_arrival_instructions'):
            create_task({
                'contact_id': booking['contact_id'],
                'task_title': f"Send arrival instructions to {booking.customer_name}",
                'task_type': 'send_arrival_instructions',
                'due_date': booking['start_datetime'] - timedelta(days=7),
                'auto_generated': True
            })
```

---

### 2.4 M3 Component Standards

**Mybizz uses Material Design 3 components exclusively for all UI development.**

#### Essential M3 Components (Always Use)

**Navigation & Layout (2):**
1. **NavigationDrawerLayout** - Primary layout for admin interfaces (8+ destinations)
2. **NavigationLink** - Navigation menu items with `navigate_to` property

**Typography (2):**
3. **Text** - Body text, labels, captions (use with M3 typography roles)
4. **Heading** - Section headers, page titles (use with M3 typography roles)

**Buttons (2):**
5. **Button** - Primary/secondary/tertiary actions (use filled/outlined/text roles)
6. **IconButton** - Icon-only actions (edit, delete, etc.)

**Form Inputs (7):**
7. **TextBox** - Single-line text input (use `outlined` role)
8. **TextArea** - Multi-line text input (use `outlined` role)
9. **DropdownMenu** - Selection from list (use `outlined` role)
10. **Checkbox** - Boolean options
11. **RadioButton** - Single selection from options
12. **DatePicker** - Date selection (use `outlined` role)
13. **FileLoader** - File upload

**Display Components (1):**
14. **Card** - Content containers (use `elevated` or `outlined` roles)

**Containers (3):**
15. **ColumnPanel** - Vertical stacking (main layout structure)
16. **LinearPanel** - Horizontal/vertical layouts
17. **FlowPanel** - Responsive wrapping (tags, chips, etc.)

**Total Essential: 17 components**

#### Good to Have M3 Components (Complex Forms)

18. **DataGrid** - Tabular data display
19. **RepeatingPanel** - Dynamic lists
20. **Switch** - Toggle settings/features
21. **RadioGroupPanel** - Grouped radio options
22. **ButtonMenu** - Menu attached to button
23. **IconButtonMenu** - Actions menu (edit/delete)
24. **AvatarMenu** - User profile menu
25. **MenuItem** - Menu list items
26. **Divider** - Visual separation
27. **Plot** - Charts and graphs (Plotly integration)

**Total Good to Have: 10 components**

#### Components to AVOID

**Anvil Extras Components (NOT M3-compliant):**
- ❌ Tabs → Use NavigationLink in sidebar
- ❌ Pivot → Use custom DataGrid
- ❌ MultiSelectDropDown → Use DropdownMenu + Chips
- ❌ Autocomplete → Use DropdownMenu with search
- ❌ Quill → Use TextArea
- ❌ Switch (Extras version) → Use M3 Switch
- ❌ Slider (Extras version) → Use M3 Slider
- ❌ RadioGroup → Use M3 RadioGroupPanel
- ❌ CheckBoxGroup → Use multiple Checkboxes
- ❌ Popover → Use M3 menus
- ❌ Navigation.build_menu → Use NavigationDrawerLayout
- ❌ Messaging module → Use Anvil Events
- ❌ Serialisation module → Not needed
- ❌ Logging.Logger → Use print() or Anvil logging

**Legacy Anvil Patterns to AVOID:**
- ❌ Custom sidebar layouts → Use NavigationDrawerLayout
- ❌ Link + click handlers → Use NavigationLink.navigate_to
- ❌ XYPanel for layout → Use ColumnPanel/LinearPanel
- ❌ Hardcoded colors → Use theme: color roles
- ❌ Generic Label → Use Text/Heading with M3 typography roles
- ❌ Routing for internal admin navigation → Use M3 NavigationLink (Routing IS used for public pages)

#### Component Naming Conventions

**Essential Prefixes:**
- `nav_` - NavigationLink (e.g., nav_dashboard, nav_bookings)
- `btn_` - Button, IconButton (e.g., btn_save, btn_cancel)
- `lbl_` - Text, Heading (e.g., lbl_page_title, lbl_section_header)
- `txt_` - TextBox, TextArea (e.g., txt_customer_name, txt_notes)
- `dd_` - DropdownMenu (e.g., dd_status, dd_category)
- `cb_` - Checkbox (e.g., cb_agree_terms, cb_newsletter)
- `rb_` - RadioButton (e.g., rb_option_a, rb_option_b)
- `dp_` - DatePicker (e.g., dp_start_date, dp_end_date)
- `fu_` - FileLoader (e.g., fu_upload_avatar, fu_import_data)
- `card_` - Card (e.g., card_revenue, card_summary)
- `col_` - ColumnPanel (e.g., col_main, col_content)
- `lp_` - LinearPanel (e.g., lp_header, lp_actions)
- `flow_` - FlowPanel (e.g., flow_tags, flow_metrics)

**Good to Have Prefixes:**
- `dg_` - DataGrid (e.g., dg_contacts, dg_products)
- `rp_` - RepeatingPanel (e.g., rp_items, rp_history)
- `sw_` - Switch (e.g., sw_feature_enabled)
- `menu_` - ButtonMenu, IconButtonMenu, AvatarMenu (e.g., menu_user, menu_actions)
- `plot_` - Plot (e.g., plot_revenue_trend)

#### M3 Typography Roles

**Use these roles on Text/Heading components:**

```python
# Display (largest - hero text)
component.role = 'display-large'     # 57sp
component.role = 'display-medium'    # 45sp
component.role = 'display-small'     # 36sp

# Headline (page titles, section headers)
component.role = 'headline-large'    # 32sp - Page titles
component.role = 'headline-medium'   # 28sp - Section headers
component.role = 'headline-small'    # 24sp - Card titles

# Title (list items, card headers)
component.role = 'title-large'       # 22sp - List items
component.role = 'title-medium'      # 16sp - Card headers
component.role = 'title-small'       # 14sp - Items

# Body (main content)
component.role = 'body-large'        # 16sp - Main content
component.role = 'body-medium'       # 14sp - Body text (default)
component.role = 'body-small'        # 12sp - Captions

# Label (buttons, chips, fields)
component.role = 'label-large'       # 14sp - Buttons
component.role = 'label-medium'      # 12sp - Chips
component.role = 'label-small'       # 11sp - Field labels
```

#### M3 Color Roles

**Use theme: prefix for all colors:**

```python
# Primary colors (main actions)
component.background_color = 'theme:Primary'
component.foreground_color = 'theme:On Primary'

# Secondary colors (less prominent)
component.background_color = 'theme:Secondary'
component.foreground_color = 'theme:On Secondary'

# Surface colors (cards, containers)
component.background_color = 'theme:Surface'
component.foreground_color = 'theme:On Surface'
component.background_color = 'theme:Surface Variant'

# Error colors (validation)
component.background_color = 'theme:Error'
component.foreground_color = 'theme:On Error'

# Background
component.background_color = 'theme:Background'
component.foreground_color = 'theme:On Background'
```

#### M3 Button Hierarchy

**Visual hierarchy communicates importance:**

```python
# Primary action (Save, Submit, Confirm)
self.btn_save.role = 'filled-button'  # or default (filled is default)
self.btn_save.icon = 'fa:save'

# Secondary action (Cancel, Back, Edit)
self.btn_cancel.role = 'outlined'
self.btn_cancel.icon = 'fa:times'

# Tertiary action (Learn More, View Details)
self.btn_details.role = 'text-button'
```

#### M3 Input Roles

**Use outlined role for cleaner forms:**

```python
# TextBox and TextArea
self.txt_customer_name.role = 'outlined'
self.txt_notes.role = 'outlined'

# DropdownMenu
self.dd_status.role = 'outlined'

# DatePicker
self.dp_start_date.role = 'outlined'

# Error state
if not valid:
    self.txt_email.role = 'outlined-error'
    self.txt_email.placeholder = "Email required"
else:
    self.txt_email.role = 'outlined'
```

#### M3 Card Variants

**Cards display content about a single subject:**

```python
# Elevated card (dashboard metrics, summary)
self.card_revenue.role = None  # Default is elevated
self.card_revenue.background_color = 'theme:Surface'

# Outlined card (list items, secondary content)
self.card_contact.role = 'outlined-card'

# Filled card (special emphasis)
self.card_featured.role = 'filled-card'
```

#### Form Type Standards

**List Forms (ContactListForm, ProductListForm):**
- NavigationDrawerLayout
- Heading (headline-large) for page title
- LinearPanel for header with filters
- TextBox (outlined) for search
- DropdownMenu (outlined) for filters
- Button (filled) for "New" action
- DataGrid for list data
- IconButton for row actions

**Editor Forms (ContactEditorForm, ProductEditorForm):**
- Card (outlined) for form container
- Heading (headline-small) for section headers
- TextBox (outlined) for single-line inputs
- TextArea (outlined) for multi-line inputs
- DropdownMenu (outlined) for selections
- DatePicker (outlined) for dates
- Checkbox for boolean flags
- LinearPanel for action buttons
- Button (filled) for Save
- Button (outlined) for Cancel

**Dashboard Forms (MarketingDashboardForm):**
- NavigationDrawerLayout
- Heading (headline-large) for page title
- LinearPanel (horizontal) for metrics row
- Card (elevated) for each metric
- Plot for charts
- DataGrid for summary tables
- LinearProgressIndicator for loading states

---

### 2.5 Data Binding System

**Mybizz uses Anvil's data binding system for all form-data interactions.**

#### Core Pattern: self.item Property

**Standard Implementation:**

```python
class ContactEditorForm(ContactEditorFormTemplate):
  def __init__(self, contact=None, **properties):
    # Store data in self.item
    self.item = contact or {}
    
    # Initialize components (data bindings apply automatically)
    self.init_components(**properties)
  
  def btn_save_click(self, **event_args):
    # self.item is automatically updated by two-way bindings
    anvil.server.call('save_contact', self.item)
    self.raise_event('x-close')
```

#### Two-Way Data Bindings with Write Back

**Configure in Designer:**

1. Select component (e.g., TextBox)
2. Click data binding icon for `text` property
3. Set binding: `self.item['first_name']`
4. Toggle **W** (Write Back) ON
5. Done - no event handlers needed!

**What Write Back Does:**

```python
# WITHOUT Write Back (manual - DON'T DO THIS)
@handle("txt_first_name", "change")
def txt_first_name_change(self, **event_args):
  self.item['first_name'] = self.txt_first_name.text  # Manual update

# WITH Write Back (automatic - DO THIS)
# No event handler needed!
# TextBox automatically updates self.item['first_name'] on lost_focus/pressed_enter
```

#### Supported Components for Two-Way Bindings

**Always use write back for these:**

- **TextBox** - Bind `text` property → `self.item['field_name']`
- **TextArea** - Bind `text` property → `self.item['description']`
- **DatePicker** - Bind `date` property → `self.item['date_field']`
- **DropdownMenu** - Bind `selected_value` property → `self.item['status']`
- **Checkbox** - Bind `checked` property → `self.item['agree']`
- **RadioButton** - Bind `selected` property → `self.item['option']`
- **Slider** - Bind `value` property → `self.item['rating']`
- **Switch** - Bind `checked` property → `self.item['enabled']`
- **NumberPicker** - Bind `number` property → `self.item['quantity']`

#### Refresh Data Bindings

**When to use `refresh_data_bindings()`:**

```python
# Case 1: After modifying self.item in place
def load_contact(self, contact_id):
  self.item['id'] = contact_id  # Modifying in place
  self.item['name'] = "Updated"  # Modifying in place
  self.refresh_data_bindings()  # Manual refresh needed

# Case 2: After reassigning self.item completely
def load_contact(self, contact_id):
  self.item = anvil.server.call('get_contact', contact_id)
  # NO refresh needed - reassignment triggers automatic refresh

# Case 3: After server call that updates self.item
def btn_save_click(self, **event_args):
  updated = anvil.server.call('save_contact', self.item)
  self.item = updated  # Reassignment triggers automatic refresh
```

#### Data Binding Best Practices

**DO:**
- Use `self.item` property for all form data
- Enable write back (W toggle ON) for all input components
- Use `self.item = data` for initial load (automatic refresh)
- Call `refresh_data_bindings()` only when modifying in place
- Pass Data Table rows directly: `self.item = contact_row`

**DON'T:**
- Manually update `self.item` in change event handlers (redundant with write back)
- Forget to enable write back toggle (data won't update)
- Call `refresh_data_bindings()` unnecessarily (wastes resources)
- Mix manual updates with write back (choose one pattern)

#### Write Back Timing

**Write back triggers on:**
- `lost_focus` event (component loses focus)
- `pressed_enter` event (user presses Enter in TextBox/TextArea)

**Write back does NOT trigger on:**
- `change` event (every keystroke)
- `refresh_data_bindings()` call (only reads, doesn't write)
- Programmatic property assignment (`self.txt.text = "value"`)

#### Complete Data Binding Workflow

**Example: Contact Editor Form**

```python
# 1. In Designer:
#    - Bind txt_first_name.text → self.item['first_name'] (W ON)
#    - Bind txt_last_name.text → self.item['last_name'] (W ON)
#    - Bind txt_email.text → self.item['email'] (W ON)
#    - Bind dd_status.selected_value → self.item['status'] (W ON)

# 2. In Code:
class ContactEditorForm(ContactEditorFormTemplate):
  def __init__(self, contact=None, **properties):
    # Set self.item BEFORE init_components
    self.item = contact or {
      'first_name': '',
      'last_name': '',
      'email': '',
      'status': 'lead'
    }
    
    # Initialize components (data bindings apply automatically)
    self.init_components(**properties)
  
  def btn_save_click(self, **event_args):
    # Validate
    if not self.item['email']:
      self.txt_email.role = 'outlined-error'
      anvil.alert("Email required")
      return
    
    # Save (self.item already updated by write back)
    result = anvil.server.call('save_contact', self.item)
    
    if result['success']:
      self.raise_event('x-close')
    else:
      anvil.alert(result['error'])
```

**Total Event Handlers Needed: 1** (btn_save_click)  
**Event Handlers Eliminated: 4** (no change handlers for txt_first_name, txt_last_name, txt_email, dd_status)

---

## 3. Data Architecture

### 3.1 Database Schema

**Core Configuration:**

```
tbl_config (one row per client)
├─ business_name, logo
├─ primary_color, accent_color
├─ system_currency
├─ features_enabled (JSON)
├─ home_template (text)
├─ home_config (JSON)
├─ google_maps_api_key
├─ social_facebook, social_instagram, social_twitter, social_linkedin
├─ privacy_policy, terms_conditions
└─ client_id (link to Users)
```

**Authentication:**

```
tbl_users (extended from Anvil Users)
├─ role (admin/manager/staff/customer)
├─ permissions (JSON)
├─ status (active/inactive/suspended)
└─ last_login (datetime)
```

**Bookings:**

```
tbl_bookings
├─ customer_id
├─ service_id
├─ booking_number
├─ start_datetime, end_datetime, duration
├─ status (pending/confirmed/cancelled/completed)
├─ notes, total_amount, payment_status
└─ client_id

tbl_services
├─ name, description
├─ duration (minutes), price
├─ category
├─ availability_settings (JSON)
└─ client_id

tbl_availability
├─ day_of_week (0-6)
├─ start_time, end_time
├─ is_available
└─ client_id
```

**E-commerce:**

```
tbl_products
├─ name, slug, description
├─ price, compare_at_price
├─ images
├─ inventory_count, track_inventory
├─ categories, tags
├─ variants (JSON)
├─ status
└─ client_id

tbl_orders
├─ customer_id
├─ order_number
├─ items (JSON), subtotal, tax, shipping, total
├─ payment_method, payment_status
├─ shipping_address (JSON), shipping_status
├─ created_date, completed_date
└─ client_id

tbl_order_items
├─ order_id
├─ product_id
├─ product_name (snapshot)
├─ quantity, price, subtotal
└─ client_id
```

**Financial:**

```
tbl_invoices
├─ customer_id
├─ invoice_number
├─ line_items (JSON), subtotal, tax, discount, total
├─ issue_date, due_date, paid_date
├─ status (draft/sent/paid/overdue)
├─ payment_method
└─ client_id

tbl_subscriptions
├─ customer_id
├─ subscription_number
├─ plan_name, billing_amount
├─ billing_interval (monthly/quarterly/yearly)
├─ status (active/paused/cancelled)
├─ gateway_subscription_id
└─ client_id
```

**Content:**

```
tbl_blog_posts
├─ title, slug, content
├─ excerpt, featured_image
├─ author, published_date, status
├─ categories, tags
├─ views_count
└─ client_id

tbl_landing_pages
├─ title, slug, template_type
├─ config (JSON)
├─ status (draft/published)
├─ views_count, conversions_count
└─ client_id
```

**Security & Compliance:**

```
tbl_audit_log
├─ user_id
├─ action (login/update_product/delete_customer)
├─ resource_type, resource_id
├─ ip_address, timestamp
└─ client_id

tbl_email_log
├─ recipient, subject
├─ template_used
├─ status (sent/failed)
└─ client_id
```

### 3.2 Data Flow Patterns

**Read Operations:**
```python
@anvil.server.callable
def get_all_bookings():
    user = anvil.users.get_user()
    # app_tables exists in CLIENT's environment
    bookings = app_tables.tbl_bookings.search(
        client_id=user
    )
    return list(bookings)
```

**Write Operations:**
```python
@anvil.server.callable
def create_booking(booking_data):
    user = anvil.users.get_user()
    booking = app_tables.tbl_bookings.add_row(
        client_id=user,
        customer_id=booking_data['customer_id'],
        booking_number=generate_booking_number(),
        **booking_data
    )
    return {'success': True, 'booking_id': booking.get_id()}
```

**Data Isolation:**
- Master template code runs in CLIENT's Anvil environment
- `app_tables` reference is CLIENT's Data Tables
- Complete isolation - Client A cannot access Client B's data

---

## 4. Security Architecture

### 4.1 Security Layers

```
┌────────────────────────────────────────────────────────────┐
│ Layer 1: Anvil Platform Security (Infrastructure)         │
│ - HTTPS/TLS encryption                                     │
│ - DDoS protection                                          │
│ - Server-side execution sandboxing                         │
│ - Built-in CSRF protection                                 │
└────────────────────────────────────────────────────────────┘
                           ↓
┌────────────────────────────────────────────────────────────┐
│ Layer 2: Application RBAC (Role-Based Access Control)     │
│ - @require_role decorators                                 │
│ - @require_permission decorators                           │
│ - Server-side permission enforcement                       │
└────────────────────────────────────────────────────────────┘
                           ↓
┌────────────────────────────────────────────────────────────┐
│ Layer 3: Data Encryption                                   │
│ - Sensitive data encrypted at rest                         │
│ - API keys in Anvil Secrets                                │
│ - Payment tokens encrypted                                 │
└────────────────────────────────────────────────────────────┘
                           ↓
┌────────────────────────────────────────────────────────────┐
│ Layer 4: Audit Logging                                     │
│ - All sensitive actions logged                             │
│ - User attribution                                         │
│ - Timestamped events                                       │
└────────────────────────────────────────────────────────────┘
```

### 4.2 RBAC Implementation

**Role Hierarchy:**
- Owner: Full access (1 per instance)
- Manager: Most features (0-3 per instance)
- Admin: Day-to-day operations (0-10 per instance)
- Staff: Limited access (0-20 per instance)
- Customer: Own data only

**Permission Decorators:**
```python
# server_code/server_auth/rbac.py

def require_role(allowed_roles):
    """Decorator to enforce role-based access"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            user = anvil.users.get_user()
            if not user or user['role'] not in allowed_roles:
                raise Exception("Access denied: insufficient permissions")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def require_permission(permission_name):
    """Decorator to enforce permission-based access"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            user = anvil.users.get_user()
            permissions = user.get('permissions', {})
            if not permissions.get(permission_name, False):
                raise Exception(f"Access denied: missing permission '{permission_name}'")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Usage examples:
@anvil.server.callable
@require_role(['owner', 'manager', 'admin'])
def delete_customer(customer_id):
    """Only admins can delete customers"""
    pass

@anvil.server.callable
@require_permission('bookings.manage')
def create_booking(booking_data):
    """Requires bookings.manage permission"""
    pass
```

**Standard Permissions:**
- `bookings.view`, `bookings.manage`
- `products.view`, `products.manage`
- `customers.view`, `customers.manage`
- `settings.view`, `settings.manage`
- `analytics.view`

### 4.3 Data Encryption

```python
# server_code/server_shared/encryption.py

import anvil.secrets
from cryptography.fernet import Fernet

def get_encryption_key():
    """Get encryption key from Anvil Secrets"""
    return anvil.secrets.get_secret('encryption_key')

def encrypt(data):
    """Encrypt sensitive data"""
    fernet = Fernet(get_encryption_key())
    return fernet.encrypt(data.encode()).decode()

def decrypt(encrypted_data):
    """Decrypt sensitive data"""
    fernet = Fernet(get_encryption_key())
    return fernet.decrypt(encrypted_data.encode()).decode()

# Usage:
@anvil.server.callable
def store_payment_method(customer_id, card_token):
    """Store encrypted payment token"""
    encrypted_token = encrypt(card_token)
    
    customer = app_tables.customers.get_by_id(customer_id)
    customer['payment_token'] = encrypted_token
    
    return {'success': True}
```

**What Gets Encrypted:**
- Payment tokens
- API keys (stored in Anvil Secrets)
- Customer PII (optional, based on compliance requirements)
- Sensitive business data

### 4.4 Input Validation

**Always validate user inputs:**

```python
import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_html(text):
    """Remove HTML tags"""
    return re.sub(r'<[^>]+>', '', text)

def validate_amount(amount):
    """Validate monetary amount"""
    try:
        value = float(amount)
        return value > 0
    except:
        return False

@anvil.server.callable
def create_customer(name, email):
    # Validate inputs
    if not validate_email(email):
        return {'success': False, 'error': 'Invalid email address'}
    
    # Sanitize text inputs
    safe_name = sanitize_html(name)
    
    # Proceed with creation
    customer = app_tables.customers.add_row(
        name=safe_name,
        email=email,
        created=datetime.now()
    )
    
    return {'success': True, 'customer_id': customer.get_id()}
```

### 4.5 Audit Logging

```python
# server_code/server_shared/audit.py

@anvil.server.callable
def log_audit_event(action, resource_type, resource_id, changes=None):
    """Log security-relevant events"""
    user = anvil.users.get_user()
    
    app_tables.tbl_audit_log.add_row(
        user_id=user,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        changes=changes,
        ip_address=anvil.server.context.request.client_ip,
        timestamp=datetime.now()
    )

# Usage in sensitive operations:
@anvil.server.callable
def delete_customer(customer_id):
    customer = app_tables.customers.get_by_id(customer_id)
    customer_data = dict(customer)
    
    customer.delete()
    
    # Log the deletion
    log_audit_event(
        action='delete_customer',
        resource_type='customer',
        resource_id=customer_id,
        changes={'deleted_data': customer_data}
    )
    
    return {'success': True}
```

---

## 5. Integration Architecture

### 5.1 Payment Gateways

**Dual Gateway Support:**

**Stripe (Global)**
```python
# server_code/server_payments/stripe_service.py

import stripe
import anvil.secrets

stripe.api_key = anvil.secrets.get_secret('stripe_secret_key')

@anvil.server.callable
def create_stripe_payment_intent(amount, currency='usd'):
    """Create payment intent for one-time payment"""
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents
            currency=currency
        )
        return {'success': True, 'client_secret': intent.client_secret}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@anvil.server.callable
def create_stripe_subscription(customer_id, price_id):
    """Create subscription"""
    try:
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{'price': price_id}]
        )
        return {'success': True, 'subscription_id': subscription.id}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@anvil.server.http_endpoint('/webhooks/stripe', methods=['POST'])
def handle_stripe_webhook(**params):
    """Handle Stripe webhook events"""
    payload = params['payload']
    sig_header = params['headers']['Stripe-Signature']
    
    endpoint_secret = anvil.secrets.get_secret('stripe_webhook_secret')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        
        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object
            # Update order status
            pass
            
        elif event.type == 'invoice.payment_succeeded':
            invoice = event.data.object
            # Update subscription status
            pass
        
        return {'status': 'success'}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}
```

**Paystack (Africa)**
```python
# server_code/server_payments/paystack_service.py

import anvil.http
import anvil.secrets

def get_paystack_headers():
    """Get Paystack API headers"""
    secret_key = anvil.secrets.get_secret('paystack_secret_key')
    return {
        'Authorization': f'Bearer {secret_key}',
        'Content-Type': 'application/json'
    }

@anvil.server.callable
def initialize_paystack_payment(amount, email, currency='ZAR'):
    """Initialize payment"""
    try:
        response = anvil.http.request(
            'https://api.paystack.co/transaction/initialize',
            method='POST',
            headers=get_paystack_headers(),
            json={
                'amount': int(amount * 100),  # Convert to cents
                'email': email,
                'currency': currency
            }
        )
        
        data = response.json()
        if data['status']:
            return {
                'success': True,
                'reference': data['data']['reference'],
                'authorization_url': data['data']['authorization_url']
            }
        else:
            return {'success': False, 'error': data['message']}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@anvil.server.callable
def verify_paystack_payment(reference):
    """Verify payment"""
    try:
        response = anvil.http.request(
            f'https://api.paystack.co/transaction/verify/{reference}',
            method='GET',
            headers=get_paystack_headers()
        )
        
        data = response.json()
        if data['status'] and data['data']['status'] == 'success':
            return {'success': True, 'data': data['data']}
        else:
            return {'success': False, 'error': 'Payment not successful'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@anvil.server.http_endpoint('/webhooks/paystack', methods=['POST'])
def handle_paystack_webhook(**params):
    """Handle Paystack webhook events"""
    payload = params['payload']
    
    # Verify webhook signature
    secret = anvil.secrets.get_secret('paystack_webhook_secret')
    signature = params['headers'].get('X-Paystack-Signature')
    
    # Process event
    event = payload.get('event')
    
    if event == 'charge.success':
        # Update order status
        pass
    
    return {'status': 'success'}
```

### 5.2 Email Integration (Zoho)

```python
# server_code/server_emails/zoho_integration.py

import anvil.email
import anvil.secrets

@anvil.server.callable
def send_transactional_email(to_email, subject, body_html, from_name=None):
    """Send transactional email via Zoho"""
    try:
        config = get_config()
        business_name = config['business_name']
        
        # Zoho credentials from Secrets
        zoho_username = anvil.secrets.get_secret('zoho_email_username')
        zoho_password = anvil.secrets.get_secret('zoho_email_password')
        
        # Send via Anvil's email service configured with Zoho SMTP
        anvil.email.send(
            to=to_email,
            from_address=f"{from_name or business_name} <{zoho_username}>",
            subject=subject,
            html=body_html
        )
        
        # Log email
        app_tables.tbl_email_log.add_row(
            recipient=to_email,
            subject=subject,
            template_used='transactional',
            status='sent',
            sent_date=datetime.now()
        )
        
        return {'success': True}
    except Exception as e:
        # Log failure
        app_tables.tbl_email_log.add_row(
            recipient=to_email,
            subject=subject,
            template_used='transactional',
            status='failed',
            error_message=str(e),
            sent_date=datetime.now()
        )
        return {'success': False, 'error': str(e)}

@anvil.server.callable
def send_booking_confirmation(booking_id):
    """Send booking confirmation email"""
    booking = app_tables.tbl_bookings.get_by_id(booking_id)
    customer = booking['customer_id']
    
    subject = f"Booking Confirmation - {booking['booking_number']}"
    body_html = f"""
    <h2>Booking Confirmed</h2>
    <p>Dear {customer['first_name']},</p>
    <p>Your booking has been confirmed.</p>
    <p><strong>Booking Number:</strong> {booking['booking_number']}</p>
    <p><strong>Date & Time:</strong> {booking['start_datetime']}</p>
    <p>Thank you for choosing us!</p>
    """
    
    return send_transactional_email(
        to_email=customer['email'],
        subject=subject,
        body_html=body_html
    )
```

### 5.3 Marketing Integration (Brevo)

```python
# server_code/server_marketing/brevo_integration.py

import anvil.http
import anvil.secrets

def get_brevo_headers():
    """Get Brevo API headers"""
    api_key = anvil.secrets.get_secret('brevo_api_key')
    return {
        'api-key': api_key,
        'Content-Type': 'application/json'
    }

@anvil.server.callable
def send_campaign_email(contact_id, campaign_id, sequence_day):
    """Send email from campaign sequence"""
    contact = app_tables.tbl_contacts.get_by_id(contact_id)
    campaign = app_tables.tbl_email_campaigns.get_by_id(campaign_id)
    
    sequence_emails = campaign['sequence_emails']
    email_data = sequence_emails[sequence_day]
    
    try:
        response = anvil.http.request(
            'https://api.brevo.com/v3/smtp/email',
            method='POST',
            headers=get_brevo_headers(),
            json={
                'to': [{'email': contact['email'], 'name': contact['first_name']}],
                'subject': email_data['subject'],
                'htmlContent': email_data['html_content'],
                'sender': {'email': 'noreply@Mybizz.com', 'name': 'Mybizz'}
            }
        )
        
        return {'success': True, 'message_id': response.json()['messageId']}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@anvil.server.http_endpoint('/webhooks/brevo', methods=['POST'])
def handle_brevo_webhook(**params):
    """Handle Brevo webhook events (opens, clicks)"""
    payload = params['payload']
    event_type = payload.get('event')
    
    if event_type == 'opened':
        # Track email open
        pass
    elif event_type == 'click':
        # Track email click
        pass
    
    return {'status': 'success'}
```

### 5.4 Shipping Integration

**Bob Go (South Africa):**
```python
# server_code/server_shipping/bobgo_service.py

import anvil.http
import anvil.secrets

@anvil.server.callable
def get_bobgo_rates(origin, destination, weight):
    """Get shipping rates from Bob Go"""
    api_key = anvil.secrets.get_secret('bobgo_api_key')
    
    try:
        response = anvil.http.request(
            'https://api.bobgo.co.za/v1/rates',
            method='POST',
            headers={'Authorization': f'Bearer {api_key}'},
            json={
                'origin': origin,
                'destination': destination,
                'weight': weight
            }
        )
        
        return {'success': True, 'rates': response.json()}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@anvil.server.callable
def create_bobgo_shipment(order_id):
    """Create shipment with Bob Go"""
    order = app_tables.tbl_orders.get_by_id(order_id)
    
    # Create shipment via Bob Go API
    # Return tracking number
    pass
```

**Easyship (International):**
```python
# server_code/server_shipping/easyship_service.py

import anvil.http
import anvil.secrets

@anvil.server.callable
def get_easyship_rates(order_data):
    """Get shipping rates from Easyship"""
    api_key = anvil.secrets.get_secret('easyship_api_key')
    
    try:
        response = anvil.http.request(
            'https://api.easyship.com/v1/rates',
            method='POST',
            headers={'Authorization': f'Bearer {api_key}'},
            json=order_data
        )
        
        return {'success': True, 'rates': response.json()}
    except Exception as e:
        return {'success': False, 'error': str(e)}
```

---

## 6. Deployment Architecture

### 6.1 Development Workflow

```
┌────────────────────────────────────────────────────────────┐
│  master_template_dev (Development App)                     │
│  - Active development                                       │
│  - Feature branches                                        │
│  - Testing                                                 │
└────────────────────────────────────────────────────────────┘
                           ↓
                    Testing Complete
                           ↓
┌────────────────────────────────────────────────────────────┐
│  master_template_staging (Staging App - Clone)            │
│  - Pre-production testing                                  │
│  - User acceptance testing                                 │
│  - Performance testing                                     │
└────────────────────────────────────────────────────────────┘
                           ↓
                    Approval to Publish
                           ↓
┌────────────────────────────────────────────────────────────┐
│  master_template (Published Dependency)                    │
│  - Version: V1.0, V1.1, V1.2...                           │
│  - Frozen snapshot                                         │
│  - Client instances depend on this                         │
└────────────────────────────────────────────────────────────┘
                           ↓
                   Client Pulls Update
                           ↓
┌────────────────────────────────────────────────────────────┐
│  Client Instance (e.g., client_yogastudio)                │
│  - Updates dependency to new version                       │
│  - Tests in their environment                              │
│  - Rolls back if issues                                    │
└────────────────────────────────────────────────────────────┘
```

### 6.2 Publishing Process

**Step 1: Prepare Release**
1. Complete features in master_template_dev
2. Update version number
3. Write release notes
4. Run test suite

**Step 2: Publish**
1. In Anvil IDE: Publish → Create new published version
2. Tag version (e.g., V1.2.0)
3. Add release notes

**Step 3: Notify Clients**
1. Create notification in Mybizz_management
2. Email clients about new version
3. Document changes in release notes

**Step 4: Client Update**
1. Client reviews release notes
2. Client updates dependency in their app
3. Client tests in their environment
4. Client can roll back if issues

### 6.3 Versioning Strategy

**Semantic Versioning:**
- V1.0.0 - Initial release
- V1.1.0 - Minor features, backwards compatible
- V1.0.1 - Bug fixes, backwards compatible
- V2.0.0 - Breaking changes

**Update Types:**
- **Critical Security:** Push notification, recommend immediate update
- **Bug Fixes:** Standard notification
- **New Features:** Standard notification
- **Breaking Changes:** Advance notice, migration guide

---

## 7. Performance & Scalability

### 7.1 Performance Optimization

**Server Call Optimization:**
```python
# ❌ BAD: Multiple calls in loop
for item in items:
  anvil.server.call('process_item', item)  # N calls!

# ✅ GOOD: Single batch call
anvil.server.call('process_items_batch', items)  # 1 call
```

**Background Tasks for Long Operations:**
```python
# For operations > 30 seconds
@anvil.server.background_task
def generate_report():
    data = process_large_dataset()  # No timeout
    
    # Save result
    app_tables.reports.add_row(data=data)
    
    # Notify user
    anvil.email.send(...)
```

**Lazy Loading:**
```python
@anvil.server.callable
def get_customers_page(page=1, page_size=50):
    """Return paginated results"""
    offset = (page - 1) * page_size
    
    customers = app_tables.customers.search()
    page_data = list(customers)[offset:offset+page_size]
    
    return {
        'customers': page_data,
        'page': page,
        'total_pages': total // page_size
    }
```

**Caching Strategy:**
- Dashboard metrics: Cached 1 hour
- Segment counts: Updated nightly
- Campaign stats: Real-time (low volume)

### 7.2 Database Indexing

**Critical Indexes:**
```sql
-- Performance-critical indexes
tbl_contacts: instance_id, email (composite)
tbl_contacts: status
tbl_contact_events: contact_id, event_date (composite)
tbl_bookings: instance_id, start_datetime (composite)
tbl_orders: instance_id, order_status (composite)
```

### 7.3 Scalability (V1.x Limits)

**100 Client Maximum:**
- Each client = separate Anvil account
- No shared resources
- Linear scaling
- Manual provisioning acceptable (2 hours/client)

**Per-Client Capacity:**
- Up to 10,000 contacts
- Up to 100 active campaigns
- Up to 50 emails/hour (Brevo limit)
- Unlimited bookings, orders, products (within Anvil storage limits)

---

## 8. Compliance & Standards

### 8.1 GDPR/POPIA Compliance

**Data Export:**
```python
@anvil.server.callable
def export_customer_data(customer_id):
    """Export all customer data (GDPR compliance)"""
    customer = app_tables.customers.get_by_id(customer_id)
    
    # Collect all related data
    data = {
        'customer': dict(customer),
        'bookings': [dict(b) for b in app_tables.bookings.search(customer_id=customer)],
        'orders': [dict(o) for b in app_tables.orders.search(customer_id=customer)],
        'contacts': [dict(c) for c in app_tables.contacts.search(email=customer['email'])]
    }
    
    return data
```

**Right to be Forgotten:**
```python
@anvil.server.callable
def delete_customer_data(customer_id):
    """Delete all customer data (GDPR compliance)"""
    customer = app_tables.customers.get_by_id(customer_id)
    
    # Delete related data
    for booking in app_tables.bookings.search(customer_id=customer):
        booking.delete()
    
    for order in app_tables.orders.search(customer_id=customer):
        order.delete()
    
    # Anonymize instead of delete if financial records exist
    if has_financial_records(customer):
        customer['first_name'] = '[DELETED]'
        customer['last_name'] = '[DELETED]'
        customer['email'] = f'deleted_{customer.get_id()}@deleted.com'
    else:
        customer.delete()
    
    return {'success': True}
```

**Cookie Consent:**
- Cookie consent banner on public pages
- Preferences stored in browser localStorage
- Compliance with EU cookie law

**Privacy Policy:**
- Template provided
- Customizable per client
- Always accessible on website

### 8.2 PCI DSS Compliance

**Payment Token Handling:**
- NEVER store full credit card numbers
- Only store tokenized references from payment gateways
- Use Stripe/Paystack's PCI-compliant tokenization
- Encrypt payment tokens at rest

**Security Requirements:**
- HTTPS enforced (Anvil handles this)
- No client-side storage of payment data
- Server-side payment processing only
- Regular security audits

### 8.3 Data Retention

**Retention Policies:**
- Contacts: Retained indefinitely (unless deleted by user)
- Transactions: Retained 7 years (tax compliance)
- Audit logs: Retained 2 years
- Email logs: Retained 90 days
- Tasks: Auto-deleted 90 days after completion

---

## 9. Anvil Compliance Checklist

**All Mybizz development MUST:**

- ✅ Use Anvil Data Tables (not external databases)
- ✅ Use Anvil Users service for authentication
- ✅ Use Anvil Secrets for API keys
- ✅ Use `@anvil.server.callable` for all server functions
- ✅ Use Anvil's built-in components when available
- ✅ Avoid global variables in server modules
- ✅ Handle all exceptions in server functions
- ✅ Return structured responses (`{'success': bool, 'data': ...}`)
- ✅ Use Anvil packages for organization
- ✅ Test in Anvil's environment

**Security Requirements:**

- ✅ All server functions have RBAC decorators
- ✅ Sensitive data encrypted at rest
- ✅ Webhook signatures verified
- ✅ Input validation on all user inputs
- ✅ Audit logging for sensitive actions
- ✅ GDPR data export implemented
- ✅ Right to be forgotten implemented
- ✅ Cookie consent banner
- ✅ Privacy policy published

**Code Quality Standards:**

- ✅ Forms follow `PascalCase` naming
- ✅ Server modules follow `snake_case` naming
- ✅ All functions have docstrings
- ✅ Error handling implemented everywhere
- ✅ No hardcoded credentials (use Anvil Secrets)
- ✅ Package organization follows feature-based structure
- ✅ Documentation updated for new features

---

## 10. Version History

| Version | Date | Changes |
|---------|------|---------|
| v11.0 | Jan 26, 2026 | **M3 Compliance Update**: Updated Section 2.2 Navigation Architecture to NavigationDrawerLayout + NavigationLink pattern. Added Section 2.4 M3 Component Standards (17 essential + 10 good-to-have components). Added Section 2.5 Data Binding System (self.item pattern + write back). Removed all Anvil Extras references. Added M3 theme specification to header. |
| v10.0 | Jan 25, 2026 | Production architecture specification for V1.x (100 clients). Complete system architecture documented. |

---

**END OF ARCHITECTURE SPECIFICATION V11.0**

**Status:** ✅ Active Specification  
**Production Ready:** Yes, for V1.x development  
**M3 Compliant:** ✅ 100% Material Design 3

