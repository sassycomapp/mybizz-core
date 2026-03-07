# MyBizz — Development Log

**Location:** `mybizz-core/docs/dev_log.md`
**Purpose:** A sequential record of decisions and development process — the bread-crumb trail. This is not a technical document. It captures what was decided, why, and in what order. It is intended to be read when developing subsequent verticals to understand the reasoning behind earlier choices.

**Structure:** Session-based. Each entry represents one development session regardless of date. Sessions are numbered sequentially and titled descriptively. Date is recorded but is secondary to sequence.

---

## Session 1 — Project Direction & Vertical Selection

**Date:** 2026-03-07

### Context

MyBizz was originally conceived and partially built as a four-vertical, Open Verticals platform — a single master template serving all business types simultaneously. Development reached Stage 1.2 (Authentication System complete, all tests passing) before being paused due to funding constraints.

On resuming, the decision was made not to continue building the full four-vertical platform but instead to isolate one vertical and develop it as a focused, standalone product first. The same Anvil app (mybizz-core), repo, and dev environment are being repurposed — nothing was discarded.

### The Four Verticals & Their Features

The original platform was designed around four business verticals. Features common to all four are noted. Features unique to specific verticals are noted against those verticals.

**Features common to all four verticals:**
Website, Authentication, CRM, Email Marketing, Payments, Invoicing, Blog, Analytics, Support Tickets

---

**Hospitality** *(guesthouses, B&Bs, boutique hotels, restaurants)*
- All common features
- Bookings — room reservations (date range, deposit/full payment, check-in/out)
- Bookings — restaurant table reservations (party size, floor plan, dietary requirements)

**Consulting & Services** *(salons, therapists, personal trainers, consultants, clinics)*
- All common features
- Bookings — service appointments (provider selection, meeting type, intake forms, reminders)

**E-commerce** *(online retailers, physical and digital product sellers)*
- All common features
- Product Catalogue (variants, inventory tracking)
- Shopping Cart & Checkout
- Shipping (Bob Go for SA domestic, Easyship for international)
- Memberships & Recurring Billing

**Memberships & Subscriptions** *(gyms, studios, clubs, subscription boxes, online courses)*
- All common features
- Membership Tiers
- Recurring Billing
- Access Control
- Upgrade / Downgrade / Pause / Cancel flows

---

### Complexity Ranking

Before selecting a vertical, the four were ranked by development complexity:

1. **E-commerce** — most complex. Shipping integrations, product variants, inventory, cart edge cases, and order management add significant scope not present in any other vertical.
2. **Hospitality** — two distinct booking systems (rooms and tables) sharing infrastructure but with different logic. The dual nature adds meaningful complexity.
3. **Memberships & Subscriptions** — recurring billing and access control flows add complexity, but no booking system and no physical products.
4. **Consulting & Services** — most straightforward. Single booking system (appointments), no physical products, no shipping, well-bounded scope.

### Decision

**Consulting & Services will be developed first.**

Reasoning: it is the least complex vertical, which means the fastest path to a working, shippable product. The patterns established here — auth, CRM, website, bookings, payments, email — will carry forward directly to subsequent verticals. Starting with the simplest vertical reduces risk and builds a solid, tested foundation.

### What Carries Forward From Stage 1.2

The following work is complete and will be retained or repurposed:
- Anvil app (mybizz-core), live at mybizz.live
- Stage 1.2 Authentication System — LoginForm, SignupForm, PasswordResetForm, server_auth, rate limiting, RBAC, all tests passing
- Full dev environment — VS Code, Continue.dev, OpenRouter, GitHub, Uplink
- All rules documentation in the global .continue/rules/ path

---

*Log continues in Session 2*
