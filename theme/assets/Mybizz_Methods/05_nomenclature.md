# MyBizz Nomenclature & Naming Conventions

**Version:** 2.1  
**Last Updated:** February 2, 2026  
**Purpose:** Define naming standards for MyBizz platform development

---

## File & Folder Naming

### Folders
- **Convention**: `PascalCase_WithUnderscores`
- **Examples**: `Temp_WorkInProgress`, `Client_Forms`, `Server_Modules`

### Files
- **Convention**: `lowercase_with_underscores.ext`
- **Examples**: `backup_strategy_analysis.md`, `customer_service.py`, `booking_form.py`

---

## Version & Release System

| Term | Format | Example |
|------|--------|---------|
Not in use | **Version** | `V{major}.x` | V1.x, V2.x |
Not in use| **Release** | `V{major}.{minor}` | V1.0, V1.1, V1.2 |
| **Phase** | `Phase {number}: {Name}` | Phase 1: Authentication |
| **Stage** | `Stage {phase}.{number}: {Name}` | Stage 1.1: User Auth System |
| **Task** | `T{stage}-{number}: {Action}` | T1.1-001: Create users table |

---

## App Instances

### Development Apps
- **Primary**: `Mybizz_core`
- **Experiments**: `workshop_experiments`
- **Production**: `master_template` (when V1.0 ready)

### Client Apps
- **Pattern**: `client_{businessname}`
- **Examples**: `client_yogastudio`, `client_janes_consulting`
- **Rules**: Lowercase, underscores only, max ~30 chars

---

## User Terminology

| Term | Definition |
|------|-----------|
| **Client** | MyBizz subscriber (business owner) |
| **Customer** | Client's end user (their customer) |
| **Subscriber** | Synonym for Client |
| **Visitor** | Public website visitor (not logged in) |

---

## Anvil Component Prefixes

| Component | Prefix | Example |
|-----------|--------|---------|
| Button | `btn_` | `btn_save`, `btn_cancel` |
| TextBox | `txt_` | `txt_customer_name` |
| TextArea | `txt_` | `txt_notes` |
| DropDown/DropdownMenu | `dd_` | `dd_status` |
| Label/Text/Heading | `lbl_` | `lbl_page_title` |
| DatePicker | `dp_` | `dp_booking_date` |
| FileLoader | `fu_` | `fu_upload` |
| Link/NavigationLink | `lnk_`/`nav_` | `lnk_home`, `nav_dashboard` |
| CheckBox | `chk_` | `chk_agree_terms` |
| RadioButton | `rdo_` | `rdo_payment_method` |
| Switch | `sw_` | `sw_enabled` |
| Image | `img_` | `img_logo` |
| Panel/Container | `pnl_`/`col_`/`lp_` | `pnl_header`, `col_content` |
| Card | `card_` | `card_details` |
| DataGrid | `dg_` | `dg_customers` |
| RepeatingPanel | `rp_` | `rp_items` |
| Plot | `plot_` | `plot_revenue` |

---

## Form Naming

### Pattern
- **Format**: `{Entity}{Type}Form`
- **Examples**: `CustomerListForm`, `BookingEditorForm`, `DashboardForm`

### Types
- `ListForm` - Data listing/browsing
- `EditorForm` - Create/edit single record
- `ViewerForm` - Read-only detail view
- `DashboardForm` - Summary/metrics view

---

## Module Naming

### Server Modules
- **Format**: `{purpose}_service.py`
- **Examples**: `customer_service.py`, `booking_service.py`, `email_service.py`

### Client Modules
- **Format**: `{purpose}_utils.py` or `{purpose}_helpers.py`
- **Examples**: `validation_utils.py`, `format_helpers.py`

---

## Package Organization

### Server Packages
- **services** - Business logic (`customer_service.py`)
- **integrations** - External APIs (`paypal_integration.py`)
- **utils** - Helper functions (`date_utils.py`)
- **models** - Data models/schemas

### Client Packages
- **forms** - UI forms organized by feature
- **components** - Reusable UI components
- **utils** - Client-side helpers

---

## Database Tables

### Naming
- **Format**: Lowercase, underscores
- **Examples**: `customers`, `bookings`, `transactions`, `user_settings`

### Linked Columns
- **Format**: `{table}_link`
- **Example**: `customer_link` (links to customers table)

---

## Transaction Types

- `room_booking` - Hospitality
- `appointment` - Services
- `product_sale` - E-commerce
- `membership` - Subscriptions

---

## Currency Terms

| Term | Definition |
|------|-----------|
| **System Currency** | Primary currency for client's administration (immutable) |
| **Display Currency** | Optional secondary currency for customer pricing |

---

## Critical Concepts

### Open Verticals
All features available to all clients. No vertical locking.

### Grandfathering
First 50 clients: $25/month lifetime. Clients 51-100: $50/month.

### Pull-Based Updates
Clients control when they update master_template. Not automatic.

### Master Template
Published Anvil dependency containing all MyBizz features.

### Client Instance
Individual Anvil app for one business, depends on master_template.

---

## Anvil-Specific

### Server vs Client
- **Server Module**: Backend, accesses Data Tables, uses secrets
- **Client Module**: Browser, UI only, no Data Tables access

### Decorator
```python
@anvil.server.callable  # Makes server function callable from client
```

---

## Common Abbreviations

| Abbrev | Full Term |
|--------|-----------|
| MVP | Minimum Viable Product |
| API | Application Programming Interface |
| CRM | Customer Relationship Management |
| UI | User Interface |
| CRUD | Create, Read, Update, Delete |

---

**Maintained By:** MyBizz Development Team  
**Next Review:** After major feature additions or quarterly
