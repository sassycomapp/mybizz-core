# Session 3 — Phase 1 Refactoring

**Date:** 2026-03-07

---

## 1. Objective

Execute Phase 1 Refactoring as defined in Session 2. Produce a clean, correctly scoped codebase and schema before any new development begins. Four tasks in sequence.

---

## 2. Pre-Work

- [ ] Backup Anvil app to hard drive
- [ ] Backup repo to hard drive
- [ ] Confirm active branch is master: `git status`
- [ ] Verify ANVIL_UPLINK_KEY is set: `echo $env:ANVIL_UPLINK_KEY`
- [ ] Run smoke test: `python scripts/test_uplink.py`

---

## 3. Task 1 — Schema Cleanup

**Status:** ⚪ Not started

Executed per `schema-change-instructions.md` in `docs/`.

Summary of changes:
- 13 tables deleted (e-commerce, hospitality, memberships, shipping)
- `bookings` trimmed — 3 hospitality columns removed
- `invoice` trimmed — 2 columns removed
- `services` extended — `pricing_model`, `images`, `video_url` added

**Outcome:** *(to be recorded on completion)*

---

## 4. Task 2 — Rules Files Update

**Status:** ⚪ Not started

Files to replace in `C:\Users\dev-p\.continue\rules\`:

| File | Action |
|---|---|
| `platform_overview.md` | Replace with new Consulting & Services version |
| `platform_status.md` | Replace with updated version |

All other rules files remain unchanged.

**Outcome:** *(to be recorded on completion)*

---

## 5. Task 3 — Code Scaffold Cleanup

**Status:** ⚪ Not started

Packages to remove from the codebase:

**Client packages:**
- `products/` — entire package (ProductListForm, ProductEditorForm, ShoppingCartForm, CheckoutForm)

**Server packages:**
- `server_products/` — entire package (product_service.py, order_service.py, inventory_service.py)
- Shipping-related modules within `server_payments/` — any Bob Go or Easyship integration code

**Rule:** Delete cleanly. Do not comment out. Do not disable. Removed means removed.

Everything else stays exactly as it is. No renaming.

**Outcome:** *(to be recorded on completion)*

---

## 6. Task 4 — Verify & Test

**Status:** ⚪ Not started

- [ ] Uplink smoke test passing: `python scripts/test_uplink.py`
- [ ] Auth tests passing: `pytest tests/1.2-auth/ -v` — all 23 local tests green
- [ ] Uplink integration tests passing: 15/15
- [ ] App loads at mybizz.live — no errors
- [ ] Backup repo after all tests green

**Outcome:** *(to be recorded on completion)*

---

## 7. Session Outcome

*(to be completed at end of session)*

---

*Session 3 open. Proceeds to Stage 1.3 on completion.*
