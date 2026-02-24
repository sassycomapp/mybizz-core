---
description: "02_dev_policy.md - Mybizz Development policy"
globs: ["**/*"]
alwaysApply: true
---


# Mybizz Development Policy

**Document Version:** 6.0  
**Date:** February 05, 2026  
**Status:** Active Policy  
**Applicability:** All Mybizz V1.x development work  
**UI Compliance:** Material Design 3 (Mandatory)

---

## Core Principle: Anvil-First Development

**Policy Statement:** All development MUST comply 100% with Anvil's best practices and methodologies. We are building on the Material 3 Design theme, using the M3 Dependency (4UK6WHQ6UX7AKELK) all our work must strictly adhere to these principles

**Governing Mandate:**
> Mybizz is an Anvil application. Use Anvil methods, components, services, and patterns wherever possible. Custom solutions are justified ONLY when Anvil lacks native capability and when they are specifically approved by the human developer

**Mybizz V1.x Architecture:**
- **Single master_template app** containing all features (not modular apps)
- **Anvil package system** for organization (client_code/, server_code/)
- **Open Verticals architecture** - all features available to all clients
- **Maximum 100 clients** for V1.x
- **Published dependency model** - client instances depend on master_template

### 1.1 Anvil Native Solutions First

**Before implementing any feature:**
1. 
2. ✅ Check Anvil's built-in components and services
3. ✅ Review Anvil documentation for native solutions
4. ✅ Examine Anvil's example apps for patterns
5. ✅ Consult Anvil community forum for established approaches
6. ⚠️ Only then consider custom implementation

**Resources to check FIRST:**
- Anvil Documentation: https://anvil.works/docs
- Anvil's M3 Standard: https://anvil.works/docs/ui/app-themes/material-3
- Anvil API Reference: https://anvil.works/docs/api
- Anvil HTTP APIs: https://anvil.works/docs/http-apis
- Example Apps: https://anvil.works/learn/tutorials
- Community Forum: https://anvil.works/forum
- Anvil Codes of Practice: "C:\_Data\MyBizz\mybizz-core\theme\assets\dev-docs\Anvil_Methods"

### 1.2 Anvil Built-In Services

**Always prefer Anvil's integrated services:**

**Data Management:**
- ✅ Data Tables (not external databases)
- ✅ Data Files (for static assets)
- ✅ Media objects (for binary data)

**Authentication & Users:**
- ✅ Anvil Users service
- ✅ Built-in login forms
- ✅ MFA support where available
- ✅ Anvil's permission system for RBAC

**Integrations:**
- ✅ Anvil's Google integration
- ✅ Anvil's Stripe integration
- ✅ Anvil's email service (for system emails)
- ✅ Built-in HTTP API system

**Routing:**
- ✅ Anvil's built-in routing system (`@anvil.server.route`)
- ✅ URL hash navigation
- ❌ External routing libraries

**Deployment:**
- ✅ Anvil's hosting service
- ✅ Custom domains via Anvil
- ✅ Environment management

### 1.3 Custom Code Justification

**If custom implementation is considered:**

**MUST document:**
1. Why Anvil's native solution is insufficient
2. What specific limitation is being addressed
3. How the custom solution maintains Anvil compatibility
4. Future migration path if Anvil adds native support

**External Libraries Policy:**
- ✅ Use Anvil-native dependencies via Anvil's dependency management
- ✅ Use JavaScript libraries via `anvil.js` when Anvil lacks feature
- ⚠️ Avoid Python packages that conflict with Anvil's environment
- ❌ Never circumvent Anvil's security model
- ❌ Never use packages that require system-level access

**When in doubt:** Ask on Anvil Forum before implementing custom solution

### 1.4 Navigation Standards

**Policy Statement:** Use M3 NavigationLink for internal navigation, Routing for public pages.

**Mybizz uses two navigation systems:**
1. **M3 NavigationLink** - Internal SPA navigation (authenticated admin/customer areas)
2. **Routing Dependency (3PIDO5P3H4VPEMPL)** - URL-based navigation (public pages, shareable content)

**Reference:** Docs/Anvil_Methods/anvil_cop_m3_navigation_routing.md

### Internal Navigation (M3 NavigationLink)

**Use for:** Admin/customer authenticated areas where URLs are not needed

```python
# AdminLayout (NavigationDrawerLayout)
class AdminLayout(NavigationDrawerLayoutTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.build_navigation()
    
    def build_navigation(self):
        # Set navigate_to property (NO click handlers)
        self.nav_dashboard.navigate_to = 'DashboardForm'
        self.nav_bookings.navigate_to = 'BookingListForm'
        
        # Feature-based visibility
        features = anvil.server.call('get_features')
        self.nav_bookings.visible = features.get('bookings_enabled')
```

**NavigationLink Standards:**
- **Always** set `navigate_to` property in Designer or `__init__`
- **Never** use click handlers when `navigate_to` is set
- Use `nav_` prefix for all NavigationLinks
- Selected state auto-managed by NavigationDrawerLayout

### Public Navigation (Routing)

**Use for:** Public pages, shareable URLs, bookmarkable content, SEO

**Routing Dependency:** 3PIDO5P3H4VPEMPL

```python
from routing import router

# Static route
@router.route("/")
class HomePage(HomePageTemplate):
    def __init__(self, routing_context, **properties):
        self.init_components(**properties)

# Route with parameters
@router.route("/products/:id")
class ProductDetail(ProductDetailTemplate):
    def __init__(self, routing_context, **properties):
        self.product_id = routing_context.params['id']
        self.init_components(**properties)
```

### Mybizz Navigation Architecture

**Admin/Customer Areas (M3 NavigationLink):**
```
AdminLayout (NavigationDrawerLayout)
├─ nav_dashboard → DashboardForm
├─ nav_bookings → BookingListForm (if enabled)
├─ nav_products → ProductListForm (if enabled)
├─ nav_contacts → ContactListForm
└─ nav_settings → SettingsForm
```

**Public Pages (Routing):**
```
Routes:
/                → HomePage
/products        → ProductCatalog
/products/:id    → ProductDetail
/booking         → BookingForm
/blog            → BlogList
/blog/:slug      → BlogPost
/contact         → ContactForm
```

### Authentication Pattern

```python
# Public login (routed)
@router.route("/login")
class LoginForm(LoginFormTemplate):
    def btn_login_click(self, **event_args):
        user = anvil.users.login_with_form()
        if user:
            open_form('AdminLayout')  # Switch to M3 navigation

# Admin layout (M3 NavigationLink)
class AdminLayout(NavigationDrawerLayoutTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        if not anvil.users.get_user():
            navigate(path="/login")
        self.nav_dashboard.navigate_to = 'DashboardForm'
```

### Decision Matrix

| Requirement | Solution |
|-------------|----------|
| Admin navigation | M3 NavigationLink |
| Customer portal navigation | M3 NavigationLink |
| Shareable product URLs | Routing |
| Bookmarkable blog posts | Routing |
| Browser back/forward support | Routing |
| Public pages (SEO) | Routing |
| Feature flag visibility | M3 NavigationLink |

### Anti-Patterns

**❌ Don't use NavigationLink click handlers:**
```python
# ❌ WRONG
self.nav_dashboard.navigate_to = 'DashboardForm'
def nav_dashboard_click(self, **event_args):
    open_form('DashboardForm')

# ✅ RIGHT
self.nav_dashboard.navigate_to = 'DashboardForm'
```

**❌ Don't use Routing for admin areas:**
```python
# ❌ WRONG: Routing in admin
@router.route("/admin/dashboard")
class DashboardForm...

# ✅ RIGHT: M3 NavigationLink
self.nav_dashboard.navigate_to = 'DashboardForm'
```

**❌ Don't use NavigationLink for public pages:**
```python
# ❌ WRONG: No shareable URL
self.nav_products.navigate_to = 'ProductCatalog'

# ✅ RIGHT: Routed public page
@router.route("/products")
class ProductCatalog...
```

### 1.5 Anvil Development Workflow

**Development Environment:**
- ✅ Use Anvil's browser-based IDE for all development
- ✅ Test in Anvil's built-in environment first
- ✅ Use Anvil's version control (Git integration)
- ✅ Use Anvil's app cloning for staging environments

**Component Creation Priority:**
1. Check Anvil's built-in components first (Button, TextBox, DataGrid, etc.)
2. Check Anvil Extras library second (additional community components)
3. Create custom component only if 1 & 2 insufficient

**Data Operations:**
- ✅ Use Anvil Data Tables for all persistent data
- ✅ Use Anvil's query syntax (`app_tables.table_name.search()`)
- ✅ Use Anvil's relationships and links between tables
- ❌ Never use external databases for client data (unless justified)

**Forms and UI:**
- ✅ Use Anvil's drag-and-drop form designer
- ✅ Use Anvil's Material Design theme system
- ✅ Use Anvil's responsive design features
- ⚠️ Custom HTML/CSS only when Anvil's designer insufficient

**Server Functions:**
- ✅ All business logic in `@anvil.server.callable` functions
- ✅ Use `@anvil.server.background_task` for long operations
- ✅ Use Anvil's built-in session management
- ❌ Never expose database directly to client code

**Deployment:**
- ✅ Use Anvil's built-in hosting (anvil.app domain or custom)
- ✅ Use Anvil's environment management for secrets
- ✅ Use Anvil's app cloning for test/staging
- ❌ Never deploy Anvil apps to external hosting

---

## 1.2 Material Design 3 Compliance (Mandatory)

**Policy Statement:** All UI development MUST use Material Design 3 (M3) components and patterns exclusively.

**M3 Theme Specification:**
- **Theme:** Material Design 3  
- **Dependency ID:** 4UK6WHQ6UX7AKELK  
- **Routing Dependency:** 3PIDO5P3H4VPEMPL (required for NavigationLink.navigate_to)  
- **Status:** Mandatory for all forms and components

### Component Usage Policy

**MUST Use - Essential M3 Components (17):**

**Navigation & Layout:**
1. ✅ NavigationDrawerLayout - Primary layout for admin interfaces (8+ destinations)
2. ✅ NavigationLink - Navigation menu items with `navigate_to` property

**Typography:**
3. ✅ Text - Body text, labels (use M3 typography roles)
4. ✅ Heading - Headers, titles (use M3 typography roles)

**Buttons:**
5. ✅ Button - All actions (use filled/outlined/text roles for hierarchy)
6. ✅ IconButton - Icon-only actions

**Form Inputs:**
7. ✅ TextBox - Single-line input (use `outlined` role)
8. ✅ TextArea - Multi-line input (use `outlined` role)
9. ✅ DropdownMenu - Selections (use `outlined` role)
10. ✅ Checkbox - Boolean options
11. ✅ RadioButton - Single selection
12. ✅ DatePicker - Date input (use `outlined` role)
13. ✅ FileLoader - File uploads

**Display:**
14. ✅ Card - Content containers (use `elevated` or `outlined` roles)

**Containers:**
15. ✅ ColumnPanel - Vertical layouts
16. ✅ LinearPanel - Horizontal/vertical layouts
17. ✅ FlowPanel - Responsive wrapping

**Good to Have M3 Components (10):**
18. ✅ DataGrid - Tabular data
19. ✅ RepeatingPanel - Dynamic lists
20. ✅ Switch - Toggles
21. ✅ RadioGroupPanel - Grouped radios
22. ✅ ButtonMenu, IconButtonMenu, AvatarMenu - Menus
23. ✅ MenuItem - Menu items
24. ✅ Divider - Visual separation
25. ✅ Plot - Charts (Plotly)

**MUST NOT Use - Blocked Components:**

**Anvil Extras (NOT M3-compliant):**
- ❌ Tabs → Use NavigationLink in sidebar
- ❌ Pivot → Use custom DataGrid
- ❌ MultiSelectDropDown → Use DropdownMenu + Chips
- ❌ Autocomplete → Use DropdownMenu with search
- ❌ Quill → Use TextArea
- ❌ Switch (Extras) → Use M3 Switch
- ❌ Slider (Extras) → Use M3 Slider
- ❌ RadioGroup → Use M3 RadioGroupPanel
- ❌ CheckBoxGroup → Use multiple Checkboxes
- ❌ Popover → Use M3 menus
- ❌ navigation.build_menu → Use NavigationDrawerLayout
- ❌ messaging module → Use Anvil Events
- ❌ serialisation module → Not needed
- ❌ logging.Logger → Use print()

**Legacy Patterns:**
- ❌ Custom sidebar layouts → Use NavigationDrawerLayout
- ❌ Link + click handlers (for internal nav) → Use NavigationLink.navigate_to
- ❌ XYPanel for layout → Use ColumnPanel/LinearPanel
- ❌ Hardcoded colors → Use theme: color roles
- ❌ Generic Label → Use Text/Heading with roles

### Navigation Policy - TWO SYSTEMS

**mybizz uses TWO separate navigation systems:**

1. **M3 NavigationLink** - Internal SPA navigation (authenticated areas, NO URLs)
2. **Routing Dependency** - URL routing (public pages, shareable content, WITH URLs)

**Reference:** See `Docs/Anvil_Methods/anvil_cop_m3_navigation_routing.md` for complete guidance

#### 1. Internal Navigation (M3 NavigationLink)

**Use For:** Admin/customer dashboards, settings, authenticated areas where URLs not needed

**MUST:**
- ✅ Use NavigationDrawerLayout for all admin interfaces with 8+ destinations
- ✅ Use NavigationLink components for all navigation items
- ✅ Set `navigate_to` property on NavigationLinks (NO click handlers)
- ✅ Use feature-based visibility in `build_navigation()` method
- ✅ Use `selected` property to highlight active navigation item
- ✅ Use `open_form()` only for programmatic navigation (not menu clicks)

**MUST NOT:**
- ❌ Create custom layout forms instead of using NavigationDrawerLayout
- ❌ Use Link components with click handlers for internal navigation
- ❌ Manually call `open_form()` in NavigationLink click handlers
- ❌ Use Routing Dependency for internal admin navigation
- ❌ Hardcode navigation visibility without checking features

#### 2. URL Routing (Routing Dependency)

**Dependency:** `3PIDO5P3H4VPEMPL` (Routing)

**Use For:** Public pages requiring shareable URLs, SEO, browser history

**MUST:**
- ✅ Use routing for blog posts (e.g., `/blog/post-slug`)
- ✅ Use routing for product pages (e.g., `/products/:id`)
- ✅ Use routing for landing pages (e.g., `/landing/:slug`)
- ✅ Use routing for public booking pages (e.g., `/book`)
- ✅ Use routing for SEO-critical pages
- ✅ Use `@router.route()` decorator on public Forms
- ✅ Use `navigate(path=...)` for programmatic URL navigation

**MUST NOT:**
- ❌ Use routing for admin dashboard navigation (use M3 NavigationLink)
- ❌ Use routing for settings/configuration pages (use M3 NavigationLink)
- ❌ Mix routing and M3 navigation in same UI area (confuses users)

**Example - Public Product Page (uses Routing):**
```python
from routing import router

@router.route("/products/:id")
class ProductDetailPage(ProductDetailPageTemplate):
    def __init__(self, routing_context, **properties):
        self.product_id = routing_context.params['id']
        self.init_components(**properties)
```

**Example - Admin Product Management (uses M3 NavigationLink):**
```python
# In AdminLayout - NavigationLink set to ProductListForm
# NO routing needed - internal navigation only
```

### Typography Policy

**MUST:**
- ✅ Use M3 typography roles on all Text/Heading components
- ✅ Page titles: `headline-large` (32sp)
- ✅ Section headers: `headline-small` (24sp)
- ✅ Body text: `body-medium` (14sp)
- ✅ Field labels: `label-medium` (12sp)

**MUST NOT:**
- ❌ Use generic Label components without typography roles
- ❌ Use arbitrary font sizes or styles

### Color Policy

**MUST:**
- ✅ Use theme: prefix for all colors
- ✅ Primary actions: `theme:Primary` background
- ✅ Cards: `theme:Surface` or `theme:Surface Variant`
- ✅ Errors: `theme:Error` for validation states

**MUST NOT:**
- ❌ Use hardcoded hex colors (#FFFFFF, #000000, etc.)
- ❌ Use RGB values (rgb(255, 255, 255))

### Button Hierarchy Policy

**MUST:**
- ✅ Primary actions: `filled-button` role (Save, Submit, Confirm)
- ✅ Secondary actions: `outlined` role (Cancel, Back, Edit)
- ✅ Tertiary actions: `text-button` role (Learn More, View Details)

**MUST NOT:**
- ❌ Use same button role for all actions (eliminates visual hierarchy)

### Input Component Policy

**MUST:**
- ✅ Use `outlined` role for all TextBox/TextArea components in forms
- ✅ Use `outlined` role for all DropdownMenu components in forms
- ✅ Use `outlined` role for all DatePicker components
- ✅ Use `outlined-error` role for validation errors
- ✅ Provide error messages via placeholder text when invalid

**MUST NOT:**
- ❌ Use filled role for form inputs (outlined is cleaner)
- ❌ Leave inputs without error state handling

### Data Binding Policy

**MUST:**
- ✅ Use `self.item` property for all form data storage
- ✅ Enable write back (W toggle ON) for all input components
- ✅ Set `self.item` BEFORE `self.init_components()`
- ✅ Use two-way bindings: `component.property → self.item['field_name']`
- ✅ Call `refresh_data_bindings()` when modifying self.item in place

**MUST NOT:**
- ❌ Create manual change event handlers for input components
- ❌ Forget to enable write back toggle
- ❌ Call `refresh_data_bindings()` after `self.item =` reassignment (automatic)

### Component Naming Policy

**MUST:**
- ✅ Use established prefixes:
  - `nav_` - NavigationLink
  - `btn_` - Button, IconButton
  - `lbl_` - Text, Heading
  - `txt_` - TextBox, TextArea
  - `dd_` - DropdownMenu
  - `cb_` - Checkbox
  - `rb_` - RadioButton
  - `dp_` - DatePicker
  - `card_` - Card
  - `col_` - ColumnPanel
  - `lp_` - LinearPanel
  - `flow_` - FlowPanel

**MUST NOT:**
- ❌ Use arbitrary component names without prefixes in complex forms

### Prohibited Practices

**The following are STRICTLY PROHIBITED:**

1. ❌ Using Anvil Extras components when M3 alternatives exist
2. ❌ Creating custom sidebar layouts instead of NavigationDrawerLayout
3. ❌ Using Link components with click handlers for navigation
4. ❌ Using routing module (@routing.route, routing.start())
5. ❌ Hardcoding colors instead of using theme: roles
6. ❌ Using XYPanel for primary layout structure
7. ❌ Creating manual change event handlers when write back is available
8. ❌ Using generic Label components without typography roles
9. ❌ Ignoring button hierarchy (all buttons same role)
10. ❌ Using filled role for form inputs (use outlined)

---

## 2. Code Quality Standards

### 2.1 Error Handling (Non-Negotiable)

**Every server function:**
```python
@anvil.server.callable
def example_function(param):
  try:
    # Business logic
    result = process_data(param)
    return {'success': True, 'data': result}
  except Exception as e:
    print(f"Error in example_function: {e}")  # Log for debugging
    return {'success': False, 'error': str(e)}
```

**Every server call:**
```python
result = anvil.server.call('example_function', param)
if result['success']:
  # Handle success
  self.display_data(result['data'])
else:
  # Always show user-friendly error
  Notification(f"Error: {result['error']}", style="danger").show()
```

### 2.2 State Management Rules

**CRITICAL:** Never use global variables in server modules

**❌ WRONG:**
```python
# sm_example.py
cache = {}  # NEVER DO THIS - state persists across requests!

@anvil.server.callable
def dangerous_function():
    cache['data'] = get_data()  # BUG: Shared across all users!
    return cache['data']
```

**✅ CORRECT:**
```python
# Option 1: Use session (per-user state)
@anvil.server.callable
def safe_function():
    session = anvil.server.session
    session['data'] = get_data()
    return session['data']

# Option 2: Use database (persistent state)
@anvil.server.callable
def safe_function():
    user = anvil.users.get_user()
    user_config = app_tables.config.get(user=user)
    return user_config['data']

# Option 3: Return state to client (stateless server)
@anvil.server.callable
def safe_function():
    data = get_data()
    return data  # Client manages state
```

### 2.3 Naming Conventions

**Forms (PascalCase):**
- `LoginForm`, `CustomerList`, `BookingDetail`

**Server modules (snake_case):**
- `auth_service.py`, `booking_service.py`, `email_service.py`

**Functions (snake_case):**
- `get_customer()`, `create_booking()`, `send_email()`

**Database tables (prefix + snake_case):**
- `tbl_customers`, `tbl_bookings`, `tbl_products`

**Anvil packages (lowercase):**
- `client_code/auth/`, `server_code/bookings/`

### 2.4 Documentation Requirements

**Every server function must have:**
```python
@anvil.server.callable
def create_customer(name, email):
    """Create new customer record.
    
    Args:
        name (str): Customer full name
        email (str): Customer email address
        
    Returns:
        dict: {'success': bool, 'customer_id': str} or {'success': False, 'error': str}
    """
    try:
        # Implementation
        pass
    except Exception as e:
        return {'success': False, 'error': str(e)}
```

---

## 3. Security Standards

### 3.1 Role-Based Access Control (RBAC)

**ALL sensitive server functions must check permissions:**

```python
from server_code.server_auth import rbac

@anvil.server.callable
@rbac.require_role(['owner', 'manager', 'admin'])
def delete_customer(customer_id):
    """Only admins can delete customers"""
    # Implementation
    pass

@anvil.server.callable
@rbac.require_permission('bookings.manage')
def create_booking(booking_data):
    """Requires bookings.manage permission"""
    # Implementation
    pass
```

**Standard roles:**
- `owner` - Full access
- `manager` - Most features
- `admin` - Day-to-day operations
- `staff` - Limited access
- `customer` - Own data only

### 3.2 Input Validation

**ALWAYS validate user inputs:**

```python
import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_html(text):
    """Remove HTML tags"""
    return re.sub(r'<[^>]+>', '', text)

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

### 3.3 Secrets Management

**NEVER hardcode credentials:**

```python
# ❌ WRONG
STRIPE_KEY = "sk_live_abc123..."

# ✅ CORRECT: Use Anvil Secrets
stripe_key = anvil.secrets.get_secret('stripe_api_key')
```

**All API keys, passwords, and tokens MUST be stored in Anvil Secrets.**

### 3.4 Data Encryption

**Sensitive data must be encrypted at rest:**

```python
from server_code.server_shared import encryption

@anvil.server.callable
def store_payment_method(customer_id, card_token):
    """Store encrypted payment token"""
    encrypted_token = encryption.encrypt(card_token)
    
    customer = app_tables.customers.get_by_id(customer_id)
    customer['payment_token'] = encrypted_token
    
    return {'success': True}
```

---

## 4. Performance Guidelines

### 4.1 Server Call Optimization

**Minimize server calls:**
```python
# ❌ WRONG: Multiple calls in loop
for item in items:
  anvil.server.call('process_item', item)  # N calls!

# ✅ CORRECT: Single batch call
anvil.server.call('process_items_batch', items)  # 1 call
```

### 4.2 30-Second Server Timeout

**For operations longer than 30 seconds, use background tasks:**

```python
import anvil.server

# ❌ WRONG: Long operation in regular call
@anvil.server.callable
def generate_huge_report():
    data = process_millions_of_records()  # TIMEOUT!
    return data

# ✅ CORRECT: Use background task
@anvil.server.background_task
def generate_huge_report_background():
    """Background tasks can run for hours"""
    data = process_millions_of_records()  # No timeout
    
    # Save result to database
    app_tables.reports.add_row(
        report_type='huge_report',
        data=data,
        generated=datetime.now()
    )
    
    # Notify user via email
    user = anvil.users.get_user()
    anvil.email.send(
        to=user['email'],
        subject="Report Ready",
        text="Your report has been generated."
    )

# Client calls background task
@anvil.server.callable
def start_report_generation():
    """Start background task, return immediately"""
    task = anvil.server.launch_background_task('generate_huge_report_background')
    return {'success': True, 'task_id': task.get_id()}
```

**Background Task Progress Tracking:**
```python
@anvil.server.background_task
def import_products(product_list):
    total = len(product_list)
    
    for i, product in enumerate(product_list):
        import_single_product(product)
        
        # Update progress
        anvil.server.task_state['progress'] = (i + 1) / total * 100
        anvil.server.task_state['current'] = i + 1
        anvil.server.task_state['total'] = total
```

### 4.3 Lazy Loading

**For large datasets:**
```python
@anvil.server.callable
def get_customers_page(page=1, page_size=50):
    """Return paginated results"""
    offset = (page - 1) * page_size
    
    customers = app_tables.customers.search(
        tables.order_by('created', ascending=False)
    )
    
    # Get page slice
    page_data = list(customers)[offset:offset+page_size]
    total = len(list(app_tables.customers.search()))
    
    return {
        'customers': page_data,
        'page': page,
        'total_pages': (total + page_size - 1) // page_size,
        'total_count': total
    }
```

---

## 5. Package Organization

### 5.1 Standard Package Structure

```
master_template/
├─ client_code/                    # Client-side packages
│  ├─ auth/                        # Authentication forms
│  ├─ dashboard/                   # Dashboard
│  ├─ bookings/                    # Booking management
│  ├─ products/                    # Product catalog
│  ├─ customers/                   # CRM
│  ├─ marketing/                   # Marketing tools
│  ├─ settings/                    # Configuration
│  └─ shared/                      # Reusable components
│
└─ server_code/                    # Server-side packages
   ├─ server_auth/                 # Authentication service
   ├─ server_bookings/             # Booking logic
   ├─ server_products/             # Product service
   ├─ server_customers/            # Customer service
   ├─ server_marketing/            # Marketing service
   ├─ server_payments/             # Payment integrations
   └─ server_shared/               # Utilities, validators
```

### 5.2 Feature-Based Organization

**Each feature package contains:**
- Forms (client-side UI)
- Service modules (server-side logic)
- Shared components
- Database queries

**Example - Bookings feature:**
```
client_code/bookings/
├─ BookingsListForm
├─ BookingDetailForm
├─ BookingCalendarForm
└─ shared_components/

server_code/server_bookings/
├─ booking_service.py
├─ calendar_service.py
└─ validation.py
```

---

## 6. Testing Protocol

### 6.1 Manual Testing Checklist

**Before committing code:**
- [ ] Feature works in all 4 verticals
- [ ] Works for all role levels
- [ ] Error handling tested
- [ ] Mobile responsive
- [ ] Browser tested (Chrome, Firefox, Safari)

### 6.2 Integration Testing

**Test integration points:**
- [ ] CRM updates from bookings/orders
- [ ] Email campaigns trigger correctly
- [ ] Payment webhooks process
- [ ] Analytics update

---

## 7. AI Model Strategy

### 7.1 Model Allocation

**Devstral 2 (Free, Unlimited) - 80% of work:**
- Phases 1-8 implementation
- Form creation (all forms in dev plan)
- CRUD operations
- Standard server functions
- First-draft implementations

**Claude Sonnet 4.5 (20M tokens/month) - 20% of work:**
- Phase 9: Platform Management
- Third-party API integrations (review & polish)
- Security & compliance (architectural review)
- Complex business logic (validation & optimization)
- Code review & refactoring
- Production deployment (critical path validation)

### 7.2 Token Budget (20M/month)

| Use Case | Tokens | Priority |
|----------|--------|----------|
| Phase 9 (Platform Management) | 8-10M | Critical |
| API Integration Review | 2-3M | High |
| Security Review (Phase 6.5) | 2-3M | High |
| Code Polish & Refactoring | 3-4M | Medium |
| Complex Bug Fixing | 2-3M | As needed |
| Emergency Reserve | 2-3M | Reserve |

### 7.3 Workflow Patterns

**Standard Flow (Devstral):**
1. Devstral (mybizz-builder) → Implement
2. Testing droid → Validate
3. Anvil-standards droid → Compliance check
4. Backup-manager → Backup

**Complex Flow (Sonnet Review):**
1. Devstral → First implementation
2. Testing droid → Initial validation
3. Sonnet 4.5 → Architectural review
4. Sonnet 4.5 → Refactor/optimize
5. Testing droid → Final validation
6. Backup-manager → Backup

**Critical Flow (Sonnet-First):**
1. Sonnet 4.5 → Design approach
2. Sonnet 4.5 → Implement critical paths
3. Devstral → Fill standard/repetitive parts
4. Sonnet 4.5 → Integration review
5. Testing → Comprehensive validation
6. Backup-manager → Critical backup

### 7.4 Sonnet 4.5 Triggers

**Always use Sonnet for:**
- Stripe/Paystack integration (payment processing)
- Multi-client provisioning (Phase 9.1)
- Billing automation (Phase 9.4)
- Security features (encryption, audit logging, GDPR)
- Update distribution (Phase 9.3)

**Consider Sonnet for:**
- Complex business logic (booking algorithms, pricing calculations)
- Performance optimization (slow queries, indexing)
- Architecture decisions (new feature design, refactoring)

### 7.5 Model Switch Triggers

**Devstral → Sonnet:**
- Inconsistent output across attempts
- Tests failing repeatedly
- Security-sensitive code
- Complex orchestration
- API integration failing after 2-3 attempts

**Sonnet → Devstral:**
- Approach validated and clear
- Pattern established (repetitive work)
- Standard CRUD operations
- Token budget running low

---

## 8. Version Control

### 8.1 Commit Message Format

```
[TYPE] Brief description

Detailed explanation of changes

Affects: [Components affected]
Testing: [How tested]
```

**Types:**
- `[FEATURE]` - New functionality
- `[FIX]` - Bug fix
- `[REFACTOR]` - Code improvement
- `[SECURITY]` - Security improvement

### 8.2 Branching Strategy

- `master` - Production-ready code
- `dev` - Development integration
- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes

---

## 9. Enforcement

**Every change must:**
- ✅ Follow this policy
- ✅ Include error handling
- ✅ Include documentation
- ✅ Pass manual testing
- ✅ Be reviewed before merging

**Violation Severity:**
- **Critical:** Security issue, data loss risk → Immediate fix required
- **High:** Policy violation affecting quality → Fix before merge
- **Medium:** Best practice deviation → Document and plan fix
- **Low:** Style/formatting → Fix when convenient

---

## 10. Version History

| Version | Date | Changes |
|---------|------|---------|
| v6.0 | Feb 05, 2026 | Added Section 7: AI Model Strategy (Devstral 2 + Sonnet 4.5 allocation). Updated Section 1.4 Navigation Standards to M3 NavigationLink + Routing (replaced outdated open_form() guidance). Renumbered subsequent sections. |
| v5.0 | Jan 26, 2026 | **M3 Compliance Update**: Added Section 1.2 Material Design 3 Compliance (Mandatory). Added Component Usage Policy (17 essential + 10 good-to-have M3 components). Added Navigation, Typography, Color, Button Hierarchy, Input Component, Data Binding, and Component Naming policies. Added Prohibited Practices section. Removed all Anvil Extras guidance. |
| v4.0 | Jan 25, 2026 | Production development policy for V1.x. Comprehensive Anvil-first standards. |

---

*This policy is mandatory for all Mybizz development work. Deviations require documented justification.*

**GOVERNING PRINCIPLES:**  
1. Mybizz is an Anvil application. Always use Anvil's native capabilities first.  
2. Mybizz uses Material Design 3 exclusively. All UI must be M3-compliant.
