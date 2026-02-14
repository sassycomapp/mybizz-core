# Mybizz Platform - System Design

**Document Version:** 9.0  
**Date:** January 26, 2026  
**Status:** Active Design Document  
**Platform Capacity:** 100 clients (V1.x)  
**Architecture:** Single master_template, Open Verticals  
**UI Theme:** Material Design 3 (M3)

---

## 1. System Overview

### 1.1 What Mybizz Is

Mybizz is a complete online business management platform delivered as a subscription service. Each subscription provides:

1. Professional public-facing website
2. Embedded operational tools (bookings, inventory, orders)
3. Customer relationship management (CRM)
4. Revenue management (payments, invoicing, accounting)
5. Marketing capabilities (email campaigns, lead capture)
6. Business intelligence (analytics, reporting)

**Key Innovation:** Plug-and-play business solution for 4 business types (verticals), where owners insert their data to have a fully operational online business.

### 1.2 Target Scale

- **Maximum:** 100 clients (V1.x)
- **Revenue Model:** $25/month (first 50), $50/month (remaining 50)
- **Annual Revenue:** $45,000/year
- **Direct Costs:** $18,000/year (Anvil hosting: 100 × $15/month)
- **Net Income:** $27,000/year
- **Support Load:** ~100 hours/month (sustainable for solo founder)

### 1.3 Four Business Verticals

**Open Verticals Architecture:** All features available to all clients. Clients activate what they need via toggles.

**1. Hospitality**
- Guesthouses, B&Bs, boutique hotels, restaurants
- Room management (accommodation): Reservations, check-in/check-out, housekeeping
- Table management (restaurants): Table reservations, seating preferences, party size, dietary requirements
- Unified booking infrastructure for both room and table bookings

**2. Consulting & Services**
- Professional services, appointments, consultants, therapists, salons
- Service scheduling, appointment booking, client management

**3. E-commerce**
- Digital and physical product sales
- Inventory management, order fulfillment, shipping

**4. Memberships & Subscriptions**
- Recurring revenue businesses, clubs, gyms
- Membership tiers, access control, renewal management

---

## 2. Architecture Overview

### 2.1 Dependency Architecture

```
┌──────────────────────────────────────────────────────────┐
│  Mybizz Founder Account                                  │
│                                                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │  master_template_dev                               │  │
│  │  - Development workspace                           │  │
│  │  - All features in one app                         │  │
│  │  - Anvil packages for organization                 │  │
│  └────────────────────────────────────────────────────┘  │
│                     ↓                                     │
│                 Published as                              │
│                     ↓                                     │
│  ┌────────────────────────────────────────────────────┐  │
│  │  master_template (V1.0, V1.1, V1.2...)            │  │
│  │  - Published dependency                            │  │
│  │  - Versioned releases                              │  │
│  │  - Pull-based updates                              │  │
│  └────────────────────────────────────────────────────┘  │
│                                                           │
└──────────────────────────────────────────────────────────┘
                     ↓
          Consumed by 100 Client Instances
                     ↓
┌──────────────────────────────────────────────────────────┐
│  Client Instance (e.g., client_yogastudio)               │
│                                                           │
│  - Depends on: master_template (specific version)        │
│  - Anvil Data Tables (client's business data)            │
│  - Client owns and controls: data, theme, features       │
│                                                           │
│  Complete data isolation - no shared resources           │
└──────────────────────────────────────────────────────────┘
```

**Key Characteristics:**
- **One codebase** (master_template) powers all 100 clients
- **Complete data isolation** - each client in separate Anvil account
- **Instant updates** - publish once, available to all
- **Zero code duplication** - reduces bugs, ensures consistency
- **Client controls updates** - pull-based, not forced

### 2.2 Package Organization

```
master_template/
├─ client_code/                    # Client-side packages (browser)
│  ├─ auth/                        # Authentication forms
│  ├─ dashboard/                   # Main dashboard
│  ├─ bookings/                    # Booking management
│  ├─ products/                    # E-commerce
│  ├─ customers/                   # CRM
│  ├─ marketing/                   # Email campaigns
│  ├─ blog/                        # Content management
│  ├─ settings/                    # Configuration
│  └─ shared/                      # Layouts, components
│
└─ server_code/                    # Server-side packages
   ├─ server_auth/                 # Authentication service
   ├─ server_bookings/             # Booking logic
   ├─ server_products/             # Product service
   ├─ server_customers/            # Customer service
   ├─ server_marketing/            # Marketing service
   ├─ server_payments/             # Payment integrations
   ├─ server_emails/               # Email service
   ├─ server_analytics/            # Reporting
   └─ server_shared/               # Utilities, validators
```

---

## 3. Core Features

### 3.1 Authentication & Administration

**Authentication:**
- Email/password login
- Password reset
- Role-based access control (RBAC)
- Roles: Owner, Manager, Admin, Staff, Customer

**Dashboard:**
- Key metrics (revenue, bookings, customers, orders)
- Recent activity feed
- Storage usage monitoring
- System notifications

**Settings:**
- Business profile (name, logo, contact info)
- Feature activation toggles
- Theme customization (colors)
- Currency settings
- User & permissions management

**Navigation:**
- Material Design 3 NavigationDrawerLayout for admin interfaces (20+ destinations)
- NavigationLink components with navigate_to property (automatic navigation)
- 4 Layout Forms: AdminLayout, CustomerLayout, BlankLayout, ErrorLayout
- Feature-based visibility (show/hide menu items based on enabled features)
- Role-based visibility (show/hide based on permissions)

### 3.2 Public Website

**Standard Pages:**
- Home Page (7 professional templates)
- About Page
- Contact Page (with form submission)
- Privacy Policy
- Terms & Conditions

**Dynamic Pages:**
- Services listing & detail (if services enabled)
- Product catalog & detail (if e-commerce enabled)
- Room listings (if hospitality enabled)
- Blog listing & posts (if blog enabled)

**Landing Pages:**
5 templates for marketing campaigns:
- Lead Capture
- Product Launch
- Event Registration
- Video Sales Letter (VSL)
- Membership Funnel

**Features:**
- Template-based rendering
- Configuration-driven content
- Mobile responsive
- SEO optimization

### 3.3 CRM & Marketing

**Contact Management:**
- Contact database with status (Lead/Customer/Inactive)
- Activity timeline
- Tags and segmentation
- Import/export (CSV)

**Segmentation:**
- Pre-built segments (VIP customers, Repeat buyers, Inactive contacts)
- Custom segment builder
- Real-time calculation, cached counts

**Email Marketing (Brevo Integration):**
- Email campaigns (sequences)
- Trigger-based enrollment
- Broadcast emails (one-time)
- Webhook tracking (opens, clicks)

**Task Automation:**
- Manual tasks (follow-ups, reminders)
- Auto-generated tasks (arrival instructions, review requests)
- Calendar integration

**Integration:**
- Bookings/Orders automatically update contact records
- Auto-enrollment in campaigns based on triggers
- Background processing (hourly for campaigns, daily for tasks)

### 3.4 Payments & E-commerce

**Payment Gateways:**
- Stripe (global)
- Paystack (Africa-optimized)
- PayPal (one-time payments only, not subscriptions)
- Client selects ONE primary gateway

**Multi-Currency Model:**

**System Currency (Immutable):**
- Set once during client onboarding (e.g., USD)
- CANNOT be changed after first transaction
- ALL admin reporting, analytics, and accounting in system currency
- Business owner sees everything in system currency

**Customer Display Currency (Optional):**
- Business can set product prices in customer's local currency (e.g., ZAR)
- When price set to ZAR, mybizz converts system price (USD) → ZAR using configured exchange rate
- Customer sees price in ZAR, pays in ZAR via payment gateway
- Payment received in ZAR, converted back to USD for admin reporting
- Exchange rate manually configured in settings, updated as needed

**Example:**
1. Business system currency: USD
2. Product price in system: $50 USD
3. Business sets customer price: R850 ZAR (using exchange rate 1 USD = 17 ZAR)
4. Customer sees: R850 ZAR on website
5. Customer pays: R850 ZAR via Paystack
6. Admin sees revenue: $50 USD in dashboard/reports

**Benefits:**
- ✅ Simple: Single source of truth (system currency)
- ✅ Flexible: Display prices in customer's local currency
- ✅ Transparent: Admin always sees consistent currency reporting
- ✅ Scalable: Supports international customers without currency confusion

**V1.x Limitation:** One payment gateway per instance (cannot mix Stripe + Paystack). Multi-country businesses expanding need separate mybizz instances per region OR accept currency conversion at gateway.

**Product Catalog:**
- Product management (name, description, price, images)
- Inventory tracking
- Categories and tags
- Product variants

**Shopping Cart & Checkout:**
- Cart management
- Customer details
- Payment processing
- Order confirmation

**Invoicing:**
- Invoice generation
- PDF creation
- Email delivery
- Payment tracking

**Subscriptions:**
- Recurring billing
- Membership tiers
- Gateway integration (Stripe/Paystack)

### 3.5 Bookings & Appointments

**Calendar System:**
- Month/week/day views
- Availability display
- Click-to-book interface
- Supports both rooms (accommodation) and tables (restaurants)

**Availability Management:**
- Business hours by day
- Blocked dates
- Service-specific availability
- Table/room capacity management

**Booking Flow - Accommodation:**
- Room selection
- Date range (check-in/check-out)
- Guest details
- Special requests
- Payment (deposit or full)
- Confirmation email

**Booking Flow - Restaurant:**
- Date and time selection
- Party size
- Table/area preference (optional)
- Dietary requirements
- Special occasions
- Deposit (optional, for large parties)
- Confirmation email + SMS reminders

**Services Management:**
- Service catalog (for appointments)
- Room catalog (for accommodation)
- Table management (for restaurants)
- Duration and pricing
- Category organization

### 3.6 Shipping & Logistics

**3 Shipping Options:**
1. Manual Shipping - Business handles directly
2. Bob Go (South Africa) - API integration
3. Easyship (International) - API integration

**Features:**
- Rate calculation
- Label generation
- Tracking integration
- Shipping confirmation emails

### 3.7 Analytics & Reporting

**Dashboard Analytics:**
- Revenue metrics
- Booking metrics
- Customer metrics
- Product performance

**Reports:**
- Revenue by period
- Customer lifetime value
- Inventory levels
- Sales velocity

**Data Export:**
- PDF reports
- CSV export
- Custom date ranges

---

## 4. Technical Stack

### 4.1 Platform

**Anvil.works:**
- Full-stack Python framework
- Material Design 3 (M3) UI theme
- NavigationDrawerLayout for navigation
- No DevOps required
- Built-in hosting
- Automatic backups
- HTTPS/TLS encryption

**Why Anvil:**
- Python front-end and back-end
- Material Design 3 components built-in
- Dependency system (perfect for Mybizz architecture)
- Visual form designer
- Built-in security
- Professional hosting included

### 4.2 Data Storage

**Anvil Data Tables:**
- PostgreSQL-backed
- Automatic relationships
- Built-in query system
- Automatic backups
- No database setup required

**Storage per Client:**
- Contacts: Up to 10,000
- Unlimited bookings, orders, products (within Anvil limits)
- Email campaigns: Up to 100 active

### 4.3 Integrations

**Payment Processing:**
- Stripe API
- Paystack API

**Email Services:**
- Zoho (transactional emails)
- Brevo (marketing campaigns)

**Shipping:**
- Bob Go API (South Africa)
- Easyship API (International)

**Other:**
- Google Maps API (optional)
- Social media links

### 4.4 Security

**Infrastructure Security (Anvil):**
- HTTPS/TLS encryption
- DDoS protection
- Server-side execution sandboxing
- Built-in CSRF protection

**Application Security:**
- Role-based access control (RBAC)
- Permission decorators on all sensitive functions
- Input validation
- Data encryption at rest
- Audit logging

**Compliance:**
- GDPR data export
- Right to be forgotten
- Cookie consent
- Privacy policy templates
- PCI DSS compliance (via payment gateways)

---

## 5. Development Workflow

### 5.1 Environment Structure

```
master_template_dev     → Development (active work)
master_template_staging → Staging (pre-production testing)
master_template         → Published (production dependency)
```

### 5.2 Publishing Process

1. Complete features in master_template_dev
2. Test in staging environment
3. Publish new version with release notes
4. Notify clients of update availability
5. Clients pull update when ready

### 5.3 Client Provisioning

**Mybizz_management App (Separate):**
- Client onboarding interface
- Automated app cloning
- User creation
- Configuration initialization
- Monitoring dashboard
- Billing automation
- Update distribution

**Process:**
1. Enter business details
2. Clone master_template
3. Create owner user
4. Initialize configuration
5. Set up email (Zoho)
6. Onboarding checklist

---

## 6. Feature Configuration

### 6.1 Open Verticals Model

**All features available to all clients.** Clients activate what they need:

**Feature Toggles:**
- ☑ Bookings & Appointments
- ☑ Product Sales (E-commerce)
- ☑ Memberships & Subscriptions
- ☑ Professional Services
- ☑ Hospitality Management
- ☑ Blog & Content
- ☑ Email Marketing
- ☑ Reviews & Testimonials

**Examples:**
- Yoga studio: Bookings + Memberships + Products (retail)
- Consultant: Services + Blog + Email Marketing
- B&B: Hospitality (rooms) + Bookings + Blog
- Online store: E-commerce + Email Marketing + Reviews

### 6.2 Configuration System

**tbl_config (one row per client):**
- business_name, logo
- primary_color, accent_color
- system_currency
- features_enabled (JSON object)
- home_template
- social media links
- API credentials (encrypted)

**Behavior:**
- Navigation adapts to enabled features
- Forms show/hide based on features
- Terminology changes by vertical context
- All business logic feature-aware

---

## 7. Data Model Summary

### 7.1 Core Tables

```
tbl_config              # Business configuration
tbl_users               # Staff & customer accounts
tbl_contacts            # CRM database
tbl_contact_events      # Activity timeline
tbl_email_campaigns     # Email sequences
tbl_segments            # Custom segments
tbl_tasks               # Task management
tbl_bookings            # Appointments/reservations
tbl_services            # Service catalog
tbl_availability        # Business hours
tbl_products            # Product catalog
tbl_orders              # Order management
tbl_order_items         # Order line items
tbl_invoices            # Invoicing
tbl_subscriptions       # Recurring billing
tbl_blog_posts          # Blog content
tbl_landing_pages       # Marketing landing pages
tbl_audit_log           # Security audit trail
tbl_email_log           # Email delivery log
```

### 7.2 Data Isolation

**Critical:** Each client instance operates in a separate Anvil account.

- Master template code runs in CLIENT's environment
- `app_tables` reference is CLIENT's Data Tables
- Zero cross-tenant data access
- Client owns 100% of their data

---

## 8. Anvil Methodology Alignment

### 8.1 Best Practices

**Always use Anvil-native solutions:**
- Data Tables (not external databases)
- Users service (authentication)
- Secrets (API keys)
- Built-in components
- Dependency system
- Package organization

**Server-side patterns:**
- `@anvil.server.callable` for all server functions
- No global variables in server modules
- State via `anvil.server.session` or database
- Background tasks for long operations (>30s timeout)
- Error handling everywhere

**Client-side patterns:**
- `open_form()` for navigation
- Layout Forms for structure
- Feature-based component visibility
- Material Design theme

### 8.2 Performance

**Optimization:**
- Batch server calls (avoid loops)
- Background tasks for heavy processing
- Lazy loading for large datasets
- Caching (dashboard metrics, segment counts)
- Critical database indexes

**Limits:**
- 30-second server call timeout
- Use background tasks for longer operations
- 100 clients maximum (V1.x capacity)

---

## 9. Update Distribution Model

### 9.1 Pull-Based Updates

**Client Controls Updates:**
1. Mybizz publishes new version
2. Client notified via email/dashboard
3. Client reviews release notes
4. Client updates dependency when ready
5. Client can roll back if issues

**Update Types:**
- Critical Security: Immediate notification
- Bug Fixes: Standard notification
- New Features: Standard notification
- Breaking Changes: Advance notice + migration guide

### 9.2 Versioning

**Semantic Versioning:**
- V1.0.0 - Initial release
- V1.1.0 - Minor features (backwards compatible)
- V1.0.1 - Bug fixes (backwards compatible)
- V2.0.0 - Breaking changes

---

## 10. Management App

**Mybizz_management (Separate App):**

**Purpose:** Mybizz founder's internal tools for managing 100 client instances.

**Features:**
- Client provisioning (automated app creation)
- Client monitoring (health scores, alerts)
- Revenue tracking (MRR, churn rate)
- Update distribution
- Billing automation (Stripe subscriptions)
- Support ticket system (for Mybizz support)

**Architecture:**
- Clone of master_template PLUS management features
- Separate from master_template (security isolation)
- NOT included in client instances
- Owner access only

---

## VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| v9.0 | Jan 26, 2026 | **M3 Compliance Update**: Added Material Design 3 (M3) theme to header. Updated Section 3 navigation to reference NavigationDrawerLayout + NavigationLink. Added M3 mentions to Technical Stack (Section 4). All UI now M3-compliant. |
| v8.0 | Jan 25, 2026 | Production conceptual design for V1.x (100 clients). Open verticals architecture. |

---

**END OF SYSTEM DESIGN DOCUMENT - V9.0 (M3 COMPLIANT)**

**Status:** ✅ Active Design  
**Audience:** AI assistants and developer (solo founder)  
**Purpose:** Technical reference for implementation

