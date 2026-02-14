# [LoginForm] - UI Setup Instructions

**Purpose**: [User authentication via email/password]
**Last Updated**: 2026-02-06

---

## Component Hierarchy
```
Card (card_auth) 
>Column panel (col_form) {nested in card_auth}
>>Flow panel (lp_header) {nested in col_form}
>>>Heading (lbl_title) | {nested in lp_header}
>>Spacer {nested in col_form}
>>Flow panel (lp_email) {nested in col_form}
>>>Label (lbl_email) | TextBox (txt_email) {nested in lp_email}
>>Flow panel (lp_password) {nested in col_form}
>>>Label (lbl_password) | TextBox (txt_password) {nested in lp_password}
>>Checkbox (cb_remember) {nested in col_form}
>>Flow panel (lp_actions) {nested in col_form}
>>>Button (btn_login) | Spacer | Button (btn_forgot) {nested in lp_actions}
>>Flow panel (lp_links) {nested in col_form}
>>>Link (link_signup) | Spacer | Link (link_forgot) {nested in lp_links}
>>Label (lbl_error) {nested in col_form}
```

---

## Component Properties (Designer Only)

| Component Name | Property | Value | Notes |
|----------------|----------|-------|-------|
| card_auth | role | outlined-card | M3 card container |
| card_auth | width | 400 | Fixed width for form |
| col_form | width | fill | Full width inside card |
| col_form | padding | medium | M3 spacing |
| col_form | gap | medium | M3 spacing |
| lp_header | spacing_above | small | M3 spacing |
| lp_header | spacing_below | medium | M3 spacing |
| lbl_title | role | headline-small | M3 typography |
| lbl_title | text | Sign In | Form title |
| lp_email | spacing_above | small | M3 spacing |
| lp_email | spacing_below | small | M3 spacing |
| lbl_email | role | label-small | M3 typography |
| lbl_email | text | Email address | Field label |
| txt_email | role | outlined | M3 text field |
| txt_email | placeholder | Email address | Input placeholder |
| txt_email | (W) | ✓ | Write-back enabled |
| lp_password | spacing_above | small | M3 spacing |
| lp_password | spacing_below | small | M3 spacing |
| lbl_password | role | label-small | M3 typography |
| lbl_password | text | Password | Field label |
| txt_password | role | outlined | M3 text field |
| txt_password | hide_text | True | Security |
| txt_password | (W) | ✓ | Write-back enabled |
| cb_remember | text | Remember me | Checkbox label |
| lp_actions | spacing_above | medium | M3 spacing |
| lp_actions | spacing_below | small | M3 spacing |
| btn_login | role | filled-button | M3 primary action |
| btn_login | text | Sign In | Button text |
| btn_forgot | role | text-button | M3 secondary action |
| btn_forgot | text | Forgot password? | Button text |
| lp_links | spacing_above | small | M3 spacing |
| lp_links | spacing_below | small | M3 spacing |
| link_signup | text | Sign up | Navigation link |
| link_forgot | text | Forgot password? | Navigation link |
| lbl_error | role | body-small | M3 typography |
| lbl_error | foreground | theme:Error | M3 error color |
| lbl_error | visible | False | Hidden by default |
| lbl_error | text | Invalid email or password | Error message |
```

---

## Expected Visual Appearance

The LoginForm should display as a centered outlined card with a fixed width of 400 pixels. The card contains a vertically stacked form with proper M3 spacing and typography.

**Layout Structure:**
- The form is contained within an outlined card for visual separation from the page background
- Components are arranged in a single ColumnPanel with consistent spacing
- Each form field has a label above the input field
- The login button is positioned to the left with a "Forgot password?" button to the right
- "Remember me" checkbox is displayed below the password field
- Links for "Sign up" and "Forgot password?" are displayed at the bottom
- Error message appears in red below the form fields when validation fails

**Visual Hierarchy:**
- Large headline "Sign In" at the top
- Email and password fields with outlined text fields
- Primary "Sign In" button with filled-button role
- Secondary actions using text-button role
- Error message in theme:Error color when visible

**M3 Design Tokens Applied:**
- Consistent spacing using M3 spacing tokens (small, medium)
- Proper typography hierarchy (headline-small for title, label-small for labels, body-small for error)
- Theme colors for error state (theme:Error)
- Outlined card container for form grouping
- Filled button for primary action, text buttons for secondary actions

**Responsive Behavior:**
- Fixed width maintains consistent form appearance across screen sizes
- Card content adapts to smaller screens while maintaining readability
- Error message appears inline below form fields
- Navigation links remain accessible on all screen sizes
