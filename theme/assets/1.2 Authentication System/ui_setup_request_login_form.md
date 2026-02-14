# UI Designer Setup Instructions - 1.2 Login Form

## TASK: Generate Anvil Designer UI Setup Instructions

### Context
I need step-by-step UI setup instructions for building the **[FORM_NAME]** form in Anvil Designer using Material 3 components.

### Form Details
- **Form Name**: [loginForm]
- **Form Purpose**: [ser authentication via email/password] 
- **Parent Section**: Phase 1, Section 1.2 - Authentication System
- **Architecture**: UI Form → Server Module (server_auth.service)

---

## Required Output Format
Save output as C:\_Data\MyBizz\mybizz-core\theme\assets\dev-docs\1.2 Authentication System\ui_setup_login_form.md
Generate a markdown file named `ui_setup_login_form.md` with the following structure:

### 1. Component Hierarchy
Use this nesting notation:
```
Content panel (component_name)
>Column panel (component_name) {nested in content_panel}
>>Flow panel (component_name) {nested in column_panel}
>>>Label (lbl_name) | TextBox (txt_name) | Button (btn_name) {nested in flow_panel}
>Spacer
>>Label (lbl_name) {nested in column_panel}
>>Button (btn_name) | Spacer | Button (btn_name)
```

**Rules:**
- Use `>` for each nesting level
- Use `|` to separate components in the same horizontal row
- Include component type and exact name using proper prefixes (see anvil_m3_component_recommendations.md and 05_nomenclature.md)
- Show {nested in parent_name} for clarity

### 2. Component Properties Table
Create a table with ONLY properties that MUST be set in Anvil Designer (cannot be set programmatically):

```markdown
| Component Name | Property | Value | Notes |
|----------------|----------|-------|-------|
| lbl_title | role | headline-large | M3 typography |
| lbl_title | text | Sign In | Display text |
| txt_email | role | outlined | M3 input style |
| txt_email | placeholder | Email address | |
| txt_email | (W) | ✓ | Write-back enabled |
| txt_password | role | outlined | M3 input style |
| txt_password | hide_text | True | Security |
| txt_password | (W) | ✓ | Write-back enabled |
| btn_login | role | filled-button | M3 primary action |
| btn_login | text | Sign In | |
| lbl_error | role | body-small | M3 typography |
| lbl_error | foreground | theme:Error | M3 error color |
| lbl_error | visible | False | Hidden by default |
```

**Include:**
- M3 `role` properties (MUST use M3 components from anvil_m3_component_recommendations.md)
- Text content (text, placeholder)
- Layout properties that cannot be set in code (spacing_above, spacing_below if critical)
- Visual properties locked to Designer (foreground colors using theme: syntax)
- Write-back (W) property for text inputs
- Boolean properties (hide_text, visible, enabled)

**Exclude:**
- Event handlers
- Programmatically configurable properties

### 3. Expected Visual Appearance
Describe what the developer should see after setup:
- Overall layout (centered card, full-width form, etc.)
- Component arrangement (stacked vertically, horizontal button row, etc.)
- Visual hierarchy (title at top, error message below inputs, etc.)
- M3 design tokens applied (proper spacing, typography scales, theme colors)

---

## Source Documents to Reference

1. C:\_Data\MyBizz\mybizz-core\theme\assets\dev-docs\Anvil_Methods
2. C:\_Data\MyBizz\mybizz-core\theme\assets\dev-docs\Factory_Methods
3. C:\_Data\MyBizz\mybizz-core\theme\assets\dev-docs\Mybizz_Methods
4. C:\_Data\MyBizz\.factory\droids Each droid has references to the docs which it requires
5. C:\_Data\MyBizz\mybizz-core\theme\assets\dev-docs\Factory_Methods\droid_document_mapping.md.md

---

## Constraints

- ONLY M3 components where possible (prefer M3 over legacy)
- ALL components must use proper naming prefixes (btn_, txt_, lbl_, col_, etc.)
- NO event handler definitions (will be wired later in code)
- NO summaries, checklists, or cross-references
- NO properties that can be set programmatically
- Include Write-back (W) property for all text input components
- Use theme: syntax for colors (e.g., theme:Error, theme:Primary)

---

## Authentication Form Specific Requirements

### For LoginForm:
- Email input field (TextBox, outlined role, write-back enabled)
- Password input field (TextBox, outlined role, hide_text=True, write-back enabled)
- Login button (filled-button role)
- "Forgot Password?" link (text-button role or NavigationLink)
- "Sign Up" link (text-button role or NavigationLink)
- Error message label (body-small role, theme:Error, hidden by default)

---

## Output File Template

Generate: `ui_setup_login_form.md`

Start with:
```markdown
# [LoginForm] - UI Setup Instructions

**Purpose**: [`User authentication via email/password`]
**Last Updated**: [DATE]

---

## Component Hierarchy
[hierarchy here]

---

## Component Properties (Designer Only)
[table here]

---

## Expected Visual Appearance
[description here]
```

---

## Factory.ai Command  - Task Instruction

```
Using the provided context documents and the prompt template above, generate the UI setup instructions for LoginForm. Follow the exact format specified, reference anvil_m3_component_recommendations.md for component selection, and include only Designer-required properties in the properties table.
```

---

## Notes

- This prompt template is designed to work with Factory.ai droids that have access to all project documentation
- The output will be a step-by-step guide for manual UI construction in Anvil Designer
- No coding is included - event handlers will be wired in a separate phase
- All M3 compliance is enforced through component selection and role properties
