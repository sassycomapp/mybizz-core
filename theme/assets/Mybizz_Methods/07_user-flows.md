---
description: "07_user_flows.md - Mybizz User flows"
globs: ["**/*"]
alwaysApply: true
---


# Mybizz Platform - User Flows

**Document Version:** 6.0  
**Date:** January 26, 2026  
**Status:** Updated for M3 Navigation & Components  
**UI Standard:** Material Design 3 (M3) - All forms use NavigationDrawerLayout + M3 components  
**Purpose:** Define all critical user journeys through the system  
**Reference:** Aligned with 01_conceptual_design.md, 04_architecture_specification.md

---

## Document Overview

This document defines the complete user journey maps for all actors in the Mybizz platform:

| Flow | Actor | Purpose |
|------|-------|---------|
| 1. Client Onboarding | New Subscriber | Signup to operational website |
| 2A. Customer Booking - Room Reservation | Guest | Book accommodation |
| 2B. Customer Booking - Restaurant Table | Diner | Reserve restaurant table |
| 3. Customer Booking - Services | Client | Book appointment/consultation |
| 4. E-Commerce Purchase | Customer | Purchase products online |
| 5. Membership Subscription | Member | Subscribe to membership tier |
| 6. Admin Daily Operations | Business Owner/Staff | Manage daily business |
| 7. Content Management | Content Manager | Update website content |
| 8. Customer Support | Customer/Staff | Handle support tickets |
| 9. Error Recovery | All Users | Handle errors gracefully |
| 10. Contact Management | Business Owner | View and manage all contacts |
| 11. Email Campaign Setup | Business Owner | Activate automated campaigns |
| 12. Marketing Dashboard Review | Business Owner | Monitor marketing performance |
| 13. Website Homepage Customization | Business Owner | Customize homepage template and content |
| 14. Landing Page Creation | Business Owner/Marketing Manager | Create conversion-focused landing pages |
| 15. Visitor Contact Form Submission | Website Visitor | Contact business via website form |
| 16. Lead Capture via Landing Page | Marketing Campaign Visitor | Capture leads from landing pages |

---

## M3 UI STANDARDS NOTE

**All user flows reference Material Design 3 (M3) components and patterns:**

**Navigation:**
- Admin flows use **NavigationDrawerLayout** with **NavigationLink** components
- NavigationLinks automatically open target forms via `navigate_to` property
- Navigation drawer automatically collapses to hamburger menu on mobile

**Forms:**
- List forms: NavigationDrawerLayout + DataGrid + M3 components
- Editor forms: Card (outlined) + TextBox (outlined) + Button (filled/outlined)
- Dashboard forms: Card (elevated) + Plot + Heading (headline-large)

**Components:**
- TextBox/TextArea: Use `outlined` role
- Buttons: Use `filled-button` (primary), `outlined` (secondary), `text-button` (tertiary)
- Cards: Use `elevated` (dashboards) or `outlined` (forms)
- Typography: Use M3 roles (headline-large, body-medium, etc.)

**Data Binding:**
- All editor forms use `self.item` pattern with two-way write back bindings
- No manual change event handlers needed

For complete M3 standards, see **04_architecture_specification.md** Section 2.4 and 2.5.

---

## 1. Client Onboarding Flow

**Actor:** New Subscriber (Business Owner)  
**Goal:** Get from signup to operational business website  
**Duration:** 2-4 hours (including Mybizz provisioning)

### Flow Steps:

```
START: Subscriber visits Mybizz marketing site
  ↓
1. SELECT TEMPLATE (Not Permanent)
   • View website templates:
     - Hospitality template (rooms, dates, availability)
     - Consulting template (services, appointments, calendar)
     - Ecommerce template (products, shop, inventory)
     - Memberships template (tiers, member benefits, access)
     - Hybrid templates (Studio, Wellness, etc.)
   • Select template that matches primary business type
   • NOTE: Template can be changed later
   • NOTE: All features available regardless of template (Open Verticals)
  ↓
2. PAYMENT & SIGNUP
   • Provide business information:
     - Business name
     - Email
     - Phone
     - Address
     - Country (determines system currency)
   • Create password
   • Choose billing cycle:
     - Monthly: $50/month (or $25/month for first 50 beta clients)
   • Select payment gateway for Mybizz subscription:
     - Stripe (global)
     - Paystack (Africa: South Africa, Nigeria, Ghana, Kenya)
   • Enter payment method
   • Complete payment
  ↓
3. PROVISIONING (Mybizz Founder - 1-2 hours)
   Manual steps performed by Mybizz:
   • Create Anvil account for client (Mybizz pays $15/month)
   • Clone master_template to client's account
   • Configure dependency to published version
   • Initialize empty data tables
   • Set system currency (immutable after this point)
   • Set up subdomain (clientname.Mybizz.app)
   • Create admin credentials (Owner role)
   • Send welcome email with login details
  ↓
4. ONBOARDING TIER SELECTION
   Client chooses onboarding approach:
   
   TIER 1: Standard Setup (Free - Included)
   • 30-minute guided video call
   • Client does pre-work (logo, content prepared)
   • Mybizz imports data during call
   • Quick feature walkthrough
   → Continue to Step 5A
   
   TIER 2: Premium Setup ($200 One-Time)
   • Mybizz does ALL setup work
   • No client pre-work required
   • Client receives fully operational website
   • 1-hour detailed walkthrough call
   → Skip to Step 6 (Mybizz handles 5A-5C)
  ↓
5A. BRANDING CONFIGURATION (Standard Tier)
    • Upload logo (PNG/JPG, max 2MB)
    • Set brand colors:
      - Primary color (buttons, CTAs)
      - Secondary color (accents)
      - Background color
    • Select font family (Google Fonts)
    • Set business tagline
  ↓
5B. EMAIL PROVIDER SETUP (CRITICAL)
    Tier 2: Transactional Emails (Zoho - Required)
    • Mybizz helps set up Zoho Workplace Free:
      - 5 business email addresses on client's domain
      - contact@, bookings@, orders@, support@, noreply@
    • Mybizz configures DNS records (MX, SPF, DKIM)
    • Store SMTP credentials (encrypted)
    • Send test email to verify deliverability
    
    Tier 3: Marketing Emails (Brevo - Optional, Future)
    • Client can set up Brevo account later
    • Mybizz provides CSV export for email lists
    • Not required for initial launch
  ↓
5C. PAYMENT GATEWAY SETUP
    Client chooses primary gateway based on market:
    
    STRIPE (Global Markets):
    • Client creates Stripe account
    • Gets API keys (test mode first)
    • Enters into Mybizz settings (encrypted)
    • Processes test transaction ($1)
    • Verifies webhook delivery
    
    PAYSTACK (African Markets):
    • Client creates Paystack account
    • Gets API keys (test mode first)
    • Enters into Mybizz settings (encrypted)
    • Processes test transaction
    • Verifies webhook delivery
    
    PAYPAL (Optional - One-Time Payments Only):
    • Client creates PayPal Business account
    • Configures Smart Button
    • Tests sandbox payment
    • NOTE: Cannot handle subscriptions
  ↓
5D. FEATURE ACTIVATION (Open Verticals)
    • Navigate to Settings → Features
    • Activate features needed for business:
      ☑ Bookings & Appointments (if service-based)
      ☑ Product Sales (if selling products)
      ☑ Memberships & Subscriptions (if recurring revenue)
      ☑ Professional Services (if consulting/appointments)
      ☑ Hospitality Management (if rooms/accommodation)
      ☑ Blog & Content (recommended for all)
    • Navigation menu updates automatically
    • Feature-specific pages added automatically
  ↓
6. INVENTORY SETUP
   Based on activated features:
   
   IF Hospitality activated:
   • Add room types (name, capacity, amenities, rate)
   • Set availability rules
   • Configure check-in/check-out times
   
   IF Services activated:
   • Add service types (name, duration, price)
   • Set provider availability
   • Configure appointment rules
   
   IF Ecommerce activated:
   • Add products (name, description, price, images)
   • Set inventory levels
   • Configure shipping options
   
   IF Memberships activated:
   • Create membership tiers (name, benefits, price)
   • Set billing cycles
   • Configure access rules
  ↓
7. COURIER SETUP (If Ecommerce with Physical Products)
   Optional integrations:
   
   IF South Africa shipping needed:
   • Create Bob Go account
   • Enter API credentials (encrypted)
   • Test rate calculation
   
   IF International shipping needed:
   • Create Easyship account
   • Enter API credentials (encrypted)
   • Test rate calculation
   
   Manual shipping always available as fallback
  ↓
8. GO LIVE CHECKLIST
   Review setup requirements:
   ☑ Branding configured (logo, colors)
   ☑ Email provider working (Zoho test email sent)
   ☑ Payment gateway working (test transaction completed)
   ☑ At least 1 bookable item/product/service added
   ☑ Test booking/order completed successfully
   ☑ Public website previewed and approved
   
   • Switch payment gateway to live mode
   • Mark account as "live"
   • Public website becomes active
  ↓
9. SUCCESS MILESTONES TRACKING
   Dashboard shows progress:
   ✅ Account created
   ✅ Logo uploaded
   ✅ Payment gateway connected
   ⚠️ First product/service added (0 of 1) ← Current
   ⚪ Test transaction completed
   ⚪ First real sale 🎉
   
   Automated nudge emails sent at Day 3, 7, 14 if stalled
  ↓
END: Operational website ready for customers

**Total Time:**
- Standard Tier: 2-4 hours (client involved throughout)
- Premium Tier: 1 hour client time (Mybizz does 4-5 hours work)
```

### Key Decision Points:

| Step | Decision | Impact |
|------|----------|--------|
| Step 1 | Template selection | Determines initial layout (changeable later) |
| Step 2 | Country selection | Sets system currency (IMMUTABLE) |
| Step 4 | Onboarding tier | Determines who does setup work |
| Step 5C | Payment gateway | Stripe (global) vs Paystack (Africa) |
| Step 5D | Feature activation | Determines available functionality |
| Step 7 | Courier setup | Optional, manual always available |

---

## 2. Customer Booking Flow - Hospitality

**Actor:** Guest (End User)  
**Goal:** Book accommodation or restaurant table  
**Duration:** 5-10 minutes

### 2A. Room Booking Flow:

```
START: Guest visits client's accommodation website
  ↓
1. BROWSE AVAILABILITY
   • Select check-in date (calendar picker)
   • Select check-out date (calendar picker)
   • Enter number of guests
   • Click "Search Availability"
  ↓
1a. AVAILABILITY CHECK RESULTS
   
   IF zero availability for selected dates:
   • Show message: "No rooms available for these dates"
   • Display alternative options:
     ☐ "Show nearby available dates" (±3 days)
     ☐ "Adjust guest count" (fewer guests may open options)
     ☐ "View waitlist" (if business enables this feature)
   • Calendar shows availability indicators:
     - Green dots: Full availability
     - Yellow dots: Limited availability
     - Red dots: No availability
   → User returns to date selection with visual guidance
   
   EDGE CASES:
   • Past dates selected: Show error "Cannot book past dates"
   • Check-out before check-in: Show error "Check-out must be after check-in"
   • Dates more than 365 days ahead: Show warning "Bookings limited to 12 months"
   • Guest count exceeds all room capacity: "Maximum capacity is [X] guests"
   • Same-day booking after cutoff time: Show next-day minimum
   
   IF availability exists:
   → Proceed to Step 2
  ↓
2. VIEW AVAILABLE ROOMS
   • System displays available room types
   • Each shows:
     - Room name and photo
     - Capacity (max guests)
     - Amenities (icons: WiFi, AC, TV, etc.)
     - Price per night
     - Total price for stay
   • Filter by: Price, Capacity, Amenities
   • Sort by: Price, Name, Popularity
  ↓
3. SELECT ROOM
   • Click "Book Now" on preferred room
   • Room details expand:
     - Photo gallery (swipeable)
     - Full description
     - Complete amenities list
     - Room size
     - Cancellation policy
     - House rules
  ↓
4. ENTER GUEST DETAILS
   IF guest has account:
   • Log in → details pre-filled
   • Edit if needed
   
   IF guest is new:
   • Enter:
     - First name, Last name
     - Email address
     - Phone number
     - Country
   • Option: ☐ Create account for faster future bookings
  ↓
5. SPECIAL REQUESTS
   • Text field for special requests
   • Common request checkboxes:
     ☐ Early check-in (if available)
     ☐ Late checkout (if available)
     ☐ Ground floor room
     ☐ Quiet location
     ☐ Extra bed/crib
     ☐ Airport pickup (if offered)
   • Estimated arrival time (dropdown)
  ↓
6. REVIEW BOOKING
   Display booking summary:
   ┌─────────────────────────────────┐
   │ Room: Deluxe Double             │
   │ Check-in: Jan 15, 2026 (2 PM)   │
   │ Check-out: Jan 18, 2026 (11 AM) │
   │ Nights: 3                       │
   │ Guests: 2                       │
   ├─────────────────────────────────┤
   │ Rate: $150/night                │
   │ Subtotal: $450.00               │
   │ Tax (15%): $67.50               │
   │ TOTAL: $517.50                  │
   └─────────────────────────────────┘
   • Option: "Edit Booking" to go back
   • Option: "Apply Promo Code"
  ↓
7. PAYMENT
   Payment amount options (business configurable):
   ○ Full payment now ($517.50)
   ○ Deposit now (50% = $258.75), balance at check-in
   
   Payment methods:
   ○ Credit/Debit Card (Stripe/Paystack)
   ○ PayPal
   
   • Enter payment details
   • Review cancellation policy
   • ☐ I agree to the terms and conditions
   • Click "Complete Booking"
  ↓
7a. PAYMENT PROCESSING
   
   Show processing indicator (max 30 seconds)
   
   EDGE CASES - Payment Gateway Timeouts:
   
   IF payment gateway times out (30s):
   • Do NOT retry automatically (duplicate charge risk)
   • Show: "Payment processing - checking status..."
   • Poll gateway for status (3 attempts, 5s intervals)
   • RESULTS:
     - Confirmed: Proceed to confirmation
     - Failed: Show error + "Try again" button with new transaction
     - Unknown: Show "Payment pending" + booking ID + support contact
   
   EDGE CASES - Payment Declined:
   • Card declined: "Payment declined. Please use different card"
   • Insufficient funds: "Insufficient funds. Try different payment method"
   • Card expired: "Card expired. Please update card details"
   • Security check failed: "Payment blocked for security. Contact your bank"
   
   EDGE CASES - Room Availability Changed:
   • IF room sold between review and payment:
     - Stop payment processing
     - Show: "Room no longer available"
     - Offer: Similar rooms at same/higher price
     - Refund any captured payment immediately
   
   EDGE CASES - Promo Code Issues:
   • Invalid code: "Promo code not valid"
   • Expired code: "This code expired on [date]"
   • Already used: "Code already used on this account"
   • Minimum not met: "Minimum $500 required for this code"
   
   IF payment successful:
   → Proceed to Step 8
  ↓
8. CONFIRMATION
   Display confirmation:
   ┌─────────────────────────────────┐
   │ ✓ BOOKING CONFIRMED            │
   │                                 │
   │ Booking #: BK-2026-001234      │
   │ Confirmation sent to:           │
   │ guest@email.com                 │
   │                                 │
   │ [Add to Calendar]               │
   │ [View Booking Details]          │
   │ [Print Confirmation]            │
   └─────────────────────────────────┘
   
   Automated email sent:
   • Booking confirmation
   • Check-in instructions
   • Property address and directions
   • Contact information
   • Cancellation policy reminder
  ↓
END: Booking confirmed, guest receives email
```

### 2B. Restaurant Table Booking Flow:

```
START: Guest visits restaurant website
  ↓
1. SELECT RESERVATION DETAILS
   • Select date (calendar picker)
   • Select time (dropdown: 12:00, 12:30, 13:00...)
   • Select party size (1-20 guests)
   • Click "Find a Table"
  ↓
2. VIEW AVAILABLE TABLES
   • System shows available time slots:
     ○ 12:00 - Available
     ○ 12:30 - Available
     ○ 13:00 - Last table!
     ○ 13:30 - Unavailable
   • Click preferred time
  ↓
3. ENTER GUEST DETAILS
   • Name
   • Email
   • Phone
   • Special occasion? (Birthday, Anniversary, Business)
  ↓
4. SPECIAL REQUESTS
   • Dietary requirements:
     ☐ Vegetarian
     ☐ Vegan
     ☐ Gluten-free
     ☐ Allergies (specify)
   • Seating preference:
     ○ Indoor
     ○ Outdoor/Patio
     ○ No preference
   • Additional notes
  ↓
5. CONFIRM RESERVATION
   • Review details
   • No payment required (standard)
   • OR deposit required for large parties (configurable)
   • Click "Confirm Reservation"
  ↓
6. CONFIRMATION
   • Reservation confirmed
   • Confirmation email sent
   • SMS reminder option
   • Add to calendar option
  ↓
END: Table reserved
```

### 2B. Restaurant Table Reservation Flow:

```
START: Diner visits restaurant website
  ↓
1. SELECT DINING DETAILS
   • Select date (calendar picker)
   • Select time slot (dropdown: 12:00 PM, 12:30 PM, 1:00 PM...)
   • Select party size (dropdown: 1-20 guests)
   • Click "Check Availability"
  ↓
1a. AVAILABILITY CHECK RESULTS
   
   IF zero availability for selected time:
   • Show message: "No tables available for [party size] at [time]"
   • Display alternative options:
     ☐ "Show nearby available times" (±30 mins, ±1 hour)
     ☐ "Try different party size"
     ☐ "View waitlist" (if enabled)
   • Time slot grid shows availability indicators:
     - Green: Available
     - Yellow: Limited availability
     - Red: Fully booked
   → User returns to time selection with visual guidance
   
   EDGE CASES:
   • Past time selected: Show error "Cannot book past times"
   • Same-day booking after cutoff: Show next available day
   • Party size exceeds capacity: "Maximum capacity is [X] guests. Contact us for larger parties"
   • Time outside restaurant hours: Show error "Restaurant hours: [hours]"
   
   IF availability exists:
   → Proceed to Step 2
  ↓
2. SELECT TABLE/AREA (Optional - if configured)
   IF restaurant offers table selection:
   • View floor plan or area options:
     - Main dining room
     - Bar area
     - Patio/outdoor
     - Private dining room
   • Each shows:
     - Capacity
     - Ambiance (quiet, lively, romantic)
     - Special features (window view, fireplace)
   
   IF simple booking (no table selection):
   • Skip to Step 3
  ↓
3. ENTER GUEST DETAILS
   IF diner has account:
   • Log in → details pre-filled
   • Edit if needed
   
   IF diner is new:
   • Enter:
     - Full name
     - Email address
     - Phone number (required for confirmation/reminders)
   • Option: ☐ Create account for faster future bookings
  ↓
4. SPECIAL REQUESTS
   • Dietary requirements:
     ☐ Vegetarian
     ☐ Vegan
     ☐ Gluten-free
     ☐ Kosher/Halal
     ☐ Allergies (text field to specify)
   • Seating preference:
     ○ Indoor
     ○ Outdoor/Patio
     ○ Window seat
     ○ Quiet area
     ○ No preference
   • Special occasion:
     ☐ Birthday (complimentary dessert?)
     ☐ Anniversary
     ☐ Business meeting
     ☐ Celebration
   • Additional notes (free text)
  ↓
5. REVIEW RESERVATION
   Display summary:
   ┌─────────────────────────────────┐
   │ RESERVATION SUMMARY            │
   │                                 │
   │ Restaurant: [Name]              │
   │ Date: Jan 15, 2026              │
   │ Time: 7:00 PM                   │
   │ Party Size: 4 guests            │
   │ Area: Patio                     │
   │                                 │
   │ Contact: John Doe               │
   │ Phone: +1-555-0123              │
   │                                 │
   │ Special: Birthday celebration   │
   └─────────────────────────────────┘
   
   Deposit options (business configurable):
   ○ No deposit required (standard)
   ○ Deposit required for parties 8+ ($50 per person)
   ○ Deposit required for special occasions ($100)
   
   • Cancellation policy displayed
   • ☐ I agree to the cancellation policy
   • Option: "Edit Reservation" to go back
   • Click "Confirm Reservation"
  ↓
5a. PAYMENT (IF DEPOSIT REQUIRED)
   
   IF deposit required:
   • Show deposit amount
   • Payment methods:
     ○ Credit/Debit Card (Stripe/Paystack)
     ○ PayPal
   • Enter payment details
   • Process payment (see payment edge cases in Flow 2A, Step 7a)
   
   IF no deposit:
   • Skip to Step 6
  ↓
6. CONFIRMATION
   Display confirmation:
   ┌─────────────────────────────────┐
   │ ✓ RESERVATION CONFIRMED        │
   │                                 │
   │ Reservation #: RES-2026-001234 │
   │                                 │
   │ We look forward to seeing you! │
   │                                 │
   │ [Add to Calendar]               │
   │ [View Details]                  │
   │ [Get Directions]                │
   └─────────────────────────────────┘
   
   Automated communications:
   • Confirmation email sent immediately
   • SMS confirmation (if phone provided)
   • Reminder SMS 24 hours before (optional)
   • Reminder email 24 hours before
   • Direction/parking info included
   • Contact info for changes/cancellations
  ↓
END: Table reservation confirmed

### RESTAURANT-SPECIFIC EDGE CASES:

**No-Show Prevention:**
• Require phone number for all reservations
• Send 24-hour reminder with confirmation link
• If no confirmation, send 2-hour reminder
• Track no-show rate per customer
• Optional: Require deposit for repeat no-shows

**Cancellation Handling:**
• Allow cancellation up to X hours before (configurable: 2-24 hours)
• Late cancellation: Charge deposit (if collected)
• Easy cancellation via email link (no login required)
• Free up table immediately for other bookings
• Send cancellation confirmation

**Waitlist Management:**
• IF fully booked, offer waitlist signup
• Collect: Name, phone, party size, flexible time range
• Auto-notify if cancellation occurs
• 15-minute response window
• Remove from waitlist after booking or no response

**Walk-in Integration:**
• Staff can mark tables as "walk-in occupied"
• Updates real-time availability
• Prevents double-booking
• Walk-ins become contacts in CRM (optional email capture)

**Large Party Handling:**
• Parties 8+ may require phone confirmation
• Show message: "Please call us to confirm large party booking"
• Optional: Auto-create task for staff to call customer
• Higher deposit amount for large parties
```

### Error Scenarios (Combined Room + Restaurant):

| Scenario | System Response |
|----------|-----------------|
| No availability | Show alternative times/dates, offer waitlist signup |
| Payment fails | Show error, allow retry, offer alternative method, hold booking 15 mins |
| Session timeout | Save progress, prompt to continue |
| Invalid dates/times | Prevent selection, show available range |
| Duplicate booking | Check existing reservations, warn before creating duplicate |
| Party size exceeded | Show max capacity, offer to contact restaurant directly |

---

## 3. Customer Booking Flow - Services

**Actor:** Client (End User)  
**Goal:** Book appointment or consultation  
**Duration:** 3-8 minutes

### Flow Steps:

```
START: Client visits service provider's website
  ↓
1. BROWSE SERVICES
   • View service categories:
     - Consultations
     - Treatments
     - Classes
     - etc.
   • Each service shows:
     - Name and description
     - Duration (30 min, 60 min, etc.)
     - Price
     - Provider(s) available
  ↓
2. SELECT SERVICE
   • Click "Book Now" on desired service
   • Service details expand:
     - Full description
     - What to expect
     - Preparation instructions
     - Cancellation policy
  ↓
3. SELECT PROVIDER (If Multiple)
   • View available providers:
     - Photo and name
     - Specializations
     - Ratings/reviews
     - Availability indicator
   • Select preferred provider
   • OR select "Any available provider"
  ↓
4. SELECT DATE & TIME
   • Calendar shows availability:
     - Green = Available slots
     - Gray = Unavailable
   • Select date
   • View available time slots for that date:
     ○ 09:00 AM ○ 09:30 AM ○ 10:00 AM
     ○ 10:30 AM ○ 11:00 AM ○ 11:30 AM
     ○ 02:00 PM ○ 02:30 PM ○ 03:00 PM
   • Select time slot
  ↓
5. MEETING TYPE (If Applicable)
   Select appointment format:
   ○ In-Person (at [business address])
   ○ Video Call (Zoom/Google Meet link provided)
   ○ Phone Call (provider will call you)
   
   IF In-Person:
   • Display business address
   • Show map
   • Parking instructions
   
   IF Video Call:
   • Note: "Link will be sent before appointment"
  ↓
6. ENTER CLIENT DETAILS
   IF existing client (logged in):
   • Details pre-filled
   • Review and confirm
   
   IF new client:
   • Enter:
     - Name
     - Email
     - Phone
   • Health/intake form (if required by service type)
   • Option: Create account
  ↓
7. APPOINTMENT NOTES
   • "What would you like to discuss/address?"
   • Text area for client to describe needs
   • Helps provider prepare
  ↓
8. REVIEW & PAYMENT
   Display summary:
   ┌─────────────────────────────────┐
   │ Service: Business Consultation  │
   │ Provider: Sarah Johnson         │
   │ Date: January 20, 2026          │
   │ Time: 10:00 AM - 11:00 AM       │
   │ Format: Video Call              │
   ├─────────────────────────────────┤
   │ Duration: 60 minutes            │
   │ Price: $150.00                  │
   │ Tax: $0.00                      │
   │ TOTAL: $150.00                  │
   └─────────────────────────────────┘
   
   Payment timing (business configurable):
   ○ Pay now (required)
   ○ Pay now (optional, pay after service)
   ○ Deposit now, balance after
   
   • Enter payment details
   • Click "Confirm Appointment"
  ↓
9. CONFIRMATION
   • Appointment confirmed
   • Automated emails sent:
     - Immediate confirmation
     - 24-hour reminder
     - 1-hour reminder (optional)
   • Calendar invite attached
   • IF Video Call: Link included in emails
  ↓
END: Appointment booked
```

### Recurring Appointments:

```
After initial booking confirmation:
  ↓
RECURRING OPTION
   • "Would you like to make this a recurring appointment?"
   • Options:
     ○ One-time only
     ○ Weekly (same day/time each week)
     ○ Bi-weekly
     ○ Monthly
   
   IF recurring selected:
   • Set number of occurrences (or ongoing)
   • Review total commitment
   • Payment: Per-session or package deal
   • Confirm recurring series
```

---

## 4. E-Commerce Purchase Flow

**Actor:** Customer  
**Goal:** Purchase products (physical or digital)  
**Duration:** 5-15 minutes

### Flow Steps:

```
START: Customer visits online store
  ↓
1. BROWSE PRODUCTS
   • View product categories (sidebar or menu)
   • Filter by:
     - Category
     - Price range
     - Availability (in stock only)
     - Rating
   • Sort by:
     - Featured
     - Price (low to high / high to low)
     - Newest
     - Best selling
   • Grid or list view toggle
  ↓
2. VIEW PRODUCT DETAILS
   • Click product card
   • Product page shows:
     - Image gallery (main + thumbnails)
     - Product name
     - Price (in customer's display currency if configured)
     - SKU
     - Stock status
     - Full description
     - Specifications
     - Customer reviews/ratings
   
   IF product has variants:
   • Select variant options:
     - Size: [S] [M] [L] [XL]
     - Color: [Red] [Blue] [Green]
   • Price/stock updates based on selection
   
   • Select quantity
   • Click "Add to Cart"
  ↓
3. CART NOTIFICATION
   Modal appears:
   ┌─────────────────────────────────┐
   │ ✓ Added to Cart                │
   │                                 │
   │ [Product Name] x 1              │
   │ $49.99                          │
   │                                 │
   │ Cart Total: $49.99 (1 item)     │
   │                                 │
   │ [Continue Shopping]             │
   │ [View Cart] [Checkout]          │
   └─────────────────────────────────┘
  ↓
4. REVIEW CART
   Cart page displays:
   ┌─────────────────────────────────────────────┐
   │ YOUR CART (2 items)                         │
   ├─────────────────────────────────────────────┤
   │ [IMG] Product A                             │
   │       Size: M, Color: Blue                  │
   │       Qty: [1] [-][+]    $49.99    [Remove] │
   ├─────────────────────────────────────────────┤
   │ [IMG] Product B                             │
   │       Qty: [2] [-][+]    $59.98    [Remove] │
   ├─────────────────────────────────────────────┤
   │                     Subtotal: $109.97       │
   │              Shipping: Calculated at checkout│
   │                   Tax: Calculated at checkout│
   ├─────────────────────────────────────────────┤
   │ [Continue Shopping]      [Proceed to Checkout]│
   └─────────────────────────────────────────────┘
  ↓
5. CHECKOUT - CUSTOMER INFO
   IF logged in:
   • Details pre-filled, option to edit
   
   IF guest:
   • Enter:
     - Email address
     - First name, Last name
     - Phone (optional)
   • Option: ☐ Create account for order tracking
  ↓
6. CHECKOUT - SHIPPING (Physical Products Only)
   IF digital products only:
   • Skip to Step 8
   
   IF physical products:
   • Enter shipping address:
     - Street address
     - Apartment/unit (optional)
     - City
     - State/Province
     - ZIP/Postal code
     - Country
   • ☐ Save address for future orders
   • ☐ Billing address same as shipping
  ↓
7. CHECKOUT - SHIPPING METHOD
   System calculates shipping options:
   
   IF Bob Go configured (South Africa):
   ┌─────────────────────────────────┐
   │ Select Shipping Method:        │
   │ ○ The Courier Guy - R99        │
   │   (2-3 business days)          │
   │ ○ Dawn Wing - R79              │
   │   (3-5 business days)          │
   │ ○ Pargo Pickup Point - R59     │
   │   (4-6 business days)          │
   └─────────────────────────────────┘
   
   IF Easyship configured (International):
   ┌─────────────────────────────────┐
   │ Select Shipping Method:        │
   │ ○ DHL Express - $45            │
   │   (3-5 business days)          │
   │ ○ FedEx Economy - $32          │
   │   (7-10 business days)         │
   │ ○ Standard Post - $15          │
   │   (14-21 business days)        │
   └─────────────────────────────────┘
   
   IF Manual shipping only:
   • Business-defined shipping rates displayed
   • Or "Shipping calculated separately"
  ↓
8. CHECKOUT - PAYMENT
   Order summary:
   ┌─────────────────────────────────┐
   │ ORDER SUMMARY                  │
   │                                 │
   │ Subtotal (2 items): $109.97    │
   │ Shipping: $12.99               │
   │ Tax (15%): $18.44              │
   │                                 │
   │ TOTAL: $141.40                 │
   └─────────────────────────────────┘
   
   Payment methods:
   ○ Credit/Debit Card (Stripe/Paystack)
   ○ PayPal
   
   • Enter payment details
   • ☐ Save payment method for future orders
   • Review terms and conditions
   • Click "Place Order"
  ↓
8a. PAYMENT PROCESSING & EDGE CASES
   
   Show processing indicator (max 30 seconds)
   
   EDGE CASE - Gateway Timeout (30s):
   • Do NOT retry automatically (duplicate charge risk)
   • Show: "Payment processing - checking status..."
   • Poll gateway for status (3 attempts, 5 second intervals)
   • RESULTS:
     - Confirmed: Create order, proceed to confirmation
     - Failed: Show error + "Try again" button (new transaction)
     - Unknown: Create pending order + show "Payment verification in progress"
       → Send email with order ID + support contact
       → Manual verification by business within 24 hours
   
   EDGE CASE - Payment Declined:
   • Card declined: "Payment declined. Please try different payment method"
   • Insufficient funds: "Transaction could not be processed. Insufficient funds"
   • Security check failed: "Payment blocked by security check. Contact your bank"
   • Card expired: "Card expired. Please update payment details"
   • 3D Secure failed: "3D Secure authentication failed. Try again or use different card"
   
   EDGE CASE - Stock Changed During Checkout:
   • IF product sold out between cart and payment:
     - Stop payment processing
     - Remove out-of-stock items from cart
     - Show: "[Product Name] is now out of stock. Removed from order"
     - Update order total
     - Option to continue with remaining items OR cancel
   • IF quantity reduced (low stock):
     - Adjust quantity to available amount
     - Show: "Only [X] available. Quantity adjusted"
     - Update order total
     - Require customer confirmation before processing payment
   
   EDGE CASE - Price Changed:
   • IF product price increased since cart add:
     - Show: "Price changed for [Product Name]: $49.99 → $54.99"
     - Update cart total
     - Require customer confirmation: "Proceed with updated price?"
   • IF product price decreased:
     - Auto-apply lower price (customer benefit)
     - Show confirmation: "Good news! Price reduced to $44.99"
   
   EDGE CASE - Shipping Rate Changed:
   • IF courier rates updated during checkout:
     - Recalculate shipping
     - Show notification if significant change (>10%)
     - Require reconfirmation if increase >15%
   
   EDGE CASE - Session Expiry:
   • IF checkout session expired (30 minutes):
     - Show: "Checkout session expired for security"
     - Save cart contents
     - Redirect to cart page
     - Retain all entered information if logged in
   
   EDGE CASE - Duplicate Order Prevention:
   • IF "Place Order" clicked multiple times:
     - Disable button after first click
     - Show processing indicator
     - Ignore subsequent clicks
     - Set order reference before payment to prevent duplicates
   
   BEST PRACTICES:
   • Always create order record BEFORE processing payment
   • Order status: "Pending Payment" until payment confirms
   • Use idempotency keys (Stripe/Paystack) to prevent duplicate charges
   • Log all payment attempts for troubleshooting
   • Send abandoned cart recovery email if payment fails (after 1 hour)
   
   IF payment successful:
   • Update order status: "Paid"
   • Reserve inventory
   • Generate invoice
   → Proceed to Step 9
  ↓
9. ORDER CONFIRMATION
   Success page:
   ┌─────────────────────────────────┐
   │ ✓ ORDER CONFIRMED              │
   │                                 │
   │ Order #: ORD-2026-005678       │
   │                                 │
   │ Confirmation email sent to:     │
   │ customer@email.com              │
   │                                 │
   │ [Track Order]                   │
   │ [Continue Shopping]             │
   └─────────────────────────────────┘
   
   IF Digital Products:
   • Download links displayed immediately
   • Download links also sent via email
   • Links expire after X days (configurable)
   
   IF Physical Products:
   • Estimated delivery date shown
   • Tracking info sent when shipped
  ↓
END: Order placed, confirmation email sent
```

### Post-Purchase Flow (Physical Products):

```
Order placed → Merchant notified
  ↓
MERCHANT: Process Order
  • View in Orders dashboard
  • Pick and pack items
  • Create shipment (manual or via API)
  • Enter tracking number
  • Mark as "Shipped"
  ↓
SYSTEM: Notify Customer
  • Email with tracking number
  • Link to track shipment
  ↓
CUSTOMER: Track Delivery
  • View order status in account
  • Track via carrier website
  ↓
DELIVERY: Order Arrives
  • Customer receives package
  • Order status: "Delivered"
  ↓
POST-DELIVERY: Review Request
  • Email sent after delivery
  • "How was your order? Leave a review"
  ↓
END: Transaction complete
```

---

## 5. Membership Subscription Flow

**Actor:** Member (End User)  
**Goal:** Subscribe to membership tier  
**Duration:** 5-10 minutes

### Flow Steps:

```
START: Visitor views membership/pricing page
  ↓
1. BROWSE MEMBERSHIP TIERS
   Display tier comparison:
   ┌───────────────────────────────────────────────────┐
   │         BRONZE        SILVER         GOLD        │
   │         $29/mo        $59/mo         $99/mo      │
   ├───────────────────────────────────────────────────┤
   │ Features:                                         │
   │ Basic content     ✓             ✓             ✓  │
   │ Monthly webinar   ✗             ✓             ✓  │
   │ Community forum   ✗             ✓             ✓  │
   │ 1-on-1 coaching   ✗             ✗             ✓  │
   │ Priority support  ✗             ✗             ✓  │
   ├───────────────────────────────────────────────────┤
   │ [Select]          [Select]       [Select]        │
   │                   Most Popular                   │
   └───────────────────────────────────────────────────┘
  ↓
2. SELECT TIER
   • Click "Select" on desired tier
   • Tier details page:
     - Full benefits description
     - What's included
     - Cancellation policy
     - FAQ for this tier
  ↓
3. BILLING CYCLE SELECTION
   Choose billing frequency:
   ○ Monthly: $59/month
   ○ Quarterly: $159/quarter (save 10%)
   ○ Annual: $590/year (save 17%)
   
   IF trial available:
   • "Start with 14-day free trial"
   • ☐ Yes, start free trial
  ↓
4. CREATE ACCOUNT
   IF existing customer:
   • Log in
   • Proceed to payment
   
   IF new member:
   • Enter:
     - Name
     - Email
     - Password
     - Phone (optional)
   • ☐ Agree to terms and membership agreement
  ↓
5. PAYMENT SETUP
   • Enter payment details:
     - Credit/Debit Card (Stripe/Paystack)
   • Note: "Your card will be charged automatically each billing cycle"
   
   IF trial selected:
   • "Card will be charged $59 on [date] unless cancelled"
   
   Payment gateways:
   • Stripe (handles recurring billing)
   • Paystack (handles recurring billing for Africa)
   • Note: PayPal NOT available for subscriptions
  ↓
6. CONFIRM SUBSCRIPTION
   Review summary:
   ┌─────────────────────────────────┐
   │ MEMBERSHIP SUMMARY             │
   │                                 │
   │ Tier: Silver                    │
   │ Billing: Monthly               │
   │ Amount: $59.00/month           │
   │                                 │
   │ Trial: 14 days free            │
   │ First charge: Feb 1, 2026      │
   │                                 │
   │ ☐ I agree to the membership    │
   │   terms and auto-renewal       │
   │                                 │
   │ [Start Membership]              │
   └─────────────────────────────────┘
  ↓
7. MEMBERSHIP ACTIVATED
   Success page:
   ┌─────────────────────────────────┐
   │ ✓ WELCOME TO SILVER!           │
   │                                 │
   │ Your membership is now active.  │
   │                                 │
   │ [Access Member Area]            │
   │ [View Member Benefits]          │
   │ [Download Member Guide]         │
   └─────────────────────────────────┘
   
   Automated emails:
   • Welcome email with login details
   • Getting started guide
   • Member benefits overview
   • How to get help
  ↓
END: Member has full access to tier benefits
```

### Membership Management Flows:

```
UPGRADE TIER:
Member → Account → Membership → Upgrade
  • View higher tiers
  • Select new tier
  • Proration calculated automatically
  • Confirm upgrade
  • Immediate access to new benefits

DOWNGRADE TIER:
Member → Account → Membership → Change Plan
  • View lower tiers
  • Select new tier
  • Effective at next billing cycle
  • Confirm downgrade

PAUSE MEMBERSHIP:
Member → Account → Membership → Pause
  • Select pause duration (1-3 months)
  • Confirm pause
  • Access suspended until resume date
  • No charges during pause

CANCEL MEMBERSHIP:
Member → Account → Membership → Cancel
  • Exit survey (optional)
  • Retention offer displayed (optional)
  • Confirm cancellation
  • Access until end of billing period
  • Confirmation email sent
```

---

## 6. Admin Daily Operations Flow

**Actor:** Business Owner / Staff  
**Goal:** Manage daily business operations  
**Duration:** Ongoing throughout day

### Navigation Reference:

**Navigation Method:** Material Design 3 NavigationDrawerLayout with NavigationLink components  
**Layout:** Forms render within AdminLayout (NavigationDrawerLayoutTemplate with navigation drawer)

**M3 Navigation Architecture:**
```
📊 Dashboard (nav_dashboard)

▼ Sales & Operations
   📅 Bookings (nav_bookings - if enabled)
   🛒 Products (nav_products - if enabled)
   📦 Orders (nav_orders - if enabled)
   🛏️ Rooms (nav_rooms - if hospitality enabled)
   💼 Services (nav_services - if services enabled)
   🎫 Memberships (nav_memberships - if memberships enabled)

▼ Customers & Marketing
   👥 Contacts (nav_contacts)
   📧 Campaigns (nav_campaigns - if marketing enabled)
   📨 Broadcasts (nav_broadcasts - if marketing enabled)
   🎯 Segments (nav_segments - if marketing enabled)
   ✅ Tasks (nav_tasks - if marketing enabled)

▼ Content & Website
   ✍️ Blog (nav_blog - if enabled)
   📄 Pages (nav_pages)
   🖼️ Media (nav_media)

▼ Finance & Reports
   💳 Payments (nav_payments)
   📑 Invoices (nav_invoices)
   📊 Reports (nav_reports)
   📈 Analytics (nav_analytics)

⚙️ Settings (nav_settings - Owner/Manager only)
```

**How M3 navigation works:**
1. User clicks NavigationLink in drawer (e.g., nav_dashboard, nav_bookings)
2. NavigationLink's `navigate_to` property automatically opens target form
3. Form renders in AdminLayout's content panel
4. NavigationLink automatically highlights (selected=True)
5. NO click handlers needed - M3 handles navigation automatically

**M3 vs Traditional Pattern:**
- ✅ M3: NavigationLink with navigate_to property (declarative)
- ❌ Old: Link with click handler calling open_form() (imperative)

**Mobile Responsiveness:**
- Desktop/Tablet: Navigation drawer visible as persistent sidebar
- Mobile: Navigation drawer collapses to modal overlay (hamburger menu)
- Automatic - no code required

### Morning Dashboard Review:

```
START: Admin logs into dashboard
  ↓
1. VIEW DASHBOARD OVERVIEW
   Dashboard displays:
   ┌─────────────────────────────────────────────┐
   │ TODAY'S METRICS                             │
   │ Revenue: $1,247    Bookings: 3    Orders: 5 │
   ├─────────────────────────────────────────────┤
   │ ALERTS                                      │
   │ ⚠ Low stock: Widget Pro (2 remaining)      │
   │ ⚠ 2 reviews pending approval               │
   │ ℹ 1 support ticket awaiting response       │
   ├─────────────────────────────────────────────┤
   │ RECENT ACTIVITY                             │
   │ • John D. booked Deluxe Room - 10 mins ago │
   │ • Order #5678 placed - 25 mins ago         │
   │ • Sarah M. cancelled appointment - 1 hr ago│
   ├─────────────────────────────────────────────┤
   │ STORAGE USAGE                               │
   │ Database: ████████░░ 85,423 / 150,000 (57%)│
   │ Media: ████░░░░░░ 4.2 GB / 10 GB (42%)     │
   └─────────────────────────────────────────────┘
  ↓
2. PROCESS PENDING ITEMS
   Click alert → Opens relevant Form via `open_form()`:
   
   A. Low Stock Alert:
      • Click alert → Opens ProductList Form (filtered: low stock)
      • Review stock levels
      • Reorder or adjust alerts
   
   B. Pending Reviews:
      • Click alert → Opens ReviewModerationForm
      • Read each review
      • Approve (publish) or Reject
      • Optional: Write business response
   
   C. Support Tickets:
      • Click alert → Opens TicketManagementForm
      • Read customer message
      • Respond or assign to staff
  ↓
3. CHECK TODAY'S CALENDAR
   Click "Bookings" NavigationLink (nav_bookings) → Opens BookingCalendarForm
   
   Day view shows:
   ┌─────────────────────────────────────────────┐
   │ TODAY: January 15, 2026                     │
   ├─────────────────────────────────────────────┤
   │ 09:00  Consultation - Jane S. (Video)      │
   │ 11:00  Check-out - Room 102 - Smith family │
   │ 14:00  Check-in - Room 101 - Johnson party │
   │ 14:00  Check-in - Room 103 - Garcia couple │
   │ 15:30  Massage - Mike T. (In-person)       │
   └─────────────────────────────────────────────┘
   
   Prepare for scheduled events
  ↓
4. PROCESS NEW ORDERS
   Click "Orders" NavigationLink (nav_orders) → Opens OrderListForm (filtered: Pending)
   
   For each order:
   • Review order details
   • Check inventory availability
   • Print packing slip
   • Mark as "Processing"
   • Pick and pack items
   • Create shipment
   • Mark as "Shipped"
  ↓
END: Morning routine complete
```

### Processing a Booking:

```
Notification: "New booking received"
  ↓
1. OPEN BOOKING DETAIL
   • Click notification → Calls `open_form('BookingDetail', booking_id=...)`
   • OR: Click "Bookings" NavigationLink (nav_bookings) → Opens BookingListForm → Click booking row
  ↓
2. REVIEW BOOKING DETAILS
   ┌─────────────────────────────────────────────┐
   │ BOOKING #BK-2026-001234                     │
   │ Status: PENDING                             │
   ├─────────────────────────────────────────────┤
   │ Customer: John Smith                        │
   │ Email: john@email.com                       │
   │ Phone: +1 555-0123                          │
   ├─────────────────────────────────────────────┤
   │ Room: Deluxe Double                         │
   │ Check-in: Jan 20, 2026 (2:00 PM)           │
   │ Check-out: Jan 23, 2026 (11:00 AM)         │
   │ Guests: 2                                   │
   ├─────────────────────────────────────────────┤
   │ Special Requests:                           │
   │ "Arriving late, around 8 PM. Need quiet     │
   │  room if possible."                         │
   ├─────────────────────────────────────────────┤
   │ Payment: $517.50 PAID (Stripe)             │
   └─────────────────────────────────────────────┘
  ↓
3. CONFIRM BOOKING
   • Verify availability (system shows conflicts if any)
   • Assign specific room number (if applicable)
   • Note special requests for housekeeping
   • Click "Confirm Booking"
   • Status changes: PENDING → CONFIRMED
  ↓
4. AUTOMATED NOTIFICATIONS
   System sends:
   • Confirmation email to guest
   • Calendar event created
   • Housekeeping notified (if integrated)
  ↓
END: Booking confirmed and ready
```

### Check-In Process (Hospitality):

```
Guest arrives for check-in
  ↓
1. FIND BOOKING
   • Search by guest name, email, or booking number
   • OR: Dashboard shows "Today's Check-ins"
  ↓
2. VERIFY GUEST
   • Confirm identity
   • Check payment status (paid/balance due)
   • Collect balance if required
  ↓
3. PROCESS CHECK-IN
   • Click "Check In"
   • Assign room key/code
   • Provide WiFi password
   • Explain house rules
   • Update room status to "Occupied"
  ↓
4. RECORD CHECK-IN
   • System logs check-in time
   • Guest status: "Checked In"
   • Room status: "Occupied"
  ↓
END: Guest checked in
```

---

## 7. Content Management Flow

**Actor:** Business Owner / Content Manager  
**Goal:** Update website content and publish blog posts  
**Duration:** 15-60 minutes per task

**Navigation Note:** All navigation uses Material Design 3 NavigationDrawerLayout with NavigationLink components. NavigationLinks have a `navigate_to` property set to the target form name (e.g., nav_bookings.navigate_to='BookingListForm'). Clicking a NavigationLink automatically opens the form - no click handlers required. For programmatic navigation, `open_form('FormName', **params)` can still be used.

### Updating Website Content:

```
START: Admin wants to update homepage
  ↓
1. OPEN PAGE EDITOR
   Click "Pages" NavigationLink (nav_pages) → Opens PageEditorForm
   → Select "Home Page" from list → Opens HomePageEditorForm
  ↓
2. SELECT ELEMENT TO EDIT
   Page shows editable sections:
   • Hero headline
   • Hero subheadline
   • Hero image
   • About section text
   • Featured services/products
   • Testimonials
   • Contact info
  ↓
3. EDIT TEXT CONTENT
   • Click text element → Edit mode
   • Change text
   • Character counter shows: "45 of 100 characters"
   • Save changes
  ↓
4. EDIT IMAGE CONTENT
   • Click image element → Edit mode
   • Current image displayed with info:
     - Filename: hero_bg.jpg
     - Dimensions: 1920x1080
     - Required: "Must be 1920x1080"
   • Click "Change Image"
   • Upload new image
   • System validates dimensions
   • Confirm change
  ↓
5. PREVIEW CHANGES
   • Click "Preview"
   • View as customer sees it
   • Check desktop and mobile views
  ↓
6. PUBLISH
   • Click "Publish Changes"
   • Changes go live immediately
  ↓
END: Website content updated
```

### Publishing a Blog Post:

```
START: Admin wants to create blog post
  ↓
1. CREATE NEW POST
   Dashboard → Content → Blog → New Post
  ↓
2. WRITE CONTENT
   ┌─────────────────────────────────────────────┐
   │ Title: [________________________]           │
   │                                             │
   │ ┌─────────────────────────────────────────┐│
   │ │ B I U │ H1 H2 │ • │ 1. │ 🔗 │ 📷 │ { } ││
   │ ├─────────────────────────────────────────┤│
   │ │                                         ││
   │ │ Write your post content here...         ││
   │ │                                         ││
   │ │                                         ││
   │ └─────────────────────────────────────────┘│
   └─────────────────────────────────────────────┘
   
   • Write post using rich text editor
   • Add images (upload or select from library)
   • Add formatting (headers, lists, bold, etc.)
  ↓
3. SET METADATA
   Sidebar options:
   • Excerpt: [Short summary for previews]
   • Category: [Select from dropdown]
   • Tags: [keyword1, keyword2, ...]
   • Featured Image: [Upload/Select]
   • Author: [Select staff member]
  ↓
4. SEO SETTINGS
   • SEO Title: [Custom title for search]
   • Meta Description: [160 characters max]
   • URL Slug: [auto-generated, editable]
  ↓
5. PUBLISH OPTIONS
   ○ Save as Draft (continue later)
   ○ Publish Now (goes live immediately)
   ○ Schedule (select date and time)
   
   • Select option
   • Click corresponding button
  ↓
6. SHARE (If Published)
   • Social share buttons appear:
     - Share to Facebook
     - Share to Twitter/X
     - Share to LinkedIn
     - Share to WhatsApp
     - Copy Link
   • Select platforms
   • Customize message if needed
  ↓
END: Blog post published
```

---

## 8. Customer Support Flow

**Actor:** Customer (submitting) / Staff (responding)  
**Goal:** Resolve customer issues efficiently  
**Duration:** Minutes to hours depending on complexity

### Customer Submits Ticket:

```
START: Customer has issue or question
  ↓
1. ACCESS SUPPORT
   Options:
   • Click "Help" in navigation
   • Click "Contact Support" in footer
   • Access from customer account
  ↓
2. SEARCH KNOWLEDGE BASE FIRST
   • Search box: "How do I reset password?"
   • System searches KB articles
   • Matching articles displayed:
     - "How to Reset Your Password"
     - "Account Access Issues"
   
   IF answer found:
   • Customer reads article
   • Issue resolved → END
   
   IF not found:
   • Click "Still need help? Submit a ticket"
  ↓
3. SUBMIT SUPPORT TICKET
   Form:
   ┌─────────────────────────────────────────────┐
   │ SUBMIT SUPPORT REQUEST                      │
   ├─────────────────────────────────────────────┤
   │ Subject: [________________________]         │
   │                                             │
   │ Category: [Select...]                       │
   │   • Booking/Reservation                     │
   │   • Payment/Billing                         │
   │   • Technical Issue                         │
   │   • General Question                        │
   │   • Other                                   │
   │                                             │
   │ Priority: ○ Low  ○ Medium  ○ High          │
   │                                             │
   │ Description:                                │
   │ ┌─────────────────────────────────────────┐│
   │ │                                         ││
   │ │                                         ││
   │ └─────────────────────────────────────────┘│
   │                                             │
   │ Attachments: [Upload files]                │
   │                                             │
   │ [Submit Ticket]                             │
   └─────────────────────────────────────────────┘
  ↓
4. TICKET CREATED
   • Ticket number assigned: TKT-2026-000123
   • Confirmation email sent
   • Customer can track status
  ↓
END: Ticket submitted, awaiting response
```

### Staff Responds to Ticket:

```
START: Staff sees new ticket notification
  ↓
1. VIEW TICKET QUEUE
   Dashboard → Help → Tickets
   
   ┌─────────────────────────────────────────────┐
   │ SUPPORT TICKETS                             │
   ├─────────────────────────────────────────────┤
   │ [Filter: All | Open | In Progress | Closed]│
   ├─────────────────────────────────────────────┤
   │ 🔴 TKT-000123  Payment not processed       │
   │    John S. - High - 10 mins ago            │
   │                                             │
   │ 🟡 TKT-000122  How to change booking       │
   │    Mary T. - Medium - 2 hours ago          │
   │                                             │
   │ 🟢 TKT-000121  General question            │
   │    Bob R. - Low - 1 day ago                │
   └─────────────────────────────────────────────┘
  ↓
2. OPEN TICKET
   • Click ticket to view full details
   • See customer info, history, attachments
  ↓
3. RESPOND TO CUSTOMER
   ┌─────────────────────────────────────────────┐
   │ TICKET: TKT-000123                          │
   │ Status: Open → [Change to: In Progress ▼]  │
   ├─────────────────────────────────────────────┤
   │ CUSTOMER MESSAGE:                           │
   │ "I tried to pay for my booking but it       │
   │  keeps showing an error..."                 │
   ├─────────────────────────────────────────────┤
   │ YOUR RESPONSE:                              │
   │ ┌─────────────────────────────────────────┐│
   │ │ Hi John,                                ││
   │ │                                         ││
   │ │ I'm sorry to hear about the payment    ││
   │ │ issue. I've checked your booking and...││
   │ └─────────────────────────────────────────┘│
   │                                             │
   │ ☐ Add internal note (not visible to customer)│
   │                                             │
   │ [Send Response] [Send & Mark Resolved]      │
   └─────────────────────────────────────────────┘
  ↓
4. FOLLOW UP
   • Customer receives email notification
   • Customer can reply to continue conversation
   • Staff monitors until resolved
  ↓
5. CLOSE TICKET
   • Issue resolved
   • Mark as "Resolved"
   • Customer can reopen if needed
  ↓
END: Ticket resolved
```

---

## 9. Error Recovery Flows

### Payment Failure Recovery:

```
Customer attempts payment → Payment fails
  ↓
1. DISPLAY ERROR
   ┌─────────────────────────────────────────────┐
   │ ⚠ Payment could not be processed           │
   │                                             │
   │ This could be due to:                       │
   │ • Incorrect card details                    │
   │ • Insufficient funds                        │
   │ • Card declined by bank                     │
   └─────────────────────────────────────────────┘
  ↓
2. OFFER RETRY
   • "Please verify your card details"
   • Allow edit card number
   • [Try Again with Same Card]
  ↓
IF successful → Continue to confirmation

IF still fails:
  ↓
3. ALTERNATIVE PAYMENT
   • "Would you like to try a different payment method?"
   • Options:
     ○ Different credit/debit card
     ○ PayPal (if available)
  ↓
4. HOLD BOOKING/ORDER
   • Save as "Payment Pending"
   • Hold for 15 minutes
   • Send email with payment link
   • Customer can complete payment later
  ↓
5. EXPIRY
   IF not paid within 15 minutes:
   • Release inventory
   • Notify customer: "Your booking has expired"
   • Encourage to try again
```

### Out of Stock Recovery:

```
Customer adds item → Item goes out of stock during checkout
  ↓
1. DETECT AT CHECKOUT
   • System checks real-time inventory
   • Item no longer available
  ↓
2. NOTIFY CUSTOMER
   ┌─────────────────────────────────────────────┐
   │ ⚠ Item Unavailable                         │
   │                                             │
   │ Sorry, "Product Name" is no longer         │
   │ available in the requested quantity.        │
   │                                             │
   │ [Remove from Cart]                          │
   │ [Notify When Available]                     │
   └─────────────────────────────────────────────┘
  ↓
3. OFFER ALTERNATIVES
   • "Similar products you might like:"
   • Display 3-5 related items
   • Allow add to cart
  ↓
4. WAITLIST OPTION
   IF customer wants notification:
   • Capture email (if guest)
   • Add to product waitlist
   • "We'll email you when it's back in stock"
```

### Session Timeout Recovery:

```
Customer in middle of checkout → Session expires
  ↓
1. DETECT TIMEOUT
   • 30 minutes of inactivity
   • Session expires
  ↓
2. PRESERVE CART
   • Cart contents saved to database
   • Associated with email (if provided) or cookie
  ↓
3. PROMPT RE-LOGIN
   ┌─────────────────────────────────────────────┐
   │ Your session has expired                    │
   │                                             │
   │ Don't worry - your cart has been saved!    │
   │                                             │
   │ [Log In to Continue]                        │
   │ [Continue as Guest]                         │
   └─────────────────────────────────────────────┘
  ↓
4. RESTORE SESSION
   • Customer logs in or continues
   • Cart automatically restored
   • Continue from where they left off
```

---

## Flow Design Principles

### 1. Progressive Disclosure
- Show only relevant information at each step
- Expand details on demand
- Don't overwhelm users with all options upfront

### 2. Clear Navigation
- Always show clear call-to-action
- Indicate progress (Step 2 of 5)
- Provide "Back" option at every step
- Show what happens next

### 3. Error Prevention
- Validate inputs in real-time
- Show requirements clearly before input
- Disable invalid actions
- Confirm destructive actions

### 4. Recovery Paths
- Every error has a clear solution
- Offer alternatives when primary path fails
- Never dead-end the user
- Save progress automatically

### 5. Confirmation & Feedback
- Confirm all significant actions
- Show success messages prominently
- Send email confirmations for all transactions
- Provide tracking and status visibility

### 6. Accessibility
- Keyboard navigation support
- Screen reader compatibility
- Sufficient color contrast
- Clear, readable fonts

---

## 10. Contact Management Flow

**Actor:** Business Owner  
**Goal:** View and manage all customer/lead contacts  
**Entry Point:** Dashboard → Contacts  
**Duration:** 2-5 minutes

### Flow Steps:

```
START: User clicks "Contacts" in main navigation
  ↓
1. LOAD CONTACT LIST
   System displays ContactListForm:
   
   • Total contact count with status breakdown:
     Total: 234 | Customers: 156 (67%) | Leads: 78 (33%)
   
   • Pre-built segments for vertical (Hospitality example):
     - VIP Guests (3+ stays): 12 contacts [View]
     - Repeat Guests (2+ stays): 34 contacts [View]
     - Haven't Returned (180+ days): 45 contacts [View]
     - Upcoming Guests (next 30 days): 8 contacts [View]
     - Birthday This Month: 3 contacts [View]
   
   • Search bar with real-time filtering
   • Contact DataGrid showing:
     Name | Email | Status | Total Spent | Last Contact
  ↓
2. USER ACTIONS (Choose One):
   
   A. VIEW SEGMENT
      • User clicks segment: "VIP Guests"
      • List filters to show only VIP contacts (12 contacts)
      • Segment metrics displayed
      • User can export segment to CSV
   
   B. SEARCH CONTACT
      • User types "Sarah" in search
      • List filters in real-time
      • Matching contacts shown instantly
   
   C. VIEW CONTACT DETAIL
      • User clicks contact row: "Sarah Johnson"
      • System opens ContactDetailForm showing:
        - Contact info (name, email, phone, status)
        - Quick stats (R2,340 spent, 3 transactions)
        - Activity timeline (bookings, emails, notes)
        - Active campaigns (currently enrolled sequences)
      • User can:
        - Add note to contact
        - Create booking (pre-fills contact info)
        - Send email
        - Enroll in campaign
   
   D. ADD NEW CONTACT
      • User clicks "[+ Add Contact]"
      • ContactEditorForm opens
      • User enters: First Name, Last Name, Email, Phone
      • User sets Status: Lead or Customer
      • User adds tags (optional)
      • User clicks [Save]
      • Contact created, appears in list
   
   E. BULK ACTIONS
      • User selects multiple contacts (checkboxes)
      • User applies action:
        - Add tag: "Newsletter"
        - Enroll in campaign: "Re-engagement"
        - Export selected to CSV
  ↓
END: User manages contacts efficiently
```

**Success Criteria:**
- Find any contact in < 30 seconds
- Segments update automatically
- Search is instant
- Bulk actions work correctly
- Contact detail shows complete history

**Integration Points:**
- Bookings automatically create/update contacts
- Orders automatically create/update contacts
- Forms automatically create lead contacts
- Review submissions update contact timeline

---

## 11. Email Campaign Setup Flow

**Actor:** Business Owner  
**Goal:** Activate automated email sequence  
**Entry Point:** Marketing → Email Campaigns → [+ New Campaign]  
**Duration:** 3-5 minutes (first time), 30 seconds (subsequent)

### Flow Steps:

```
START: User navigates to Marketing → Email Campaigns
  ↓
1. VIEW CAMPAIGNS DASHBOARD
   System displays EmailCampaignListForm:
   
   Active Campaigns (3):
   ┌─────────────────────────────────────────────┐
   │ Abandoned Booking Recovery      ● ACTIVE   │
   │ 47 enrolled | 8 conversions (17%)          │
   │ [View] [Pause] [Edit]                      │
   └─────────────────────────────────────────────┘
   
   ┌─────────────────────────────────────────────┐
   │ Welcome New Guests              ● ACTIVE   │
   │ 34 enrolled | 41% open rate                │
   │ [View] [Pause] [Edit]                      │
   └─────────────────────────────────────────────┘
   
   [+ New Campaign] button
  ↓
2. USER CLICKS [+ New Campaign]
   EmailCampaignEditorForm opens
  ↓
3. STEP 1: CHOOSE CAMPAIGN TYPE
   System shows pre-built templates for vertical:
   
   [Hospitality Templates]
   ○ Abandoned Booking Recovery (3 emails)
   ○ Welcome New Guests (5 emails)
   ⦿ Post-Stay Follow-Up (3 emails) [Selected]
   ○ Re-engagement (90+ days) (3 emails)
   
   • User selects template
   • System loads email sequence preview
   • User clicks [Next]
  ↓
4. STEP 2: REVIEW SEQUENCE
   System displays email sequence:
   
   Email 1 - "Thank You for Staying" (24 hours after checkout)
   Subject: "We hope you enjoyed your stay at [Business Name]"
   Preview: "Hi {{first_name}}, Thank you for choosing..."
   [Preview Full Email]
   
   Email 2 - "Leave a Review" (48 hours after checkout)
   Subject: "Share your experience - Help future guests"
   [Preview Full Email]
   
   Email 3 - "Come Back Soon" (7 days after checkout)
   Subject: "15% off your next stay"
   [Preview Full Email]
   
   • User can preview/edit emails (optional)
   • Most users keep defaults
   • User clicks [Next]
  ↓
5. STEP 3: SET TRIGGER
   System shows trigger configuration:
   
   Activate this campaign when:
   ⦿ Guest checks out (booking status = completed)
   
   First email sends:
   [24▼] hours after checkout
   
   • User reviews trigger (default usually correct)
   • User clicks [Next]
  ↓
6. STEP 4: ACTIVATE
   System shows confirmation:
   
   Ready to Activate!
   
   Campaign: Post-Stay Follow-Up
   Emails: 3 (Day 1, Day 2, Day 7)
   Trigger: Guest checkout
   
   When activated:
   ✓ Guests auto-enrolled after checkout
   ✓ Emails send on schedule
   ✓ Opens/clicks tracked automatically
   ✓ Reviews from emails tracked
   
   • User clicks [Activate Campaign]
  ↓
7. CAMPAIGN ACTIVATED
   • System creates campaign record
   • Status set to: Active
   • System returns to campaigns dashboard
   • Campaign appears in Active list
   • System monitors bookings for trigger
   • Auto-enrolls guests on checkout
  ↓
END: Campaign running automatically
```

**Success Criteria:**
- Setup takes < 5 minutes for first-time users
- Pre-built templates need zero customization
- Triggers work reliably
- Enrollments happen automatically
- Tracking is automatic

**Background Process:**
- Hourly job checks active enrollments
- Sends next email if schedule says it's time
- Updates enrollment sequence_day
- Logs opens/clicks via Brevo webhooks
- Updates campaign performance metrics

---

## 12. Marketing Dashboard Review Flow

**Actor:** Business Owner  
**Goal:** Review marketing performance and take action  
**Entry Point:** Marketing → Dashboard OR Dashboard widget  
**Duration:** 2-5 minutes

### Flow Steps:

```
START: User navigates to Marketing → Dashboard
  ↓
1. VIEW DASHBOARD METRICS
   System displays MarketingDashboardForm:
   
   📊 CONTACTS (This Month)
   Total: 234 | New: 23 (+11%)
   Customers: 156 (67%) | Leads: 78 (33%)
   
   💰 REVENUE
   This Month: R24,500 | Last: R21,300 (+15%)
   Avg Customer Value: R845
   
   📧 EMAIL PERFORMANCE
   Sent: 487 | Opened: 289 (59%)
   Clicked: 78 (16%) | Conversions: 12
   
   🎯 TOP LEAD SOURCES
   1. Website Form (34%) - R8,400
   2. Booking Widget (28%) - R6,900
   3. Email Pop-up (19%) - R4,700
   4. Referral (12%) - R2,900
   5. Social (7%) - R1,600
   
   ⚠️ NEEDS ATTENTION
   • 22 contacts inactive 90+ days
     [Send Re-engagement Campaign]
   • 8 abandoned bookings (48 hours)
     [View Abandoned Bookings]
   • 3 birthdays this week
     [Send Birthday Offers]
  ↓
2. USER ACTIONS (Choose One):
   
   A. INVESTIGATE METRIC
      • User clicks "Email Performance"
      • System opens detailed report:
        - Abandoned Booking Recovery: 60% open, 17% conversion
        - Welcome Sequence: 41% open, 12% click
        - Re-engagement: 32% open, 14% conversion
      • User identifies best performers
   
   B. TAKE ACTION ON ALERT
      • User clicks [Send Re-engagement Campaign]
      • System confirms: "Send to 22 inactive contacts?"
      • User clicks [Yes]
      • System enrolls 22 contacts
      • Alert disappears
      • Success message: "✅ 22 contacts enrolled in re-engagement"
   
   C. VIEW DETAILED REPORT
      • User clicks "View All Reports"
      • System shows 5 reports:
        1. Contact Growth
        2. Email Performance
        3. Revenue by Source
        4. Customer Activity
        5. Marketing ROI
      • User selects report
      • System displays detailed metrics with charts
   
   D. CHANGE TIME PERIOD
      • User clicks: [This Month ▼]
      • Options: This Week | This Month | This Quarter
      • User selects "This Quarter"
      • All metrics recalculate
      • Charts update
   
   E. EXPORT DATA
      • User clicks [Export]
      • Options:
        ○ Export to PDF
        ○ Export to CSV
        ○ Email me this report
        ○ Schedule weekly email
      • User selects option
      • System generates and delivers
  ↓
END: User understands marketing performance
     Takes action on opportunities
     Has data to improve strategies
```

**Success Criteria:**
- Dashboard loads in < 3 seconds
- Metrics are accurate and current
- Alerts are actionable
- Reports exportable
- Interface is visual and clear

**Alert Logic:**
- System runs nightly at 2am
- Calculates all metrics
- Identifies attention-needed items:
  - Contacts inactive 90+ days (re-engagement opportunity)
  - Abandoned bookings/carts recent 48 hours (recovery opportunity)
  - Upcoming birthdays/anniversaries (personalization opportunity)
- Generates actionable alerts
- One-click actions from dashboard

---


## 13. Website Homepage Customization Flow

**Actor:** Business Owner  
**Goal:** Customize homepage to match business branding and offerings  
**Duration:** 30-60 minutes  
**Frequency:** Once (initial setup), rarely thereafter

### Flow Steps:

```
START: Admin logged in, navigates to website settings
  ↓
1. NAVIGATE TO WEBSITE SETTINGS
   Route: /admin/settings/website
   • Click "Settings" NavigationLink (nav_settings) in admin navigation
   • Click "Website" tab
   • Page loads with current website configuration
  ↓
2. SELECT HOME PAGE TEMPLATE
   • View 7 template options with preview images:
     - Template 1: Classic Business (general use)
     - Template 2: E-commerce Focus (product showcase)
     - Template 3: Hospitality (room/accommodation showcase)
     - Template 4: Service Professional (consultant layout)
     - Template 5: Membership/Community (tier comparison)
     - Template 6: Event/Booking Focus (calendar visual)
     - Template 7: Minimalist/Portfolio (clean design)
   • Click template card to see full preview (opens in new tab)
   • Current template is highlighted
   • Click "Select" button on desired template
   System: Saves template selection to tbl_config.home_template
   • Confirmation: "Template selected! Configure your content below."
  ↓
3. CONFIGURE HERO SECTION
   Form fields displayed:
   • Headline (text input) - "Welcome to [Business Name]"
   • Subheadline (text input) - "Your tagline here"
   • Hero Image:
     - Upload button (max 5MB, JPG/PNG)
     - OR Image URL input
     - Preview thumbnail shown
   • CTA Button Text - "Get Started"
   • CTA Button Link - Dropdown (Contact, Services, Shop, Book Now, etc.)
   
   System: Auto-saves every 30 seconds
   • Draft indicator: "Last saved: 5 seconds ago"
  ↓
4. CONFIGURE FEATURES SECTION
   • "Add Feature" button (max 5 features)
   • For each feature:
     - Icon selector (Font Awesome icons, searchable)
     - Title (text input)
     - Description (textarea, 100 chars max)
     - Delete button
   • Drag to reorder features
   • Toggle: "Show features section" (on/off)
  ↓
5. CONFIGURE SERVICES SHOWCASE
   • Toggle: "Show services on homepage" (on/off)
   • Number slider: "How many services to display" (1-6)
   • Display style: Radio buttons (Cards / List / Carousel)
   
   IF services_enabled = false:
   • Warning: "Services feature is disabled. Enable in Features settings."
   • Disable toggle (grayed out)
  ↓
6. CONFIGURE TESTIMONIALS
   • "Add Testimonial" button (max 10 testimonials)
   • For each testimonial:
     - Customer Name (text input)
     - Testimonial Text (textarea, 300 chars max)
     - Rating (1-5 star selector)
     - Customer Photo (optional upload)
     - Company Name (optional)
     - Delete button
   • Drag to reorder testimonials
   • Auto-displays first 3 testimonials (or all if < 3)
  ↓
7. CONFIGURE FINAL CTA SECTION
   • Headline (text input) - "Ready to get started?"
   • Subheadline (optional) - "Join hundreds of happy customers"
   • CTA Button Text - "Contact Us"
   • CTA Button Link - Dropdown selection
  ↓
8. PREVIEW & PUBLISH
   • "Preview" button (opens homepage in new tab)
   • Review all sections
   • "Save Changes" button
   
   System Actions:
   • Validates all required fields
   • Saves to tbl_config.home_config (simpleObject)
   • Clears homepage cache
   • Success message: "Homepage updated successfully!"
   • "View Live Site" link
  ↓
END: Homepage is live with new configuration
```

### Success Criteria:
- Template selection saved
- All configuration fields populated
- Homepage renders correctly with selected template
- Mobile responsive layout works
- All CTAs link to correct pages

### Error Handling:
- **Missing required field:** "Please complete all required fields"
- **Image too large:** "Image must be under 5MB. Please compress or choose another."
- **Invalid URL:** "Please enter a valid URL (https://...)"
- **Save failure:** "Error saving. Please try again." (retry button shown)

---

## 14. Landing Page Creation Flow

**Actor:** Business Owner / Marketing Manager  
**Goal:** Create conversion-focused landing page for marketing campaign  
**Duration:** 20-40 minutes  
**Frequency:** Per campaign (multiple campaigns possible)

### Flow Steps:

```
START: Admin navigates to landing pages management
  ↓
1. NAVIGATE TO LANDING PAGES
   Route: /admin/landing-pages
   • Click "Customers & Marketing" NavigationLink section in admin navigation
   • Click "Landing Pages" submenu
   • Page displays:
     - Data grid of existing landing pages
     - Columns: Title, Template, Status, Views, Conversions, Conversion Rate
     - "Create New Landing Page" button (prominent)
  ↓
2. CLICK CREATE NEW
   Modal opens: "Choose Landing Page Template"
   • Display 5 template cards with descriptions:
     
     Template 1: Lead Capture
     - Use for: Email list building, lead magnets
     - Features: Email form, benefits list, trust badges
     
     Template 2: Product Launch
     - Use for: Promoting specific product/service
     - Features: Hero image, features, testimonials, buy button
     
     Template 3: Event Registration
     - Use for: Workshops, webinars, retreats
     - Features: Event details, speaker bio, registration form
     
     Template 4: Video Sales Letter (VSL)
     - Use for: Long-form video content
     - Features: Video player, key points, CTA
     
     Template 5: Membership Funnel
     - Use for: Membership tier selection
     - Features: Benefits, pricing tiers, testimonials
   
   • Click "Select" on desired template
   System: Template selection saved temporarily
  ↓
3. CONFIGURE BASIC SETTINGS
   Form displayed:
   • Landing Page Title (internal name) - "Summer Workshop 2026"
   • URL Slug (auto-generated from title, editable)
     - Validation: lowercase, hyphens only, unique
     - Preview URL shown: Mybizz.app/landing/summer-workshop-2026
   • Status: Draft (default) or Published (radio buttons)
  ↓
4. CONFIGURE TEMPLATE-SPECIFIC CONTENT
   (Example for Event Registration template)
   
   Section 1: Event Details
   • Event Name: "Summer Coding Workshop"
   • Date: Date picker
   • Time: "9:00 AM - 5:00 PM"
   • Location: "Online" or address input
   • Event Image: Upload (max 5MB)
   
   Section 2: Benefits
   • "Add Benefit" button (max 5)
   • Each benefit: Text input
   • Drag to reorder
   
   Section 3: Speaker/Host
   • Name: Text input
   • Bio: Textarea (300 chars)
   • Photo: Upload button
   
   Section 4: Registration CTA
   • CTA Button Text: "Register Now"
   • CTA Target: Dropdown
     - Booking Page
     - Custom URL
     - Email Collection (saves to tbl_leads)
   
   Section 5: FAQ (optional)
   • "Add FAQ" button
   • Question and Answer pairs
   
   Section 6: Advanced Settings (collapsible)
   • Limited Spots: Toggle + number input
   • Thank You Message: Textarea
   • Privacy Text: Textarea
   
   System: Auto-saves every 30 seconds
  ↓
5. PREVIEW LANDING PAGE
   • "Preview" button (opens in new tab)
   • Landing page opens with BlankLayout (no header/footer)
   • Review all sections
   • Test form submission (if applicable)
   • Test on mobile view
   
   IF issues found:
   → Return to step 4, make adjustments
  ↓
6. PUBLISH LANDING PAGE
   • Click "Publish" button
   
   System Actions:
   • Validates all required fields
   • Checks slug uniqueness
   • Saves to tbl_landing_pages:
     - title, slug, template_type
     - config (simpleObject with all settings)
     - status = 'published'
     - published_date = now()
     - views_count = 0
     - conversions_count = 0
   
   Success Modal:
   • "Landing page published successfully!"
   • Copy URL button: https://Mybizz.app/landing/summer-workshop-2026
   • Share buttons: Email, Facebook, Twitter, LinkedIn
   • "View Analytics" button
   • "Create Another" button
  ↓
7. SHARE LANDING PAGE
   Options:
   • Copy URL to clipboard
   • Send test email to self
   • Share on social media
   • Add to email campaign (if marketing_enabled)
   • Embed in website
  ↓
END: Landing page is live and ready for marketing campaign
```

### Success Criteria:
- Landing page published with unique URL
- All content displayed correctly
- Form submission works (if applicable)
- Mobile responsive
- Analytics tracking active (views, conversions)

### Error Handling:
- **Duplicate slug:** "This URL is already taken. Please choose another."
- **Missing required field:** "Please complete: [field name]"
- **Image upload failed:** "Upload failed. Check file size and format."
- **Publish failure:** "Unable to publish. Please try again." (with retry)

---

## 15. Visitor Contact Form Submission Flow

**Actor:** Website Visitor (Potential Customer)  
**Goal:** Contact business owner via website contact form  
**Duration:** 2-3 minutes  
**Frequency:** Variable (per visitor need)

### Flow Steps:

```
START: Visitor browsing business website
  ↓
1. NAVIGATE TO CONTACT PAGE
   Route: /contact (from main navigation)
   • Click "Contact" in website header
   • Page loads with:
     - Contact form
     - Business details (phone, email, address, hours)
     - Google Maps embed (if configured)
     - Social media links
  ↓
2. VIEW BUSINESS INFORMATION
   Displayed information:
   • Business Name
   • Address (if provided)
   • Phone Number (clickable for mobile)
   • Email Address (clickable)
   • Business Hours
   • Google Maps location
   • Social media icons (Facebook, Instagram, etc.)
   
   Visitor can:
   • Call directly (click phone number)
   • Email directly (click email)
   • View location on map
   • Visit social media pages
   OR
   → Continue to Step 3 to submit contact form
  ↓
3. COMPLETE CONTACT FORM
   Form fields:
   • Name: Text input (required)
   • Email: Email input (required)
   • Phone: Phone input (optional)
   • Message: Textarea (required, max 1000 chars)
   
   Validation (client-side):
   • Name: Not empty
   • Email: Valid format (contains @)
   • Message: Not empty, under 1000 chars
   
   Character counter shown: "Characters remaining: 950/1000"
  ↓
4. SUBMIT FORM
   • Click "Send Message" button
   • Button shows loading spinner
   
   System Actions (server-side):
   1. Validate inputs (server-side check)
   2. Save to tbl_contact_submissions:
      - name, email, phone, message
      - submitted_date = now()
      - status = 'new'
      - client_id = business owner
   3. Send email to business owner:
      Subject: "New Contact Form Submission - [Business Name]"
      Body: Name, email, phone, message
      Link to: /admin/settings/contact-submissions
   4. Send auto-reply to visitor (if configured):
      Subject: "We received your message"
      Body: Thank you message, expected response time
   
   Success Display:
   • Form disappears
   • Success message shown:
     "Thank you for contacting us!
      We've received your message and will respond within 24 hours.
      Check your email for confirmation."
   • "Back to Home" button
  ↓
END: Submission recorded, emails sent
```

### Alternative Path: Direct Communication
```
FROM Step 2: View Business Information
  ↓
Visitor clicks phone number
  → Opens phone dialer (mobile) or Skype (desktop)
  → Visitor calls directly
  
Visitor clicks email address
  → Opens email client
  → Pre-populated "To:" field
  → Visitor sends email directly
  
Visitor clicks map
  → Opens in Google Maps app
  → Get directions to business
```

### Success Criteria:
- Form submission saved to database
- Business owner receives email notification
- Visitor receives confirmation (if auto-reply enabled)
- Form resets after successful submission
- Visitor can submit another message if needed

### Error Handling:
- **Missing required field:** "Please complete all required fields"
- **Invalid email:** "Please enter a valid email address"
- **Message too long:** "Message must be under 1000 characters"
- **Submission failed:** "Error sending message. Please try again or email us directly at [email]"
- **Rate limit exceeded:** "Too many submissions. Please wait 5 minutes and try again."

---

## 16. Lead Capture via Landing Page Flow

**Actor:** Marketing Campaign Visitor  
**Goal:** Capture lead email for follow-up marketing  
**Duration:** 30-60 seconds  
**Frequency:** Once per visitor per campaign

### Flow Steps:

```
START: Visitor arrives from marketing campaign (email, ad, social)
  ↓
1. ARRIVE AT LANDING PAGE
   URL: https://Mybizz.app/landing/summer-special
   Source: Facebook Ad, Email Campaign, Social Media Post
   
   Page displayed with BlankLayout:
   • No header navigation (no distractions)
   • No footer
   • Single focused page
   • Template: Lead Capture
   
   System Action:
   • Track page view: tbl_landing_pages.views_count += 1
   • Log visitor: IP address, timestamp, referrer
  ↓
2. VIEW LANDING PAGE CONTENT
   Visible elements:
   • Compelling Headline: "Get Your Free Marketing Guide"
   • Subheadline: "Learn 10 proven strategies to grow your business"
   • Hero image or video
   • Benefits list (with checkmarks):
     ✓ Increase sales by 30%
     ✓ Double your email list
     ✓ Boost engagement
   • Email capture form (prominent)
   • Trust badges: "100% Privacy Guaranteed"
   • Social proof: "Join 5,000+ happy subscribers"
   
   Visitor reads content and decides to proceed
  ↓
3. ENTER EMAIL ADDRESS
   Single-field form:
   • Email Input: Placeholder "Enter your email"
   • Submit Button: "Download Free Guide" (action-oriented text)
   
   Client-side validation:
   • Email format check (contains @ and .)
   • Not empty
   • Real-time validation (red/green indicator)
  ↓
4. SUBMIT EMAIL
   • Click "Download Free Guide" button
   • Button shows loading spinner
   
   System Actions (server-side):
   1. Validate email format (server-side check)
   2. Check for duplicate in tbl_leads
      IF duplicate:
      • Update existing lead record
      • Update source = 'landing_page'
      • Update landing_page_id
      ELSE:
      • Create new lead in tbl_leads:
        - email
        - source = 'landing_page'
        - landing_page_id (link to this landing page)
        - captured_date = now()
        - status = 'new'
        - client_id = business owner
   3. Track conversion:
      • tbl_landing_pages.conversions_count += 1
   4. Trigger welcome email (if marketing_enabled):
      • Send email with download link
      • Enroll in welcome sequence
      • Send to Brevo/marketing platform
   5. Generate download link (if applicable)
  ↓
5. DISPLAY THANK YOU MESSAGE
   Form disappears, replaced with:
   • Success message:
     "Success! Check your email for the download link."
   • Instruction:
     "We've sent your free guide to [email]
      If you don't see it, check your spam folder."
   • CTA (optional):
     "While you're here, check out our services" → Link to main website
   • Social sharing:
     "Share this with friends!" → Social buttons
  ↓
6. RECEIVE WELCOME EMAIL
   Email delivered to visitor:
   • Subject: "Your Free Marketing Guide is Ready!"
   • Body:
     - Thank you message
     - Download link/attachment
     - Brief intro to business
     - CTA: "Schedule a free consultation"
     - Unsubscribe link (compliance)
   
   Visitor clicks download link:
   → PDF/guide downloads
   → Visitor is now a lead in the system
  ↓
END: Lead captured, email sent, download delivered
```

### Alternative Path: Visitor Abandons
```
FROM Step 2: View Landing Page Content
  ↓
Visitor scrolls, reads, but doesn't submit
  ↓
Visitor closes tab or navigates away
  ↓
System: Page view recorded (but no conversion)
  → Conversion rate remains at current level
  → No lead captured
  
Business Owner can see:
  • Landing page had X views
  • Y conversions
  → Conversion rate = Y/X * 100%
  → Identify low-performing landing pages
  → Optimize content and test improvements
```

### Success Criteria:
- Lead email captured in tbl_leads
- Conversion tracked in tbl_landing_pages
- Welcome email delivered
- Download link/content accessible
- Lead enrolled in marketing sequence (if enabled)

### Error Handling:
- **Invalid email:** "Please enter a valid email address"
- **Empty field:** "Please enter your email to continue"
- **Submission failed:** "Oops! Something went wrong. Please try again."
- **Email delivery failed:** "We couldn't send your email. Please contact us at [support email]"
- **Rate limit:** "Too many submissions. Please try again in 5 minutes."

### Analytics Tracked:
- Page views (tbl_landing_pages.views_count)
- Conversions (tbl_landing_pages.conversions_count)
- Conversion rate (calculated: conversions/views * 100%)
- Traffic source (referrer URL)
- Time spent on page (optional, if implemented)
- Device type (mobile vs desktop)

### Business Owner Follow-Up:
After lead is captured, business owner:
1. Receives notification: "New lead captured from [landing page name]"
2. Views lead in /admin/customers/contacts (CRM)
3. Lead status: 'new'
4. Can:
   - Add to specific email campaign
   - Send manual follow-up
   - Create task for follow-up
   - Convert to customer (if purchases)


## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-30 | Dev Team | Initial user flows |
| 2.0 | 2026-01-01 | Dev Team | Added error flows |
| 3.0 | 2026-01-15 | AI + Founder | **MAJOR UPDATE:** Aligned with conceptual_design_v5. Updated onboarding for Open Verticals (template selection not permanent). Added Paystack gateway option. Updated couriers to Bob Go + Easyship. Added complete Membership flow. Added Restaurant booking flow. Updated navigation references. Fixed payment options (PayPal one-time only). Added Customer Support flow. Enhanced all flows with detailed UI mockups. |
| 4.0 | 2026-01-17 | AI + Founder | **CRM & MARKETING UPDATE:** Added 3 new flows for Phase 5. Flows 10-12 cover: Contact Management, Email Campaign Setup, and Marketing Dashboard Review. Aligned with conceptual_design_v6.md and CRM design documents. Updated flow index. |
| 5.0 | 2026-01-19 | AI + Founder | **WEBSITE & LANDING PAGES UPDATE:** Added 4 new flows for website and landing pages functionality. Flows 13-16 cover: Website Homepage Customization, Landing Page Creation, Visitor Contact Form Submission, and Lead Capture via Landing Page. Aligned with 01B_website_conceptual_design_v1.md and website architecture documents. Updated flow index. Added detailed error handling and analytics tracking for landing pages. |

---

**Document Status:** ✅ **FINALIZED for V1.x Development**  
**Reference:** 01_conceptual_design.md, 04_architecture_specification.md  
**Next Review:** After Phase 2 completion (validate website & landing page flows)

---

## VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| v6.0 | Jan 26, 2026 | **M3 Compliance Update**: Updated header to reference v9/v11 system documents. Added M3 UI Standards Note section. Updated Navigation Reference section for NavigationDrawerLayout + NavigationLink pattern. Updated all inline navigation references from "sidebar" to "NavigationLink". Added M3 mobile responsiveness notes. All flows now reflect M3 component standards. |
| v5.0 | Jan 22, 2026 | Updated for simplified navigation. Added website & landing page flows (Phase 2). |

---

**END OF USER FLOWS V6.0 (M3 COMPLIANT)**

*These flows are the blueprint for all user interactions. Implementation should follow these specifications unless design improvements are identified and documented during development.*
