# Schema Change Instructions — Phase 1 Refactoring
# Mybizz — Consulting & Services
# Date: 2026-03-07

> **IMPORTANT:** Take a full backup of the Anvil app before making any changes.
> Work through this document in order. Complete each section before moving to the next.
> After all changes are made, run the Uplink smoke test to confirm the app is healthy.

---

## PRE-WORK

- [x ] Backup Anvil app to hard drive
- [x ] Backup repo to hard drive
- [x ] Backup .continue (global) to hard drive
- [x ] Confirm active branch is master: `git status`
- [x ] Open Anvil editor at mybizz.live
- [x ] Backup Anvil app clone to Anvil

---

## SECTION 1 — DELETE THESE TABLES ENTIRELY

Delete each of the following tables from the Anvil Data Tables editor.
Check each off as done. Order does not matter for deletions.

- [x ] `cart`
- [x ] `cart_items`
- [x ] `courier_config`
- [x ] `guestbook_entries`
- [x ] `membership_tiers`
- [x ] `order_items`
- [x ] `orders`
- [x ] `product_categories`
- [x ] `product_variants`
- [x ] `products`
- [x ] `shipments`
- [x ] `subscriptions`
- [x ] `vertical_config`

**13 tables total.**

---

## SECTION 2 — TRIM COLUMNS FROM EXISTING TABLES

### 2.1 Table: `bookings`

Remove these columns:

- [x ] `check_in_time` (hospitality-specific)
- [x ] `check_out_time` (hospitality-specific)
- [x ] `num_guests` (hospitality-specific)

Keep all other columns — they are all relevant to Consulting & Services.

### 2.2 Table: `invoice`

Remove these columns:

- [x ] `subscription_id` (memberships-specific)
- [x ] `order_id` (e-commerce-specific)

Keep all other columns.

---

## SECTION 3 — ADD COLUMNS TO EXISTING TABLES

### 3.1 Table: `services`

Add these new columns:

| Column name | Type | Notes |
|---|---|---|
- [x ]| `pricing_model` | Text (string) | Values: `duration` or `unit`. Required. |
- [x ]| `images` | Simple Object | List of media references for service images. |
- [x ]| `video_url` | Text (string) | URL to hosted video (YouTube, Vimeo, etc.). Optional. |

**After adding:** the `services` table should have these columns in total:
`service_id`, `name`, `description`, `duration_minutes`, `price`, `category`, `provider_id`, `is_active`, `created_at`, `meeting_type`, `pricing_model`, `images`, `video_url`

Note: `duration_minutes` remains in the schema. It is required when `pricing_model` is `duration` and ignored when `pricing_model` is `unit`. No need to make it nullable at the schema level — this is handled in application logic.

---

## SECTION 4 — VERIFY TABLES THAT STAY UNCHANGED

These tables require no changes. Confirm each is still present and intact after the deletions above.

- [ ] `users`
- [ ] `rate_limits`
- [ ] `contacts`
- [ ] `contact_events`
- [ ] `contact_campaigns`
- [ ] `services` (now updated per Section 3)
- [ ] `bookings` (now trimmed per Section 2)
- [ ] `bookable_resources`
- [ ] `availability_rules`
- [ ] `availability_exceptions`
- [ ] `business_profile`
- [ ] `config`
- [ ] `theme_config`
- [ ] `blog_posts`
- [ ] `blog_categories`
- [ ] `email_campaigns`
- [ ] `email_templates`
- [ ] `email_log`
- [ ] `email_config`
- [ ] `payment_config`
- [ ] `invoice` (now trimmed per Section 2)
- [ ] `invoice_items`
- [ ] `activity_log`
- [ ] `segments`
- [ ] `tasks`
- [ ] `tickets`
- [ ] `ticket_messages`
- [ ] `kb_articles`
- [ ] `kb_categories`
- [ ] `lead_captures`
- [ ] `pages`
- [ ] `reviews`
- [ ] `time_entries`
- [ ] `events`
- [ ] `event_registrations`
- [ ] `expenses`
- [ ] `files`
- [ ] `webhook_log`
- [ ] `backups`
- [ ] `client_notes`
- [ ] `customers`

---

## SECTION 5 — POST-CHANGE VERIFICATION

- [x ] All 13 deleted tables are gone from the Data Tables list
- [x ] `bookings` no longer has `check_in_time`, `check_out_time`, `num_guests`
- [x] `invoice` no longer has `subscription_id`, `order_id`
- [x ] `services` now has `pricing_model`, `images`, `video_url`
- [x ] All retained tables from Section 4 are present and intact
- [X ] Run Uplink smoke test: `python scripts/test_uplink.py`
- [ ] Run auth tests: `pytest tests/1.2-auth/ -v` — all 23 should still pass
- [ ] Backup repo after successful verification

---

## NOTES

**Why delete rather than disable?** Dead tables and dead code create noise for the AI development agent. A clean schema produces more accurate, reliable agent behaviour. Tables belonging to other verticals will be present in those vertical's own app — they are not lost.

**Why keep `customers` table?** The `customers` table exists alongside `contacts` in the current schema. Both are retained for now. Their relationship will be resolved during Stage 1.3 and the CRM phase. Do not delete either at this stage.

**Why keep `events` and `event_registrations`?** These are potentially useful for a consulting/services business running workshops, seminars, or group sessions. Retained pending a decision in a later session.

**Why keep `time_entries`?** Relevant for consultants who bill by time. Retained.

**Why keep `expenses`?** Relevant for business owners tracking costs. Retained.

---

*End of schema change instructions.*
*On completion, proceed to Task 3 — Code scaffold cleanup.*
