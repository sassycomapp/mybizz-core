# Security & Compliance Reference

**Document Type:** Reference Material  
**Version:** 1.1  
**Date Created:** December 31, 2025  
**Last Reviewed:** January 16, 2026  
**Status:** Active - Compliance Reference  
**Related Docs:** 02_dev_policy_v4.md, 03_dev_plan.md (Phase 6.5)

---

## Purpose

This document provides comprehensive **compliance-specific** security guidance for Mybizz platform. It focuses on regulatory requirements (GDPR, POPIA, CCPA, PCI DSS) and implementation standards.

**Document Scope:**
- ✅ Compliance requirements and procedures
- ✅ Data subject rights (access, deletion, portability)
- ✅ Audit logging and reporting requirements
- ✅ Regulatory-specific implementation patterns

**For general development security standards, see:** `02_dev_policy_v4.md` (Anvil-first security implementation)

**Note:** This is a **reference document** to consult when implementing compliance features in Phase 6.5. It complements (not duplicates) the development policy.

**Compliance Jurisdictions:**
- **GDPR** - European Union (General Data Protection Regulation)
- **POPIA** - South Africa (Protection of Personal Information Act)
- **CCPA** - California, USA (California Consumer Privacy Act)
- **PCI DSS** - Payment Card Industry Data Security Standard (Level 4)

---

## PART 1: SECURITY REQUIREMENTS

### 1.1 Data Encryption

#### **At Rest**
**Provider:** Anvil handles database encryption automatically
- ✅ All data tables encrypted at rest
- ✅ Media objects encrypted
- ✅ Backups encrypted

**Additional Measures:**
- Sensitive fields (API keys, secrets) encrypted via Anvil Secrets
- Custom encryption for client secrets using Fernet symmetric encryption
- Encryption keys stored in Anvil Secrets (never in code)

**Implementation:**
```python
# sm_security.py
from cryptography.fernet import Fernet
import anvil.secrets

def encrypt_value(plaintext):
    """Encrypt sensitive data"""
    master_key = anvil.secrets.get_secret('encryption_master_key')
    cipher = Fernet(master_key.encode())
    encrypted = cipher.encrypt(plaintext.encode())
    return encrypted.decode()

def decrypt_value(ciphertext):
    """Decrypt sensitive data"""
    master_key = anvil.secrets.get_secret('encryption_master_key')
    cipher = Fernet(master_key.encode())
    decrypted = cipher.decrypt(ciphertext.encode())
    return decrypted.decode()
```

#### **In Transit**
**Provider:** Anvil enforces HTTPS automatically
- ✅ All client-server communication encrypted (TLS 1.2+)
- ✅ Custom domains: SSL certificates auto-provisioned
- ✅ No mixed content (all resources loaded via HTTPS)

**Verification:**
- Check custom domain SSL status in Anvil dashboard
- Test with SSL Labs (https://www.ssllabs.com/ssltest/)
- Ensure no HTTP-only resources

### 1.2 Authentication & Access Control

#### **Password Policies**
**Minimum requirements:**
- Length: 8+ characters
- Complexity: At least 1 uppercase, 1 lowercase, 1 number
- Reuse: Cannot reuse last 3 passwords
- Expiration: 90 days (optional, recommended for admin accounts)

**Implementation:** Anvil Users service enforces basic policies. Add custom validation:
```python
import re

def validate_password(password):
    """Enforce password policy"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain number"
    return True, "Password valid"
```

#### **Multi-Factor Authentication (MFA)**
**Status:** Optional for clients, recommended for Mybizz staff
- Anvil Users service supports Google Authenticator
- Implementation: Enable in Anvil Users settings
- Enforce for: Admin accounts, Mybizz staff

#### **Session Management**
**Requirements:**
- Session timeout: 30 minutes of inactivity
- Absolute timeout: 8 hours
- Concurrent sessions: Allowed (user can be logged in on multiple devices)
- Session termination: Logout clears all session data

**Implementation:**
```python
# Client-side (JavaScript)
import anvil.js
from anvil import *

# Track last activity
last_activity = datetime.now()

def reset_inactivity_timer():
    global last_activity
    last_activity = datetime.now()

# On any user interaction
@anvil.js.on_event('click', document)
def user_activity(event):
    reset_inactivity_timer()

# Check timeout every minute
def check_session_timeout():
    global last_activity
    if (datetime.now() - last_activity).total_seconds() > 1800:  # 30 min
        anvil.users.logout()
        open_form('frm_login')
        Notification("Session expired due to inactivity").show()

# Run timer
anvil.js.window.setInterval(check_session_timeout, 60000)  # Every 1 min
```

### 1.3 API Security

#### **Rate Limiting**
**Limits:**
- Unauthenticated requests: 10/minute per IP
- Authenticated requests: 100/minute per user
- Admin API: 1000/minute

**Implementation:**
```python
# sm_rate_limit.py
from datetime import datetime, timedelta
from anvil.tables import app_tables

def check_rate_limit(identifier, limit=100, window_minutes=1):
    """
    Check if request exceeds rate limit using Data Tables for persistence.
    
    Args:
        identifier (str): User ID or IP address
        limit (int): Maximum requests allowed in window
        window_minutes (int): Time window in minutes
    
    Returns:
        tuple: (allowed: bool, message: str)
    """
    now = datetime.now()
    
    # Get or create rate limit record
    record = app_tables.tbl_rate_limits.get(identifier=identifier)
    
    if not record:
        # First request - create record
        app_tables.tbl_rate_limits.add_row(
            identifier=identifier,
            count=1,
            reset_time=now + timedelta(minutes=window_minutes),
            last_request=now
        )
        return True, "OK"
    
    # Check if window expired
    if now > record['reset_time']:
        # Reset counter for new window
        record['count'] = 1
        record['reset_time'] = now + timedelta(minutes=window_minutes)
        record['last_request'] = now
        return True, "OK"
    
    # Increment count
    record['count'] += 1
    record['last_request'] = now
    
    # Check limit
    if record['count'] > limit:
        seconds_until_reset = (record['reset_time'] - now).total_seconds()
        return False, f"Rate limit exceeded. Try again in {int(seconds_until_reset)} seconds"
    
    return True, "OK"

@anvil.server.callable
def rate_limited_api_call():
    """Example rate-limited API call with persistent rate limiting"""
    user = anvil.users.get_user()
    identifier = str(user.get_id()) if user else anvil.server.request.origin
    
    allowed, message = check_rate_limit(identifier, limit=100)
    if not allowed:
        return {'success': False, 'error': message}
    
    # Process request
    return {'success': True, 'data': 'response'}
```

**Required Table:** `tbl_rate_limits`
- identifier (string, indexed) - User ID or IP address
- count (number) - Request count in current window
- reset_time (datetime) - When current window expires
- last_request (datetime) - Timestamp of most recent request

**Cleanup:** Implement background task to delete records older than 24 hours:
```python
@anvil.server.background_task
def cleanup_rate_limits():
    """Run daily to remove old rate limit records"""
    cutoff = datetime.now() - timedelta(days=1)
    old_records = app_tables.tbl_rate_limits.search(
        last_request=q.less_than(cutoff)
    )
    for record in old_records:
        record.delete()
```

**Why Data Tables?**
- ✅ Survives server restarts
- ✅ Works across Anvil's multi-server environment
- ✅ Actually provides security (not bypassable)
- ✅ Anvil-native, no external dependencies
- ✅ Automatic persistence and replication
```

#### **Input Validation**
**All user inputs must be validated:**
- **SQL Injection:** Anvil Data Tables API prevents this automatically
- **XSS (Cross-Site Scripting):** Sanitize HTML inputs
- **Command Injection:** Never pass user input directly to system commands
- **Path Traversal:** Validate file paths, never allow `../`

**Implementation:**
```python
import re
import html

def sanitize_html(text):
    """Sanitize HTML to prevent XSS"""
    # Escape HTML entities
    return html.escape(text)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_filename(filename):
    """Validate filename (no path traversal)"""
    if '..' in filename or '/' in filename or '\\' in filename:
        return False
    # Only allow alphanumeric, dash, underscore, dot
    pattern = r'^[a-zA-Z0-9._-]+$'
    return re.match(pattern, filename) is not None
```

### 1.4 Vulnerability Protection

#### **DDoS Protection**
**Provider:** Anvil infrastructure includes basic DDoS protection
**Additional measures:**
- Rate limiting (per above)
- Cloudflare integration (optional, for custom domains)
- Monitor traffic patterns

#### **Common Vulnerabilities (OWASP Top 10)**

| Vulnerability | Protection Measure |
|---------------|-------------------|
| Injection | Anvil Data Tables API (parameterized queries) |
| Broken Authentication | Anvil Users service + MFA |
| Sensitive Data Exposure | Encryption at rest & in transit |
| XML External Entities (XXE) | Not applicable (no XML processing) |
| Broken Access Control | Server-side permission checks |
| Security Misconfiguration | Follow Anvil best practices |
| Cross-Site Scripting (XSS) | Input sanitization |
| Insecure Deserialization | Anvil handles serialization securely |
| Using Components with Known Vulnerabilities | Keep Anvil dependencies updated |
| Insufficient Logging & Monitoring | Anvil provides logs, add custom audit logs |

---

## PART 2: COMPLIANCE REQUIREMENTS

### 2.1 GDPR (European Union)

#### **Applicability**
Mybizz must comply if serving EU customers or processing EU residents' data.

#### **Core Principles**
1. **Lawfulness, fairness, transparency** - Clear privacy policy
2. **Purpose limitation** - Only collect data for specified purposes
3. **Data minimization** - Only collect necessary data
4. **Accuracy** - Keep data up-to-date
5. **Storage limitation** - Don't keep data longer than needed
6. **Integrity & confidentiality** - Secure data
7. **Accountability** - Demonstrate compliance

#### **Key Requirements**

**1. Consent Management**
- ✅ Clear consent before collecting personal data
- ✅ Opt-in (not opt-out) for marketing
- ✅ Easy withdrawal of consent
- ✅ Cookie consent banner

**Implementation:**
- Consent checkbox during registration (not pre-checked)
- "Unsubscribe" link in all marketing emails
- Cookie banner on public pages

**2. Right to Access**
- ✅ Users can request copy of their data
- ✅ Provide data in machine-readable format (CSV, JSON)
- ✅ Respond within 30 days

**Implementation:**
```python
@anvil.server.callable
def export_my_data():
    """Export all user data (GDPR Article 15)"""
    user = anvil.users.get_user()
    if not user:
        return {'success': False, 'error': 'Not logged in'}
    
    # Gather all data
    data = {
        'user_profile': dict(user),
        'customers': list(app_tables.customers.search(owner=user)),
        'transactions': list(app_tables.transactions.search(user=user)),
        'invoices': list(app_tables.invoices.search(user=user)),
        # ... all other tables
    }
    
    # Convert to JSON
    import json
    json_data = json.dumps(data, default=str, indent=2)
    
    # Create downloadable file
    from anvil import BlobMedia
    blob = BlobMedia('application/json', json_data.encode(), name='my_data.json')
    
    return {'success': True, 'file': blob}
```

**3. Right to Deletion ("Right to be Forgotten")**
- ✅ Users can request data deletion
- ✅ Anonymize data (don't delete outright if needed for legal compliance)
- ✅ Notify third parties (if data shared)

**Implementation:**
```python
@anvil.server.callable
def delete_my_account():
    """Anonymize user data (GDPR Article 17)"""
    user = anvil.users.get_user()
    if not user:
        return {'success': False, 'error': 'Not logged in'}
    
    # Anonymize instead of delete (preserve financial records for compliance)
    user['email'] = f"deleted_{user.get_id()}@anonymized.local"
    user['enabled'] = False
    
    # Anonymize related records
    for customer in app_tables.customers.search(owner=user):
        customer['name'] = "ANONYMIZED"
        customer['email'] = "deleted@anonymized.local"
    
    # Keep financial records (7 years legal requirement)
    # But anonymize personal identifiers
    
    anvil.users.logout()
    return {'success': True}
```

**4. Data Breach Notification**
- ✅ Notify supervisory authority within 72 hours
- ✅ Notify affected users if high risk
- ✅ Document all breaches

**5. Privacy Policy**
Must include:
- What data we collect
- Why we collect it
- How we use it
- How long we keep it
- User rights (access, deletion, etc.)
- Contact for data protection officer (DPO)

**Template location:** `/docs/legal/privacy_policy_template.md` (to be created)

### 2.2 POPIA (South Africa)

#### **Applicability**
Mybizz MUST comply (based in South Africa, processes SA personal information).

#### **Comparison to GDPR**
POPIA is similar to GDPR with some differences:

| Aspect | GDPR | POPIA |
|--------|------|-------|
| Consent | Explicit, opt-in | Consent required |
| Data Subject Rights | Access, deletion, portability | Access, correction, deletion |
| Data Breach Notification | 72 hours to authority | Must notify if risk of harm |
| Penalties | Up to €20M or 4% revenue | Up to R10M or 10 years prison |
| Regulator | National DPAs | Information Regulator (SA) |

#### **Key Requirements**

**1. Lawful Processing**
Must have lawful basis (same as GDPR):
- Consent
- Contract performance
- Legal obligation
- Legitimate interest

**2. Purpose Specification**
- Collect data for specific purpose
- Don't use for incompatible purposes

**3. Information Quality**
- Keep data accurate and up-to-date
- Provide correction mechanism

**4. Openness (Transparency)**
- Privacy notice required
- Explain how data is processed

**5. Security Safeguards**
- Implement appropriate security measures
- Protect against loss, damage, unauthorized access

**6. Data Subject Participation**
- Right to access personal information
- Right to request correction
- Right to object to processing

**Implementation:** Similar to GDPR (use same export/delete functions).

**7. Information Regulator Notification**
- Register as "Responsible Party" with Information Regulator
- **Action required:** File with Information Regulator (South Africa)
- **Timeline:** ASAP after launch

### 2.3 CCPA (California, USA)

#### **Applicability**
If Mybizz has California customers or processes California residents' data.

#### **Key Differences from GDPR**
- Applies to for-profit entities only (Mybizz qualifies)
- Thresholds: Gross revenue >$25M OR >50,000 consumers/households OR >50% revenue from selling data
- **Mybizz likely below thresholds** but comply anyway as best practice

#### **Key Requirements**

**1. Right to Know**
- What personal information collected
- Sources of information
- Purposes of collection
- Third parties shared with

**2. Right to Delete**
- Same as GDPR

**3. Right to Opt-Out of Sale**
- "Do Not Sell My Personal Information" link
- **Mybizz:** We don't sell data, so this is N/A (but state clearly in privacy policy)

**4. Non-Discrimination**
- Cannot discriminate against users who exercise privacy rights

**Implementation:** GDPR compliance covers most CCPA requirements.

### 2.4 PCI DSS (Payment Card Industry)

#### **Applicability**
Any business that processes, stores, or transmits credit card data.

#### **Mybizz Level**
**Level 4** (lowest level):
- Processes <20,000 e-commerce transactions/year per brand
- All transactions via Stripe/PayPal (reduces scope significantly)

#### **Compliance Strategy**
**Outsource to PCI-compliant providers:**
- ✅ **Stripe** handles all card data (PCI Level 1 compliant)
- ✅ **PayPal** handles all card data (PCI Level 1 compliant)
- ✅ Mybizz NEVER stores card numbers (only Stripe/PayPal tokens)

#### **Reduced Scope (SAQ A)**
Since we use Stripe/PayPal hosted checkout:
- No card data on Mybizz servers
- No card data storage
- Tokens only (Stripe customer IDs, PayPal transaction IDs)

**Self-Assessment Questionnaire:** SAQ A (shortest, ~20 questions)
**Validation:** Annual self-assessment + quarterly network scans

#### **Requirements We Must Meet**

**1. Secure Network**
- ✅ HTTPS enforced (Anvil handles)
- ✅ No default passwords (enforced)

**2. Protect Cardholder Data**
- ✅ N/A - We don't store card data

**3. Vulnerability Management**
- ✅ Keep Anvil dependencies updated
- ✅ Secure coding practices (02_dev_policy.md)

**4. Access Control**
- ✅ Admin accounts with strong passwords + MFA
- ✅ Unique IDs for all users
- ✅ Log access to systems

**5. Monitor & Test**
- ✅ Anvil provides logs
- ✅ Regular security reviews
- ✅ Penetration testing (annually)

**6. Information Security Policy**
- ✅ Documented in 02_dev_policy.md

**Action Required:**
- Complete SAQ A annually
- Submit to acquiring bank if required
- Keep evidence of compliance

---

## PART 3: IMPLEMENTATION CHECKLIST

### 3.1 Phase 6.5 Implementation (Security & Compliance)

**Stage 18.5: Security Hardening**
- [ ] Implement password validation (strength requirements)
- [ ] Configure session timeout (30 min inactivity)
- [ ] Implement rate limiting on API endpoints
- [ ] Add input validation to all forms
- [ ] XSS protection (sanitize HTML inputs)
- [ ] Review Anvil security settings
- [ ] Enable MFA for admin accounts

**Stage 18.6: Compliance Implementation**
- [ ] Create privacy policy (GDPR, POPIA, CCPA compliant)
- [ ] Create terms of service
- [ ] Implement cookie consent banner
- [ ] Implement data export function (GDPR Article 15)
- [ ] Implement account deletion function (GDPR Article 17)
- [ ] Create data retention policy document
- [ ] Set up audit logging (who did what, when)
- [ ] Register with Information Regulator (South Africa)
- [ ] Complete PCI DSS SAQ A

**Stage 18.7: Backup & Recovery**
- [ ] Verify Anvil backup configuration
- [ ] Implement weekly automated CSV exports
- [ ] Implement pre-update snapshots
- [ ] Create disaster recovery plan document
- [ ] Test backup restore process

**Stage 18.8: Security Testing**
- [ ] Run OWASP Top 10 vulnerability scan
- [ ] Conduct basic penetration testing
- [ ] Review all server functions for security issues
- [ ] Test rate limiting
- [ ] Test session timeout
- [ ] Create security incident response plan

### 3.2 Ongoing Compliance Maintenance

**Monthly:**
- Review access logs for suspicious activity
- Update dependencies (Anvil auto-updates)
- Review user access permissions

**Quarterly:**
- PCI DSS network scan (if required)
- Security policy review
- Privacy policy review (ensure still accurate)

**Annually:**
- Complete PCI DSS SAQ A
- Penetration testing
- Disaster recovery drill
- Compliance audit (GDPR, POPIA, CCPA)
- Review with legal counsel (optional but recommended)

---

## PART 4: INCIDENT RESPONSE

### 4.1 Data Breach Response Plan

**If personal data breach detected:**

**Within 1 Hour:**
1. **Contain breach** - Stop data leak, isolate affected systems
2. **Assess impact** - How many users affected? What data exposed?
3. **Notify founder** immediately

**Within 24 Hours:**
4. **Document incident** - What happened, when, how discovered
5. **Notify technical lead** for remediation
6. **Begin user notification** (if high risk)

**Within 72 Hours (GDPR requirement):**
7. **Notify regulators:**
   - EU: National Data Protection Authority
   - SA: Information Regulator
   - CA: Attorney General (if CCPA applies)

8. **Provide:**
   - Nature of breach
   - Likely consequences
   - Measures taken to mitigate
   - Contact details for more information

**Post-Incident:**
9. **Remediate vulnerabilities** that caused breach
10. **Update security procedures**
11. **Conduct post-mortem**
12. **Document lessons learned**

### 4.2 Security Incident Response Plan

**For non-data-breach security incidents:**

**Incident Categories:**
- Unauthorized access attempts
- DDoS attack
- Malware detection
- Insider threat
- Phishing attack targeting users
- Vulnerability discovery

**Response Process:**
1. **Detect & Log** - Document incident details
2. **Assess Severity** - Low, Medium, High, Critical
3. **Contain** - Prevent further damage
4. **Eradicate** - Remove threat
5. **Recover** - Restore normal operations
6. **Document** - Post-incident report

**Contact:** Maintain list of security contacts (Anvil support, legal counsel, etc.)

---

## PART 5: LEGAL DOCUMENTS

### 5.1 Privacy Policy

**Required sections:**
1. Who we are (Mybizz contact info)
2. What data we collect
3. Why we collect it (lawful basis)
4. How we use it
5. Who we share it with (Stripe, PayPal, Brevo, etc.)
6. How long we keep it (data retention policy)
7. User rights (access, deletion, etc.)
8. Security measures
9. Cookies we use
10. How to contact us
11. How to complain (regulators' contact info)
12. Changes to policy (effective date)

**Template:** Create in `/docs/legal/privacy_policy.md`

### 5.2 Terms of Service

**Required sections:**
1. Acceptance of terms
2. Account registration
3. Subscription & billing
4. User responsibilities
5. Prohibited uses
6. Intellectual property
7. Termination
8. Limitation of liability
9. Governing law (South Africa)
10. Dispute resolution

**Template:** Create in `/docs/legal/terms_of_service.md`

### 5.3 Cookie Policy

**Required sections:**
1. What cookies are
2. Types of cookies we use:
   - Essential (authentication, session)
   - Analytics (if using Google Analytics)
   - Marketing (if using tracking)
3. How to manage cookies
4. More information (link to privacy policy)

**Implementation:** Cookie consent banner (Anvil custom component)

---

## PART 6: AUDIT & MONITORING

### 6.1 Audit Logging

**What to log:**
- User login/logout
- Account creation/deletion
- Password changes
- Permission changes
- Data exports (GDPR requests)
- Failed login attempts
- Administrative actions
- Data modifications (who, what, when)

**Implementation:**
```python
# sm_audit.py
from datetime import datetime
from anvil.tables import app_tables

@anvil.server.callable
def log_audit_event(event_type, description, user=None):
    """Log security/compliance event"""
    if user is None:
        user = anvil.users.get_user()
    
    app_tables.tbl_audit_log.add_row(
        timestamp=datetime.now(),
        event_type=event_type,
        description=description,
        user=user,
        ip_address=anvil.server.request.origin
    )
```

**Retention:** 7 years (matches financial record retention)

### 6.2 Compliance Reporting

**Quarterly Report:**
- Number of data subject requests (access, deletion)
- Data breaches (if any)
- Security incidents
- Compliance status (green/yellow/red)

**Annual Report:**
- PCI DSS SAQ A completion
- Penetration test results
- Disaster recovery drill results
- Compliance gaps identified
- Remediation plans

---

## Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-31 | Dev Team | Initial security & compliance reference |
| 1.1 | 2026-01-16 | Dev Team | **REVIEWED POST-RATIONALIZATION:** Clarified document purpose as compliance reference (distinct from dev_policy). Added scope statement. Updated related docs reference to 02_dev_policy_v4.md. Confirmed relevance for Phase 6.5 implementation. No substantive changes to compliance requirements. |

---

**Last Updated:** January 16, 2026  
**Next Review:** Before Phase 6.5 implementation (Security & Compliance phase)  
**Related Policy:** 02_dev_policy_v4.md (development security standards)  
**Contact:** Mybizz Development Team
