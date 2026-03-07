# Session 4 — Stage 1.3 Dashboard & Navigation

**Date:** 2026-03-07
**Status:** COMPLETE

---

## 1. Objective

Build the dashboard and navigation foundation — the skeleton that all future admin features hang off. Layouts, navigation structure, dashboard form, and navigation helpers. No live data wiring — metrics return stubs until Phase 3/4/5 data exists.

---

## 2. Files Produced

| File | Status |
|---|---|
| `client_code/layouts/AdminLayout/__init__.py` | Full rewrite |
| `client_code/layouts/CustomerLayout/__init__.py` | Full rewrite |
| `client_code/dashboard/DashboardForm/__init__.py` | Full rewrite |
| `client_code/shared/navigation_helpers.py` | New file |
| `server_code/server_dashboard/service.py` | Full rewrite |
| `client_code/public_pages/HomePage/__init__.py` | Updated |
| `C:\Users\dev-p\.continue\rules\ref_anvil_navigation.md` | Corrected and extended |

---

## 3. What Was Built

### AdminLayout
Full programmatic navigation. Auth check on `__init__` — redirects to `LoginForm` if unauthenticated or non-admin role. `_NAV_STRUCTURE` constant defines all 20 destinations and 4 divider labels for the C&S vertical. `build_navigation()` creates all NavigationLink components programmatically, stored as `self._nav_links`. `nav_vault` hidden unless role is owner. `set_active_link(attr_name)` available for content forms to highlight the current page.

### CustomerLayout
Same pattern as AdminLayout. Six destinations: My Dashboard, My Bookings, My Invoices, My Reviews, Support, Account. Auth check redirects to LoginForm if unauthenticated.

### DashboardForm
Calls `require_auth()` before `init_components()`. Four metric cards built programmatically in a LinearPanel: Revenue, Bookings, Customers, Time Entries. Calls `get_dashboard_metrics()` on load and updates card values from response.

### navigation_helpers.py
Three functions: `require_auth()` redirects to LoginForm if no user. `require_admin()` redirects if not owner/manager/admin/staff. `navigate_to_dashboard()` routes by role to DashboardForm, ClientPortalForm, or LoginForm.

### server_dashboard/service.py
Three `@anvil.server.callable` functions, all returning `{'success': bool, 'data': ...}`. `get_dashboard_metrics()` uses `getattr(app_tables, ...)` guards — safe at any build phase, falls back to zero stubs if tables do not exist yet. `get_recent_activity()` returns empty list. `get_storage_usage()` returns stub dict.

### HomePage startup wiring
If user is authenticated, calls `navigate_to_dashboard()` and returns. Otherwise renders public page normally.

---

## 4. Key Decisions

### navigate_to requires a Form instance, not a string
The rules file `ref_anvil_navigation.md` previously stated `navigate_to` accepts a string. This was wrong. The Anvil M3 API requires a Form class instance: `navigate_to=DashboardForm()`. Using it requires importing the target Form class explicitly.

### open_form(string) via lambda is the approved pattern for programmatic layouts
AdminLayout has 20 navigation destinations. Most target forms do not exist yet. Importing a non-existent module raises `ImportError` at startup and breaks the entire app. `open_form(string)` resolves the form name at click time, not import time — safe regardless of whether target forms exist. This is an Anvil-documented alternative to `navigate_to` and is the approved pattern for AdminLayout and CustomerLayout for the lifetime of the phased build.

### getattr(app_tables) guards on dashboard metrics
Server dashboard functions check for table existence before querying. This means `get_dashboard_metrics()` is safe to call at any build phase and will never raise an error due to missing tables.

---

## 5. Rules File Updated

`ref_anvil_navigation.md` corrected and extended:
- §2 now documents that `navigate_to` requires a Form instance and explains when each approach applies
- §8 anti-patterns updated — `navigate_to = 'string'` added as wrong pattern
- Approved deviation for programmatic layouts documented explicitly
- Route examples updated to C&S vertical throughout
- `last_updated` stamp updated to 20260307

---

## 6. Tests

- Smoke test: PASSED
- Local pytest 23/23: PASSED

---

## 7. Backup

`C:\_Data\Daily off site Backup\Mybizz consulting (session 4 done)`

---

*Session 4 closed. Stage 1.3 complete. Session 5 opens at Stage 1.4 — Settings & Configuration.*
