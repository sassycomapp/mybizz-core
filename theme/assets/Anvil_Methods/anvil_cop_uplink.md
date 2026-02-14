# Anvil Uplink Code of Practice
## Safe Integration Standard for Factory.AI + Anvil.works

**Version:** 1.0  
**Date:** January 31, 2026  
**Purpose:** Safe, controlled Uplink usage for Factory Droid  
**Scope:** Connection management, data integrity, error handling, guardrails

---

## PHILOSOPHY

**Uplink is Powerful - Use it Carefully**

Anvil Uplink grants full server privileges:
- ✅ Can read all code
- ✅ Can write all code
- ✅ Can access Data Tables
- ✅ Can call server functions
- ⚠️ **Can potentially wreck everything**

**Therefore:**
- Use Uplink from Day 1 (don't phase it in)
- Follow strict guardrails (non-negotiable)
- Backup before operations (always)
- Log all activities (complete audit trail)
- Verify results (never trust blindly)

**This is the standard. This doesn't change.**

---

## TABLE OF CONTENTS

1. [Uplink Overview](#1-uplink-overview)
2. [Connection Management](#2-connection-management)
3. [Security Requirements](#3-security-requirements)
4. [Data Integrity Guardrails](#4-data-integrity-guardrails)
5. [Operation Patterns](#5-operation-patterns)
6. [Error Handling](#6-error-handling)
7. [Logging and Monitoring](#7-logging-and-monitoring)
8. [Backup Integration](#8-backup-integration)
9. [Common Operations](#9-common-operations)
10. [Emergency Procedures](#10-emergency-procedures)

---

## 1. UPLINK OVERVIEW

### What is Anvil Uplink?

**Definition:** Anvil Uplink connects external Python code to your Anvil app via secure WebSocket connection.

**Purpose:** Enables Factory Droid (running locally via Factory Bridge) to interact with Anvil app (running on Anvil servers).

**Connection Flow:**
```
Factory Droid (Local VSCode + Factory Bridge)
         ↕ (WebSocket - wss://anvil.works/uplink)
    Anvil App (Cloud)
         ↕
    Anvil Data Tables (Cloud)
```

### Uplink Capabilities

**What Uplink Can Do:**

**1. Server Functions:**
```python
# Call existing server function
result = anvil.server.call('get_contacts')

# Register new server function
@anvil.server.callable
def new_function():
    pass
```

**2. Data Tables (via Server Functions):**
```python
# Must access through server layer
@anvil.server.callable
def get_data():
    user = anvil.users.get_user()
    return app_tables.contacts.search(instance_id=user)
```

**3. Anvil Services:**
```python
# Access Anvil services via server
@anvil.server.callable
def send_notification(email):
    anvil.email.send(to=email, subject="...", text="...")
```

**4. App Logs:**
```python
# Read app logs (if accessible)
# Log operations
import logging
logger.info("Operation completed")
```

### Uplink Limitations

**What Uplink Cannot Do:**

**1. Direct Client Code Access:**
- ❌ Cannot modify forms in UI designer
- ❌ Cannot change client modules directly
- ✅ Must use server as proxy

**2. App Settings:**
- ❌ Cannot change app configuration
- ❌ Cannot modify Data Tables schema
- ❌ Cannot adjust app settings
- ✅ Must use Anvil IDE for these

**3. Direct Data Tables Access:**
- ❌ Cannot access app_tables directly from Uplink script
- ✅ Must call server functions that access app_tables

---

## 2. CONNECTION MANAGEMENT

### Uplink Key Security

**CRITICAL SECURITY RULE:**

**Uplink Key = Full Access to Your Anvil App**

**Therefore:**
- ✅ Store in environment variable (NEVER in code)
- ✅ Keep secret (like a password)
- ❌ NEVER commit to repository
- ❌ NEVER share publicly
- ❌ NEVER include in logs

### Obtaining Uplink Key

**Steps:**
1. Open Anvil IDE
2. Click + in Sidebar Menu
3. Select "Uplink"
4. Choose deployment environment
5. Click "Enable Server Uplink Key"
6. Copy key (one-time display)

**Store Key:**
```bash
# Add to environment variable (Linux/Mac)
export ANVIL_UPLINK_KEY="your-uplink-key-here"

# Add to ~/.bashrc or ~/.zshrc for persistence
echo 'export ANVIL_UPLINK_KEY="your-key"' >> ~/.bashrc

# Verify
echo $ANVIL_UPLINK_KEY
```

### Connection Pattern

**Standard Connection Code:**

```python
# uplink_connection.py - Standard connection pattern

import anvil.server
import logging
import os
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def connect_to_anvil():
    """
    Connect to Anvil via Uplink with proper error handling.
    
    Returns:
        bool: True if connected successfully, False otherwise
    """
    # Get Uplink key from environment
    uplink_key = os.environ.get('ANVIL_UPLINK_KEY')
    
    if not uplink_key:
        logger.error("ANVIL_UPLINK_KEY environment variable not set")
        return False
    
    try:
        # Attempt connection
        logger.info("Connecting to Anvil via Uplink...")
        anvil.server.connect(uplink_key)
        logger.info("✅ Connected to Anvil successfully")
        
        # Verify connection
        try:
            # Call a simple test function to verify
            result = anvil.server.call('test_connection')
            logger.info(f"Connection verified: {result}")
        except Exception as e:
            logger.warning(f"Could not verify connection: {e}")
            # Connection established but test failed (acceptable)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to connect to Anvil: {e}", exc_info=True)
        return False

def disconnect_from_anvil():
    """
    Gracefully disconnect from Anvil.
    """
    logger.info("Disconnecting from Anvil...")
    # Anvil Uplink handles disconnection automatically on script end
    logger.info("✅ Disconnected")

if __name__ == "__main__":
    # Test connection
    if connect_to_anvil():
        print("Connection successful!")
        disconnect_from_anvil()
        sys.exit(0)
    else:
        print("Connection failed!")
        sys.exit(1)
```

### Connection Verification

**Always Verify Connection Before Operations:**

```python
def verify_uplink_connected():
    """
    Verify Uplink connection is active.
    
    Returns:
        bool: True if connected, False otherwise
    """
    try:
        # Simple test - call a known server function
        anvil.server.call('test_connection')
        return True
    except Exception as e:
        logger.error(f"Uplink connection not active: {e}")
        return False
```

**Use Before Operations:**
```python
# Before any Uplink operation
if not verify_uplink_connected():
    logger.error("Cannot proceed - not connected to Anvil")
    return False

# Proceed with operation
result = anvil.server.call('some_function')
```

---

## 3. SECURITY REQUIREMENTS

### Authentication Requirements

**MANDATORY: Always Verify Authentication**

```python
@anvil.server.callable
def secure_function():
    """
    CORRECT: Verify authentication before any operation
    """
    # Get authenticated user
    user = anvil.users.get_user()
    
    # Verify user is authenticated
    if not user:
        raise Exception("Authentication required")
    
    # Proceed with operation
    return perform_operation(user)
```

**NEVER:**
```python
@anvil.server.callable
def insecure_function():
    """
    WRONG: No authentication check
    """
    # This is insecure!
    return app_tables.sensitive_data.search()
```

### Multi-Tenant Data Isolation

**MANDATORY: Always Filter by instance_id**

**Reference:** Anvil Data Tables Code of Practice

**CORRECT:**
```python
@anvil.server.callable
def get_contacts():
    """Filter by instance_id (secure)"""
    user = anvil.users.get_user()
    if not user:
        raise Exception("Authentication required")
    
    # ALWAYS filter by instance_id
    return app_tables.contacts.search(instance_id=user)
```

**WRONG:**
```python
@anvil.server.callable
def get_all_contacts():
    """No instance_id filter (SECURITY VIOLATION)"""
    # This exposes ALL tenants' data!
    return app_tables.contacts.search()
```

### Input Validation

**MANDATORY: Validate All Inputs Server-Side**

```python
@anvil.server.callable
def create_contact(email: str, first_name: str):
    """
    Validate inputs before processing
    """
    user = anvil.users.get_user()
    if not user:
        raise Exception("Authentication required")
    
    # Validate email
    if not email or not validate_email(email):
        raise ValueError("Invalid email address")
    
    # Validate first_name
    if not first_name or len(first_name) < 2:
        raise ValueError("First name must be at least 2 characters")
    
    # Input validated - proceed
    return app_tables.contacts.add_row(
        instance_id=user,
        email=email,
        first_name=first_name,
        created_at=datetime.now()
    )
```

**NEVER:**
```python
@anvil.server.callable
def create_contact(email, first_name):
    """No validation (dangerous)"""
    # No checks - accepts anything!
    return app_tables.contacts.add_row(
        email=email,
        first_name=first_name
    )
```

### Secret Management

**NEVER Include Secrets in Code:**

```python
# ❌ WRONG
API_KEY = "sk_live_abc123..."
UPLINK_KEY = "server_..."

# ✅ CORRECT
API_KEY = os.environ.get('API_KEY')
UPLINK_KEY = os.environ.get('ANVIL_UPLINK_KEY')
```

**Store Secrets in:**
1. Environment variables (local development)
2. Anvil App Secrets (production)
3. Secure key management system

---

## 4. DATA INTEGRITY GUARDRAILS

### Backup Before Data Operations

**RULE 1: ALWAYS Backup Before Data Table Modifications**

```python
def modify_data_tables():
    """
    CORRECT: Backup before modifications
    """
    # Step 1: Create backup
    logger.info("Creating backup before data modification...")
    backup_result = subprocess.run(
        ['./backup_repo.sh', 'before-data-modification'],
        capture_output=True
    )
    
    if backup_result.returncode != 0:
        logger.error("Backup failed - aborting operation")
        return False
    
    # Step 2: Proceed with modification
    try:
        result = anvil.server.call('modify_contacts')
        logger.info("Data modification successful")
        
        # Step 3: Create backup after success
        subprocess.run(
            ['./backup_repo.sh', 'data-modification-complete'],
            capture_output=True
        )
        
        return True
        
    except Exception as e:
        logger.error(f"Data modification failed: {e}")
        # Restore from backup if needed
        return False
```

### Read Before Write

**RULE 2: Always Read Current State Before Modifying**

```python
@anvil.server.callable
def update_contact(contact_email: str, updates: dict):
    """
    CORRECT: Read before write
    """
    user = anvil.users.get_user()
    if not user:
        raise Exception("Authentication required")
    
    # Step 1: Read current state
    contact = app_tables.contacts.get(
        instance_id=user,
        email=contact_email
    )
    
    if not contact:
        raise Exception(f"Contact {contact_email} not found")
    
    # Step 2: Log current state
    logger.info(f"Current contact state: {dict(contact)}")
    
    # Step 3: Apply updates
    for key, value in updates.items():
        contact[key] = value
    contact['updated_at'] = datetime.now()
    
    # Step 4: Log new state
    logger.info(f"Updated contact state: {dict(contact)}")
    
    return contact
```

### Verify After Write

**RULE 3: Always Verify Changes Succeeded**

```python
@anvil.server.callable
def create_order(customer_email: str, price: float):
    """
    CORRECT: Verify after write
    """
    user = anvil.users.get_user()
    if not user:
        raise Exception("Authentication required")
    
    # Find customer
    customer = app_tables.customers.get(
        instance_id=user,
        email=customer_email
    )
    
    # Calculate order
    order_calc = calculate_order_total(price, 0.2, 10000.0)
    
    # Create order
    order = app_tables.orders.add_row(
        instance_id=user,
        customer=customer,
        total=order_calc['total'],
        status='pending',
        created_at=datetime.now()
    )
    
    # Verify creation
    verify = app_tables.orders.get(
        instance_id=user,
        customer=customer,
        created_at=order['created_at']
    )
    
    if not verify:
        logger.error("Order creation verification failed!")
        raise Exception("Failed to verify order creation")
    
    logger.info(f"Order created and verified: {order.get_id()}")
    return order
```

### Never Bulk Delete Without Verification

**RULE 4: Bulk Deletes Require Extra Caution**

```python
@anvil.server.callable
def delete_test_data():
    """
    CORRECT: Verify before bulk delete
    """
    user = anvil.users.get_user()
    if not user:
        raise Exception("Authentication required")
    
    # Find test records
    test_contacts = app_tables.contacts.search(
        instance_id=user,
        source='Test'
    )
    
    # Convert to list and verify
    test_list = list(test_contacts)
    logger.info(f"Found {len(test_list)} test contacts to delete")
    
    # Require confirmation for large deletes
    if len(test_list) > 10:
        logger.warning(f"Large delete operation: {len(test_list)} records")
        # In Factory's case, log warning and proceed
        # In production, might require user confirmation
    
    # Delete with verification
    deleted_count = 0
    for contact in test_list:
        email = contact['email']
        contact.delete()
        deleted_count += 1
        logger.debug(f"Deleted test contact: {email}")
    
    logger.info(f"Deleted {deleted_count} test contacts")
    return deleted_count
```

---

## 5. OPERATION PATTERNS

### Safe Operation Template

**Use This Pattern for All Uplink Operations:**

```python
def safe_uplink_operation(operation_name: str, *args, **kwargs):
    """
    Template for safe Uplink operations.
    
    Args:
        operation_name: Name of operation for logging
        *args, **kwargs: Operation-specific arguments
    
    Returns:
        Operation result or None if failed
    """
    # Step 1: Log operation start
    logger.info(f"Starting operation: {operation_name}")
    
    # Step 2: Verify Uplink connected
    if not verify_uplink_connected():
        logger.error(f"Cannot perform {operation_name} - not connected")
        return None
    
    # Step 3: Create backup (if data operation)
    if kwargs.get('backup_required', False):
        logger.info(f"Creating backup before {operation_name}...")
        subprocess.run(['./backup_repo.sh', f'before-{operation_name}'])
    
    # Step 4: Perform operation with error handling
    try:
        result = _perform_operation(operation_name, *args, **kwargs)
        logger.info(f"✅ {operation_name} completed successfully")
        
        # Step 5: Create backup after success (if data operation)
        if kwargs.get('backup_required', False):
            subprocess.run(['./backup_repo.sh', f'{operation_name}-complete'])
        
        return result
        
    except Exception as e:
        logger.error(f"❌ {operation_name} failed: {e}", exc_info=True)
        
        # Step 6: Handle failure
        if kwargs.get('backup_required', False):
            logger.warning(f"Consider restoring from backup: before-{operation_name}")
        
        return None

def _perform_operation(operation_name: str, *args, **kwargs):
    """
    Actual operation implementation.
    Override this for specific operations.
    """
    raise NotImplementedError("Override this method")
```

### Read Operations (Safe)

**Reading data is always safe:**

```python
@anvil.server.callable
def get_contact_count():
    """Safe read operation - no backup needed"""
    user = anvil.users.get_user()
    if not user:
        raise Exception("Authentication required")
    
    contacts = app_tables.contacts.search(instance_id=user)
    count = len(list(contacts))
    
    logger.info(f"Contact count: {count}")
    return count
```

### Write Operations (Careful)

**Writing data requires backup:**

```python
def create_contact_with_backup(email: str, first_name: str):
    """Write operation - backup required"""
    # Backup before
    logger.info("Creating backup before contact creation...")
    subprocess.run(['./backup_repo.sh', 'before-contact-create'])
    
    try:
        # Perform write
        result = anvil.server.call(
            'create_contact',
            email=email,
            first_name=first_name
        )
        
        # Verify
        verify = anvil.server.call('get_contact_by_email', email)
        if not verify:
            raise Exception("Contact creation verification failed")
        
        # Backup after success
        subprocess.run(['./backup_repo.sh', 'contact-create-complete'])
        
        logger.info(f"✅ Contact created: {email}")
        return result
        
    except Exception as e:
        logger.error(f"❌ Contact creation failed: {e}")
        logger.warning("Consider restoring from backup: before-contact-create")
        raise
```

### Test Operations (Extra Careful)

**Test operations with test data:**

```python
def run_integration_test():
    """Integration test - backup before, cleanup after"""
    # Backup before tests
    logger.info("Creating backup before integration tests...")
    subprocess.run(['./backup_repo.sh', 'before-integration-tests'])
    
    try:
        # Setup test data
        logger.info("Setting up test data...")
        test_customer = anvil.server.call(
            'create_customer',
            email='test@example.com',
            source='Test'  # Mark as test data
        )
        
        # Run tests
        logger.info("Running tests...")
        test_results = []
        
        # Test 1
        result1 = test_create_order(test_customer)
        test_results.append(result1)
        
        # Test 2
        result2 = test_order_validation(test_customer)
        test_results.append(result2)
        
        # Cleanup test data
        logger.info("Cleaning up test data...")
        cleanup_test_data()
        
        # Verify cleanup
        remaining = anvil.server.call('count_test_data')
        if remaining > 0:
            logger.warning(f"Cleanup incomplete: {remaining} test records remain")
        
        # Backup after tests pass
        if all(test_results):
            subprocess.run(['./backup_repo.sh', 'integration-tests-passing'])
            logger.info("✅ All integration tests passed")
        else:
            logger.error("❌ Some integration tests failed")
        
        return test_results
        
    except Exception as e:
        logger.error(f"Integration tests failed: {e}", exc_info=True)
        cleanup_test_data()  # Always cleanup
        raise
```

---

## 6. ERROR HANDLING

### Connection Errors

**Handle Uplink connection failures:**

```python
def handle_connection_error():
    """Handle Uplink connection failures"""
    try:
        anvil.server.connect(os.environ.get('ANVIL_UPLINK_KEY'))
        
    except anvil.server.SerializationError as e:
        logger.error(f"Serialization error: {e}")
        # Data type issue - check function arguments
        
    except anvil.server.TimeoutError as e:
        logger.error(f"Timeout error: {e}")
        # Connection timeout - retry
        
    except Exception as e:
        logger.error(f"Connection error: {e}", exc_info=True)
        # Other connection issues
```

### Data Table Errors

**Handle Data Tables operation failures:**

```python
@anvil.server.callable
def safe_data_tables_operation():
    """Handle Data Tables errors gracefully"""
    user = anvil.users.get_user()
    if not user:
        raise Exception("Authentication required")
    
    try:
        # Attempt operation
        contact = app_tables.contacts.get(
            instance_id=user,
            email='test@example.com'
        )
        
        if contact:
            # Process contact
            return process_contact(contact)
        else:
            # Not found - not an error, just no result
            logger.info("Contact not found")
            return None
            
    except anvil.tables.TableError as e:
        logger.error(f"Data Tables error: {e}", exc_info=True)
        raise Exception(f"Database operation failed: {e}")
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise
```

### Retry Logic

**Implement retry for transient failures:**

```python
def retry_operation(func, max_attempts=3, delay=1):
    """
    Retry operation on failure.
    
    Args:
        func: Function to retry
        max_attempts: Maximum retry attempts
        delay: Delay between retries (seconds)
    
    Returns:
        Function result or raises exception
    """
    import time
    
    for attempt in range(1, max_attempts + 1):
        try:
            logger.info(f"Attempt {attempt}/{max_attempts}")
            result = func()
            logger.info(f"✅ Operation succeeded on attempt {attempt}")
            return result
            
        except Exception as e:
            logger.warning(f"Attempt {attempt} failed: {e}")
            
            if attempt == max_attempts:
                logger.error(f"All {max_attempts} attempts failed")
                raise
            
            logger.info(f"Retrying in {delay} seconds...")
            time.sleep(delay)

# Usage
def unreliable_operation():
    return anvil.server.call('sometimes_fails')

result = retry_operation(unreliable_operation, max_attempts=3, delay=2)
```

---

## 7. LOGGING AND MONITORING

### Comprehensive Logging

**Log ALL Uplink Activities:**

```python
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/user/Mybizz-planning/uplink_operations.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('uplink_operations')

def log_operation(operation_name: str, details: dict):
    """
    Log Uplink operation with details.
    
    Args:
        operation_name: Name of operation
        details: Dict with operation details
    """
    logger.info(
        f"UPLINK OPERATION: {operation_name}",
        extra={
            "operation": operation_name,
            "timestamp": datetime.now().isoformat(),
            **details
        }
    )

# Usage
log_operation(
    "create_contact",
    {
        "email": "new@example.com",
        "result": "success",
        "record_id": contact.get_id()
    }
)
```

### Operation Audit Trail

**Maintain audit trail of all Uplink operations:**

```python
class UplinkAuditLogger:
    """
    Audit logger for all Uplink operations.
    Logs to file and optionally to Data Tables.
    """
    
    def __init__(self, log_file: str):
        self.log_file = log_file
        self.logger = logging.getLogger('uplink_audit')
    
    def log_read(self, table_name: str, filters: dict):
        """Log read operation"""
        self.logger.info(f"READ: {table_name} with filters {filters}")
    
    def log_write(self, table_name: str, action: str, record_id: str):
        """Log write operation"""
        self.logger.info(f"WRITE: {action} on {table_name}, record {record_id}")
    
    def log_delete(self, table_name: str, record_id: str):
        """Log delete operation"""
        self.logger.warning(f"DELETE: {table_name}, record {record_id}")
    
    def log_error(self, operation: str, error: Exception):
        """Log error"""
        self.logger.error(f"ERROR in {operation}: {error}", exc_info=True)

# Usage
audit = UplinkAuditLogger('/home/user/Mybizz-planning/uplink_audit.log')

# Log read
audit.log_read('contacts', {'instance_id': user, 'email': 'test@example.com'})

# Log write
audit.log_write('contacts', 'CREATE', contact.get_id())

# Log delete
audit.log_delete('contacts', contact.get_id())
```

---

## 8. BACKUP INTEGRATION

### Backup Before Uplink Operations

**RULE: Backup before ANY write operation via Uplink**

```python
def uplink_operation_with_backup(operation_name: str, operation_func):
    """
    Execute Uplink operation with automatic backup.
    
    Args:
        operation_name: Name for backup and logging
        operation_func: Function to execute
    
    Returns:
        Operation result
    """
    # Backup before
    logger.info(f"Creating backup before {operation_name}...")
    backup_result = subprocess.run(
        ['./backup_repo.sh', f'before-{operation_name}'],
        capture_output=True,
        text=True
    )
    
    if backup_result.returncode != 0:
        logger.error(f"Backup failed: {backup_result.stderr}")
        raise Exception("Backup failed - aborting operation")
    
    logger.info(f"Backup created: before-{operation_name}")
    
    # Execute operation
    try:
        result = operation_func()
        
        # Backup after success
        logger.info(f"Creating backup after successful {operation_name}...")
        subprocess.run(
            ['./backup_repo.sh', f'{operation_name}-complete'],
            capture_output=True
        )
        
        logger.info(f"✅ {operation_name} completed with backups")
        return result
        
    except Exception as e:
        logger.error(f"❌ {operation_name} failed: {e}")
        logger.warning(f"Restore from: before-{operation_name}")
        raise

# Usage
def my_write_operation():
    return anvil.server.call('create_something')

result = uplink_operation_with_backup(
    'create-customer',
    my_write_operation
)
```

### Backup Verification

**Verify backup before proceeding:**

```python
def verify_backup_exists(backup_name: str) -> bool:
    """
    Verify backup was created successfully.
    
    Args:
        backup_name: Name of backup to verify
    
    Returns:
        True if backup exists, False otherwise
    """
    import os
    
    backup_path = f'/home/user/Mybizz-backups/{backup_name}'
    
    if not os.path.exists(backup_path):
        logger.error(f"Backup not found: {backup_path}")
        return False
    
    # Check if backup contains files
    file_count = len(os.listdir(backup_path))
    if file_count == 0:
        logger.error(f"Backup is empty: {backup_path}")
        return False
    
    logger.info(f"✅ Backup verified: {backup_name} ({file_count} files)")
    return True

# Usage
backup_name = '2026-02-01_14-30_before-data-migration'
if not verify_backup_exists(backup_name):
    logger.error("Cannot proceed - backup verification failed")
    sys.exit(1)

# Proceed with operation
perform_data_migration()
```

---

## 9. COMMON OPERATIONS

### Operation 1: Reading Data

**Safe - No backup required:**

```python
def read_contacts():
    """Read contacts - safe operation"""
    logger.info("Reading contacts via Uplink...")
    
    contacts = anvil.server.call('get_all_contacts')
    logger.info(f"Retrieved {len(list(contacts))} contacts")
    
    return contacts
```

### Operation 2: Creating Records

**Requires backup:**

```python
def create_contact_safe(email: str, first_name: str):
    """Create contact with full safety protocol"""
    
    # Backup before
    subprocess.run(['./backup_repo.sh', 'before-contact-create'])
    
    try:
        # Create
        contact = anvil.server.call(
            'create_contact',
            email=email,
            first_name=first_name
        )
        
        # Verify
        verify = anvil.server.call('verify_contact_exists', email)
        if not verify:
            raise Exception("Contact creation verification failed")
        
        # Backup after
        subprocess.run(['./backup_repo.sh', 'contact-create-complete'])
        
        logger.info(f"✅ Contact created: {email}")
        return contact
        
    except Exception as e:
        logger.error(f"❌ Contact creation failed: {e}")
        raise
```

### Operation 3: Updating Records

**Requires backup:**

```python
def update_contact_safe(email: str, updates: dict):
    """Update contact with full safety protocol"""
    
    # Read current state
    logger.info(f"Reading current state of {email}...")
    current = anvil.server.call('get_contact_by_email', email)
    if not current:
        raise Exception(f"Contact {email} not found")
    
    logger.info(f"Current state: {dict(current)}")
    
    # Backup before
    subprocess.run(['./backup_repo.sh', 'before-contact-update'])
    
    try:
        # Update
        updated = anvil.server.call(
            'update_contact',
            email=email,
            updates=updates
        )
        
        # Verify changes
        verify = anvil.server.call('get_contact_by_email', email)
        for key, value in updates.items():
            if verify[key] != value:
                raise Exception(f"Update verification failed for {key}")
        
        logger.info(f"Updated state: {dict(verify)}")
        
        # Backup after
        subprocess.run(['./backup_repo.sh', 'contact-update-complete'])
        
        logger.info(f"✅ Contact updated: {email}")
        return updated
        
    except Exception as e:
        logger.error(f"❌ Contact update failed: {e}")
        raise
```

### Operation 4: Deleting Records

**Requires extra caution:**

```python
def delete_contact_safe(email: str):
    """Delete contact with extra safety checks"""
    
    # Verify exists
    logger.info(f"Verifying {email} exists...")
    contact = anvil.server.call('get_contact_by_email', email)
    if not contact:
        logger.warning(f"Contact {email} not found - nothing to delete")
        return False
    
    logger.info(f"Contact to delete: {dict(contact)}")
    
    # Backup before delete
    subprocess.run(['./backup_repo.sh', 'before-contact-delete'])
    
    # Confirm (in Factory's case, log warning)
    logger.warning(f"DELETING contact: {email}")
    
    try:
        # Delete
        result = anvil.server.call('delete_contact', email)
        
        # Verify deletion
        verify = anvil.server.call('get_contact_by_email', email)
        if verify:
            raise Exception("Contact deletion verification failed - still exists")
        
        # Backup after
        subprocess.run(['./backup_repo.sh', 'contact-delete-complete'])
        
        logger.info(f"✅ Contact deleted: {email}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Contact deletion failed: {e}")
        raise
```

### Operation 5: Running Tests

**Special test protocol:**

```python
def run_integration_tests_safe():
    """Run integration tests with proper protocol"""
    
    # Backup before tests
    subprocess.run(['./backup_repo.sh', 'before-integration-tests'])
    
    logger.info("Starting integration tests...")
    
    try:
        # Setup test data
        test_data = anvil.server.call('setup_test_data')
        logger.info(f"Test data created: {len(test_data)} records")
        
        # Run tests
        test_results = []
        
        for test_name in ['test_1', 'test_2', 'test_3']:
            try:
                result = anvil.server.call(f'run_{test_name}')
                test_results.append((test_name, True, None))
                logger.info(f"✅ {test_name} passed")
            except Exception as e:
                test_results.append((test_name, False, str(e)))
                logger.error(f"❌ {test_name} failed: {e}")
        
        # Cleanup test data
        logger.info("Cleaning up test data...")
        anvil.server.call('cleanup_test_data')
        
        # Verify cleanup
        remaining = anvil.server.call('count_test_data')
        if remaining > 0:
            logger.warning(f"Cleanup incomplete: {remaining} test records remain")
        
        # Summary
        passed = sum(1 for _, success, _ in test_results if success)
        failed = len(test_results) - passed
        
        logger.info(f"Test results: {passed} passed, {failed} failed")
        
        # Backup if all passed
        if failed == 0:
            subprocess.run(['./backup_repo.sh', 'integration-tests-passing'])
            logger.info("✅ All tests passed - backup created")
        else:
            logger.warning("Some tests failed - no backup created")
        
        return test_results
        
    except Exception as e:
        logger.error(f"Test execution failed: {e}", exc_info=True)
        # Ensure cleanup even on failure
        try:
            anvil.server.call('cleanup_test_data')
        except:
            pass
        raise
```

---

## 10. EMERGENCY PROCEDURES

### Emergency Stop

**If something goes wrong:**

```python
def emergency_stop():
    """
    Emergency stop for Uplink operations.
    Call this if operation is going wrong.
    """
    logger.critical("🚨 EMERGENCY STOP INITIATED")
    
    # Stop all operations
    # (In Factory's case, this stops the script)
    
    # Log emergency
    logger.critical("All operations halted")
    logger.critical("Review logs: /home/user/Mybizz-planning/uplink_operations.log")
    logger.critical("Last backup: check dev_log.md")
    
    # Exit
    sys.exit(1)
```

### Emergency Restore

**If data corrupted:**

```python
def emergency_restore(backup_name: str):
    """
    Emergency restore from backup.
    
    Args:
        backup_name: Name of backup to restore
    """
    logger.critical(f"🚨 EMERGENCY RESTORE from {backup_name}")
    
    # Verify backup exists
    backup_path = f'/home/user/Mybizz-backups/{backup_name}'
    if not os.path.exists(backup_path):
        logger.critical(f"BACKUP NOT FOUND: {backup_path}")
        logger.critical("Cannot restore - backup missing")
        sys.exit(1)
    
    # Backup current state (even if broken)
    logger.info("Backing up current broken state...")
    subprocess.run(['./backup_repo.sh', 'broken-state-backup'])
    
    # Restore from backup
    logger.info(f"Restoring from {backup_name}...")
    working_dir = '/home/user/Mybizz-master-template'
    
    # Clear working directory
    import shutil
    shutil.rmtree(working_dir)
    
    # Copy backup to working directory
    shutil.copytree(backup_path, working_dir)
    
    logger.critical(f"✅ Restored from {backup_name}")
    logger.critical("Verify Anvil syncs from GitHub")
    logger.critical("Test application functionality")
    
    # Document in dev log
    with open('/home/user/Mybizz-planning/dev_log.md', 'a') as f:
        f.write(f"\n## EMERGENCY RESTORE - {datetime.now().isoformat()}\n")
        f.write(f"- Restored from: {backup_name}\n")
        f.write(f"- Reason: Data corruption / operation failure\n")
        f.write(f"- Action: Review what went wrong, fix issue, continue\n\n")
```

### Contact Points

**If Factory encounters issues:**

1. **Log Files:**
   - `/home/user/Mybizz-planning/uplink_operations.log`
   - `/home/user/Mybizz-planning/dev_log.md`

2. **Backups:**
   - `/home/user/Mybizz-backups/`
   - Check dev log for latest "known good" backup

3. **Anvil Logs:**
   - Open Anvil IDE
   - View App Logs
   - Check for errors

4. **GitHub:**
   - Check if Anvil synced to GitHub
   - Review recent commits

---

## UPLINK SAFETY CHECKLIST

### Before Using Uplink
- [ ] Uplink key stored in environment variable
- [ ] Uplink key NOT in code or repository
- [ ] Connection verification working
- [ ] Logging configured
- [ ] Backup script tested
- [ ] Dev log setup complete

### Before Each Operation
- [ ] Understand what operation does
- [ ] Know if operation modifies data
- [ ] Backup if data modification
- [ ] Verify Uplink connected
- [ ] Log operation start

### During Operation
- [ ] Authentication checked
- [ ] Instance_id filter applied
- [ ] Inputs validated
- [ ] Operation logged
- [ ] Errors handled

### After Operation
- [ ] Result verified
- [ ] Backup if successful
- [ ] Dev log updated
- [ ] Next steps documented
- [ ] Cleanup completed

---

## CONCLUSION

**Uplink is Powerful - Use it Responsibly**

**Core Principles:**
1. ✅ Security first (authentication, validation, instance_id)
2. ✅ Backup before writes (always)
3. ✅ Verify after writes (always)
4. ✅ Log everything (complete audit trail)
5. ✅ Handle errors (gracefully)
6. ✅ Test carefully (cleanup after)

**Remember:**
- Uplink from Day 1 (consistent method)
- Follow guardrails (non-negotiable)
- Backup religiously (safety net)
- Document completely (dev log)
- Verify operations (never trust blindly)

**With proper protocols, Uplink enables confident, rapid development.**

---

**END OF ANVIL UPLINK CODE OF PRACTICE v1.0**
