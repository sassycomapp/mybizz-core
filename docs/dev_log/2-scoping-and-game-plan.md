# Session 2 — Scoping & Game Plan

**Date:** 2026-03-07

---

## 1. Vertical Selection Confirmed

Consulting & Services selected as the first vertical to develop. Reasoning recorded in Session 1. This session moves from that decision into concrete scoping and a game plan for execution.

---

## 2. Architecture Decisions

### 2.1 Single Vertical — No Toggle System

Each vertical will be developed as a completely separate, self-contained Anvil app. There is no toggle system between verticals. The Open Verticals architecture of the original platform concept is not carried forward into this project. This keeps each vertical clean, simple, and purposeful.

### 2.2 Code Ownership — Dependency Model Retained

Two options were considered:

- **Clone to client's own Anvil account** — client gets a copy of the app in their own account. Code is exposed and effectively unprotected. IP risk is significant.
- **Dependency model** — client app runs in our ecosystem, depending on the master template. Client never has access to the source code. All API keys stored in our Vault.

**Decision: Dependency model is retained.** The code is our primary asset. Protecting it is non-negotiable. The hosting cost per client is manageable and already factored into pricing. Centralised maintenance and updates are a further advantage.

### 2.3 Design & Standards

- Anvil M3 design system retained throughout. No exceptions.
- All coding standards, naming conventions, security policies, and testing workflows established in the rules files are carried forward intact. These are vertical-agnostic and represent hard-won quality standards that must not be diluted.

---

## 3. Feature Scope — Consulting & Services

### 3.1 What This Vertical Includes

- Public-facing website (Home, About, Contact, Privacy Policy, Terms)
- Authentication (Stage 1.2 complete — carried forward as-is)
- Dashboard & Navigation
- Settings & Configuration
- The Vault (encrypted API key storage)
- Service Catalogue (browsable, with booking and payment integrated)
- Bookings & Appointments (calendar, availability, provider selection, meeting types, intake forms, reminders)
- CRM & Contacts
- Email Marketing
- Payments & Invoicing
- Blog
- Analytics & Reporting
- Support Tickets (including Knowledge Base)

### 3.2 What Is Explicitly Excluded

- Product catalogue (browsable e-commerce shop)
- Shopping cart
- Shipping (Bob Go, Easyship)
- Inventory management
- Room reservations
- Restaurant table bookings
- Membership tiers and recurring billing
- Access control flows
- Toggle/vertical switching system

### 3.3 Payment Model

Payment happens at the point of booking — not through a separate cart and checkout process. The service catalogue is the equivalent of the product catalogue for this vertical: the customer browses services, selects one, and proceeds directly to booking and payment.

There is no e-commerce shopping cart. The payment flow is integrated into the booking process. Invoicing is generated from completed bookings.

**One payment gateway per client instance.** All payments go to the business's central account (Stripe or Paystack). This is the standard model for consulting and services businesses — the business takes payment, providers are paid internally by salary, commission, or contractor arrangement.

### 3.4 Service Catalogue

The service catalogue is purposely simple in V1:

- Service name, description, duration, price
- Category (optional grouping)
- Provider (staff user — see §4.1)
- Availability
- Images (multiple, stored as media references)
- Video URL (link to hosted video — YouTube, Vimeo, etc.)

Images and video are included from the outset. A therapist, trainer, or consultant needs to showcase their work visually. This is not an enhancement — it is a baseline expectation for this vertical.

Enhancements such as packages, bundles, and promotional pricing are deferred to a future update. The core catalogue is built to be extensible.

---

## 4. Provider Model

### 4.1 Providers Are Staff Users

A service provider (therapist, trainer, consultant, practitioner) is a Staff-role user in the system. The existing `services.provider_id → users` link is correct and sufficient.

- Solo consultant: the owner is the only provider.
- Multi-provider business (e.g. day spa with multiple therapists): each therapist has a Staff user account with their own booking schedule, services, and fees.

No schema change is required. The RBAC system already supports this model.

### 4.2 Revenue Reporting by Provider

Revenue attribution per provider is a reporting concern, not an architectural one. A query on `bookings` filtered by `service_id → provider_id` produces revenue, appointment count, and utilisation per therapist for any date range. This is implemented as part of the Analytics & Reporting phase.

---

## 5. Schema Assessment

The anvil.yaml was reviewed in full. The existing schema is more developed than the rules files suggested — 40+ tables are present. The approach is surgical editing, not rebuilding.

### 5.1 Tables to Delete Entirely

These tables belong to other verticals and have no place in Consulting & Services:

`cart`, `cart_items`, `courier_config`, `guestbook_entries`, `membership_tiers`, `order_items`, `orders`, `product_categories`, `product_variants`, `products`, `shipments`, `subscriptions`, `vertical_config`

### 5.2 Tables Requiring Column Trimming

- `bookings` — remove `check_in_time`, `check_out_time`, `num_guests` (hospitality-specific)
- `invoice` — remove `subscription_id`, `order_id` (not applicable to this vertical)

### 5.3 Tables Requiring Additions

- `services` — add `images` (simpleObject — list of media references) and `video_url` (string)

### 5.4 Tables That Stay Untouched

`users`, `rate_limits`, `contacts`, `contact_events`, `services`, `bookable_resources`, `availability_rules`, `availability_exceptions`, `business_profile`, `config`, `theme_config`, `blog_posts`, `blog_categories`, `email_campaigns`, `contact_campaigns`, `email_templates`, `email_log`, `email_config`, `payment_config`, `invoice`, `invoice_items`, `activity_log`, `segments`, `tasks`, `tickets`, `ticket_messages`, `kb_articles`, `kb_categories`, `lead_captures`, `pages`, `reviews`, `time_entries`, `events`, `event_registrations`, `expenses`, `files`, `webhook_log`, `backups`, `client_notes`

---

## 6. Game Plan

Development proceeds in two phases.

---

### Phase 1 — Refactoring (Session 3)

The app must be correctly scoped before any new development begins. Four tasks, executed in this order:

**Task 1 — Schema cleanup**
Highest-risk task, done first while the app is clean. Delete the 13 tables listed in §5.1. Trim columns from `bookings` and `invoice` as listed in §5.2. Add `images` and `video_url` to `services` as listed in §5.3.

**Task 2 — Rules files update**
Rewrite `platform_overview.md` and `platform_status.md` to reflect single-vertical, Consulting & Services scope. All other rules files stay as-is — they are vertical-agnostic.

**Task 3 — Code scaffold cleanup**
Remove client and server packages that belong exclusively to excluded features: `products`, `server_products`, shipping-related modules in `server_payments`. No renaming. Everything that stays, stays exactly as it is.

**Task 4 — Verify & test**
Run smoke test via Uplink. Confirm auth system still passes all 23 local and 15 integration tests. Confirm app loads and navigates correctly. Backup before and after.

---

### Phase 2 — Development (Sessions 4 onward)

With a clean, correctly scoped foundation, development resumes at **Stage 1.3 — Dashboard & Navigation** and proceeds stage by stage per the original build plan, adapted for this vertical.

Indicative stage sequence:
- Stage 1.3 — Dashboard & Navigation
- Stage 1.4 — Settings & Configuration
- Stage 1.5 — The Vault
- Stage 1.6 — AdminLayout Full Navigation
- Phase 2 — Public Website
- Phase 3 — Payments & Invoicing
- Phase 4 — Bookings & Appointments (including Service Catalogue)
- Phase 5 — CRM & Email Marketing
- Phase 6 — Security hardening & compliance
- Phase 7 — Analytics & Reporting
- Phase 8 — Vertical polish
- Phase 9 — Client provisioning & billing automation
- Phase 10 — Final testing & production launch

Each stage will have its own session file where appropriate.

---

## 7. Refactoring Workflow Summary

| Item | Action |
|---|---|
| Anvil app (mybizz-core) | Refactor in place — no rename |
| Repo (mybizz-core) | Refactor in place — no rename |
| Rules files (technical) | No change — vertical-agnostic |
| Rules files (platform_overview, platform_status) | Rewrite for new scope |
| MCPs | No change |
| Prompts | Rewrite per stage as development proceeds |
| config.yaml | No change |
| Data table schema | Surgical edit — delete, trim, add as per §5 |
| Client/server scaffold | Delete excluded packages cleanly — no commenting out |
| Auth system (Stage 1.2) | Carried forward untouched |

---

*Session 2 closed. Session 3 will execute Phase 1 — Refactoring.*
