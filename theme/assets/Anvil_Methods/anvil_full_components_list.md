# Component Naming Prefix Guide

**Legend:**
- ✅ **ESSENTIAL** - Always use prefix
- 🟡 **GOOD TO HAVE** - Use in complex forms (15+ components)
- ⚪ **NO PREFIX** - Use semantic names only

---

## Group: Layout

| # | Component | Prefix | Status | Notes |
|---|-----------|--------|--------|-------|
| 1 | Slot | - | ⚪ NO PREFIX | Rare, semantic name better |

---

## Group: Theme Components

| # | Component | Prefix | Status | Notes |
|---|-----------|--------|--------|-------|
| 2 | Outlined Card | `card_` | 🟡 GOOD TO HAVE | If multiple cards in form |
| 3 | Outlined Button | `btn_` | ✅ ESSENTIAL | Same as regular Button |
| 4 | Outlined TextBox | `txt_` | ✅ ESSENTIAL | Same as regular TextBox |

---

## Group: Custom Components (Anvil Extras)

| # | Component | Prefix | Status | Notes |
|---|-----------|--------|--------|-------|
| 5 | Switch | `sw_` | 🟡 GOOD TO HAVE | If multiple switches |
| 6 | Slider | `slider_` | 🟡 GOOD TO HAVE | If multiple sliders |
| 7 | MessagePill | - | ⚪ NO PREFIX | Rare, semantic name |
| 8 | Chip | - | ⚪ NO PREFIX | Rare, semantic name |
| 9 | MultiSelectDropDown | `dd_` | ✅ ESSENTIAL | Treat as dropdown |
| 10 | PageBreak | - | ⚪ NO PREFIX | Rare, obvious |
| 11 | Tabs | - | ⚪ NO PREFIX | Usually one per form |
| 12 | Quill | - | ⚪ NO PREFIX | Rich text editor, rare |
| 13 | ChipsInput | - | ⚪ NO PREFIX | Rare, semantic name |
| 14 | Autocomplete | `ac_` | 🟡 GOOD TO HAVE | If multiple autocompletes |
| 15 | Determinate | - | ⚪ NO PREFIX | Progress bar, semantic |
| 16 | Indeterminate | - | ⚪ NO PREFIX | Progress bar, semantic |
| 17 | Pivot | - | ⚪ NO PREFIX | Rare component |
| 18 | RadioGroup | `rg_` | 🟡 GOOD TO HAVE | If multiple radio groups |
| 19 | CheckBoxGroup | `cbg_` | 🟡 GOOD TO HAVE | If multiple checkbox groups |

---

## Group: Routing

| # | Component | Prefix | Status | Notes |
|---|-----------|--------|--------|-------|
| 20 | NavLink | `link_` | 🟡 GOOD TO HAVE | Optional, context clear |
| 21 | Anchor | - | ⚪ NO PREFIX | Rare, semantic name |

---

## Group: Common Components (Material 3)

| # | Component | Prefix | Status | Notes |
|---|-----------|--------|--------|-------|
| 22 | Button | `btn_` | ✅ ESSENTIAL | Very common |
| 23 | Text | `lbl_` | ✅ ESSENTIAL | Use lbl_ for display text |
| 24 | Link | `link_` | 🟡 GOOD TO HAVE | If multiple links |
| 25 | Checkbox | `cb_` | ✅ ESSENTIAL | Very common |
| 26 | TextBox | `txt_` | ✅ ESSENTIAL | Very common |
| 27 | Card | `card_` | 🟡 GOOD TO HAVE | If multiple cards |

---

## Group: Typography (Material 3)

| # | Component | Prefix | Status | Notes |
|---|-----------|--------|--------|-------|
| 28 | Text | `lbl_` | ✅ ESSENTIAL | Display text = label |
| 29 | Heading | `lbl_` | ✅ ESSENTIAL | Heading = special label |
| 30 | Link | `link_` | 🟡 GOOD TO HAVE | If multiple links |
| 31 | RichText | - | ⚪ NO PREFIX | Rare, semantic name |

---

## Group: Buttons (Material 3)

| # | Component | Prefix | Status | Notes |
|---|-----------|--------|--------|-------|
| 32 | Button | `btn_` | ✅ ESSENTIAL | Very common |
| 33 | IconButton | `btn_` | ✅ ESSENTIAL | Same as Button |
| 34 | ToggleIconButton | `btn_` or `toggle_` | 🟡 GOOD TO HAVE | Context dependent |

---

## Group: Display (Material 3)

| # | Component | Prefix | Status | Notes |
|---|-----------|--------|--------|-------|
| 35 | Avatar | - | ⚪ NO PREFIX | Usually one, semantic |
| 36 | Card | `card_` | 🟡 GOOD TO HAVE | If multiple cards |
| 37 | InteractiveCard | `card_` | 🟡 GOOD TO HAVE | Same as Card |
| 38 | CardContentContainer | `col_` | ✅ ESSENTIAL | It's a container |
| 39 | SidesheetContent | `col_` | ✅ ESSENTIAL | It's a container |
| 40 | Divider | - | ⚪ NO PREFIX | Obvious, semantic |

---

## Group: Form Input (Material 3)

| # | Component | Prefix | Status | Notes |
|---|-----------|--------|--------|-------|
| 41 | Checkbox | `cb_` | ✅ ESSENTIAL | Very common |
| 42 | RadioButton | `rb_` | ✅ ESSENTIAL | Very common |
| 43 | TextBox | `txt_` | ✅ ESSENTIAL | Very common |
| 44 | TextArea | `txt_` | ✅ ESSENTIAL | Treat as TextBox |
| 45 | DropdownMenu | `dd_` | ✅ ESSENTIAL | Very common |
| 46 | Switch | `sw_` | 🟡 GOOD TO HAVE | If multiple switches |
| 47 | FileLoader | `fu_` | ✅ ESSENTIAL | Common for uploads |
| 48 | Slider | `slider_` | 🟡 GOOD TO HAVE | If multiple sliders |
| 49 | DatePicker | `dp_` | ✅ ESSENTIAL | Very common |
| 50 | RadioGroupPanel | `rg_` or `panel_` | 🟡 GOOD TO HAVE | Context dependent |

---

## Group: Navigation (Material 3)

| # | Component | Prefix | Status | Notes |
|---|-----------|--------|--------|-------|
| 51 | NavigationLink | `link_` | 🟡 GOOD TO HAVE | If multiple nav links |

---

## Group: Menus (Material 3)

| # | Component | Prefix | Status | Notes |
|---|-----------|--------|--------|-------|
| 52 | ButtonMenu | `menu_` | 🟡 GOOD TO HAVE | If multiple menus |
| 53 | IconButtonMenu | `menu_` | 🟡 GOOD TO HAVE | If multiple menus |
| 54 | AvatarMenu | `menu_` | 🟡 GOOD TO HAVE | If multiple menus |
| 55 | MenuItem | - | ⚪ NO PREFIX | Child of menu, obvious |

---

## Group: Feedback (Material 3)

| # | Component | Prefix | Status | Notes |
|---|-----------|--------|--------|-------|
| 56 | LinearProgressIndicator | - | ⚪ NO PREFIX | Usually one, semantic |
| 57 | CircularProgressIndicator | - | ⚪ NO PREFIX | Usually one, semantic |

---

## Group: Integrations (Material 3)

| # | Component | Prefix | Status | Notes |
|---|-----------|--------|--------|-------|
| 58 | Plot | `plot_` | 🟡 GOOD TO HAVE | If multiple charts |
| 59 | YouTube Video | - | ⚪ NO PREFIX | Rare, semantic |
| 60 | Google Map | - | ⚪ NO PREFIX | Usually one, semantic |
| 61 | Canvas | - | ⚪ NO PREFIX | Rare, semantic |

---

## Group: Containers (Material 3)

| # | Component | Prefix | Status | Notes |
|---|-----------|--------|--------|-------|
| 62 | ColumnPanel | `col_` | ✅ ESSENTIAL | Very common structure |
| 63 | FlowPanel | `flow_` | ✅ ESSENTIAL | Common responsive container |
| 64 | RepeatingPanel | `rp_` | ✅ ESSENTIAL | Common for lists |
| 65 | DataRowPanel | - | ⚪ NO PREFIX | Template component, semantic |
| 66 | LinearPanel | `lp_` | ✅ ESSENTIAL | Very common structure |
| 67 | GridPanel | `grid_` | 🟡 GOOD TO HAVE | If multiple grids |
| 68 | XYPanel | `xy_` | 🟡 GOOD TO HAVE | If multiple XY panels |
| 69 | Data Grid | `dg_` | ✅ ESSENTIAL | Common for tables |

---

## Group: Other (Material 3)

| # | Component | Prefix | Status | Notes |
|---|-----------|--------|--------|-------|
| 70 | Image | `img_` | 🟡 GOOD TO HAVE | If multiple images |
| 71 | Spacer | - | ⚪ NO PREFIX | Just "spacer" is fine |
| 72 | Timer | - | ⚪ NO PREFIX | Rare, semantic name |

---

## 📋 SUMMARY: Essential Prefixes (Always Use)

| Prefix | Component Types | Count |
|--------|----------------|-------|
| `col_` | ColumnPanel, CardContentContainer, SidesheetContent | 3 |
| `lp_` | LinearPanel | 1 |
| `flow_` | FlowPanel | 1 |
| `btn_` | Button, Outlined Button, IconButton | 3 |
| `lbl_` | Text, Heading (for display) | 2 |
| `txt_` | TextBox, TextArea, Outlined TextBox | 3 |
| `dd_` | DropdownMenu, MultiSelectDropDown | 2 |
| `cb_` | Checkbox | 1 |
| `rb_` | RadioButton | 1 |
| `dp_` | DatePicker | 1 |
| `fu_` | FileLoader | 1 |
| `dg_` | Data Grid | 1 |
| `rp_` | RepeatingPanel | 1 |

**Total Essential: 13 prefixes covering 21 component types**

---

## 🟡 Good to Have Prefixes (Use in Complex Forms)

| Prefix | Component Types |
|--------|----------------|
| `card_` | Card, Outlined Card, InteractiveCard |
| `link_` | Link, NavLink, NavigationLink |
| `sw_` | Switch |
| `slider_` | Slider |
| `ac_` | Autocomplete |
| `rg_` | RadioGroup, RadioGroupPanel |
| `cbg_` | CheckBoxGroup |
| `menu_` | ButtonMenu, IconButtonMenu, AvatarMenu |
| `plot_` | Plot (for multiple charts) |
| `grid_` | GridPanel |
| `xy_` | XYPanel |
| `img_` | Image (for multiple images) |

**Total Good to Have: 12 additional prefixes**

---

## ⚪ No Prefix Needed (Use Semantic Names)

**Components without prefixes (39 types):**
- Rare components: Slot, MessagePill, Chip, Quill, ChipsInput, Pivot, etc.
- Obvious components: Spacer, Divider, PageBreak, Timer
- Single-use: Avatar, Google Map, YouTube Video, Canvas
- Progress indicators: Determinate, Indeterminate, LinearProgressIndicator, CircularProgressIndicator
- Template components: DataRowPanel, MenuItem
- Specialized: RichText, Anchor, Tabs

---

## 🎯 Practical Application Guide

### **For Simple Forms (< 10 components):**
Use ONLY the 13 essential prefixes

### **For Complex Forms (15+ components):**
Use essential + good to have prefixes (25 total)

### **For Very Complex Forms (30+ components):**
Use all prefixes liberally for clarity

### **Example Naming:**
```python
# Essential (always)
self.col_main
self.lp_header
self.btn_save
self.txt_email
self.dd_status
self.cb_agree
self.dg_contacts
self.rp_items

# Good to have (complex forms)
self.card_summary
self.link_edit
self.plot_revenue
self.img_logo

# No prefix (semantic)
self.revenue_chart  # Only one plot
self.profile_avatar  # Only one avatar
self.loading_indicator  # Clear from name
self.main_content_tabs  # Only one tabs component
```

---

**Bottom line: Use 13 essential prefixes consistently, add 12 more in complex forms, skip the rest.** ✅