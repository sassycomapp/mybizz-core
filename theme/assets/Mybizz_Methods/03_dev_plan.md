# Mybizz V1.x Development Plan

**Version:** 12.0  
**Date:** January 26, 2026  
**App:** Mybizz_core_v1_2_dev → master_template (V1.0)  
**UI Standard:** Material Design 3 (M3) - All forms and components

---

## M3 COMPONENT STANDARDS (APPLY TO ALL FORMS)

**This section defines Material Design 3 component standards for ALL form creation throughout this plan.**

### Essential M3 Components (17 - Always Use)

**Navigation & Layout:**
1. ✅ NavigationDrawerLayout - Admin/customer layouts (8+ destinations)
2. ✅ NavigationLink - Navigation menu items (set navigate_to property, no click handlers)

**Typography:**
3. ✅ Text - Body text, labels (use M3 typography roles: body-medium, label-medium)
4. ✅ Heading - Headers, titles (use M3 typography roles: headline-large, headline-small)

**Buttons:**
5. ✅ Button - All actions (filled role for primary, outlined for secondary, text-button for tertiary)
6. ✅ IconButton - Icon-only actions (edit, delete)

**Form Inputs:**
7. ✅ TextBox - Single-line input (ALWAYS use `outlined` role)
8. ✅ TextArea - Multi-line input (ALWAYS use `outlined` role)
9. ✅ DropdownMenu - Selections (ALWAYS use `outlined` role)
10. ✅ Checkbox - Boolean options
11. ✅ RadioButton - Single selection
12. ✅ DatePicker - Date input (ALWAYS use `outlined` role)
13. ✅ FileLoader - File uploads

**Display:**
14. ✅ Card - Content containers (use `elevated` for metrics/dashboards, `outlined` for forms/lists)

**Containers:**
15. ✅ ColumnPanel - Vertical stacking (main layout structure)
16. ✅ LinearPanel - Horizontal/vertical layouts (headers, action rows)
17. ✅ FlowPanel - Responsive wrapping (tags, chips, metrics)

### Good to Have M3 Components (10)

18. ✅ DataGrid - Tabular data (contact lists, product lists, order lists)
19. ✅ RepeatingPanel - Dynamic lists
20. ✅ Switch - Toggle settings/features
21. ✅ RadioGroupPanel - Grouped radio options
22. ✅ ButtonMenu - Menu attached to button
23. ✅ IconButtonMenu - Actions menu (edit/delete on rows)
24. ✅ AvatarMenu - User profile menu
25. ✅ MenuItem - Menu list items
26. ✅ Divider - Visual separation
27. ✅ Plot - Charts and graphs (Plotly integration)

### Components to AVOID (Never Use)

**Anvil Extras (NOT M3-compliant):**
- ❌ Tabs → Use NavigationLink in sidebar or Card sections
- ❌ Pivot → Use custom DataGrid
- ❌ MultiSelectDropDown → Use DropdownMenu + Chips
- ❌ Autocomplete → Use DropdownMenu with search
- ❌ Quill → Use TextArea
- ❌ Switch (Extras) → Use M3 Switch
- ❌ Slider (Extras) → Use M3 Slider
- ❌ RadioGroup → Use M3 RadioGroupPanel
- ❌ CheckBoxGroup → Use multiple Checkboxes

**Legacy Patterns:**
- ❌ Custom sidebar → Use NavigationDrawerLayout
- ❌ Link + click handlers → Use NavigationLink.navigate_to
- ❌ XYPanel for layout → Use ColumnPanel/LinearPanel
- ❌ Hardcoded colors → Use theme: color roles
- ❌ Generic Label → Use Text/Heading with M3 typography roles

### Form Type Standards

**List Forms (e.g., ContactListForm, ProductListForm, OrderListForm):**
```
Structure:
- NavigationDrawerLayout (AdminLayout or CustomerLayout)
- Heading (headline-large) - Page title
- LinearPanel (horizontal) - Header with filters/search/actions
  - TextBox (outlined) - Search
  - DropdownMenu (outlined) - Status filter
  - Button (filled) - "New" action
- DataGrid - List data
- IconButtonMenu - Row actions (edit, delete)
```

**Editor Forms (e.g., ContactEditorForm, ProductEditorForm):**
```
Structure:
- Card (outlined) - Form container
- Heading (headline-small) - Section headers
- TextBox (outlined) - Single-line inputs
- TextArea (outlined) - Multi-line inputs
- DropdownMenu (outlined) - Selections
- DatePicker (outlined) - Dates
- Checkbox - Boolean flags
- FileLoader - File uploads
- LinearPanel (horizontal) - Action buttons
  - Button (filled) - "Save"
  - Button (outlined) - "Cancel"
```

**Dashboard Forms (e.g., DashboardForm, MarketingDashboardForm):**
```
Structure:
- NavigationDrawerLayout (AdminLayout)
- Heading (headline-large) - Page title
- LinearPanel (horizontal) or FlowPanel - Metrics row
  - Card (elevated) for each metric
    - Heading (headline-small) - Metric label
    - Text (display-medium) - Metric value
    - Text (body-small) - Change indicator
- Plot - Charts/graphs
- DataGrid - Summary tables
- LinearProgressIndicator - Loading states
```

### M3 Typography Roles

**Use on Text/Heading components:**
- `display-large` (57sp) - Hero text
- `display-medium` (45sp) - Large hero
- `display-small` (36sp) - Small hero
- `headline-large` (32sp) - Page titles
- `headline-medium` (28sp) - Section headers
- `headline-small` (24sp) - Card titles
- `title-large` (22sp) - List items
- `title-medium` (16sp) - Card headers
- `title-small` (14sp) - Items
- `body-large` (16sp) - Main content
- `body-medium` (14sp) - Body text (default)
- `body-small` (12sp) - Captions
- `label-large` (14sp) - Buttons
- `label-medium` (12sp) - Chips
- `label-small` (11sp) - Field labels

### M3 Color Roles

**Use theme: prefix for all colors:**
- `theme:Primary` / `theme:On Primary` - Primary actions
- `theme:Secondary` / `theme:On Secondary` - Secondary elements
- `theme:Surface` / `theme:On Surface` - Cards, containers
- `theme:Surface Variant` - Alternate surface
- `theme:Error` / `theme:On Error` - Validation errors
- `theme:Background` / `theme:On Background` - Page background

### Button Hierarchy

**Visual hierarchy communicates importance:**
- Primary action: `filled-button` role (Save, Submit, Confirm)
- Secondary action: `outlined` role (Cancel, Back, Edit)
- Tertiary action: `text-button` role (Learn More, View Details)

### Data Binding Pattern

**Use self.item pattern with write back for ALL editor forms:**

```python
class ContactEditorForm(ContactEditorFormTemplate):
  def __init__(self, contact=None, **properties):
    # Set self.item BEFORE init_components
    self.item = contact or {}
    self.init_components(**properties)
  
  def btn_save_click(self, **event_args):
    # self.item already updated by two-way bindings with write back
    anvil.server.call('save_contact', self.item)
    self.raise_event('x-close')
```

**In Designer:**
- Bind txt_first_name.text → self.item['first_name']
- Toggle **W** (Write Back) ON
- No change event handlers needed!

### Component Naming Conventions

**Essential prefixes:**
- `nav_` - NavigationLink
- `btn_` - Button, IconButton
- `lbl_` - Text, Heading
- `txt_` - TextBox, TextArea
- `dd_` - DropdownMenu
- `cb_` - Checkbox
- `rb_` - RadioButton
- `dp_` - DatePicker
- `fu_` - FileLoader
- `card_` - Card
- `col_` - ColumnPanel
- `lp_` - LinearPanel
- `flow_` - FlowPanel
- `dg_` - DataGrid
- `rp_` - RepeatingPanel
- `sw_` - Switch
- `menu_` - ButtonMenu, IconButtonMenu, AvatarMenu

**When creating forms below, assume all components follow these M3 standards unless explicitly stated otherwise.**

---

## PHASE 1: AUTHENTICATION & ADMINISTRATION

### 1.1: Project Infrastructure

1. Create Anvil app `Mybizz_core_v1_2_dev`
2. Configure app package name as `Mybizz_core`
3. Initialize git repository `Mybizz-master-template`
4. Create packages: `client_code/shared/`, `server_code/shared/`
5. **Add Material Design 3 theme:**
   - Go to Settings → Dependencies → Third Party
   - Add dependency ID: **4UK6WHQ6UX7AKELK** (M3 Theme)
   - Add dependency ID: **3PIDO5P3H4VPEMPL** (Routing - required for NavigationLink.navigate_to)
   - Set M3 as default theme
6. Create `server_code/shared/config.py` with environment configuration
7. Test app launch

### 1.2: Authentication System

1. Enable Anvil Users service
2. Extend users table columns:
   - `role` (text): admin, manager, staff, customer
   - `permissions` (simple object): JSON permissions
   - `status` (text): active, inactive, suspended
   - `last_login` (datetime)
3. Create `client_code/auth/` package
4. **Create `LoginForm` (M3 Components):**
   - Layout: BlankLayout (no navigation)
   - Card (outlined) as form container
   - Heading (headline-large): "Sign In"
   - TextBox (outlined) for email
   - TextBox (outlined, password=True) for password
   - Checkbox: "Remember me"
   - Button (filled): "Sign In"
   - Link: "Forgot password?"
   - M3 error handling with outlined-error role
5. **Create `SignupForm` (M3 Components):**
   - Layout: BlankLayout
   - Card (outlined) as form container
   - Heading (headline-large): "Create Account"
   - TextBox (outlined) for email
   - TextBox (outlined, password=True) for password
   - TextBox (outlined, password=True) for confirm password
   - TextBox (outlined) for business name
   - Checkbox: "I agree to Terms"
   - Button (filled): "Create Account"
   - Link: "Already have an account?"
6. **Create `PasswordResetForm` (M3 Components):**
   - Layout: BlankLayout
   - Card (outlined) as form container
   - Heading (headline-small): "Reset Password"
   - TextBox (outlined) for email
   - Button (filled): "Send Reset Link"
   - M3 error handling
7. Create `server_code/server_auth/` package
8. Create `server_code/server_auth/service.py`:
   ```python
   @anvil.server.callable
   def authenticate_user(email, password)
   
   @anvil.server.callable
   def create_user(email, password, business_name)
   
   @anvil.server.callable
   def reset_password(email)
   
   @anvil.server.callable
   def check_permission(user, permission_name)
   ```
9. Create `server_code/server_auth/rbac.py`:
   - Permission checking functions
   - Role validation
10. Implement startup route logic:
    - If not logged in → LoginForm
    - If logged in → DashboardForm
11. Test complete auth flow

### 1.3: Dashboard & Navigation

1. Create `client_code/dashboard/` package
2. Create `client_code/shared/` package for layouts
3. **Create `AdminLayout` (NavigationDrawerLayout template):**
   - Base template: NavigationDrawerLayoutTemplate (from M3 theme)
   - Add NavigationLink components in Designer (navigation drawer slot):
     - nav_dashboard (text="Dashboard", icon="fa:dashboard", navigate_to="DashboardForm")
     - nav_bookings (text="Bookings", icon="fa:calendar", navigate_to="BookingListForm")
     - nav_products (text="Products", icon="fa:shopping-cart", navigate_to="ProductListForm")
     - nav_contacts (text="Customers", icon="fa:users", navigate_to="ContactListForm")
     - nav_settings (text="Settings", icon="fa:cog", navigate_to="SettingsForm")
     - nav_analytics (text="Analytics", icon="fa:chart-bar", navigate_to="AnalyticsForm")
   - Implement `build_navigation()` method for feature-based visibility
   - NO click handlers on NavigationLinks (navigate_to handles navigation automatically)
4. **Create `CustomerLayout` (NavigationDrawerLayout template):**
   - Base template: NavigationDrawerLayoutTemplate
   - Add NavigationLinks for customer portal:
     - nav_my_dashboard, nav_my_bookings, nav_my_orders, nav_account, nav_logout
   - Implement feature-based visibility
5. **Create `DashboardForm` (M3 Components):**
   - Uses AdminLayout
   - Heading (headline-large): "Dashboard"
   - LinearPanel (horizontal) for metrics row:
     - Card (elevated) for revenue metric
     - Card (elevated) for bookings metric
     - Card (elevated) for customers metric
     - Card (elevated) for orders metric
   - DataGrid for recent activity
   - Card (outlined) for storage usage widget
6. **Dashboard metrics cards use:**
   - Heading (headline-small) for metric label
   - Text (display-medium) for metric value
   - Text (body-small) for change indicator
7. Create `server_code/server_dashboard/` package
8. Create `server_code/server_dashboard/service.py`:
   ```python
   @anvil.server.callable
   def get_dashboard_metrics()
   
   @anvil.server.callable
   def get_recent_activity()
   
   @anvil.server.callable
   def get_storage_usage()
   ```
9. Create `server_code/server_shared/utilities.py`:
    - Date formatting
    - Currency formatting
    - Common validation functions
10. Create `client_code/shared/navigation_helpers.py`:
    ```python
    from anvil import open_form
    import anvil.users
    
    def require_auth():
      user = anvil.users.get_user()
      if not user:
        open_form('LoginForm')
        return None
      return user
    
    def require_admin():
      user = require_auth()
      if not user or user['role'] not in ['owner', 'manager', 'admin']:
        open_form('ErrorForm', error='Access denied')
        return None
      return user
    ```
11. Test dashboard functionality and navigation

### 1.4: Settings & Configuration

1. Create `client_code/settings/` package
2. **Create `SettingsForm` (M3 Components, uses AdminLayout):**
   - NavigationDrawerLayout (AdminLayout)
   - Heading (headline-large): "Settings"
   - Use Card (outlined) containers for each section (not tabs - M3 pattern)
   - Sections stacked vertically in ColumnPanel
3. **Business Profile section (Card outlined):**
   - Heading (headline-small): "Business Profile"
   - TextBox (outlined) for business name
   - FileLoader for logo upload
   - TextBox (outlined) for email, phone
   - TextArea (outlined) for address
   - Button (filled): "Save Changes"
4. **Feature Activation section (Card outlined):**
   - Heading (headline-small): "Features"
   - Switch components for each feature:
     - sw_bookings: "Bookings & Appointments"
     - sw_ecommerce: "Product Sales"
     - sw_memberships: "Memberships"
     - sw_services: "Professional Services"
     - sw_hospitality: "Hospitality Management"
     - sw_blog: "Blog & Content"
   - Button (filled): "Save Features"
5. **Theme Customization section (Card outlined):**
   - Heading (headline-small): "Theme Colors"
   - M3 color picker components
   - Preview Card showing current theme
   - Button (filled): "Save Theme"
6. **Currency Settings section (Card outlined):**
   - Heading (headline-small): "Currency"
   - DropdownMenu (outlined) for system currency
   - Text (body-medium) for description
   - Button (filled): "Save Currency"
7. **Users & Permissions section (Card outlined):**
   - Heading (headline-small): "Team Members"
   - DataGrid for user list
   - Button (filled): "Add User"
   - IconButtonMenu for row actions (edit, delete)
8. Create database tables:
   - `tbl_config` (one row per client):
     - business_name, logo, primary_color, accent_color
     - system_currency, features_enabled (JSON)
   - `tbl_currencies` (lookup table):
     - code, name, symbol
9. Create `server_code/server_settings/` package
10. Create `server_code/server_settings/config_service.py`:
    ```python
    @anvil.server.callable
    def get_config()
    
    @anvil.server.callable
    def update_config(config_data)
    
    @anvil.server.callable
    def create_initial_config(business_name)
    ```
11. Call `create_initial_config()` during signup
12. Test settings functionality

### 1.5: Navigation & Layout System (M3 Compliant)

**Purpose:** Implement Material Design 3 navigation using NavigationDrawerLayout + NavigationLink  
**Build Time:** 6-8 hours

#### Layout Forms

Create 4 Layout Forms:
1. **AdminLayout** - NavigationDrawerLayout template (20+ destinations)
2. **CustomerLayout** - NavigationDrawerLayout template (9 destinations)
3. **BlankLayout** - No layout (Login, signup, password reset)
4. **ErrorLayout** - Minimal layout (error pages)

#### AdminLayout Implementation (M3)

**Base Template:** NavigationDrawerLayoutTemplate (from M3 theme)

**NavigationLink Components (in Designer):**

**UX Best Practice:** Use visual grouping with Divider components between sections. M3 recommends grouping for 7+ destinations to reduce cognitive load and improve navigation clarity.

Create NavigationLink components with Dividers for grouping:

```
Dashboard Group:
- nav_dashboard (text="Dashboard", icon="fa:dashboard", navigate_to="DashboardForm")

[Divider component - label="Sales & Operations"]

Sales & Operations Group:
- nav_bookings (text="Bookings", icon="fa:calendar", navigate_to="BookingListForm")
- nav_products (text="Products", icon="fa:shopping-cart", navigate_to="ProductListForm")
- nav_orders (text="Orders", icon="fa:receipt", navigate_to="OrderListForm")
- nav_rooms (text="Rooms", icon="fa:bed", navigate_to="RoomListForm")
- nav_services (text="Services", icon="fa:briefcase", navigate_to="ServiceListForm")
- nav_memberships (text="Memberships", icon="fa:id-card", navigate_to="MembershipListForm")

[Divider component - label="Customers & Marketing"]

Customers & Marketing Group:
- nav_contacts (text="Customers", icon="fa:users", navigate_to="ContactListForm")
- nav_campaigns (text="Campaigns", icon="fa:bullhorn", navigate_to="EmailCampaignListForm")
- nav_broadcasts (text="Broadcasts", icon="fa:envelope", navigate_to="EmailBroadcastForm")
- nav_segments (text="Segments", icon="fa:filter", navigate_to="SegmentManagerForm")
- nav_tasks (text="Tasks", icon="fa:tasks", navigate_to="TaskListForm")

[Divider component - label="Content & Website"]

Content & Website Group:
- nav_blog (text="Blog", icon="fa:rss", navigate_to="BlogListForm")
- nav_pages (text="Pages", icon="fa:file", navigate_to="PageListForm")
- nav_media (text="Media", icon="fa:image", navigate_to="MediaLibraryForm")

[Divider component - label="Finance & Reports"]

Finance & Reports Group:
- nav_invoices (text="Invoices", icon="fa:file-invoice", navigate_to="InvoiceListForm")
- nav_payments (text="Payments", icon="fa:credit-card", navigate_to="PaymentListForm")
- nav_reports (text="Reports", icon="fa:chart-line", navigate_to="ReportsForm")
- nav_analytics (text="Analytics", icon="fa:chart-bar", navigate_to="AnalyticsForm")

[Divider component - label="Settings"]

Settings:
- nav_settings (text="Settings", icon="fa:cog", navigate_to="SettingsForm")
```

**Implementation Notes:**
- Dividers create visual separation between groups
- Optional label on Divider for group heading (e.g., "Sales & Operations")
- Improves scanability for 20+ navigation items
- Semantic grouping makes navigation intuitive
- Feature visibility still controlled in `build_navigation()` method

**Code Implementation (feature-based visibility):**
```python
from m3.components import NavigationLink

class AdminLayout(NavigationDrawerLayoutTemplate):
  def __init__(self, **properties):
    # Initialize M3 NavigationDrawerLayout
    self.init_components(**properties)
    self.build_navigation()
  
  def build_navigation(self):
    """Configure NavigationLink visibility based on features"""
    config = anvil.server.call('get_config')
    features = config['features']
    
    # Always visible
    self.nav_dashboard.visible = True
    self.nav_contacts.visible = True
    self.nav_pages.visible = True
    self.nav_media.visible = True
    self.nav_invoices.visible = True
    self.nav_payments.visible = True
    self.nav_reports.visible = True
    self.nav_analytics.visible = True
    self.nav_settings.visible = True
    
    # Feature-based visibility (Sales & Operations)
    self.nav_bookings.visible = features.get('bookings_enabled', False)
    self.nav_products.visible = features.get('ecommerce_enabled', False)
    self.nav_orders.visible = features.get('ecommerce_enabled', False)
    self.nav_rooms.visible = features.get('hospitality_enabled', False)
    self.nav_services.visible = features.get('services_enabled', False)
    self.nav_memberships.visible = features.get('memberships_enabled', False)
    
    # Feature-based visibility (Customers & Marketing)
    self.nav_campaigns.visible = features.get('marketing_enabled', False)
    self.nav_broadcasts.visible = features.get('marketing_enabled', False)
    self.nav_segments.visible = features.get('marketing_enabled', False)
    self.nav_tasks.visible = features.get('marketing_enabled', False)
    
    # Feature-based visibility (Content & Website)
    self.nav_blog.visible = features.get('blog_enabled', False)
```

**CRITICAL:** No click handlers on NavigationLinks - the `navigate_to` property handles navigation automatically when set in Designer.

#### CustomerLayout Implementation (M3)

**Base Template:** NavigationDrawerLayoutTemplate

**NavigationLink Components:**
```
- nav_my_dashboard (text="My Dashboard", icon="fa:home", navigate_to="CustomerDashboardForm")
- nav_my_bookings (text="My Bookings", icon="fa:calendar", navigate_to="CustomerBookingListForm")
- nav_my_orders (text="My Orders", icon="fa:shopping-bag", navigate_to="CustomerOrderListForm")
- nav_my_membership (text="My Membership", icon="fa:id-card", navigate_to="CustomerMembershipForm")
- nav_payment_methods (text="Payment Methods", icon="fa:credit-card", navigate_to="PaymentMethodsForm")
- nav_invoices (text="Invoices", icon="fa:file-invoice", navigate_to="CustomerInvoiceListForm")
- nav_my_reviews (text="My Reviews", icon="fa:star", navigate_to="CustomerReviewsForm")
- nav_support (text="Support", icon="fa:life-ring", navigate_to="SupportTicketsForm")
- nav_account (text="Account", icon="fa:user", navigate_to="AccountSettingsForm")
```

**Code Implementation:**
```python
class CustomerLayout(NavigationDrawerLayoutTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.build_navigation()
  
  def build_navigation(self):
    """Configure customer portal navigation"""
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

#### Navigation Helpers

Create `client_code/shared/navigation_helpers.py`:
```python
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
```

#### Mobile Responsiveness

NavigationDrawerLayout automatically handles mobile:
- **Desktop/Tablet:** Navigation drawer visible as persistent sidebar
- **Mobile:** Navigation drawer collapses to modal overlay (hamburger menu)
- **No code required** - M3 theme handles responsive behavior automatically

---

## PHASE 2: WEBSITE & CONTENT

### 2.1: Public Website - Standard Pages

#### 2.1.1: Home Page

1. Create `client_code/public/` package
2. Create `HomePageForm`:
   - Hero section
   - Features grid
   - Services showcase (if enabled)
   - Testimonials
   - CTA section
3. Make home page template-driven (7 templates available)
4. Create `server_code/server_website/` package
5. Create `server_code/server_website/home_service.py`:
   ```python
   @anvil.server.callable
   def get_home_config()
   
   @anvil.server.callable
   def save_home_config(config_data)
   ```
6. Test home page rendering

#### 2.1.2: About Page

1. Create `AboutPageForm`:
   - Business story section
   - Team section
   - Values/mission section
2. Create `AboutPageEditorForm` (Admin):
   - Rich text editor for story
   - Team member management
   - Save functionality
3. Add `about_page` to `tbl_config`
4. Test about page

#### 2.1.3: Contact Page

1. Create `ContactPageForm`:
   - Contact form
   - Business contact info
   - Map (optional)
   - Social media links
2. Create contact form fields:
   - Name, Email, Phone, Message
   - Submit button
3. Create `tbl_contact_submissions`:
   - name, email, phone, message
   - submitted_date, status
   - client_id
4. Create server functions:
   ```python
   @anvil.server.callable
   def submit_contact_form(form_data)
   
   @anvil.server.callable
   def get_contact_submissions(status=None)
   ```
5. Email notification to business owner on submission
6. Test contact form flow

#### 2.1.4: Privacy Policy & Terms Pages

1. Create `PrivacyPolicyPage` and `TermsConditionsPage`
2. Create admin editors with rich text
3. Provide default templates
4. Add to `tbl_config`:
   - `privacy_policy`, `privacy_policy_updated`
   - `terms_conditions`, `terms_conditions_updated`
5. Test legal pages

### 2.2: Website - Home Page Templates

**7 Professional Templates:**
1. Classic Business - General professional layout
2. E-commerce Focus - Product showcase
3. Hospitality - Location and amenities focused
4. Services - Process and benefits highlighted
5. Membership - Community and tiers emphasized
6. Booking - Calendar and availability featured
7. Minimalist - Clean, text-focused design

**Implementation:**
- Template selection in admin settings
- Same data, different presentation
- All templates support all features (just styled differently)

### 2.3: Landing Pages System

**5 Landing Page Templates:**
1. Lead Capture - Email collection
2. Product Launch - Single product focus
3. Event Registration - Workshop/webinar signups
4. Video Sales Letter (VSL) - Video-first conversion
5. Membership Funnel - Tier selection

**Database:**
- `tbl_landing_pages`:
  - title, slug, template_type, config
  - status (draft/published), views_count, conversions_count

**Features:**
- Drag-and-drop builder (future)
- Template-based creation (V1.x)
- Analytics (views, conversions, conversion rate)
- Lead capture integration with CRM

### 2.4: Blog System

1. Create `client_code/blog/` package
2. Create `BlogListForm` - Public blog listing
3. Create `BlogPostForm` - Individual post view
4. Create `BlogEditorForm` (Admin):
   - Rich text editor
   - Title, excerpt, featured image
   - Categories, tags
   - SEO fields (meta title, description)
   - Publish/draft status
5. Create `tbl_blog_posts`:
   - title, slug, content
   - excerpt, featured_image
   - author, published_date, status
   - categories, tags
   - views_count
6. Create `server_code/server_blog/` package
7. Create `server_code/server_blog/blog_service.py`:
   ```python
   @anvil.server.callable
   def get_published_posts(page=1, page_size=10)
   
   @anvil.server.callable
   def get_post_by_slug(slug)
   
   @anvil.server.callable
   def create_post(post_data)
   
   @anvil.server.callable
   def update_post(post_id, post_data)
   ```
8. Test blog functionality

---

## PHASE 3: PAYMENTS & E-COMMERCE

### 3.1: Payment Gateway Integration

**Dual Gateway Support:**
- Stripe (global payments)
- Paystack (Africa-optimized)

**Client selects ONE gateway in settings**

#### Stripe Integration

1. Enable Anvil's Stripe integration
2. Create `server_code/server_payments/stripe_service.py`:
   ```python
   @anvil.server.callable
   def create_stripe_payment_intent(amount, currency)
   
   @anvil.server.callable
   def create_stripe_subscription(customer_id, price_id)
   
   @anvil.server.callable
   def handle_stripe_webhook(event_data)
   ```
3. Webhook handling for payment events
4. Test Stripe payments

#### Paystack Integration

1. Add Paystack API credentials to Secrets
2. Create `server_code/server_payments/paystack_service.py`:
   ```python
   @anvil.server.callable
   def initialize_paystack_payment(amount, email)
   
   @anvil.server.callable
   def verify_paystack_payment(reference)
   
   @anvil.server.callable
   def handle_paystack_webhook(event_data)
   ```
3. Webhook handling
4. Test Paystack payments

### 3.2: Product Catalog

1. Create `client_code/products/` package
2. Create `ProductListForm` - Public product listing
3. Create `ProductDetailForm` - Product details
4. Create `ProductEditorForm` (Admin):
   - Product name, description
   - Price, compare_at_price
   - Images (multiple)
   - Inventory tracking
   - Categories, tags
   - Variants (size, color, etc.)
5. Create `tbl_products`:
   - name, description, price, compare_at_price
   - images, inventory_count, track_inventory
   - categories, tags
   - variants (JSON), status
6. Create `server_code/server_products/` package
7. Create `server_code/server_products/product_service.py`:
   ```python
   @anvil.server.callable
   def get_products(category=None, tag=None)
   
   @anvil.server.callable
   def get_product_by_id(product_id)
   
   @anvil.server.callable
   def create_product(product_data)
   
   @anvil.server.callable
   def update_inventory(product_id, quantity_change)
   ```
8. Test product catalog

### 3.3: Shopping Cart & Checkout

1. Create `ShoppingCartForm`:
   - Cart items list
   - Quantity adjustments
   - Remove items
   - Subtotal calculation
   - Checkout button
2. Implement cart state management:
   - Client-side cart storage (session)
   - Server-side validation
3. Create `CheckoutForm`:
   - Customer details
   - Shipping address (if applicable)
   - Payment method selection
   - Order summary
   - Payment processing
4. Create `tbl_orders`:
   - customer_id, order_number
   - items (JSON), subtotal, tax, shipping, total
   - payment_method, payment_status
   - shipping_address, shipping_status
   - created_date, completed_date
5. Create `server_code/server_products/order_service.py`:
   ```python
   @anvil.server.callable
   def create_order(order_data)
   
   @anvil.server.callable
   def process_payment(order_id, payment_method)
   
   @anvil.server.callable
   def get_order_by_id(order_id)
   ```
6. Test complete checkout flow

### 3.4: Invoicing System

1. Create `InvoiceListForm` (Admin)
2. Create `InvoiceDetailForm` (Admin + Customer)
3. Create `InvoiceEditorForm` (Admin):
   - Customer selection
   - Line items
   - Tax, discount
   - Payment terms
4. Create `tbl_invoices`:
   - invoice_number, customer_id
   - line_items (JSON), subtotal, tax, discount, total
   - issue_date, due_date, paid_date
   - status (draft/sent/paid/overdue)
   - payment_method
5. Create `server_code/server_invoices/` package
6. Create PDF generation for invoices
7. Email invoices to customers
8. Test invoicing system

---

## PHASE 4: BOOKINGS & APPOINTMENTS

### 4.1: Calendar System

1. Create `client_code/bookings/` package
2. Create `BookingCalendarForm`:
   - Month/week/day views
   - Availability display
   - Click to book
3. Use calendar component (Anvil or third-party)
4. Create `tbl_bookings`:
   - customer_id, service_id
   - start_datetime, end_datetime, duration
   - status (pending/confirmed/cancelled/completed)
   - notes, total_amount, payment_status
5. Create `server_code/server_bookings/` package
6. Test calendar display

### 4.2: Availability Management

1. Create `AvailabilitySettingsForm` (Admin):
   - Business hours by day
   - Blocked dates
   - Service-specific availability
2. Create `tbl_availability`:
   - day_of_week, start_time, end_time
   - service_id (optional)
   - is_available
3. Create `tbl_blocked_dates`:
   - date, reason
   - all_day, start_time, end_time
4. Availability calculation logic:
   ```python
   @anvil.server.callable
   def get_available_slots(date, service_id)
   
   @anvil.server.callable
   def check_slot_available(datetime, service_id)
   ```
5. Test availability system

### 4.3: Booking Creation Flow

1. Create `BookingForm` (Public):
   - Service selection
   - Date/time selection
   - Customer details
   - Payment (if required)
2. Create booking confirmation email
3. Admin booking management:
   - Manual booking creation
   - Booking editing
   - Status updates
4. Create server functions:
   ```python
   @anvil.server.callable
   def create_booking(booking_data)
   
   @anvil.server.callable
   def update_booking_status(booking_id, status)
   
   @anvil.server.callable
   def get_upcoming_bookings()
   ```
5. Test booking flow end-to-end

### 4.4: Services Management

1. Create `ServiceListForm` (Admin)
2. Create `ServiceEditorForm` (Admin):
   - Service name, description
   - Duration, price
   - Category
   - Availability settings
3. Create `tbl_services`:
   - name, description
   - duration (minutes), price
   - category
   - availability_settings (JSON)
4. Display services on public site
5. Test service management

---

## PHASE 5: CRM & MARKETING

### 5.1: Contact Management

1. Create `client_code/customers/` package
2. Create `ContactListForm`:
   - Searchable contact list
   - Filters (status, segment)
   - Import/export
3. Create `ContactDetailForm`:
   - Contact information
   - Activity timeline
   - Notes section
   - Tag management
4. Create `tbl_contacts`:
   - first_name, last_name, email, phone
   - company, address
   - status (lead/customer/inactive)
   - source, tags
   - total_spent, total_transactions
   - lifecycle_stage
   - last_contact_date
5. Create `tbl_contact_events`:
   - contact_id, event_type, event_date
   - description, metadata (JSON)
6. Create `server_code/server_customers/contact_service.py`:
   ```python
   @anvil.server.callable
   def get_all_contacts(filters)
   
   @anvil.server.callable
   def get_contact_detail(contact_id)
   
   @anvil.server.callable
   def create_contact(contact_data)
   
   @anvil.server.callable
   def update_contact_from_transaction(email, transaction_data)
   ```
7. Test CRM functionality

### 5.2: Email Marketing (Brevo Integration)

1. Add Brevo API credentials to Secrets
2. Create `client_code/marketing/` package
3. Create `EmailCampaignListForm`
4. Create `EmailCampaignEditorForm`:
   - Campaign name
   - Email sequence builder
   - Trigger conditions
   - Target segment
5. Create `tbl_email_campaigns`:
   - campaign_name, campaign_type
   - sequence_emails (JSON)
   - trigger_type, target_segment
   - status (active/paused)
6. Create `tbl_contact_campaigns`:
   - contact_id, campaign_id
   - sequence_day, status
   - enrolled_date
7. Create `server_code/server_marketing/campaign_service.py`:
   ```python
   @anvil.server.callable
   def create_campaign(campaign_data)
   
   @anvil.server.callable
   def enroll_contact_in_campaign(contact_id, campaign_id)
   
   @anvil.server.background_task
   def process_email_campaigns()  # Hourly
   ```
8. Brevo API integration:
   ```python
   def send_campaign_email(contact, campaign, sequence_day)
   ```
9. Test email campaigns

### 5.3: Segmentation

1. Create `SegmentManagerForm`:
   - Pre-built segments
   - Custom segment builder
2. Pre-built segments:
   - VIP customers
   - Repeat buyers
   - Inactive contacts
   - Upcoming guests
3. Create `tbl_segments`:
   - segment_name, segment_type
   - filter_criteria (JSON)
   - contact_count (cached)
4. Real-time segment calculation
5. Test segmentation

### 5.4: Task Automation

1. Create `TaskListForm`:
   - Task list by status
   - Due date sorting
   - Assignment
2. Create `tbl_tasks`:
   - contact_id, task_title, task_type
   - due_date, completed_date, completed_by
   - status (pending/completed)
   - auto_generated (boolean)
3. Auto-task generation:
   ```python
   @anvil.server.background_task
   def create_automated_tasks():  # Daily 3am
       # Check upcoming bookings (7 days out)
       # Generate arrival instruction tasks
       # Generate review request tasks
   ```
4. Test task system

---

## PHASE 6: SHIPPING & LOGISTICS

### 6.1: Shipping Methods

**3 Shipping Options:**
1. Manual Shipping - Business handles directly
2. Bob Go (South Africa) - API integration
3. Easyship (International) - API integration

1. Create `ShippingSettingsForm`:
   - Shipping method selection
   - API credentials
   - Rate calculation settings
2. Create `tbl_shipping_methods`:
   - method_name, method_type
   - enabled, settings (JSON)
   - rate_type (flat/calculated)
3. Manual shipping configuration:
   - Flat rates by region
   - Free shipping threshold
4. Test shipping settings

### 6.2: Bob Go Integration

1. Add Bob Go API credentials to Secrets
2. Create `server_code/server_shipping/bobgo_service.py`:
   ```python
   @anvil.server.callable
   def get_bobgo_rates(origin, destination, weight)
   
   @anvil.server.callable
   def create_bobgo_shipment(order_id)
   
   @anvil.server.callable
   def track_bobgo_shipment(tracking_number)
   ```
3. Webhook handling for tracking updates
4. Test Bob Go integration

### 6.3: Easyship Integration

1. Add Easyship API credentials to Secrets
2. Create `server_code/server_shipping/easyship_service.py`:
   ```python
   @anvil.server.callable
   def get_easyship_rates(order_data)
   
   @anvil.server.callable
   def create_easyship_shipment(order_id, courier_id)
   
   @anvil.server.callable
   def track_easyship_shipment(tracking_number)
   ```
3. Test Easyship integration

### 6.4: Order Fulfillment

1. Create `OrderFulfillmentForm`:
   - Orders awaiting shipment
   - Packing list generation
   - Shipping label generation
   - Mark as shipped
2. Update order shipping status
3. Send shipping confirmation emails
4. Test fulfillment workflow

---

## PHASE 6.5: SECURITY & COMPLIANCE

### 6.5.1: Enhanced RBAC

1. Implement permission decorators:
   ```python
   @require_role(['owner', 'manager'])
   @require_permission('bookings.manage')
   def create_booking(booking_data):
   ```
2. Granular permissions:
   - `bookings.view`, `bookings.manage`
   - `products.view`, `products.manage`
   - `customers.view`, `customers.manage`
   - `settings.view`, `settings.manage`
3. Test all permission levels

### 6.5.2: Data Encryption

1. Implement encryption for sensitive data:
   - Payment tokens
   - API keys
   - Customer PII
2. Create `server_code/server_shared/encryption.py`:
   ```python
   def encrypt(data)
   def decrypt(data)
   ```
3. Test encryption/decryption

### 6.5.3: Audit Logging

1. Create `tbl_audit_log`:
   - user_id, action, entity_type, entity_id
   - changes (JSON), timestamp
2. Log sensitive actions:
   - User changes
   - Permission changes
   - Data deletions
   - Payment processing
3. Create audit log viewer (admin only)
4. Test audit logging

### 6.5.4: GDPR/POPIA Compliance

1. Data export functionality:
   ```python
   @anvil.server.callable
   def export_customer_data(customer_id)
   ```
2. Right to be forgotten:
   ```python
   @anvil.server.callable
   def delete_customer_data(customer_id)
   ```
3. Cookie consent banner
4. Privacy policy integration
5. Test compliance features

---

## PHASE 7: ANALYTICS & REPORTING

### 7.1: Dashboard Analytics

1. Create `AnalyticsDashboardForm`:
   - Revenue metrics
   - Booking metrics
   - Customer metrics
   - Product metrics
2. Date range selector
3. Export reports to PDF/CSV
4. Test analytics display

### 7.2: Revenue Reporting

1. Create `RevenueReportForm`:
   - Revenue by day/week/month
   - Revenue by product
   - Revenue by service
   - Revenue by payment method
2. Create server functions:
   ```python
   @anvil.server.callable
   def get_revenue_report(date_range, group_by)
   ```
3. Charts and visualizations
4. Test revenue reports

### 7.3: Customer Analytics

1. Create `CustomerAnalyticsForm`:
   - Customer lifetime value
   - Customer acquisition by source
   - Customer retention rate
   - Repeat purchase rate
2. Customer segmentation analysis
3. Test customer analytics

### 7.4: Inventory Reporting

1. Create `InventoryReportForm`:
   - Stock levels
   - Low stock alerts
   - Product performance
   - Sales velocity
2. Test inventory reports

---

## PHASE 8: VERTICAL OPTIMIZATION

### 8.1: Hospitality Vertical

**Specific Features:**
1. Room management
2. Check-in/check-out tracking
3. Housekeeping status
4. Guest messaging
5. Amenities showcase

**Database:**
- `tbl_rooms`: room_number, room_type, capacity, amenities, base_price

### 8.2: Services Vertical

**Specific Features:**
1. Service packages
2. Staff scheduling
3. Appointment reminders
4. Client history

**Database:**
- `tbl_service_packages`: package_name, included_services, discount

### 8.3: E-commerce Vertical

**Specific Features:**
1. Product variations
2. Bulk pricing
3. Related products
4. Abandoned cart recovery

### 8.4: Membership Vertical

**Specific Features:**
1. Membership tiers
2. Access control
3. Member benefits
4. Renewal management

**Database:**
- `tbl_membership_tiers`: tier_name, price, benefits, duration

---

## PHASE 9: PLATFORM MANAGEMENT

### 9.1: Client Provisioning

1. Create `Mybizz_management` app (separate from master_template)
2. Create `ClientOnboardingForm`:
   - Business details input
   - Pricing tier selection
   - Create client button
3. Implement automated client app creation:
   ```python
   @anvil.server.callable
   def provision_client_app(business_name, owner_email)
   ```
   Steps:
   - Clone master_template
   - Rename app
   - Create owner user
   - Initialize config
4. Create onboarding checklist
5. Test provisioning process

### 9.2: Client Monitoring

1. Create monitoring dashboard:
   - Active clients count
   - Revenue this month
   - Client health scores
   - Alerts/issues
2. Implement client health scoring
3. Create alerts system
4. Revenue aggregation (MRR)
5. Test monitoring

### 9.3: Update Distribution

1. Create `tbl_master_template_versions`:
   - version_number, release_date, release_notes
   - published_url
2. Update notification system
3. Track client update status
4. Create release notes page
5. Test update distribution

### 9.4: Billing Automation

1. Stripe subscription management
2. Failed payment handling
3. Grace period logic
4. Account suspension
5. Test billing automation

---

## PHASE 10: LAUNCH PREPARATION

### 10.1: Comprehensive Testing

1. Test authentication flows
2. Test all 4 verticals end-to-end
3. Test payment flows (Stripe, Paystack)
4. Test email system
5. Test security features
6. Mobile responsiveness testing
7. Browser compatibility testing

### 10.2: Documentation

1. Create user documentation:
   - Getting started guide
   - Feature guides
   - FAQ
2. Create video tutorials:
   - Platform overview (5 min)
   - Creating first booking (3 min)
   - Setting up payments (5 min)
3. Create onboarding checklist

### 10.3: Production Launch

1. Publish `master_template` V1.0
2. Set up production environment
3. Configure production API keys
4. Onboard first beta client
5. Set up analytics & monitoring
6. Launch marketing website
7. Activate beta pricing ($25/month for first 50 clients)
8. Begin beta client acquisition
9. Set up support channels

---

## COMPLETION CRITERIA

**Phase 1:** Authentication, dashboard, settings functional  
**Phase 2:** Public website with blog live  
**Phase 3:** Payment processing and e-commerce working  
**Phase 4:** Booking system operational  
**Phase 5:** CRM and email marketing integrated  
**Phase 6:** Shipping and fulfillment configured  
**Phase 6.5:** Security and compliance implemented  
**Phase 7:** Analytics and reporting available  
**Phase 8:** All 4 verticals polished  
**Phase 9:** Client provisioning automated  
**Phase 10:** Platform launched with first clients

---

## VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| v12.0 | Jan 26, 2026 | **M3 Compliance Update**: Added comprehensive M3 Component Standards section at document beginning (applies to all 39 form creation tasks). Updated Phase 1 for NavigationDrawerLayout + NavigationLink pattern. Updated authentication forms, dashboard, and settings to M3 components. All form specifications now inherit M3 standards. |
| v11.0 | Jan 25, 2026 | Production development plan for V1.x (100 clients). 10 phases with detailed implementation tasks. |

---

**END OF DEVELOPMENT PLAN - V12.0 (M3 COMPLIANT)**
