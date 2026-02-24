---
description: "08_sitemap.md - Mybizz sitemap"
globs: ["**/*"]
alwaysApply: true
---

# Mybizz Platform - Sitemap

**Document Version:** 5.0  
**Date:** January 22, 2026  
**Status:** Living Document  
**Last Updated:** January 19, 2026  
**Updates:** Added website and landing pages routes (Phase 2)

---

## Purpose

This sitemap tracks all routes, pages, and forms in the Mybizz Platform. It is organized by:
- **Route Type** (Public, Admin, API)
- **Development Phase** (when built)
- **Conditional Display** (vertical-specific or module-dependent)
- **Routing Implementation** (NEW - how routes are organized and implemented)

**Update Trigger:** End of each development phase or when new forms/routes added.

---

## Legend

**Status Indicators:**
- ⚪ **Not Started** - Not yet built
- 🟡 **In Progress** - Currently being developed
- ✅ **Complete** - Built and tested
- 🔄 **Revision** - Requires updates/fixes

**Conditional Indicators:**
- `[V:hospitality]` - Only visible for hospitality vertical
- `[M:email]` - Only visible if Email Marketing module active
- `[P:premium]` - Only available on Premium/Enterprise tiers
- `[R:admin]` - Requires admin role

---

## Routing Implementation Guide

**⚠️ SIMPLIFIED APPROACH - Updated Jan 22, 2026**

**Architecture:** Layout-based navigation with `open_form()`. Optional routing for public pages only.  
**Reference:** `Anvil_Navigation_Routing_Code_of_Practice.md`

**Key Changes:**
- Admin area: No routing, use `open_form()` for navigation
- Customer portal: No routing, use `open_form()` for navigation  
- Public website: Optional routing only if needed for SEO/shareable URLs

---

## Routing Implementation Guide (OLD - UNDER REVISION)

**Architecture:** Anvil Routing Dependency (hash-based navigation)  
**Related Doc:** See Section 2.3 in `04_architecture_specification_v6.md`

### Route Organization

All routes are defined in `client_code/routes/` modules:

```
client_code/
├─ startup_module.py           # Router initialization
└─ routes/
   ├─ auth_routes.py           # Login, signup, password reset (6 routes)
   ├─ public_routes.py         # Homepage, blog, shop, public pages (25+ routes)
   ├─ website_routes.py        # Website pages & landing pages (15+ routes)
   ├─ admin_routes.py          # Admin dashboard, management (85+ routes)
   ├─ vertical_routes.py       # Vertical-specific routes (conditional)
   ├─ crm_routes.py            # CRM & marketing routes (15 routes)
   └─ api_routes.py            # API endpoints (Phase 7)
```

### Route Naming Conventions

**Format:** `{Resource}{Action}Route`

Examples:
- `DashboardRoute` → `/admin` 
- `BookingsListRoute` → `/admin/bookings`
- `BookingDetailRoute` → `/admin/bookings/:id`
- `BookingEditRoute` → `/admin/bookings/:id/edit`
- `ProductDetailRoute` → `/shop/:slug`

### URL Pattern Standards

```
Public Pages:        /page-name
Blog:                /blog/:slug
Products:            /shop/:category/:slug
Booking Widget:      /booking
Invoice View:        /invoice/:token
Landing Pages:       /landing/:slug

Admin Dashboard:     /admin
Admin Resources:     /admin/resource
Admin Detail:        /admin/resource/:id
Admin Create:        /admin/resource/new
Admin Edit:          /admin/resource/:id/edit
Settings:            /admin/settings/section
```

### Route Modules Map

| Module | Route Prefix | Auth Required | Template | Routes Count |
|--------|-------------|---------------|----------|--------------|
| `auth_routes.py` | `/login`, `/signup` | No | BlankLayout | 6 |
| `public_routes.py` | `/`, `/blog`, `/shop` | No | MainLayout | 25+ |
| `website_routes.py` | `/landing`, `/about`, `/contact` | No | MainLayout/BlankLayout | 15+ |
| `admin_routes.py` | `/admin/*` | Yes (admin) | AdminLayout | 85+ |
| `vertical_routes.py` | Various | Depends | MainLayout | 30+ (varies) |
| `crm_routes.py` | `/admin/contacts/*` | Yes (admin) | AdminLayout | 15 |
| `api_routes.py` | `/_/api/*` | Varies | None | 10+ |

### Layout Templates

| Template | Used For | Navigation | Features |
|----------|----------|------------|----------|
| **MainLayout** | Public website | Top nav, footer | Logo, menu, CTA buttons |
| **AdminLayout** | Admin interface | Sidebar menu | Dashboard, breadcrumbs, user menu |
| **BlankLayout** | Login, payment, landing pages | None | Minimal chrome, centered content |
| **ErrorLayout** | 404, errors | Home link only | Error message, suggestions |

### Implementation Checklist

When adding new routes:

- [ ] Define Route class in appropriate module
- [ ] Set `path`, `form`, and `template` attributes
- [ ] Implement `before_load()` for authentication
- [ ] Implement `load_data()` if data needed
- [ ] Set `cache_form` appropriately
- [ ] Add route to module's export list
- [ ] Update this sitemap with new route
- [ ] Test route in IDE (Set startup URL)
- [ ] Verify back button works
- [ ] Test direct URL access (bookmarking)

---
## 1. Core Routes (Master Template - All Clients)

### 1.1 Authentication & Access (Phase 1: Stages 1-4)

| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/login` | `frm_login` | ⚪ | User login page | Stage Week 2 |
| `/register` | `frm_register` | ⚪ | New user registration | Stage Week 2 |
| `/reset-password` | `frm_password_reset` | ⚪ | Password reset flow | Stage Week 2 |
| `/logout` | (server action) | ⚪ | Logout and redirect | Stage Week 2 |

### 1.2 Admin Dashboard (Phase 1: Stages 1-4) `[R:admin]`

| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin` | `frm_dashboard` | ⚪ | Main admin dashboard (default landing) | Stage Week 3 |
| `/admin/settings` | `frm_settings` | ⚪ | Business settings & configuration | Stage 4 |
| `/admin/settings/branding` | `frm_branding` | ⚪ | Logo, colors, brand identity | Stage 4 |
| `/admin/settings/website` | `frm_website_settings` | ⚪ | Homepage, about, contact settings | Phase 2 Week 1-2 |
| `/admin/settings/vertical` | `frm_vertical_selector` | ⚪ | Vertical type selection (permanent) | Stage 4 |
| `/admin/settings/email-provider` | `frm_email_config` | ⚪ | Brevo/ZOHO email configuration | Stage 5 |
| `/admin/settings/currency` | `frm_currency_settings` | ⚪ | USD system + optional local currency | Stage 4 |
| `/admin/settings/storage` | `frm_storage_management` | ⚪ | Storage usage & archiving | Stage 24 |
| `/admin/settings/security` | `frm_security` | ⚪ | Secrets & encryption management | Stage 22 |

---

---

## 2. Public-Facing Routes (Client Websites)

### 2.1 Core Public Pages (Phase 2: Week 1-2)

| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/` | `frm_home` | ⚪ | Homepage (7 template options) | Phase 2 Week 1-2 |
| `/about` | `frm_about` | ⚪ | About us page (configurable sections) | Phase 2 Week 1-2 |
| `/contact` | `frm_contact` | ⚪ | Contact form + business details + map | Phase 2 Week 1-2 |
| `/privacy` | `frm_privacy_policy` | ⚪ | Privacy policy page | Phase 2 Week 1-2 |
| `/terms` | `frm_terms_conditions` | ⚪ | Terms & conditions page | Phase 2 Week 1-2 |

**Admin Routes - Website Configuration:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/settings/website` | `frm_website_settings` | ⚪ | Main website settings hub | Phase 2 Week 1-2 |
| `/admin/settings/website/homepage` | `frm_homepage_editor` | ⚪ | Homepage template selection & config | Phase 2 Week 1-2 |
| `/admin/settings/website/about` | `frm_about_editor` | ⚪ | About page content editor | Phase 2 Week 1-2 |
| `/admin/settings/website/contact` | `frm_contact_settings` | ⚪ | Contact details, Google Maps, social | Phase 2 Week 1-2 |
| `/admin/settings/website/privacy` | `frm_privacy_editor` | ⚪ | Privacy policy editor | Phase 2 Week 1-2 |
| `/admin/settings/website/terms` | `frm_terms_editor` | ⚪ | Terms & conditions editor | Phase 2 Week 1-2 |

### 2.2 Feature-Dependent Public Pages (Phase 2-4) `[M:feature_dependent]`

| Route | Form Name | Status | Description | Condition | Phase |
|-------|-----------|--------|-------------|-----------|-------|
| `/services` | `frm_services_page` | ⚪ | Services catalog | `[M:services]` | Phase 2 Week 2 |
| `/services/:slug` | `frm_service_detail` | ⚪ | Individual service detail | `[M:services]` | Phase 2 Week 2 |
| `/shop` | `frm_shop_page` | ⚪ | Product catalog | `[M:ecommerce]` | Phase 3 Week 9 |
| `/shop/:category/:slug` | `frm_product_detail_public` | ⚪ | Product detail page | `[M:ecommerce]` | Phase 3 Week 9 |
| `/rooms` | `frm_rooms_page` | ⚪ | Room/accommodation listing | `[M:hospitality]` | Phase 4 Week 12 |
| `/rooms/:slug` | `frm_room_detail` | ⚪ | Room detail page | `[M:hospitality]` | Phase 4 Week 12 |
| `/booking` | `frm_booking_page` | ⚪ | Public booking form | `[M:bookings]` | Phase 4 Week 12 |
| `/membership` | `frm_membership_page` | ⚪ | Membership tiers & signup | `[M:memberships]` | Phase 4 Week 13 |

### 2.3 Landing Pages System (Phase 2: Week 3-4)

**Public Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/landing/:slug` | `frm_landing_page` | ⚪ | Dynamic landing page (5 templates) | Phase 2 Week 3-4 |

**Admin Routes - Landing Page Management:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/landing-pages` | `frm_landing_pages_list` | ⚪ | Landing page list with analytics | Phase 2 Week 3-4 |
| `/admin/landing-pages/new` | `frm_landing_page_editor` | ⚪ | Create new landing page | Phase 2 Week 3-4 |
| `/admin/landing-pages/:id/edit` | `frm_landing_page_editor` | ⚪ | Edit landing page | Phase 2 Week 3-4 |
| `/admin/landing-pages/:id/analytics` | `frm_landing_page_analytics` | ⚪ | Landing page analytics | Phase 2 Week 3-4 |

**Landing Page Templates (5 types):**
1. Lead Capture - Email collection for lead magnets
2. Product Launch - Product/service promotion
3. Event Registration - Workshop/webinar/retreat signups
4. Video Sales Letter (VSL) - Video-focused conversion
5. Membership Funnel - Membership tier selection

**Admin Routes - Contact & Lead Management:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/contacts/submissions` | `frm_contact_submissions` | ⚪ | Contact form submissions list | Phase 2 Week 1-2 |
| `/admin/contacts/leads` | `frm_leads_list` | ⚪ | Leads captured from landing pages | Phase 2 Week 3-4 |

### 2.4 Blog Routes (Phase 2: Stage Week 6) `[M:blog]`

| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/blog` | `frm_blog_display` | ⚪ | Blog post listing | Stage Week 6 |
| `/blog/:slug` | `frm_blog_post` | ⚪ | Individual blog post | Stage Week 6 |
| `/blog/category/:slug` | `frm_blog_category` | ⚪ | Posts by category | Stage Week 6 |
| `/blog/tag/:slug` | `frm_blog_tag` | ⚪ | Posts by tag | Stage Week 6 |

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/blog` | `frm_blog_manager` | ⚪ | Blog post manager | Stage Week 6 |
| `/admin/blog/new` | `frm_blog_editor` | ⚪ | Create new post | Stage Week 6 |
| `/admin/blog/edit/:id` | `frm_blog_editor` | ⚪ | Edit existing post | Stage Week 6 |
| `/admin/blog/categories` | `frm_category_manager` | ⚪ | Manage categories | Stage Week 6 |
| `/admin/blog/tags` | `frm_tag_manager` | ⚪ | Manage tags | Stage Week 6 |

## 3. Marketing & Communication Routes (Phase 2)

### 3.1 Email Marketing (Phase 2: Stage Week 5) `[M:email]`

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/email/templates` | `frm_email_templates` | ⚪ | Email template library | Stage Week 5 |
| `/admin/email/templates/new` | `frm_email_template_editor` | ⚪ | Create new template | Stage Week 5 |
| `/admin/email/templates/edit/:id` | `frm_email_template_editor` | ⚪ | Edit template | Stage Week 5 |
| `/admin/email/log` | `frm_email_log` | ⚪ | Email sending history | Stage Week 5 |

### 3.2 Campaign Management (Phase 2: Stage Week 7) `[M:email]`

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/campaigns` | `frm_campaign_list` | ⚪ | Campaign dashboard | Stage Week 7 |
| `/admin/campaigns/new` | `frm_campaign_builder` | ⚪ | Create new campaign | Stage Week 7 |
| `/admin/campaigns/edit/:id` | `frm_campaign_builder` | ⚪ | Edit campaign | Stage Week 7 |
| `/admin/campaigns/:id/analytics` | `frm_campaign_analytics` | ⚪ | Campaign performance | Stage Week 7 |
| `/admin/newsletter/subscribers` | `frm_subscriber_list` | ⚪ | Newsletter subscriber management | Stage Week 7 |

**Public Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/newsletter/subscribe` | `frm_newsletter_signup` | ⚪ | Newsletter signup form | Stage Week 7 |
| `/newsletter/unsubscribe/:token` | `frm_unsubscribe` | ⚪ | Unsubscribe page | Stage Week 7 |

### 3.3 Social Media (Phase 2: Stage Week 7) `[M:social]`

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/social/schedule` | `frm_social_scheduler` | ⚪ | Schedule social posts | Stage Week 7 |
| `/admin/social/posts` | `frm_social_post_list` | ⚪ | Scheduled & published posts | Stage Week 7 |

---

## 4. Commerce & Payments Routes (Phase 3)

### 4.1 E-commerce (Phase 3: Stages 8-10) `[V:digital_products]` `[V:physical_products]` `[M:payments]`

**Public Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/shop` | `frm_product_catalog` | ⚪ | Product listing | Stage Week 9 |
| `/shop/:slug` | `frm_product_detail` | ⚪ | Individual product page | Stage Week 9 |
| `/shop/category/:slug` | `frm_category_products` | ⚪ | Products by category | Stage Week 9 |
| `/cart` | `frm_cart` | ⚪ | Shopping cart | Stage Week 9 |
| `/checkout` | `frm_checkout` | ⚪ | Checkout flow | Stage Week 9 |
| `/order-confirmation/:id` | `frm_order_confirmation` | ⚪ | Order confirmation page | Stage Week 9 |
| `/orders/:id` | `frm_order_tracking` | ⚪ | Order tracking (for customers) | Stage Week 10 |

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/products` | `frm_product_manager` | ⚪ | Product inventory | Stage Week 9 |
| `/admin/products/new` | `frm_product_editor` | ⚪ | Add new product | Stage Week 9 |
| `/admin/products/edit/:id` | `frm_product_editor` | ⚪ | Edit product | Stage Week 9 |
| `/admin/orders` | `frm_order_manager` | ⚪ | Order management | Stage Week 10 |
| `/admin/orders/:id` | `frm_order_detail` | ⚪ | Individual order details | Stage Week 10 |
| `/admin/inventory` | `frm_inventory_manager` | ⚪ | Stock management | Stage Week 10 |

### 4.2 Payment Infrastructure (Phase 3: Stage Week 8) `[M:payments]`

**Public Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/payment/:id` | `frm_payment_form` | ⚪ | Payment processing page | Stage Week 8 |
| `/payment/success/:id` | `frm_payment_success` | ⚪ | Payment confirmation | Stage Week 8 |
| `/payment/failed/:id` | `frm_payment_failed` | ⚪ | Payment failure handling | Stage Week 8 |

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/payments` | `frm_payment_dashboard` | ⚪ | Payment overview | Stage Week 8 |
| `/admin/payments/transactions` | `frm_transaction_list` | ⚪ | Transaction history | Stage Week 8 |
| `/admin/payments/refunds` | `frm_refund_manager` | ⚪ | Process refunds | Stage Week 8 |
| `/admin/payments/methods` | `frm_payment_methods` | ⚪ | Customer payment methods | Stage Week 8 |

### 4.3 Invoicing & Subscriptions (Phase 3: Stage Week 10-11) `[M:invoicing]`

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/invoices` | `frm_invoice_manager` | ⚪ | Invoice dashboard | Stage Week 10 |
| `/admin/invoices/new` | `frm_invoice_editor` | ⚪ | Create invoice | Stage Week 10 |
| `/admin/invoices/edit/:id` | `frm_invoice_editor` | ⚪ | Edit invoice | Stage Week 10 |
| `/admin/invoices/:id/preview` | `frm_invoice_preview` | ⚪ | Preview before sending | Stage Week 10 |
| `/admin/subscriptions` | `frm_subscription_manager` | ⚪ | Recurring billing management | Stage Week 10 |

**Public Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/invoice/:token` | `frm_invoice_view` | ⚪ | Customer invoice view | Stage Week 10 |
| `/invoice/:token/pay` | `frm_invoice_payment` | ⚪ | Pay invoice online | Stage Week 10 |

---

## 5. Booking & Operations Routes (Phase 4)

### 5.1 Base Booking System (Phase 4: Stage Week 12) `[M:booking]`

**Public Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/booking` | `frm_booking_interface` | ⚪ | Main booking interface | Stage Week 12 |
| `/booking/availability` | `frm_availability_calendar` | ⚪ | Check availability | Stage Week 12 |
| `/booking/confirm/:id` | `frm_booking_confirmation` | ⚪ | Booking confirmation | Stage Week 12 |
| `/booking/:id` | `frm_booking_details` | ⚪ | Booking details (for customers) | Stage Week 12 |

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/bookings` | `frm_booking_manager` | ⚪ | Booking dashboard | Stage Week 12 |
| `/admin/bookings/calendar` | `frm_booking_calendar` | ⚪ | Calendar view of bookings | Stage Week 12 |
| `/admin/bookings/:id` | `frm_booking_detail` | ⚪ | Individual booking details | Stage Week 12 |
| `/admin/resources` | `frm_resource_manager` | ⚪ | Manage bookable resources | Stage Week 12 |
| `/admin/availability` | `frm_availability_manager` | ⚪ | Set availability rules | Stage Week 12 |

### 5.2 Vertical-Specific Booking Routes

#### Hospitality (Phase 4: Stage Week 13) `[V:hospitality]`

**Public Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/rooms` | `frm_room_catalog` | ⚪ | Room types display | Stage Week 13 |
| `/rooms/:slug` | `frm_room_detail` | ⚪ | Individual room details | Stage Week 13 |
| `/book-room` | `frm_room_booking` | ⚪ | Room booking flow | Stage Week 13 |

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/rooms` | `frm_room_manager` | ⚪ | Room inventory management | Stage Week 13 |
| `/admin/rooms/new` | `frm_room_editor` | ⚪ | Add new room type | Stage Week 13 |
| `/admin/rooms/edit/:id` | `frm_room_editor` | ⚪ | Edit room type | Stage Week 13 |
| `/admin/housekeeping` | `frm_housekeeping` | ⚪ | Housekeeping management | Stage Week 13 |

#### Restaurant (Phase 4: Stage Week 13) `[V:restaurant]`

**Public Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/menu` | `frm_menu_display` | ⚪ | Menu display | Stage Week 13 |
| `/reservations` | `frm_table_reservation` | ⚪ | Table booking | Stage Week 13 |

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/menu` | `frm_menu_manager` | ⚪ | Menu management | Stage Week 13 |
| `/admin/menu/new` | `frm_menu_item_editor` | ⚪ | Add menu item | Stage Week 13 |
| `/admin/menu/edit/:id` | `frm_menu_item_editor` | ⚪ | Edit menu item | Stage Week 13 |
| `/admin/tables` | `frm_table_manager` | ⚪ | Table management | Stage Week 13 |
| `/admin/reservations` | `frm_reservation_manager` | ⚪ | Reservation management | Stage Week 13 |

#### Consulting/Services (Phase 4: Stage Week 13) `[V:consulting]` `[V:physical_services]`

**Public Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/services` | `frm_service_catalog` | ⚪ | Service offerings | Stage Week 13 |
| `/services/:slug` | `frm_service_detail` | ⚪ | Service details | Stage Week 13 |
| `/book-appointment` | `frm_appointment_booking` | ⚪ | Appointment scheduling | Stage Week 13 |

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/services` | `frm_service_manager` | ⚪ | Service management | Stage Week 13 |
| `/admin/appointments` | `frm_appointment_manager` | ⚪ | Appointment calendar | Stage Week 13 |
| `/admin/schedule` | `frm_schedule_manager` | ⚪ | Availability schedule | Stage Week 13 |

### 5.3 Real Estate Routes (Phase 4: Stage Week 14) `[V:real_estate_sales]` `[V:real_estate_rentals]`

**Public Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/properties` | `frm_property_listing` | ⚪ | Property search & listing | Stage Week 14 |
| `/properties/:slug` | `frm_property_detail` | ⚪ | Property details | Stage Week 14 |
| `/properties/:id/schedule-viewing` | `frm_viewing_request` | ⚪ | Schedule property viewing | Stage Week 14 |
| `/properties/:id/apply` | `frm_rental_application` | ⚪ | Rental application `[V:rentals]` | Stage Week 14 |

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/properties` | `frm_property_manager` | ⚪ | Property management | Stage Week 14 |
| `/admin/properties/new` | `frm_property_editor` | ⚪ | Add new property | Stage Week 14 |
| `/admin/properties/edit/:id` | `frm_property_editor` | ⚪ | Edit property | Stage Week 14 |
| `/admin/viewings` | `frm_viewing_manager` | ⚪ | Viewing schedule | Stage Week 14 |
| `/admin/applications` | `frm_application_manager` | ⚪ | Rental applications `[V:rentals]` | Stage Week 14 |
| `/admin/tenants` | `frm_tenant_manager` | ⚪ | Tenant management `[V:rentals]` | Stage Week 14 |

---

## 6. Customer Engagement Routes (Phase 5)

### 6.1 CRM (Phase 5: Stage Week 16) `[M:crm]`

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/customers` | `frm_customer_list` | ⚪ | Customer database | Stage Week 16 |
| `/admin/customers/new` | `frm_customer_editor` | ⚪ | Add new customer | Stage Week 16 |
| `/admin/customers/:id` | `frm_customer_profile` | ⚪ | Customer profile & history | Stage Week 16 |
| `/admin/customers/:id/edit` | `frm_customer_editor` | ⚪ | Edit customer | Stage Week 16 |
| `/admin/customers/:id/notes` | `frm_customer_notes` | ⚪ | Customer notes & communications | Stage Week 16 |
| `/admin/segments` | `frm_segment_manager` | ⚪ | Customer segmentation | Stage Week 16 |

### 6.2 Reviews & Testimonials (Phase 5: Stage Week 17) `[M:reviews]`

**Public Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/reviews` | `frm_review_display` | ⚪ | Public reviews page | Stage Week 17 |
| `/review/:token` | `frm_review_form` | ⚪ | Submit review (via email link) | Stage Week 17 |
| `/testimonials` | `frm_testimonial_display` | ⚪ | Featured testimonials | Stage Week 17 |

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/reviews` | `frm_review_manager` | ⚪ | Review management | Stage Week 17 |
| `/admin/reviews/:id` | `frm_review_detail` | ⚪ | Individual review management | Stage Week 17 |
| `/admin/testimonials` | `frm_testimonial_manager` | ⚪ | Featured testimonials | Stage Week 17 |

### 6.3 Loyalty Programs (Phase 5: Stage Week 18) `[M:loyalty]` `[P:premium]`

**Public Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/loyalty` | `frm_loyalty_info` | ⚪ | Loyalty program information | Stage Week 18 |
| `/loyalty/join` | `frm_loyalty_signup` | ⚪ | Join loyalty program | Stage Week 18 |
| `/loyalty/account` | `frm_loyalty_dashboard` | ⚪ | Customer loyalty dashboard | Stage Week 18 |

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/loyalty` | `frm_loyalty_manager` | ⚪ | Loyalty program management | Stage Week 18 |
| `/admin/loyalty/members` | `frm_loyalty_members` | ⚪ | Member management | Stage Week 18 |
| `/admin/loyalty/rewards` | `frm_reward_manager` | ⚪ | Reward configuration | Stage Week 18 |
| `/admin/loyalty/tiers` | `frm_tier_manager` | ⚪ | Tier management | Stage Week 18 |

### 6.4 Referral Programs (Phase 5: Stage Week 18) `[M:referrals]` `[P:premium]`

**Public Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/referral/:code` | `frm_referral_landing` | ⚪ | Referral landing page | Stage Week 18 |

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/referrals` | `frm_referral_manager` | ⚪ | Referral program dashboard | Stage Week 18 |
| `/admin/referrals/settings` | `frm_referral_settings` | ⚪ | Referral program configuration | Stage Week 18 |

---

## 7. Logistics & Operations Routes (Phase 6)

### 7.1 Shipping & Fulfillment (Phase 6: Stage Week 19) `[V:physical_products]` `[M:shipping]`

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/shipping` | `frm_shipping_dashboard` | ⚪ | Shipping overview | Stage Week 19 |
| `/admin/shipping/zones` | `frm_shipping_zone_manager` | ⚪ | Shipping zone configuration | Stage Week 19 |
| `/admin/shipping/rates` | `frm_shipping_rate_manager` | ⚪ | Shipping rate management | Stage Week 19 |
| `/admin/shipping/carriers` | `frm_carrier_manager` | ⚪ | Carrier integration | Stage Week 19 |
| `/admin/fulfillment` | `frm_fulfillment_queue` | ⚪ | Order fulfillment queue | Stage Week 19 |

**Public Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/track/:tracking_number` | `frm_tracking_display` | ⚪ | Package tracking (public) | Stage Week 19 |

### 7.2 Staff Management (Phase 6: Stage Week 20) `[M:staff]` `[P:premium]`

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/staff` | `frm_staff_manager` | ⚪ | Staff directory | Stage Week 20 |
| `/admin/staff/new` | `frm_staff_editor` | ⚪ | Add staff member | Stage Week 20 |
| `/admin/staff/:id` | `frm_staff_profile` | ⚪ | Staff profile | Stage Week 20 |
| `/admin/staff/:id/schedule` | `frm_staff_schedule` | ⚪ | Staff scheduling | Stage Week 20 |
| `/admin/staff/:id/permissions` | `frm_staff_permissions` | ⚪ | Role & permission management | Stage Week 20 |
| `/admin/shifts` | `frm_shift_manager` | ⚪ | Shift scheduling | Stage Week 20 |

### 7.3 Tasks & Operations (Phase 6: Stage Week 21) `[M:operations]`

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/tasks` | `frm_task_manager` | ⚪ | Task management system | Stage Week 21 |
| `/admin/tasks/new` | `frm_task_editor` | ⚪ | Create task | Stage Week 21 |
| `/admin/tasks/:id` | `frm_task_detail` | ⚪ | Task details | Stage Week 21 |
| `/admin/workflows` | `frm_workflow_manager` | ⚪ | Automated workflow configuration | Stage Week 21 |
| `/admin/checklists` | `frm_checklist_manager` | ⚪ | Checklist templates | Stage Week 21 |

---

## 8. Analytics & Reporting Routes (Phase 7)

### 8.1 Core Analytics (Phase 7: Stage Week 22) `[M:analytics]`

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/analytics` | `frm_analytics_dashboard` | ⚪ | Analytics overview | Stage Week 22 |
| `/admin/analytics/revenue` | `frm_revenue_analytics` | ⚪ | Revenue reporting | Stage Week 22 |
| `/admin/analytics/customers` | `frm_customer_analytics` | ⚪ | Customer insights | Stage Week 22 |
| `/admin/analytics/bookings` | `frm_booking_analytics` | ⚪ | Booking analysis | Stage Week 22 |
| `/admin/analytics/website` | `frm_website_analytics` | ⚪ | Website traffic | Stage Week 22 |

### 8.2 Reports (Phase 7: Stage Week 22) `[M:reports]`

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/reports` | `frm_report_library` | ⚪ | Report templates | Stage Week 22 |
| `/admin/reports/custom` | `frm_custom_report_builder` | ⚪ | Custom report builder | Stage Week 22 |
| `/admin/reports/:id` | `frm_report_viewer` | ⚪ | View generated report | Stage Week 22 |
| `/admin/reports/:id/export` | (download action) | ⚪ | Export report (PDF/CSV) | Stage Week 22 |

---

## 8.3 Compliance & Admin Tools (Phase 6.5: Stages 22-25) `[R:admin]`

**Admin Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/admin/audit-log` | `frm_audit_log` | ⚪ | Security audit trail viewer | Stage 24 |
| `/admin/data-export` | `frm_data_export` | ⚪ | GDPR data export tool | Stage 23 |
| `/admin/data-requests` | `frm_data_requests` | ⚪ | GDPR request management | Stage 23 |
| `/admin/storage` | `frm_storage_dashboard` | ⚪ | Storage usage monitoring | Stage 24 |
| `/admin/webhooks` | `frm_webhook_log` | ⚪ | Webhook event log | Stage 8 |
| `/admin/backups` | `frm_backup_log` | ⚪ | Backup status & history | Stage 24 |

---

## 9. API & Webhook Routes (All Phases)

### 9.1 Payment Webhooks (Phase 3: Stage Week 8)

| Route | Method | Status | Description | Phase |
|-------|--------|--------|-------------|-------|
| `/webhooks/stripe` | POST | ⚪ | Stripe webhook handler | Stage Week 8 |
| `/webhooks/paypal` | POST | ⚪ | PayPal IPN handler | Stage Week 8 |

### 9.2 Integration APIs (Phase 7: Stage Week 23)

| Route | Method | Status | Description | Phase |
|-------|--------|--------|-------------|-------|
| `/api/v1/bookings` | GET | ⚪ | Get bookings (read-only) | Stage Week 23 |
| `/api/v1/customers` | GET | ⚪ | Get customers (read-only) | Stage Week 23 |
| `/api/v1/products` | GET | ⚪ | Get products (read-only) | Stage Week 23 |
| `/api/v1/webhooks/register` | POST | ⚪ | Register webhook endpoint | Stage Week 23 |

---

## 10. Onboarding & Setup Routes (Phase 1 & 8)

### 10.1 Initial Setup Wizard (Phase 1: Stage Week 4 + Phase 8: Stage Week 17)

**Onboarding Routes:**
| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/setup/welcome` | `frm_setup_welcome` | ⚪ | Welcome & vertical selection | Stage Week 4 |
| `/setup/business-info` | `frm_setup_business` | ⚪ | Business information | Stage Week 4 |
| `/setup/branding` | `frm_setup_branding` | ⚪ | Branding setup | Stage Week 4 |
| `/setup/modules` | `frm_setup_modules` | ⚪ | Feature module selection | Stage Week 4 |
| `/setup/content` | `frm_setup_content` | ⚪ | Initial content setup | Stage Week 17 |
| `/setup/inventory` | `frm_setup_inventory` | ⚪ | Inventory setup (vertical-specific) | Stage Week 17 |
| `/setup/integrations` | `frm_setup_integrations` | ⚪ | Integration configuration | Stage Week 17 |
| `/setup/review` | `frm_setup_review` | ⚪ | Review & launch | Stage Week 17 |

---

## 11. Error & Utility Routes (Phase 1)

### 11.1 Error Pages (Phase 1: Stage Week 4)

| Route | Form Name | Status | Description | Phase |
|-------|-----------|--------|-------------|-------|
| `/404` | `frm_404` | ⚪ | Page not found | Stage Week 4 |
| `/403` | `frm_403` | ⚪ | Access denied | Stage Week 4 |
| `/500` | `frm_500` | ⚪ | Server error | Stage Week 4 |
| `/maintenance` | `frm_maintenance` | ⚪ | Maintenance mode page | Stage Week 4 |

---

## Route Count Summary (Planning Phase)

| Category | Count | Status |
|----------|-------|--------|
| **Authentication** | 4 | ⚪ Not Started |
| **Core Admin** | 7 | ⚪ Not Started |
| **Public Pages (Core)** | 5 | ⚪ Not Started |
| **Website Settings** | 6 | ⚪ Not Started |
| **Feature Pages (Public)** | 8 | ⚪ Not Started |
| **Landing Pages** | 5 | ⚪ Not Started |
| **Contact & Leads Admin** | 2 | ⚪ Not Started |
| **Blog Routes** | 9 | ⚪ Not Started |
| **Email Marketing** | 7 | ⚪ Not Started |
| **Campaigns** | 6 | ⚪ Not Started |
| **Social Media** | 2 | ⚪ Not Started |
| **E-commerce** | 15 | ⚪ Not Started |
| **Payments** | 7 | ⚪ Not Started |
| **Invoicing** | 7 | ⚪ Not Started |
| **Booking (Base)** | 10 | ⚪ Not Started |
| **Hospitality** | 8 | ⚪ Not Started |
| **Restaurant** | 8 | ⚪ Not Started |
| **Consulting/Services** | 8 | ⚪ Not Started |
| **Real Estate** | 11 | ⚪ Not Started |
| **CRM** | 7 | ⚪ Not Started |
| **Reviews** | 6 | ⚪ Not Started |
| **Loyalty** | 7 | ⚪ Not Started |
| **Referrals** | 3 | ⚪ Not Started |
| **Shipping** | 6 | ⚪ Not Started |
| **Staff Management** | 7 | ⚪ Not Started |
| **Tasks & Operations** | 6 | ⚪ Not Started |
| **Analytics** | 5 | ⚪ Not Started |
| **Reports** | 4 | ⚪ Not Started |
| **APIs & Webhooks** | 6 | ⚪ Not Started |
| **Onboarding** | 8 | ⚪ Not Started |
| **Error Pages** | 4 | ⚪ Not Started |
| **TOTAL** | **207+ routes** | |

**New in v4.0:**
- Added 5 core public pages (homepage templates, about, contact, privacy, terms)
- Added 6 website settings admin routes
- Added 8 feature-dependent public pages (services, shop, rooms, booking, membership)
- Added 5 landing page routes (1 public + 4 admin)
- Added 2 contact & leads management routes
- **Total increase: 26 routes**

---

## Update Log

| Date | Developer | Changes | Phase |
|------|-----------|---------|-------|
| 2025-12-30 | Dev Team | Initial sitemap created from planning docs | Planning |
| 2026-01-18 | AI + Founder | Added routing implementation guide and architecture integration | Phase 1-5 |
| 2026-01-19 | AI + Founder | Added website and landing pages routes (26 new routes). Updated public pages structure. Added homepage templates, about, contact, privacy, terms pages. Added landing page system with 5 templates. Added website settings admin routes. Updated route count from 181 to 207+. | Phase 2 |

---

## Notes

1. **Conditional Routes:** Many routes are conditional based on:
   - Vertical selection (e.g., `/rooms` only for hospitality)
   - Active modules (e.g., `/admin/campaigns` only if email module active)
   - Package tier (e.g., loyalty features only on premium)

2. **Dynamic Segments:** Routes with `:id`, `:slug`, `:token` are dynamic and handle multiple entities

3. **API Routes:** Phase 7 (Stage Week 23) includes read-only API for integrations

4. **Maintenance:** Update this document at the end of each phase before starting the next

5. **Landing Pages:** Use BlankLayout (no navigation) to maximize conversions. Public route `/landing/:slug` with 5 template types.

6. **Homepage Templates:** 7 template options (Classic, E-commerce, Hospitality, Services, Membership, Booking, Minimalist) configured via `/admin/settings/website/homepage`

---

*This sitemap is a living document. Update route statuses as forms are built and tested.*
