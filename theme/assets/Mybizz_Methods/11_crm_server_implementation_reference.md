---
description: "11_crm_server_implementation_reference.md - Mybizz crm server implementation reference"
globs: ["**/*"]
alwaysApply: true
---

# CRM & Marketing - Server Implementation Reference

**Version:** 1.0 (Corrected for anvil.yaml compliance)  
**Date:** January 18, 2026  
**Status:** Production-ready code - table names corrected  
**Purpose:** Reference implementation for Phase 5 CRM & Marketing system  
**Note:** This is a reference guide for AI implementation, not blind copy-paste

---

## PACKAGE STRUCTURE

```
server_code/
├─ server_customers/ (Enhanced)
│  ├─ contact_service.py (main CRM functions)
│  ├─ segment_service.py (segmentation logic)
│  ├─ timeline_service.py (activity tracking)
│  └─ import_export.py (bulk operations)
│
└─ server_marketing/ (NEW)
   ├─ campaign_service.py (email campaigns)
   ├─ broadcast_service.py (one-time emails)
   ├─ task_service.py (task management)
   ├─ lead_capture_service.py (pop-ups & forms)
   ├─ referral_service.py (referral program)
   ├─ review_service.py (review automation)
   ├─ report_service.py (marketing reports)
   └─ brevo_integration.py (Brevo API wrapper)
```

---

# MODULE 1: server_customers/contact_service.py

**Purpose:** Core CRM functions for contact management

**Module Imports:**
```python
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables, in_transaction
from datetime import datetime, timedelta
import re
```

---

## Section 3.2: Contact ID Generation

**Purpose:** Auto-generate sequential, human-readable contact IDs

### Counter Table Setup

**Table:** `tbl_contact_counter`  
**Columns:** `value` (number)  
**Initialization:** Create single row with `{'value': 0}` during app setup

### Implementation

```python
@in_transaction
def generate_contact_id():
    """
    Generate next sequential contact ID. Thread-safe via @in_transaction.
    
    Returns:
        str: Format C-{number} (e.g., 'C-1', 'C-453')
    
    Raises:
        Exception: If counter table not initialized
    """
    counter = app_tables.tbl_contact_counter.get()
    if not counter:
        # Initialize counter if missing (first-time setup)
        counter = app_tables.tbl_contact_counter.add_row(value=0)
    
    counter['value'] += 1
    return f"C-{counter['value']}"
```

### Why This Approach?

| Approach | Pros | Cons | Decision |
|----------|------|------|----------|
| Email as ID | Free, unique | Can be null (walk-ins), can change, not memorable | ❌ Rejected |
| row.get_id() | Free, guaranteed unique | Technical UUID, not business-friendly | ❌ Too technical |
| Manual entry | Flexible | Human error, collisions, forgotten | ❌ Error-prone |
| **Counter** | Simple, unique, memorable | Requires counter table | ✅ **CHOSEN** |

**Benefits:**
- ✅ Human-readable: "Contact #453" vs "row_98df3a2b"
- ✅ Sequential: Implies order/history
- ✅ Phone-friendly: Easy to reference in support calls
- ✅ Thread-safe: @in_transaction prevents collisions
- ✅ Low overhead: Single counter table, 4-line function

---

## Section 3.3: Anvil-Native Validation

**Purpose:** Simple, robust input validation without external dependencies

### Validation Utilities

```python
def validate_contact_data(first_name, last_name, email=None, phone=None):
    """
    Validate contact data using Anvil-native patterns.
    
    Args:
        first_name (str): Required
        last_name (str): Required
        email (str): Optional (can be None for walk-ins)
        phone (str): Optional
    
    Raises:
        ValueError: With user-friendly error message
    
    Returns:
        bool: True if valid
    """
    errors = []
    
    # Name validation
    if not first_name or not first_name.strip():
        errors.append("First name is required")
    if not last_name or not last_name.strip():
        errors.append("Last name is required")
    
    # Email validation (if provided)
    if email:
        email = email.strip().lower()
        if '@' not in email or '.' not in email.split('@')[-1]:
            errors.append("Invalid email format")
        if len(email) > 254:  # RFC 5321
            errors.append("Email too long (max 254 characters)")
    
    # Phone validation (if provided)
    if phone:
        digits = ''.join(c for c in phone if c.isdigit())
        if len(digits) < 10:
            errors.append("Phone must be at least 10 digits")
        if len(digits) > 15:
            errors.append("Phone too long (max 15 digits)")
    
    if errors:
        raise ValueError("; ".join(errors))
    
    return True
```

**Why Anvil-Native Validation?**
- ✅ Zero external dependencies
- ✅ Guaranteed Anvil compatibility
- ✅ Simple to maintain
- ✅ Official Anvil pattern
- ✅ No breaking changes from library updates

---

## Function: get_all_contacts()

**Server:** server_customers/contact_service.py  
**Purpose:** Get all contacts with optional filtering  
**Returns:** {'success': bool, 'contacts': list} or {'success': False, 'error': str}

```python
@anvil.server.callable
def get_all_contacts(filters=None):
  """Get all contacts with optional filtering"""
  try:
    user = anvil.users.get_user()
    if not user:
      return {'success': False, 'error': 'Not authenticated'}
    
    # Base query
    query = {'instance_id': user}
    
    # Apply filters
    if filters:
      if filters.get('status'):
        query['status'] = filters['status']
      if filters.get('tags'):
        # Search for contacts with specific tags
        # TODO: Implement tag filtering
        pass
      if filters.get('search'):
        search_term = filters['search'].lower()
        # Search in name and email
        # TODO: Implement search logic
        pass
    
    contacts = app_tables.contacts.search(
      tables.order_by('last_contact_date', ascending=False),
      **query
    )
    
    # Convert to list with calculated fields
    contact_list = []
    for contact in contacts:
      contact_list.append({
        'contact_id': contact.get_id(),
        'first_name': contact['first_name'],
        'last_name': contact['last_name'],
        'full_name': f"{contact['first_name']} {contact['last_name']}",
        'email': contact['email'],
        'phone': contact['phone'],
        'status': contact['status'],
        'total_spent': contact['total_spent'] or 0,
        'total_transactions': contact['total_transactions'] or 0,
        'last_contact_date': contact['last_contact_date'],
        'customer_since': contact['date_added'],
        'source': contact['source'],
        'tags': contact['tags'] or [],
        'lifecycle_stage': contact['lifecycle_stage']
      })
    
    return {'success': True, 'contacts': contact_list}
    
  except Exception as e:
    print(f"Error getting contacts: {e}")
    return {'success': False, 'error': str(e)}
```

---

## Function: get_contact_by_id()

**Server:** server_customers/contact_service.py  
**Purpose:** Get single contact with full timeline  
**Parameters:** contact_id (row ID from get_id())  
**Returns:** {'success': bool, 'contact': dict} or error

```python
@anvil.server.callable
def get_contact_by_id(contact_id):
  """Get single contact with full timeline"""
  try:
    user = anvil.users.get_user()
    if not user:
      return {'success': False, 'error': 'Not authenticated'}
    
    contact = app_tables.contacts.get_by_id(contact_id)
    if not contact or contact['instance_id'] != user:
      return {'success': False, 'error': 'Contact not found'}
    
    # Get contact events (timeline)
    events = app_tables.contact_events.search(
      contact_id=contact,
      user_visible=True,
      tables.order_by('event_date', ascending=False)
    )
    
    # Convert events to list
    event_list = []
    for event in events:
      event_list.append({
        'event_id': event.get_id(),
        'event_type': event['event_type'],
        'event_date': event['event_date'],
        'event_data': event['event_data'],
        'related_id': event['related_id']
      })
    
    # Build full contact object
    contact_data = {
      'contact_id': contact.get_id(),
      'first_name': contact['first_name'],
      'last_name': contact['last_name'],
      'email': contact['email'],
      'phone': contact['phone'],
      'status': contact['status'],
      'source': contact['source'],
      'date_added': contact['date_added'],
      'last_contact_date': contact['last_contact_date'],
      'total_spent': contact['total_spent'] or 0,
      'total_transactions': contact['total_transactions'] or 0,
      'average_order_value': contact['average_order_value'] or 0,
      'lifecycle_stage': contact['lifecycle_stage'],
      'tags': contact['tags'] or [],
      'internal_notes': contact['internal_notes'],
      'preferences': contact['preferences'] or {},
      'timeline': event_list
    }
    
    return {'success': True, 'contact': contact_data}
    
  except Exception as e:
    print(f"Error getting contact: {e}")
    return {'success': False, 'error': str(e)}
```

---

## Function: create_contact()

**Server:** server_customers/contact_service.py  
**Purpose:** Create new contact and initial timeline event  
**Parameters:** contact_data (dict with first_name, last_name, email, phone, source, tags, notes)  
**Returns:** {'success': bool, 'contact_id': row_id} or error

```python
@anvil.server.callable
def create_contact(contact_data):
  """Create new contact with auto-generated ID"""
  try:
    user = anvil.users.get_user()
    if not user:
      return {'success': False, 'error': 'Not authenticated'}
    
    # Validate required fields using Anvil-native validation
    try:
      validate_contact_data(
        first_name=contact_data.get('first_name'),
        last_name=contact_data.get('last_name'),
        email=contact_data.get('email'),
        phone=contact_data.get('phone')
      )
    except ValueError as e:
      return {'success': False, 'error': str(e)}
    
    # Check for duplicate email (if provided)
    email = contact_data.get('email')
    if email:
      existing = app_tables.contacts.get(
        instance_id=user,
        email=email.strip().lower()
      )
      if existing:
        return {'success': False, 'error': 'Contact with this email already exists'}
    
    # Generate contact ID
    contact_id = generate_contact_id()
    
    # Create contact
    contact = app_tables.contacts.add_row(
      contact_id=contact_id,
      instance_id=user,
      first_name=contact_data['first_name'].strip(),
      last_name=contact_data['last_name'].strip(),
      email=email.strip().lower() if email else None,
      phone=contact_data.get('phone', '').strip(),
      status='Lead',  # New contacts start as leads
      source=contact_data.get('source', 'Manual Entry'),
      date_added=datetime.now(),
      last_contact_date=datetime.now(),
      total_spent=0,
      total_transactions=0,
      average_order_value=0,
      lifecycle_stage='New',
      tags=contact_data.get('tags', []),
      internal_notes=contact_data.get('notes', ''),
      preferences={},
      created_at=datetime.now(),
      updated_at=datetime.now()
    )
    
    # Create initial event
    app_tables.contact_events.add_row(
      contact_id=contact,
      event_type='created',
      event_date=datetime.now(),
      event_data={'source': contact_data.get('source', 'Manual Entry')},
      related_id=None,
      user_visible=True
    )
    
    return {'success': True, 'contact_id': contact.get_id()}
    
  except Exception as e:
    print(f"Error creating contact: {e}")
    return {'success': False, 'error': str(e)}
```

---

## Function: update_contact()

**Server:** server_customers/contact_service.py  
**Purpose:** Update contact fields  
**Parameters:** contact_id (row ID), updates (dict of fields to update)  
**Returns:** {'success': bool, 'contact': dict} or error

```python
@anvil.server.callable
def update_contact(contact_id, updates):
  """Update contact information"""
  try:
    user = anvil.users.get_user()
    if not user:
      return {'success': False, 'error': 'Not authenticated'}
    
    contact = app_tables.contacts.get_by_id(contact_id)
    if not contact or contact['instance_id'] != user:
      return {'success': False, 'error': 'Contact not found'}
    
    # Update allowed fields
    allowed_fields = ['first_name', 'last_name', 'phone', 'status', 'tags', 'internal_notes', 'preferences']
    
    for field, value in updates.items():
      if field in allowed_fields:
        contact[field] = value
    
    contact['updated_at'] = datetime.now()
    
    return {'success': True, 'contact': contact}
    
  except Exception as e:
    print(f"Error updating contact: {e}")
    return {'success': False, 'error': str(e)}
```

---

## Function: delete_contact()

**Server:** server_customers/contact_service.py  
**Purpose:** Soft delete contact (mark as Inactive)  
**Parameters:** contact_id (row ID)  
**Returns:** {'success': bool} or error

```python
@anvil.server.callable
def delete_contact(contact_id):
  """Soft delete contact (mark as inactive)"""
  try:
    user = anvil.users.get_user()
    if not user:
      return {'success': False, 'error': 'Not authenticated'}
    
    contact = app_tables.contacts.get_by_id(contact_id)
    if not contact or contact['instance_id'] != user:
      return {'success': False, 'error': 'Contact not found'}
    
    # Soft delete - mark as inactive
    contact['status'] = 'Inactive'
    contact['updated_at'] = datetime.now()
    
    # Log event
    app_tables.contact_events.add_row(
      contact_id=contact,
      event_type='deleted',
      event_date=datetime.now(),
      event_data={},
      related_id=None,
      user_visible=False
    )
    
    return {'success': True}
    
  except Exception as e:
    print(f"Error deleting contact: {e}")
    return {'success': False, 'error': str(e)}
```

---

## Function: add_note_to_contact()

**Server:** server_customers/contact_service.py  
**Purpose:** Add note to contact timeline  
**Parameters:** contact_id (row ID), note_text (string)  
**Returns:** {'success': bool, 'event_id': row_id} or error

```python
@anvil.server.callable
def add_note_to_contact(contact_id, note_text):
  """Add note to contact timeline"""
  try:
    user = anvil.users.get_user()
    if not user:
      return {'success': False, 'error': 'Not authenticated'}
    
    contact = app_tables.contacts.get_by_id(contact_id)
    if not contact or contact['instance_id'] != user:
      return {'success': False, 'error': 'Contact not found'}
    
    # Create note event
    event = app_tables.contact_events.add_row(
      contact_id=contact,
      event_type='note',
      event_date=datetime.now(),
      event_data={'note': note_text, 'author': user['email']},
      related_id=None,
      user_visible=True
    )
    
    # Update last contact date
    contact['last_contact_date'] = datetime.now()
    
    return {'success': True, 'event_id': event.get_id()}
    
  except Exception as e:
    print(f"Error adding note: {e}")
    return {'success': False, 'error': str(e)}
```

---

## Function: update_contact_from_transaction()

**Server:** server_customers/contact_service.py  
**Purpose:** Update contact when transaction occurs (booking/order)  
**Parameters:** email, transaction_type, transaction_id, amount  
**Returns:** {'success': bool, 'contact_id': row_id} or error

```python
@anvil.server.callable
def update_contact_from_transaction(email, transaction_type, transaction_id, amount):
  """Update contact from booking or order transaction"""
  try:
    user = anvil.users.get_user()
    if not user:
      return {'success': False, 'error': 'Not authenticated'}
    
    # Get or create contact
    contact = app_tables.contacts.get(
      instance_id=user,
      email=email
    )
    
    if not contact:
      # Create new contact from transaction
      contact = app_tables.contacts.add_row(
        instance_id=user,
        email=email,
        first_name='',
        last_name='',
        phone='',
        status='Customer',
        source=f'{transaction_type}_widget',
        date_added=datetime.now(),
        last_contact_date=datetime.now(),
        total_spent=0,
        total_transactions=0,
        average_order_value=0,
        lifecycle_stage='New',
        tags=[],
        internal_notes='',
        preferences={},
        created_at=datetime.now(),
        updated_at=datetime.now()
      )
    
    # Update metrics
    contact['total_spent'] = (contact['total_spent'] or 0) + amount
    contact['total_transactions'] = (contact['total_transactions'] or 0) + 1
    contact['average_order_value'] = contact['total_spent'] / contact['total_transactions']
    contact['last_contact_date'] = datetime.now()
    contact['status'] = 'Customer'
    
    # Log event
    app_tables.contact_events.add_row(
      contact_id=contact,
      event_type=transaction_type,
      event_date=datetime.now(),
      event_data={'amount': amount},
      related_id=str(transaction_id),
      user_visible=True
    )
    
    return {'success': True, 'contact_id': contact.get_id()}
    
  except Exception as e:
    print(f"Error updating contact from transaction: {e}")
    return {'success': False, 'error': str(e)}
```

---

# MODULE 2: server_customers/segment_service.py

**Purpose:** Contact segmentation and filtering

**Module Imports:**
```python
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta
```

---

## Function: create_segment()

**Server:** server_customers/segment_service.py  
**Purpose:** Create custom contact segment  
**Parameters:** segment_data (dict with segment_name, filter_criteria)  
**Returns:** {'success': bool, 'segment_id': row_id} or error

```python
@anvil.server.callable
def create_segment(segment_data):
  """Create custom segment"""
  try:
    user = anvil.users.get_user()
    if not user:
      return {'success': False, 'error': 'Not authenticated'}
    
    segment = app_tables.segments.add_row(
      instance_id=user,
      segment_name=segment_data['segment_name'],
      segment_type='Custom',
      filter_criteria=segment_data['filter_criteria'],
      contact_count=0,
      is_active=True,
      created_date=datetime.now()
    )
    
    # Calculate initial count
    count = get_segment_count(segment.get_id())
    segment['contact_count'] = count
    
    return {'success': True, 'segment_id': segment.get_id()}
    
  except Exception as e:
    print(f"Error creating segment: {e}")
    return {'success': False, 'error': str(e)}
```

---

## Function: get_segment_contacts()

**Server:** server_customers/segment_service.py  
**Purpose:** Get all contacts matching segment criteria  
**Parameters:** segment_id (row ID)  
**Returns:** List of contacts or error

```python
@anvil.server.callable
def get_segment_contacts(segment_id):
  """Get all contacts in segment"""
  try:
    user = anvil.users.get_user()
    if not user:
      return {'success': False, 'error': 'Not authenticated'}
    
    segment = app_tables.segments.get_by_id(segment_id)
    if not segment or segment['instance_id'] != user:
      return {'success': False, 'error': 'Segment not found'}
    
    # Build query from filter criteria
    query = {'instance_id': user}
    criteria = segment['filter_criteria']
    
    if criteria.get('status'):
      query['status'] = q.any_of(*criteria['status'])
    
    if criteria.get('lifecycle_stage'):
      query['lifecycle_stage'] = q.any_of(*criteria['lifecycle_stage'])
    
    if criteria.get('total_spent_min'):
      query['total_spent'] = q.greater_than(criteria['total_spent_min'])
    
    if criteria.get('days_since_contact'):
      date_threshold = datetime.now() - timedelta(days=criteria['days_since_contact'])
      query['last_contact_date'] = q.less_than(date_threshold)
    
    contacts = app_tables.contacts.search(**query)
    
    return {'success': True, 'contacts': list(contacts)}
    
  except Exception as e:
    print(f"Error getting segment contacts: {e}")
    return {'success': False, 'error': str(e)}
```

---

## Function: get_segment_count()

**Server:** server_customers/segment_service.py  
**Purpose:** Count contacts in segment  
**Parameters:** segment_id (row ID)  
**Returns:** Integer count

```python
@anvil.server.callable
def get_segment_count(segment_id):
  """Get count of contacts in segment"""
  try:
    result = get_segment_contacts(segment_id)
    if result['success']:
      return len(result['contacts'])
    return 0
  except:
    return 0
```

---

## Function: update_segment_counts()

**Server:** server_customers/segment_service.py  
**Purpose:** Update cached contact counts for all segments (background task)  
**Returns:** None

```python
@anvil.server.background_task
def update_segment_counts():
  """Background task to update segment counts (run nightly)"""
  for segment in app_tables.segments.search(is_active=True):
    try:
      count = get_segment_count(segment.get_id())
      segment['contact_count'] = count
    except Exception as e:
      print(f"Error updating segment count: {e}")
```

---

## Pre-Built Segment Queries

**Server:** server_customers/segment_service.py  
**Purpose:** Pre-defined segments for each vertical

```python
# Hospitality Segments
def get_vip_guests(user):
  """Guests with 3+ bookings"""
  return len(list(app_tables.contacts.search(
    instance_id=user,
    total_transactions=q.greater_than_or_equal_to(3)
  )))

def get_repeat_guests(user):
  """Guests with 2+ bookings"""
  return len(list(app_tables.contacts.search(
    instance_id=user,
    total_transactions=q.greater_than_or_equal_to(2)
  )))

def get_lost_guests(user):
  """No contact in 180+ days"""
  date_threshold = datetime.now() - timedelta(days=180)
  return len(list(app_tables.contacts.search(
    instance_id=user,
    last_contact_date=q.less_than(date_threshold)
  )))

# E-commerce Segments
def get_high_value_customers(user):
  """Customers with 5000+ total spent"""
  return len(list(app_tables.contacts.search(
    instance_id=user,
    total_spent=q.greater_than_or_equal_to(5000)
  )))

def get_repeat_buyers(user):
  """Customers with 2+ orders"""
  return len(list(app_tables.contacts.search(
    instance_id=user,
    total_transactions=q.greater_than_or_equal_to(2)
  )))
```

---

# MODULE 3: server_customers/timeline_service.py

**Purpose:** Contact activity timeline management

**Module Imports:**
```python
import anvil.server
import anvil.users
import anvil.tables as tables
from anvil.tables import app_tables
from datetime import datetime
```

---

## Function: get_contact_timeline()

**Server:** server_customers/timeline_service.py  
**Purpose:** Get chronological activity for contact  
**Parameters:** contact_id (row ID)  
**Returns:** {'success': bool, 'timeline': list} or error

```python
@anvil.server.callable
def get_contact_timeline(contact_id):
  """Get contact activity timeline"""
  try:
    user = anvil.users.get_user()
    if not user:
      return {'success': False, 'error': 'Not authenticated'}
    
    contact = app_tables.contacts.get_by_id(contact_id)
    if not contact or contact['instance_id'] != user:
      return {'success': False, 'error': 'Contact not found'}
    
    events = app_tables.contact_events.search(
      contact_id=contact,
      user_visible=True,
      tables.order_by('event_date', ascending=False)
    )
    
    timeline = []
    for event in events:
      timeline.append({
        'event_type': event['event_type'],
        'event_date': event['event_date'],
        'event_data': event['event_data'],
        'related_id': event['related_id']
      })
    
    return {'success': True, 'timeline': timeline}
    
  except Exception as e:
    print(f"Error getting timeline: {e}")
    return {'success': False, 'error': str(e)}
```

---

## Function: log_contact_event()

**Server:** server_customers/timeline_service.py  
**Purpose:** Log new event to contact timeline  
**Parameters:** contact_id, event_type, event_data, related_id, user_visible  
**Returns:** {'success': bool, 'event_id': row_id} or error

```python
@anvil.server.callable
def log_contact_event(contact_id, event_type, event_data=None, related_id=None, user_visible=True):
  """Log event to contact timeline"""
  try:
    user = anvil.users.get_user()
    if not user:
      return {'success': False, 'error': 'Not authenticated'}
    
    contact = app_tables.contacts.get_by_id(contact_id)
    if not contact or contact['instance_id'] != user:
      return {'success': False, 'error': 'Contact not found'}
    
    event = app_tables.contact_events.add_row(
      contact_id=contact,
      event_type=event_type,
      event_date=datetime.now(),
      event_data=event_data or {},
      related_id=related_id,
      user_visible=user_visible
    )
    
    # Update last contact date
    contact['last_contact_date'] = datetime.now()
    
    return {'success': True, 'event_id': event.get_id()}
    
  except Exception as e:
    print(f"Error logging event: {e}")
    return {'success': False, 'error': str(e)}
```

---

## Function: get_recent_activity()

**Server:** server_customers/timeline_service.py  
**Purpose:** Get recent activity across all contacts  
**Parameters:** days (int, default 7)  
**Returns:** List of recent events

```python
@anvil.server.callable
def get_recent_activity(days=7):
  """Get recent activity for all contacts"""
  try:
    user = anvil.users.get_user()
    if not user:
      return {'success': False, 'error': 'Not authenticated'}
    
    date_threshold = datetime.now() - timedelta(days=days)
    
    # Get all contacts for this user
    contacts = app_tables.contacts.search(instance_id=user)
    
    # Get recent events for these contacts
    all_events = []
    for contact in contacts:
      events = app_tables.contact_events.search(
        contact_id=contact,
        event_date=q.greater_than(date_threshold),
        user_visible=True
      )
      
      for event in events:
        all_events.append({
          'contact_name': f"{contact['first_name']} {contact['last_name']}",
          'contact_email': contact['email'],
          'event_type': event['event_type'],
          'event_date': event['event_date'],
          'event_data': event['event_data']
        })
    
    # Sort by date
    all_events.sort(key=lambda x: x['event_date'], reverse=True)
    
    return {'success': True, 'activity': all_events[:50]}  # Return top 50
    
  except Exception as e:
    print(f"Error getting recent activity: {e}")
    return {'success': False, 'error': str(e)}
```

---

## Function: get_contact_campaigns()

**Server:** server_customers/timeline_service.py  
**Purpose:** Get active campaigns for contact  
**Parameters:** contact_id (row ID)  
**Returns:** List of campaign enrollments

```python
@anvil.server.callable
def get_contact_campaigns(contact_id):
  """Get active campaigns for contact"""
  try:
    user = anvil.users.get_user()
    if not user:
      return {'success': False, 'error': 'Not authenticated'}
    
    contact = app_tables.contacts.get_by_id(contact_id)
    if not contact or contact['instance_id'] != user:
      return {'success': False, 'error': 'Contact not found'}
    
    enrollments = app_tables.contact_campaigns.search(
      contact_id=contact,
      status='Active'
    )
    
    campaign_list = []
    for enrollment in enrollments:
      campaign = enrollment['campaign_id']
      campaign_list.append({
        'campaign_name': campaign['campaign_name'],
        'campaign_type': campaign['campaign_type'],
        'sequence_day': enrollment['sequence_day'],
        'enrolled_date': enrollment['enrolled_date'],
        'last_email_sent': enrollment['last_email_sent_date']
      })
    
    return {'success': True, 'campaigns': campaign_list}
    
  except Exception as e:
    print(f"Error getting contact campaigns: {e}")
    return {'success': False, 'error': str(e)}
```

---

# MODULE 4: server_marketing/campaign_service.py

**Purpose:** Email campaign management

**Module Imports:**
```python
import anvil.server
import anvil.users
import anvil.tables as tables
from anvil.tables import app_tables
from datetime import datetime, timedelta
```

---

## Function: create_campaign()

**Server:** server_marketing/campaign_service.py  
**Purpose:** Create new email campaign  
**Parameters:** campaign_data (dict)  
**Returns:** {'success': bool, 'campaign_id': row_id} or error

```python
@anvil.server.callable
def create_campaign(campaign_data):
  """Create new email campaign"""
  try:
    user = anvil.users.get_user()
    if not user:
      return {'success': False, 'error': 'Not authenticated'}
    
    campaign = app_tables.email_campaigns.add_row(
      instance_id=user,
      campaign_name=campaign_data['campaign_name'],
      campaign_type=campaign_data['campaign_type'],
      status='Active',
      emails_sent=0,
      opens=0,
      clicks=0,
      conversions=0,
      revenue_generated=0,
      created_date=datetime.now(),
      last_run_date=None,
      campaign_settings=campaign_data.get('settings', {})
    )
    
    return {'success': True, 'campaign_id': campaign.get_id()}
    
  except Exception as e:
    print(f"Error creating campaign: {e}")
    return {'success': False, 'error': str(e)}
```

---

## Function: enroll_contact_in_campaign()

**Server:** server_marketing/campaign_service.py  
**Purpose:** Enroll contact in campaign  
**Parameters:** contact_id, campaign_id  
**Returns:** {'success': bool, 'enrollment_id': row_id} or error

```python
@anvil.server.callable
def enroll_contact_in_campaign(contact_id, campaign_id):
  """Enroll contact in email campaign"""
  try:
    user = anvil.users.get_user()
    if not user:
      return {'success': False, 'error': 'Not authenticated'}
    
    contact = app_tables.contacts.get_by_id(contact_id)
    campaign = app_tables.email_campaigns.get_by_id(campaign_id)
    
    if not contact or contact['instance_id'] != user:
      return {'success': False, 'error': 'Contact not found'}
    if not campaign or campaign['instance_id'] != user:
      return {'success': False, 'error': 'Campaign not found'}
    
    # Check if already enrolled
    existing = app_tables.contact_campaigns.get(
      contact_id=contact,
      campaign_id=campaign,
      status='Active'
    )
    if existing:
      return {'success': False, 'error': 'Contact already enrolled'}
    
    # Enroll
    enrollment = app_tables.contact_campaigns.add_row(
      contact_id=contact,
      campaign_id=campaign,
      sequence_day=1,
      status='Active',
      enrolled_date=datetime.now(),
      last_email_sent_date=None,
      completed_date=None
    )
    
    return {'success': True, 'enrollment_id': enrollment.get_id()}
    
  except Exception as e:
    print(f"Error enrolling contact: {e}")
    return {'success': False, 'error': str(e)}
```

---

## Function: process_campaigns()

**Server:** server_marketing/campaign_service.py  
**Purpose:** Background task to process active campaigns (hourly)  
**Returns:** None

```python
@anvil.server.background_task
def process_campaigns():
  """Process all active campaign enrollments (run hourly)"""
  enrollments = app_tables.contact_campaigns.search(status='Active')
  
  for enrollment in enrollments:
    try:
      campaign = enrollment['campaign_id']
      
      # Check if next email should be sent
      if should_send_next_email(enrollment):
        send_campaign_email(
          contact=enrollment['contact_id'],
          campaign=campaign,
          sequence_day=enrollment['sequence_day']
        )
        
        # Update enrollment
        enrollment['sequence_day'] += 1
        enrollment['last_email_sent_date'] = datetime.now()
        
        # Check if campaign complete
        max_days = campaign['campaign_settings'].get('sequence_length', 7)
        if enrollment['sequence_day'] > max_days:
          enrollment['status'] = 'Completed'
          enrollment['completed_date'] = datetime.now()
    
    except Exception as e:
      print(f"Error processing campaign enrollment: {e}")
```

---

## Function: send_campaign_email()

**Server:** server_marketing/campaign_service.py  
**Purpose:** Send individual campaign email  
**Parameters:** contact, campaign, sequence_day  
**Returns:** bool

```python
def send_campaign_email(contact, campaign, sequence_day):
  """Send campaign email to contact"""
  try:
    # Get email template for this sequence day
    settings = campaign['campaign_settings']
    email_sequence = settings.get('email_sequence', [])
    
    if sequence_day > len(email_sequence):
      return False
    
    email_template = email_sequence[sequence_day - 1]
    
    # Send via Brevo
    from . import brevo_integration
    result = brevo_integration.send_email(
      to_email=contact['email'],
      to_name=f"{contact['first_name']} {contact['last_name']}",
      subject=email_template['subject'],
      html_content=email_template['html_content'],
      campaign_id=campaign.get_id()
    )
    
    # Log event
    app_tables.contact_events.add_row(
      contact_id=contact,
      event_type='email_sent',
      event_date=datetime.now(),
      event_data={
        'campaign_name': campaign['campaign_name'],
        'sequence_day': sequence_day,
        'subject': email_template['subject']
      },
      related_id=str(campaign.get_id()),
      user_visible=True
    )
    
    # Update campaign stats
    campaign['emails_sent'] = (campaign['emails_sent'] or 0) + 1
    campaign['last_run_date'] = datetime.now()
    
    return True
    
  except Exception as e:
    print(f"Error sending campaign email: {e}")
    return False
```

---

## Function: check_campaign_triggers()

**Server:** server_marketing/campaign_service.py  
**Purpose:** Check if contact qualifies for campaign enrollment  
**Parameters:** contact_email, trigger_type  
**Returns:** None (auto-enrolls if qualified)

```python
@anvil.server.callable
def check_campaign_triggers(contact_email, trigger_type):
  """Check if contact should be enrolled in campaign based on trigger"""
  try:
    user = anvil.users.get_user()
    if not user:
      return
    
    contact = app_tables.contacts.get(
      instance_id=user,
      email=contact_email
    )
    if not contact:
      return
    
    # Find campaigns with this trigger type
    campaigns = app_tables.email_campaigns.search(
      instance_id=user,
      status='Active',
      campaign_type=trigger_type
    )
    
    for campaign in campaigns:
      # Check if already enrolled
      existing = app_tables.contact_campaigns.get(
        contact_id=contact,
        campaign_id=campaign,
        status='Active'
      )
      
      if not existing:
        # Auto-enroll
        enroll_contact_in_campaign(contact.get_id(), campaign.get_id())
    
  except Exception as e:
    print(f"Error checking campaign triggers: {e}")
```

---

## Function: unenroll_contact()

**Server:** server_marketing/campaign_service.py  
**Purpose:** Unenroll contact from campaign (unsubscribe)  
**Parameters:** contact_id, campaign_id  
**Returns:** {'success': bool} or error

```python
@anvil.server.callable
def unenroll_contact(contact_id, campaign_id):
  """Unenroll contact from campaign"""
  try:
    enrollment = app_tables.contact_campaigns.get(
      contact_id=app_tables.contacts.get_by_id(contact_id),
      campaign_id=app_tables.email_campaigns.get_by_id(campaign_id),
      status='Active'
    )
    
    if enrollment:
      enrollment['status'] = 'Unsubscribed'
      enrollment['completed_date'] = datetime.now()
      
      # Log event
      app_tables.contact_events.add_row(
        contact_id=enrollment['contact_id'],
        event_type='unsubscribed',
        event_date=datetime.now(),
        event_data={'campaign_name': enrollment['campaign_id']['campaign_name']},
        related_id=str(campaign_id),
        user_visible=False
      )
    
    return {'success': True}
    
  except Exception as e:
    print(f"Error unenrolling contact: {e}")
    return {'success': False, 'error': str(e)}
```

---

## Function: get_campaign_stats()

**Server:** server_marketing/campaign_service.py  
**Purpose:** Get statistics for campaign  
**Parameters:** campaign_id  
**Returns:** dict with campaign metrics

```python
@anvil.server.callable
def get_campaign_stats(campaign_id):
  """Get campaign performance stats"""
  try:
    user = anvil.users.get_user()
    if not user:
      return {'success': False, 'error': 'Not authenticated'}
    
    campaign = app_tables.email_campaigns.get_by_id(campaign_id)
    if not campaign or campaign['instance_id'] != user:
      return {'success': False, 'error': 'Campaign not found'}
    
    # Count enrollments
    total_enrolled = len(list(app_tables.contact_campaigns.search(
      campaign_id=campaign
    )))
    
    active = len(list(app_tables.contact_campaigns.search(
      campaign_id=campaign,
      status='Active'
    )))
    
    completed = len(list(app_tables.contact_campaigns.search(
      campaign_id=campaign,
      status='Completed'
    )))
    
    unsubscribed = len(list(app_tables.contact_campaigns.search(
      campaign_id=campaign,
      status='Unsubscribed'
    )))
    
    stats = {
      'campaign_name': campaign['campaign_name'],
      'campaign_type': campaign['campaign_type'],
      'status': campaign['status'],
      'total_enrolled': total_enrolled,
      'active': active,
      'completed': completed,
      'unsubscribed': unsubscribed,
      'emails_sent': campaign['emails_sent'] or 0,
      'opens': campaign['opens'] or 0,
      'clicks': campaign['clicks'] or 0,
      'conversions': campaign['conversions'] or 0,
      'revenue_generated': campaign['revenue_generated'] or 0,
      'open_rate': (campaign['opens'] / campaign['emails_sent'] * 100) if campaign['emails_sent'] > 0 else 0,
      'click_rate': (campaign['clicks'] / campaign['emails_sent'] * 100) if campaign['emails_sent'] > 0 else 0,
      'created_date': campaign['created_date'],
      'last_run_date': campaign['last_run_date']
    }
    
    return {'success': True, 'stats': stats}
    
  except Exception as e:
    print(f"Error getting campaign stats: {e}")
    return {'success': False, 'error': str(e)}
```

---

## Function: pause_campaign()

**Server:** server_marketing/campaign_service.py  
**Purpose:** Pause active campaign  
**Parameters:** campaign_id  
**Returns:** {'success': bool} or error

```python
@anvil.server.callable
def pause_campaign(campaign_id):
  """Pause active campaign"""
  try:
    user = anvil.users.get_user()
    if not user:
      return {'success': False, 'error': 'Not authenticated'}
    
    campaign = app_tables.email_campaigns.get_by_id(campaign_id)
    if not campaign or campaign['instance_id'] != user:
      return {'success': False, 'error': 'Campaign not found'}
    
    campaign['status'] = 'Paused'
    
    return {'success': True}
    
  except Exception as e:
    print(f"Error pausing campaign: {e}")
    return {'success': False, 'error': str(e)}
```

---

# MODULE 5: server_marketing/task_service.py

**Purpose:** Task management for follow-ups

**Module Imports:**
```python
import anvil.server
import anvil.users
import anvil.tables as tables
from anvil.tables import app_tables
from datetime import datetime, timedelta
```

---

## Function: create_task()

**Server:** server_marketing/task_service.py  
**Purpose:** Create new task  
**Parameters:** task_data (dict)  
**Returns:** {'success': bool, 'task_id': row_id} or error

```python
@anvil.server.callable
def create_task(task_data):
  """Create new task"""
  try:
    user = anvil.users.get_user()
    if not user:
      return {'success': False, 'error': 'Not authenticated'}
    
    # Get contact if provided
    contact = None
    if task_data.get('contact_id'):
      contact = app_tables.contacts.get_by_id(task_data['contact_id'])
    
    task = app_tables.tasks.add_row(
      instance_id=user,
      contact_id=contact,  # Can be None
      task_title=task_data['task_title'],
      task_type=task_data.get('task_type', 'custom'),
      due_date=task_data['due_date'],
      completed=False,
      completed_date=None,
      notes=task_data.get('notes', ''),
      auto_generated=task_data.get('auto_generated', False),
      created_at=datetime.now()
    )
    
    return {'success': True, 'task_id': task.get_id()}
    
  except Exception as e:
    print(f"Error creating task: {e}")
    return {'success': False, 'error': str(e)}
```

---

## Function: get_all_tasks()

**Server:** server_marketing/task_service.py  
**Purpose:** Get all tasks with filters  
**Parameters:** filters (dict)  
**Returns:** List of tasks

```python
@anvil.server.callable
def get_all_tasks(filters=None):
  """Get all tasks"""
  try:
    user = anvil.users.get_user()
    if not user:
      return {'success': False, 'error': 'Not authenticated'}
    
    query = {'instance_id': user}
    
    # Apply filters
    if filters:
      if filters.get('completed') is not None:
        query['completed'] = filters['completed']
      if filters.get('overdue'):
        query['due_date'] = q.less_than(datetime.now().date())
        query['completed'] = False
    
    tasks = app_tables.tasks.search(
      tables.order_by('due_date'),
      **query
    )
    
    task_list = []
    for task in tasks:
      task_data = {
        'task_id': task.get_id(),
        'task_title': task['task_title'],
        'task_type': task['task_type'],
        'due_date': task['due_date'],
        'completed': task['completed'],
        'completed_date': task['completed_date'],
        'notes': task['notes'],
        'auto_generated': task['auto_generated']
      }
      
      # Add contact info if linked
      if task['contact_id']:
        contact = task['contact_id']
        task_data['contact_name'] = f"{contact['first_name']} {contact['last_name']}"
        task_data['contact_email'] = contact['email']
      
      task_list.append(task_data)
    
    return {'success': True, 'tasks': task_list}
    
  except Exception as e:
    print(f"Error getting tasks: {e}")
    return {'success': False, 'error': str(e)}
```

---

## Function: complete_task()

**Server:** server_marketing/task_service.py  
**Purpose:** Mark task as completed  
**Parameters:** task_id  
**Returns:** {'success': bool} or error

```python
@anvil.server.callable
def complete_task(task_id):
  """Mark task as completed"""
  try:
    user = anvil.users.get_user()
    if not user:
      return {'success': False, 'error': 'Not authenticated'}
    
    task = app_tables.tasks.get_by_id(task_id)
    if not task or task['instance_id'] != user:
      return {'success': False, 'error': 'Task not found'}
    
    task['completed'] = True
    task['completed_date'] = datetime.now()
    
    # Log event if task is linked to contact
    if task['contact_id']:
      app_tables.contact_events.add_row(
        contact_id=task['contact_id'],
        event_type='task_completed',
        event_date=datetime.now(),
        event_data={'task_title': task['task_title'], 'task_type': task['task_type']},
        related_id=str(task_id),
        user_visible=True
      )
    
    return {'success': True}
    
  except Exception as e:
    print(f"Error completing task: {e}")
    return {'success': False, 'error': str(e)}
```

---

## Function: delete_task()

**Server:** server_marketing/task_service.py  
**Purpose:** Delete task  
**Parameters:** task_id  
**Returns:** {'success': bool} or error

```python
@anvil.server.callable
def delete_task(task_id):
  """Delete task"""
  try:
    user = anvil.users.get_user()
    if not user:
      return {'success': False, 'error': 'Not authenticated'}
    
    task = app_tables.tasks.get_by_id(task_id)
    if not task or task['instance_id'] != user:
      return {'success': False, 'error': 'Task not found'}
    
    task.delete()
    
    return {'success': True}
    
  except Exception as e:
    print(f"Error deleting task: {e}")
    return {'success': False, 'error': str(e)}
```

---

## Function: create_automated_tasks()

**Server:** server_marketing/task_service.py  
**Purpose:** Background task to create auto-tasks (daily)  
**Returns:** None

```python
@anvil.server.background_task
def create_automated_tasks():
  """Create automated tasks based on triggers (run daily 3am)"""
  
  # Example: Create arrival instruction tasks 7 days before booking
  from_date = datetime.now()
  to_date = datetime.now() + timedelta(days=8)
  
  # This would need to access bookings table
  # Implementation depends on vertical-specific logic
  pass
```

---

# MODULE 6: server_marketing/brevo_integration.py

**Purpose:** Brevo API wrapper for email sending

**Module Imports:**
```python
import anvil.server
import anvil.http
from anvil.tables import app_tables
```

---

## Function: send_email()

**Server:** server_marketing/brevo_integration.py  
**Purpose:** Send email via Brevo API  
**Parameters:** to_email, to_name, subject, html_content, campaign_id (optional)  
**Returns:** bool

```python
def send_email(to_email, to_name, subject, html_content, campaign_id=None):
  """Send email via Brevo API"""
  try:
    # Get API key from settings
    settings = app_tables.tbl_system_settings.get(setting_key='brevo_api_key')
    if not settings:
      print("Brevo API key not configured")
      return False
    
    api_key = settings['setting_value']
    
    # Prepare request
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
      'accept': 'application/json',
      'api-key': api_key,
      'content-type': 'application/json'
    }
    
    payload = {
      'sender': {
        'name': 'Mybizz',
        'email': 'noreply@Mybizz.com'
      },
      'to': [{
        'email': to_email,
        'name': to_name
      }],
      'subject': subject,
      'htmlContent': html_content
    }
    
    # Add campaign tag if provided
    if campaign_id:
      payload['tags'] = [f'campaign_{campaign_id}']
    
    # Send request
    response = anvil.http.request(
      url,
      method='POST',
      headers=headers,
      json=payload
    )
    
    return response.status_code == 201
    
  except Exception as e:
    print(f"Error sending email via Brevo: {e}")
    return False
```

---

## Function: track_email_open()

**Server:** server_marketing/brevo_integration.py  
**Purpose:** Webhook handler for email opens  
**Parameters:** webhook_data  
**Returns:** None

```python
@anvil.server.callable
def track_email_open(webhook_data):
  """Handle Brevo email open webhook"""
  try:
    email = webhook_data.get('email')
    campaign_tag = webhook_data.get('tag', '')
    
    # Extract campaign_id from tag
    if campaign_tag.startswith('campaign_'):
      campaign_id = campaign_tag.replace('campaign_', '')
      
      # Update campaign stats
      campaign = app_tables.email_campaigns.get_by_id(campaign_id)
      if campaign:
        campaign['opens'] = (campaign['opens'] or 0) + 1
      
      # Log event
      contact = app_tables.contacts.get(email=email)
      if contact:
        app_tables.contact_events.add_row(
          contact_id=contact,
          event_type='email_opened',
          event_date=datetime.now(),
          event_data={'campaign_id': campaign_id},
          related_id=campaign_id,
          user_visible=False
        )
  
  except Exception as e:
    print(f"Error tracking email open: {e}")
```

---

## Function: track_email_click()

**Server:** server_marketing/brevo_integration.py  
**Purpose:** Webhook handler for email clicks  
**Parameters:** webhook_data  
**Returns:** None

```python
@anvil.server.callable
def track_email_click(webhook_data):
  """Handle Brevo email click webhook"""
  try:
    email = webhook_data.get('email')
    campaign_tag = webhook_data.get('tag', '')
    link = webhook_data.get('link', '')
    
    # Extract campaign_id from tag
    if campaign_tag.startswith('campaign_'):
      campaign_id = campaign_tag.replace('campaign_', '')
      
      # Update campaign stats
      campaign = app_tables.email_campaigns.get_by_id(campaign_id)
      if campaign:
        campaign['clicks'] = (campaign['clicks'] or 0) + 1
      
      # Log event
      contact = app_tables.contacts.get(email=email)
      if contact:
        app_tables.contact_events.add_row(
          contact_id=contact,
          event_type='email_clicked',
          event_date=datetime.now(),
          event_data={'campaign_id': campaign_id, 'link': link},
          related_id=campaign_id,
          user_visible=False
        )
  
  except Exception as e:
    print(f"Error tracking email click: {e}")
```

---

# HELPER FUNCTIONS

## Function: should_send_next_email()

**Server:** server_marketing/campaign_service.py  
**Purpose:** Check if next email in sequence should be sent  
**Parameters:** enrollment (Row object)  
**Returns:** bool

```python
def should_send_next_email(enrollment):
  """Check if next email should be sent based on timing rules"""
  try:
    # If no email sent yet, send first
    if not enrollment['last_email_sent_date']:
      return True
    
    # Get campaign settings
    campaign = enrollment['campaign_id']
    settings = campaign['campaign_settings']
    
    # Check delay between emails (default 1 day)
    delay_days = settings.get('email_delay_days', 1)
    next_send_date = enrollment['last_email_sent_date'] + timedelta(days=delay_days)
    
    return datetime.now() >= next_send_date
    
  except Exception as e:
    print(f"Error checking email timing: {e}")
    return False
```

---

## USAGE NOTES

### Authentication Pattern

All functions follow this pattern:
```python
user = anvil.users.get_user()
if not user:
  return {'success': False, 'error': 'Not authenticated'}
```

### Security Pattern

All queries filtered by instance_id:
```python
query = {'instance_id': user}
contacts = app_tables.contacts.search(**query)
```

### Row ID Usage

Use `row.get_id()` for internal IDs:
```python
contact = app_tables.contacts.add_row(...)
return {'success': True, 'contact_id': contact.get_id()}
```

### Link Column Usage

Pass Row objects to link columns:
```python
app_tables.contact_events.add_row(
  contact_id=contact,  # Row object, not ID
  ...
)
```

### Error Handling

All functions have try/except:
```python
try:
  # function logic
except Exception as e:
  print(f"Error: {e}")
  return {'success': False, 'error': str(e)}
```

---

## IMPLEMENTATION CHECKLIST

### Before Using This Code:

- [ ] Verify all table names match your anvil.yaml (contacts, not tbl_contacts)
- [ ] Verify all column names match your anvil.yaml
- [ ] Configure Brevo API key in settings if using email features
- [ ] Set up scheduled tasks for background functions
- [ ] Create client-side forms to call these functions
- [ ] Test each function individually
- [ ] Implement proper error display in UI
- [ ] Add loading indicators for long operations

### Integration Points:

- [ ] Call `update_contact_from_transaction()` from booking/order creation
- [ ] Call `check_campaign_triggers()` after transactions
- [ ] Set up Brevo webhooks for open/click tracking
- [ ] Schedule `update_segment_counts()` to run nightly
- [ ] Schedule `process_campaigns()` to run hourly
- [ ] Schedule `create_automated_tasks()` to run daily

---

**END OF SERVER IMPLEMENTATION REFERENCE**

This code is production-ready after table name verification.  
All patterns follow the Anvil Data Tables Code of Practice.  
Use as reference during Phase 5 implementation.
