---
description: "06_database_schema.md - Mybizz database schema"
globs: ["**/*"]
alwaysApply: true
---


# Mybizz Platform - Database Schema v11.0

**Document Version:** 11.0  
**Date:** January 26, 2026  
**Status:** Active for V1.x Development  
**UI Compliance:** Material Design 3 (M3) - References aligned with v11+ system docs  
**Total Tables:** 57 (46 existing + 7 CRM/Marketing + 3 Website/Landing Pages + 1 Security)  #Changed  
**Reference:** Aligned with 01_conceptual_design.md, 04_architecture_specification.md  
**Change Tracking:** Lines marked with #New or #Changed indicate updates

---

## IMPORTANT: Anvil Data Tables Reality  #New

**How Anvil Handles Row IDs:**  #New
- Every row automatically has a built-in unique ID via `row.get_id()`  #New
- Returns tuple like `[table_id, row_id]` - e.g., `[169162, 297786594]`  #New
- NO "auto", "lnumber", or "auto-increment" column types exist in Anvil  #New
- String ID columns (contact_id, event_id, etc.) must be manually populated if used  #New
- Best practice: Use `row.get_id()` for internal references, only create ID columns for user-visible IDs  #New

**Anvil Column Types:**  #New
- `string` - Text  #New
- `number` - Numbers (int/float)  #New
- `bool` - True/False  #New
- `date` - Date only  #New
- `datetime` - Date and Time  #New
- `simpleObject` - JSON data (dict/list)  #New
- `media` - Files  #New
- `link_single` - Link to one row in another table  #New
- `link_multiple` - Link to multiple rows  #New

**Reference:** See `anvil_cop_data_tables.md` for complete standards.  #New

---

## Schema Overview

| Category | Tables | Purpose |
|----------|--------|---------|
| Core | 1-6 | Files, users, activity, config |
| Bookings | 7-12 | Resources, availability, bookings, services |
| E-commerce | 13-20 | Products, cart, orders, shipments |
| Customers | 21-23 | CRM, notes, memberships |
| Content | 24-27 | Blog, pages, reviews |
| Support | 28-31 | Tickets, KB articles |
| Finance | 32-35 | Invoices, subscriptions, expenses |
| Integration | 36-42 | Email, payments, couriers, webhooks |
| CRM & Marketing | 47-53 | Contacts, campaigns, segments, tasks, lead capture |  #Changed
| Website & Landing Pages | 54-56 | Landing pages, contact forms, leads |  #New

---

## DATABASE TABLES

### CORE TABLES (1-6)

1 ☰ **files** (files) - Client: No access, Server: Full access
  - path - text
  - file - media
  - file_version - text
	
2 ☰ **users** (users) - Client: No access, Server: Full access
  - email - string
  - enabled - bool
  - last_login - datetime
  - password_hash - string
  - n_password_failures - number
  - confirmed_email - bool
  - role - string (owner, manager, admin, staff, customer, visitor)
  - account_status - string (active, suspended, deleted)
  - phone - string
  - permissions - simple_object
  - created_at - datetime
  
3 ☰ **activity_log** (activity_log) - Client: No access, Server: Full access
  - user_id - link to users
  - action_type - string
  - description - string
  - ip_address - string
  - metadata - simple_object
  - created_at - datetime

4 ☰ **config** (config) - Client: No access, Server: Full access
  - key - string
  - value - simple_object
  - category - string (system, features, currency, theme)
  - updated_at - datetime
  - updated_by - link to users
  - **Note:** Stores system_currency (IMMUTABLE), display_currency, exchange_rate, enabled_features

5 ☰ **business_profile** (business_profile) - Client: No access, Server: Full access
  - business_name - string
  - description - text
  - logo - media
  - contact_email - string
  - phone - string
  - address - text
  - website_url - string
  - social_facebook - string
  - social_instagram - string
  - social_x - string
  - social_linkedin - string
  - created_at - datetime
  - updated_at - datetime

6 ☰ **theme_config** (theme_config) - Client: No access, Server: Full access
  - primary_color - string (hex code)
  - accent_color - string (hex code)
  - font_family - string
  - header_style - string
  - updated_at - datetime

---

### BOOKING TABLES (7-12)

7 ☰ **bookable_resources** (bookable_resources) - Client: No access, Server: Full access
  - resource_id - string
  - name - string
  - resource_type - string (room, staff, equipment, space, table)
  - description - text
  - capacity - number
  - hourly_rate - number
  - daily_rate - number
  - metadata - simple_object
  - is_active - bool
  - created_at - datetime

8 ☰ **availability_rules** (availability_rules) - Client: No access, Server: Full access
  - resource_id - link to bookable_resources
  - day_of_week - number (0=Sunday, 6=Saturday)
  - start_time - string (HH:MM)
  - end_time - string (HH:MM)
  - is_active - bool

9 ☰ **availability_exceptions** (availability_exceptions) - Client: No access, Server: Full access
  - resource_id - link to bookable_resources
  - exception_date - date
  - start_time - string
  - end_time - string
  - is_available - bool
  - reason - string

10 ☰ **booking_metadata_schemas** (booking_metadata_schemas) - Client: No access, Server: Full access
  - schema_name - string
  - booking_type - string (room, appointment, service, event, table)
  - field_definitions - simple_object
  - is_active - bool

11 ☰ **bookings** (bookings) - Client: No access, Server: Full access
  - booking_id - string
  - booking_number - string (BK-YYYYMMDD-NNN)
  - customer_id - link to customers
  - contact_id - link to tbl_contacts
  - resource_id - link to bookable_resources
  - service_id - link to services
  - booking_type - string (room, appointment, service, event, table)
  - status - string (pending, confirmed, checked_in, completed, cancelled, no_show)
  - start_datetime - datetime
  - end_datetime - datetime
  - total_price - number
  - payment_status - string (unpaid, deposit_paid, paid, refunded)
  - payment_id - string (gateway transaction ID)
  - check_in_time - datetime
  - check_out_time - datetime
  - num_guests - number
  - special_requests - text
  - metadata - simple_object
  - created_at - datetime
  - updated_at - datetime

12 ☰ **services** (services) - Client: No access, Server: Full access
  - service_id - string
  - name - string
  - description - text
  - duration_minutes - number
  - price - number
  - category - string
  - provider_id - link to users
  - meeting_type - string (in_person, video, phone)
  - is_active - bool
  - created_at - datetime

---

### E-COMMERCE TABLES (13-20)

13 ☰ **product_categories** (product_categories) - Client: No access, Server: Full access
  - category_id - string
  - name - string
  - slug - string
  - description - text
  - parent_category_id - link to product_categories
  - sort_order - number

14 ☰ **products** (products) - Client: No access, Server: Full access
  - product_id - string
  - name - string
  - slug - string
  - description - text
  - price - number (system currency)
  - display_price - number (display currency, nullable)
  - compare_at_price - number
  - cost - number
  - sku - string
  - stock_quantity - number
  - low_stock_threshold - number (default 5)
  - track_inventory - bool
  - product_type - string (physical, digital, service)
  - category_id - link to product_categories
  - images - simple_object (array of URLs)
  - featured_image - media
  - digital_file - media (for digital products)
  - is_active - bool
  - created_at - datetime
  - updated_at - datetime

15 ☰ **product_variants** (product_variants) - Client: No access, Server: Full access
  - product_id - link to products
  - variant_name - string
  - sku - string
  - price_adjustment - number
  - stock_quantity - number

16 ☰ **cart** (cart) - Client: No access, Server: Full access
  - customer_id - link to users
  - session_id - string (for guest carts)
  - created_at - datetime
  - updated_at - datetime

17 ☰ **cart_items** (cart_items) - Client: No access, Server: Full access
  - cart_id - link to cart
  - product_id - link to products
  - variant_id - link to product_variants
  - quantity - number
  - price_at_add - number
  - added_at - datetime

18 ☰ **orders** (orders) - Client: No access, Server: Full access
  - order_id - string
  - order_number - string (ORD-YYYYMMDD-NNN)
  - customer_id - link to customers
  - contact_id - link to tbl_contacts
  - status - string (pending, processing, shipped, delivered, cancelled)
  - payment_status - string (pending, paid, failed, refunded)
  - payment_method - string
  - payment_gateway - string (stripe, paystack, paypal)
  - gateway_transaction_id - string
  - subtotal - number
  - tax - number
  - shipping_cost - number
  - total - number
  - currency - string
  - shipping_address - simple_object
  - billing_address - simple_object
  - notes - text
  - created_at - datetime
  - updated_at - datetime

19 ☰ **order_items** (order_items) - Client: No access, Server: Full access
  - order_id - link to orders
  - product_id - link to products
  - variant_id - link to product_variants
  - product_name - string (snapshot at purchase)
  - variant_name - string
  - quantity - number
  - unit_price - number
  - line_total - number

20 ☰ **shipments** (shipments) - Client: No access, Server: Full access
  - shipment_id - string
  - order_id - link to orders
  - shipment_number - string
  - courier_provider - string (manual, bobgo, easyship)
  - courier_name - string (for manual: "FedEx", "DHL", etc.)
  - tracking_number - string
  - tracking_url - string
  - shipping_cost - number
  - shipped_date - datetime
  - estimated_delivery - datetime
  - delivery_status - string (pending, in_transit, delivered)
  - label_url - string (PDF waybill URL)
  - created_at - datetime
  - updated_at - datetime

---

### CUSTOMER TABLES (21-23)

21 ☰ **customers** (customers) - Client: No access, Server: Full access
  - customer_id - string
  - user_id - link to users
  - contact_id - link to tbl_contacts
  - first_name - string
  - last_name - string
  - email - string
  - phone - string
  - address - simple_object
  - notes - text
  - tags - simple_object
  - lifetime_value - number
  - total_bookings - number
  - total_orders - number
  - status - string (active, inactive)
  - created_at - datetime
  - updated_at - datetime

22 ☰ **client_notes** (client_notes) - Client: No access, Server: Full access
  - customer_id - link to customers
  - author_id - link to users
  - note_text - text
  - note_type - string
  - is_confidential - bool (RBAC restricted)
  - is_important - bool
  - created_at - datetime

23 ☰ **membership_tiers** (membership_tiers) - Client: No access, Server: Full access
  - tier_id - string
  - name - string
  - description - text
  - price_monthly - number
  - price_quarterly - number
  - price_annual - number
  - benefits - simple_object (array of benefit strings)
  - access_rules - simple_object
  - sort_order - number
  - is_active - bool
  - created_at - datetime

---

### CONTENT TABLES (24-27)

24 ☰ **blog_categories** (blog_categories) - Client: No access, Server: Full access
  - category_id - string
  - name - string
  - slug - string
  - description - text

25 ☰ **blog_posts** (blog_posts) - Client: No access, Server: Full access
  - post_id - string
  - title - string
  - slug - string
  - content - text
  - excerpt - text
  - featured_image - media
  - author_id - link to users
  - category_id - link to blog_categories
  - status - string (draft, published, archived)
  - view_count - number
  - published_at - datetime
  - created_at - datetime
  - updated_at - datetime

26 ☰ **pages** (pages) - Client: No access, Server: Full access
  - page_name - string (home, about, services, contact)
  - page_title - string
  - slug - string
  - components - simple_object (JSON array of component definitions)
  - is_published - bool
  - view_count - number
  - created_at - datetime
  - updated_at - datetime

27 ☰ **reviews** (reviews) - Client: No access, Server: Full access
  - review_id - string
  - item_type - string (product, booking, service, business)
  - item_id - string
  - customer_id - link to customers
  - reviewer_name - string
  - rating - number (1-5)
  - title - string
  - comment - text
  - photos - simple_object (array of URLs)
  - is_verified_purchase - bool
  - status - string (pending, approved, rejected, spam)
  - business_response - text
  - response_at - datetime
  - helpful_count - number
  - reported_count - number
  - created_at - datetime

---

### SUPPORT TABLES (28-31)

28 ☰ **kb_categories** (kb_categories) - Client: No access, Server: Full access
  - category_id - string
  - name - string
  - slug - string
  - icon - string
  - description - text
  - sort_order - number
  - created_at - datetime

29 ☰ **kb_articles** (kb_articles) - Client: No access, Server: Full access
  - article_id - string
  - category_id - link to kb_categories
  - title - string
  - slug - string
  - content - text
  - excerpt - text
  - keywords - simple_object (array for chatbot matching)
  - view_count - number
  - helpful_count - number
  - unhelpful_count - number
  - is_published - bool
  - created_at - datetime
  - updated_at - datetime

30 ☰ **tickets** (tickets) - Client: No access, Server: Full access
  - ticket_id - string
  - ticket_number - string (TKT-YYYYMMDD-NNN)
  - customer_id - link to customers
  - customer_name - string (for guests)
  - customer_email - string
  - subject - string
  - description - text
  - category - string (general, billing, technical, complaint)
  - status - string (open, in_progress, resolved, closed)
  - priority - string (low, medium, high, urgent)
  - assigned_to - link to users
  - resolved_at - datetime
  - last_reply_at - datetime
  - created_at - datetime
  - updated_at - datetime

31 ☰ **ticket_messages** (ticket_messages) - Client: No access, Server: Full access
  - ticket_id - link to tickets
  - author_id - link to users
  - author_type - string (customer, staff)
  - message - text
  - is_internal_note - bool
  - attachments - simple_object (array of URLs)
  - created_at - datetime

---

### FINANCE TABLES (32-35)

32 ☰ **invoices** (invoices) - Client: No access, Server: Full access
  - invoice_id - string
  - invoice_number - string (INV-YYYYMMDD-NNN)
  - customer_id - link to customers
  - order_id - link to orders (nullable)
  - subscription_id - link to subscriptions (nullable)
  - invoice_date - datetime
  - due_date - datetime
  - total_amount - number
  - currency - string
  - status - string (draft, sent, paid, overdue, cancelled)
  - paid_at - datetime
  - payment_method - string
  - payment_id - string
  - pdf_url - string
  - notes - text
  - created_at - datetime

33 ☰ **invoice_items** (invoice_items) - Client: No access, Server: Full access
  - invoice_id - link to invoices
  - description - string
  - quantity - number
  - unit_price - number
  - amount - number

34 ☰ **subscriptions** (subscriptions) - Client: No access, Server: Full access
  - subscription_id - string
  - subscription_number - string (SUB-YYYYMMDD-NNN)
  - customer_id - link to customers
  - tier_id - link to membership_tiers
  - plan_name - string
  - billing_amount - number
  - billing_interval - string (monthly, quarterly, yearly)
  - currency - string
  - status - string (active, paused, cancelled, past_due)
  - start_date - datetime
  - end_date - datetime
  - next_billing_date - datetime
  - payment_gateway - string (stripe, paystack)
  - gateway_subscription_id - string
  - auto_renew - bool
  - created_at - datetime
  - updated_at - datetime
  - **Note:** PayPal cannot handle subscriptions (one-time only)

35 ☰ **expenses** (expenses) - Client: No access, Server: Full access
  - expense_id - string
  - expense_date - date
  - category - string (supplies, software, advertising, other)
  - description - string
  - amount - number
  - currency - string
  - receipt - media
  - created_by - link to users
  - created_at - datetime

---

### INTEGRATION TABLES (36-42)

36 ☰ **email_config** (email_config) - Client: No access, Server: Full access
  - email_provider - string (zoho)
  - smtp_host - string
  - smtp_port - number
  - smtp_username - string (encrypted)
  - smtp_password - string (encrypted via Secrets)
  - from_email - string
  - from_name - string
  - configured - bool
  - configured_at - datetime
  - **Note:** Zoho Workplace Free provides 5 business emails

37 ☰ **email_templates** (email_templates) - Client: No access, Server: Full access
  - template_id - string
  - name - string (booking_confirmation, order_receipt, etc.)
  - subject - string (supports {{variables}})
  - body_html - text
  - body_text - text
  - template_type - string (transactional, notification)
  - is_active - bool

38 ☰ **email_log** (email_log) - Client: No access, Server: Full access
  - recipient - string
  - subject - string
  - template_id - link to email_templates
  - status - string (sent, failed, bounced)
  - error_message - text
  - sent_at - datetime

39 ☰ **payment_config** (payment_config) - Client: No access, Server: Full access
  - active_gateway - string (stripe, paystack, paypal)
  - stripe_publishable_key - string (encrypted)
  - stripe_secret_key - string (encrypted via Secrets)
  - stripe_connected - bool
  - paystack_public_key - string (encrypted)
  - paystack_secret_key - string (encrypted via Secrets)
  - paystack_connected - bool
  - paypal_client_id - string (encrypted)
  - paypal_secret - string (encrypted via Secrets)
  - paypal_connected - bool
  - test_mode - bool
  - configured_at - datetime
  - **Note:** PayPal for one-time payments only (not subscriptions)

40 ☰ **courier_config** (courier_config) - Client: No access, Server: Full access
  - bobgo_api_key - string (encrypted via Secrets)
  - bobgo_enabled - bool
  - easyship_api_key - string (encrypted via Secrets)
  - easyship_enabled - bool
  - default_origin_address - simple_object
  - configured_at - datetime
  - **Note:** Bob Go for SA, Easyship for International

41 ☰ **webhook_log** (webhook_log) - Client: No access, Server: Full access
  - gateway - string (stripe, paystack, bobgo, easyship)
  - event_type - string
  - payload - simple_object
  - signature - string
  - verified - bool
  - processed - bool
  - error_message - text
  - received_at - datetime

42 ☰ **backups** (backups) - Client: No access, Server: Full access
  - backup_id - string
  - backup_type - string (weekly, pre_update_snapshot)
  - backup_date - datetime
  - backup_size - number (bytes)
  - backup_url - string
  - retention_days - number
  - created_at - datetime

---

## Additional Tables (Events & Time Tracking)

43 ☰ **events** (events) - Client: No access, Server: Full access
  - event_id - string
  - title - string
  - description - text
  - event_date - datetime
  - end_date - datetime
  - location - string
  - capacity - number
  - price_per_person - number
  - status - string (upcoming, in_progress, completed, cancelled)
  - created_at - datetime

44 ☰ **event_registrations** (event_registrations) - Client: No access, Server: Full access
  - registration_id - string
  - event_id - link to events
  - customer_id - link to customers
  - num_attendees - number
  - total_paid - number
  - payment_status - string
  - registration_date - datetime

45 ☰ **time_entries** (time_entries) - Client: No access, Server: Full access
  - entry_id - string
  - customer_id - link to customers
  - staff_id - link to users
  - service_id - link to services
  - booking_id - link to bookings
  - start_time - datetime
  - end_time - datetime
  - duration_hours - number
  - hourly_rate - number
  - total_amount - number
  - description - text
  - is_billable - bool
  - is_invoiced - bool
  - created_at - datetime

46 ☰ **guestbook_entries** (guestbook_entries) - Client: No access, Server: Full access
  - entry_id - string
  - customer_id - link to customers
  - booking_id - link to bookings
  - guest_name - string
  - guest_email - string
  - rating - number (1-5)
  - comment - text
  - is_approved - bool
  - is_public - bool
  - created_at - datetime

---

### CRM & MARKETING TABLES (47-53)

47 ☰ **tbl_contacts** (contacts) - Client: No access, Server: Full access
  - contact_id - string (Format: C-{number}, auto-generated via counter, indexed)  #Changed
    * Generated by contact_service.generate_contact_id()
    * Sequential, human-readable (e.g., C-1, C-2, C-453)
    * Used for customer support, admin reference
    * Implementation: 11_crm_server_implementation_reference.md Section 3.2
  - instance_id - link_single to users
  - first_name - string
  - last_name - string
  - email - string (can be null for walk-in customers, indexed)
  - phone - string
  - status - string (Lead, Customer, Inactive)
  - source - string (Website Form, Booking Widget, Manual Entry, etc.)
  - date_added - datetime
  - last_contact_date - datetime
  - total_spent - number
  - total_transactions - number
  - average_order_value - number
  - lifecycle_stage - string (New, Active, At Risk, Lost)
  - tags - simpleObject  #Changed
  - internal_notes - string  #Changed
  - preferences - simpleObject  #Changed
  - created_at - datetime
  - updated_at - datetime
  
  Note: Use row.get_id() for internal technical ID. contact_id for human-friendly reference.  #Changed

47a ☰ **tbl_contact_counter** (contact_counter) - Client: No access, Server: Full access  #New
  - value - number (Sequential counter, starts at 0)  #New
  
  Purpose: Thread-safe contact ID generation. Single row table.  #New
  Initialization: Create with one row: {'value': 0} during app setup  #New
  Usage: Increment via @in_transaction decorator in generate_contact_id()  #New
  Reference: 11_crm_server_implementation_reference.md Section 3.2  #New

48 ☰ **tbl_contact_events** (contact_events) - Client: No access, Server: Full access
  - event_id - string (Optional user-visible ID - must be manually populated)  #Changed
  - contact_id - link_single to contacts  #Changed
  - event_type - string (booking, order, email_opened, email_clicked, note, form_submit, etc.)
  - event_date - datetime
  - event_data - simpleObject  #Changed
  - related_id - string (booking_id, order_id, campaign_id, etc.)
  - user_visible - bool
  
  Note: Use row.get_id() for internal ID. Column name is contact_id (not contact) per anvil.yaml.  #New

49 ☰ **tbl_email_campaigns** (email_campaigns) - Client: No access, Server: Full access
  - campaign_id - string (Optional user-visible ID - must be manually populated)  #Changed
  - instance_id - link_single to users  #Changed
  - campaign_name - string
  - campaign_type - string (Abandoned_Cart, Welcome, Re_engagement, etc.)
  - status - string (Active, Paused, Completed)
  - emails_sent - number
  - opens - number
  - clicks - number
  - conversions - number
  - revenue_generated - number
  - created_date - datetime
  - last_run_date - datetime
  - campaign_settings - simpleObject  #Changed
  
  Note: Use row.get_id() for internal ID. campaign_id is optional for user-facing display.  #New

50 ☰ **tbl_contact_campaigns** (contact_campaigns) - Client: No access, Server: Full access
  - id - string (Optional user-visible ID - must be manually populated)  #Changed
  - contact_id - link_single to contacts  #Changed
  - campaign_id - link_single to email_campaigns  #Changed
  - sequence_day - number
  - status - string (Active, Completed, Unsubscribed)
  - enrolled_date - datetime
  - last_email_sent_date - datetime
  - completed_date - datetime
  
  Note: Column names are contact_id and campaign_id (not contact/campaign) per anvil.yaml.  #New

51 ☰ **tbl_segments** (segments) - Client: No access, Server: Full access
  - segment_id - string (Optional user-visible ID - must be manually populated)  #Changed
  - instance_id - link_single to users  #Changed
  - segment_name - string
  - segment_type - string (Pre_Built, Custom)
  - filter_criteria - simpleObject  #Changed
  - contact_count - number
  - is_active - bool
  - created_date - datetime
  
  Note: Use row.get_id() for internal ID. segment_id is optional for user-facing display.  #New

52 ☰ **tbl_tasks** (tasks) - Client: No access, Server: Full access
  - task_id - string (Optional user-visible ID - must be manually populated)  #Changed
  - instance_id - link_single to users  #Changed
  - contact_id - link_single to contacts (nullable)  #Changed
  - task_title - string
  - task_type - string (follow_up, review_request, custom, etc.)
  - due_date - date
  - completed - bool
  - completed_date - datetime
  - notes - string  #Changed
  - auto_generated - bool
  - created_at - datetime
  
  Note: Use row.get_id() for internal ID. Column name is contact_id (not contact) per anvil.yaml.  #New

53 ☰ **tbl_lead_captures** (lead_captures) - Client: No access, Server: Full access
  - capture_id - string (Optional user-visible ID - must be manually populated)  #Changed
  - instance_id - link_single to users  #Changed
  - capture_name - string
  - capture_type - string (exit_intent, timed, scroll)
  - trigger_settings - simpleObject  #Changed
  - form_fields - simpleObject  #Changed
  - offer_text - string  #Changed
  - status - string (Active, Paused)
  - captures_count - number
  - conversions_count - number
  - created_date - datetime
  
  Note: Use row.get_id() for internal ID. capture_id is optional for user-facing display.  #New


### WEBSITE & LANDING PAGES TABLES (54-56)  #New

54 ☰ **tbl_landing_pages** (landing_pages) - Client: No access, Server: Full access  #New
  - title - string (Internal name)  #New
  - slug - string (URL slug, unique per client)  #New
  - template_type - string (lead_capture, product_launch, event, vsl, membership)  #New
  - config - simpleObject (Template-specific configuration JSON)  #New
  - status - string (draft, published, archived)  #New
  - created_date - datetime  #New
  - published_date - datetime  #New
  - views_count - number  #New
  - conversions_count - number  #New
  - client_id - link_single to users  #New
  
  Note: Use row.get_id() for internal ID. Slug must be unique per client. URL: /landing/:slug  #New

55 ☰ **tbl_contact_submissions** (contact_submissions) - Client: No access, Server: Full access  #New
  - name - string  #New
  - email - string  #New
  - phone - string  #New
  - message - string  #New
  - submitted_date - datetime  #New
  - status - string (new, read, replied)  #New
  - client_id - link_single to users  #New
  
  Note: Use row.get_id() for internal ID. Captures contact form submissions from public website.  #New

56 ☰ **tbl_leads** (leads) - Client: No access, Server: Full access  #New
  - email - string  #New
  - name - string (optional)  #New
  - phone - string (optional)  #New
  - source - string (landing_page, contact_form, other)  #New
  - landing_page_id - link_single to landing_pages (optional)  #New
  - captured_date - datetime  #New
  - status - string (new, contacted, converted, lost)  #New
  - client_id - link_single to users  #New
  
  Note: Use row.get_id() for internal ID. Captures leads from landing pages and contact forms.  #New
  Note: Column name is landing_page_id (not landing_page) per Anvil conventions.  #New

### SECURITY TABLES (57)  #New

57 ☰ **tbl_rate_limits** (rate_limits) - Client: No access, Server: Full access  #New
  - identifier - string (indexed) - User ID or IP address  #New
  - count - number - Request count in current window  #New
  - reset_time - datetime - When current window expires  #New
  - last_request - datetime - Timestamp of most recent request  #New
  
  Purpose: Persistent rate limiting for API security  #New
  Implementation: 10_ref_security_compliance.md Section 1.3  #New
  Cleanup: Background task deletes records older than 24 hours  #New
  Note: Survives server restarts, works across multi-server environment  #New

---

## Schema Notes

### Currency Handling
- **system_currency** stored in config table - IMMUTABLE after first transaction
- **display_currency** optional for customer-facing prices
- **exchange_rate** manual entry, stored in config
- All monetary amounts stored in system currency, display_price fields for optional secondary currency

### Payment Gateway Support
- **Stripe** - Global markets, supports subscriptions
- **Paystack** - African markets (SA, Nigeria, Ghana, Kenya), supports subscriptions
- **PayPal** - One-time payments only, cannot handle recurring subscriptions

### Courier Integration
- **Bob Go** - South African market (The Courier Guy, Dawn Wing, Aramex, DPD)
- **Easyship** - International (DHL, FedEx, UPS, postal services)
- **Manual** - Always available as fallback

### Email Tiers
- **Tier 1:** Anvil (system emails, Mybizz → Client)
- **Tier 2:** Zoho (transactional emails, Client → Customer) - INCLUDED
- **Tier 3:** Brevo (marketing emails) - OPTIONAL, future

---

## Document Control

| Version | Date | Changes |
|---------|------|---------|
| 1.0-5.0 | Dec 2025 | Initial schema development |
| 6.0 | 2026-01-14 | 36 tables finalized |
| 7.0 | 2026-01-15 | **FINALIZATION:** Added shipments, courier_config, payment_config, email_config, webhook_log, backups, membership_tiers, invoice_items, business_profile, theme_config. Updated courier references (Bob Go + Easyship). Added PayPal to payment_config (one-time only). Total 46 tables. |
| 8.0 | 2026-01-17 | **CRM & MARKETING INTEGRATION:** Added 7 new tables (47-53) for unified contact management, email campaigns, segmentation, tasks, and lead capture. Modified tables 11 (bookings), 18 (orders), and 21 (customers) to add contact_id link. Total 53 tables. Phase 5 expansion. |

---

**Status:** ✅ FINALIZED for V1.x Development  
**Reference:** Aligned with 01_conceptual_design_v5.md, 03_dev_plan_v7.md, 04_architecture_specification_v5.md

---
# Changes made 01/17/2026:
1. Header Updated

Version: 7.0 → 8.0
Date: January 15, 2026 → January 17, 2026
Total Tables: 42 → 53
Added note about CRM/Marketing integration

2. Modified Existing Tables (Planned - Not Yet Implemented in anvil.yaml)  #Changed

Table 11 (bookings): PENDING - contact_id link to be added  #Changed
Table 18 (orders): PENDING - contact_id link to be added  #Changed
Table 21 (customers): PENDING - contact_id link to be added  #Changed

Note: These modifications are specified in the design but not yet created in Anvil Data Tables.  #New
Will be added during Phase 5 implementation per 03_dev_plan_v7.md Section 5.1.  #New

3. Added 7 New Tables (Tables 47-53) at Bottom

47: tbl_contacts - Unified contact database
48: tbl_contact_events - Activity timeline
49: tbl_email_campaigns - Email campaign definitions
50: tbl_contact_campaigns - Campaign enrollment tracking
51: tbl_segments - Contact segmentation
52: tbl_tasks - Task management
53: tbl_lead_captures - Lead generation forms

## Version 9.0 Changes (January 18, 2026)  #New

1. Corrected All CRM Table Definitions (Tables 47-53)  #New

- Changed all ID columns from "auto" type to "string" type (matches anvil.yaml reality)  #New
- Changed "link to" references to "link_single to" (correct Anvil terminology)  #New
- Changed "simple_object" to "simpleObject" (correct Anvil spelling)  #New
- Changed "text" type to "string" type where applicable (Anvil has no "text" type)  #New
- Added notes explaining Anvil's built-in row.get_id() vs. user-created ID columns  #New
- Added notes clarifying actual column names in anvil.yaml (contact_id vs contact)  #New

2. Added Anvil Reality Section  #New

- Explained how Anvil automatically handles row IDs  #New
- Listed actual Anvil column types (no "auto" or "lnumber")  #New
- Added reference to Code of Practice document  #New

3. Updated Pending Modifications  #New

- Clarified that contact_id links to bookings/orders/customers are not yet implemented  #New
- Marked as PENDING in anvil.yaml  #New

4. Document Control Updated  #New

Added version 9.0 entry with Anvil compliance corrections  #New
Updated reference to v6 conceptual design and Code of Practice  #New
Added change tracking markers (#New, #Changed) throughout  #New

---
## Version 10.0 Changes (January 19, 2026)  #New

1. Added Website & Landing Pages Tables (Tables 54-56)  #New

- Added tbl_landing_pages - Marketing landing pages with analytics tracking  #New
- Added tbl_contact_submissions - Contact form submissions from public website  #New
- Added tbl_leads - Lead capture from landing pages and contact forms  #New
- All tables follow Anvil Data Tables best practices (string IDs, proper link types)  #New

2. Website Configuration Support  #New

- Website configuration (home page templates, about page, contact settings) stored in config table  #New
- Config keys: home_template, home_config, about_config, google_maps_api_key, privacy_policy, terms_conditions  #New
- Social media links already exist in business_profile table (social_facebook, social_instagram, etc.)  #New

3. Integration with Existing Tables  #New

- tbl_leads integrates with tbl_landing_pages via landing_page_id link  #New
- tbl_leads integrates with CRM system for contact conversion  #New
- tbl_contact_submissions provides customer contact data  #New

4. Document Updates  #New

- Updated total tables from 53 to 56  #New
- Updated schema overview table  #New
- Added new category: Website & Landing Pages (54-56)  #New
- Updated reference to 01B_website_conceptual_design_v1.md  #New

---

## Implementation Checklist

### Tables to Modify in Anvil

The following existing tables require new configuration entries (via config table key-value pairs):

**4. config** - Add new configuration keys:
- Key: `home_template`, Value: (simpleObject) - Selected home page template type
- Key: `home_config`, Value: (simpleObject) - Home page configuration JSON
- Key: `about_config`, Value: (simpleObject) - About page configuration JSON
- Key: `google_maps_api_key`, Value: (simpleObject) - Google Maps API key for contact page
- Key: `privacy_policy`, Value: (simpleObject) - Privacy policy HTML content
- Key: `privacy_policy_updated`, Value: (simpleObject) - Last updated datetime
- Key: `terms_conditions`, Value: (simpleObject) - Terms & conditions HTML content
- Key: `terms_conditions_updated`, Value: (simpleObject) - Last updated datetime

Note: The config table uses key-value pattern. Add these as new rows with category='website'.

### New Tables to Add in Anvil

The following tables are completely new and must be created:

**54. tbl_landing_pages** (landing_pages)
- Columns:
  * title - string
  * slug - string
  * template_type - string
  * config - simpleObject
  * status - string
  * created_date - datetime
  * published_date - datetime
  * views_count - number
  * conversions_count - number
  * client_id - link_single to users

**55. tbl_contact_submissions** (contact_submissions)
- Columns:
  * name - string
  * email - string
  * phone - string
  * message - string
  * submitted_date - datetime
  * status - string
  * client_id - link_single to users

**56. tbl_leads** (leads)
- Columns:
  * email - string
  * name - string
  * phone - string
  * source - string
  * landing_page_id - link_single to landing_pages
  * captured_date - datetime
  * status - string
  * client_id - link_single to users

---

## Quick Reference: Table Numbers

**CORE TABLES (1-6)**
1. files
2. users
3. activity_log
4. config ← Modified with website config keys
5. business_profile
6. theme_config

**BOOKING TABLES (7-12)**
7-12. (booking-related tables)

**E-COMMERCE TABLES (13-20)**
13-20. (e-commerce-related tables)

**CUSTOMER TABLES (21-23)**
21-23. (customer-related tables)

**CONTENT TABLES (24-27)**
24-27. (content-related tables)

**SUPPORT TABLES (28-31)**
28-31. (support-related tables)

**FINANCE TABLES (32-35)**
32-35. (finance-related tables)

**INTEGRATION TABLES (36-42)**
36-42. (integration-related tables)

**CRM & MARKETING TABLES (47-53)**
47-53. (CRM and marketing-related tables)

**WEBSITE & LANDING PAGES TABLES (54-56)** ← NEW
54. tbl_landing_pages ← NEW
55. tbl_contact_submissions ← NEW
56. tbl_leads ← NEW

---

## VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| v11.0 | Jan 26, 2026 | **M3 Alignment Update**: Updated header to reference v9+ system documents (01_conceptual_design.md, 04_architecture_specification.md). Added UI Compliance note for M3 alignment. Database schema unchanged - data structure remains identical. |
| v10.0 | Jan 19, 2026 | Added Website & Landing Pages schema (Tables 54-56). Finalized for V1.x development. Added Anvil Data Tables reality section. |

---

**END OF DATABASE SCHEMA V11.0**

**Status:** ✅ Active Schema  
**Purpose:** Complete data model for Mybizz V1.x (100 clients)
