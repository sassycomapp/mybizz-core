from ._anvil_designer import SettingsFormTemplate
from anvil import *
import anvil.server
import anvil.users
from ..shared.auth_helpers import require_admin


# ---------------------------------------------------------------------------
# Tab configuration — maps each tab button name to its ColumnPanel name
# ---------------------------------------------------------------------------
_TABS = {
    'btn_tab_business': 'col_business',
    'btn_tab_email':    'col_email',
    'btn_tab_payments': 'col_payments',
    'btn_tab_theme':    'col_theme',
}

# Gateway ColumnPanel names keyed by dropdown display value
_GATEWAY_PANELS = {
    'Stripe':   'col_stripe',
    'Paystack': 'col_paystack',
    'PayPal':   'col_paypal',
}

# Original placeholder text for validated fields — used when resetting error state
_PLACEHOLDERS = {
    'txt_business_name':  'Business name',
    'txt_contact_email':  'Contact email',
    'txt_smtp_host':      'SMTP host',
    'txt_smtp_port':      'Port',
    'txt_smtp_username':  'Username',
    'txt_smtp_password':  'Password',
    'txt_from_email':     'From email address',
    'txt_from_name':      'From name',
}


class SettingsForm(SettingsFormTemplate):
    """Main settings form — four-tab interface for business, email, payments and theme."""

    # ------------------------------------------------------------------ init

    def __init__(self, **properties):
        # Auth check BEFORE init_components — redirects if not admin
        require_admin()

        self.init_components(**properties)

        # Cannot be set in Designer — LinearPanel orientation must be set in code
        self.lp_tab_bar.orientation = 'horizontal'

        # Set in Designer; also set here for safety in case Designer value is lost
        self.txt_smtp_password.hide_text = True

        # Missing from Designer build — must be set in code
        self.lbl_section_from.scale = 'small'

        # Mark the settings nav link as active in the parent layout
        self.get_open_form().set_active_link('nav_settings')

        # Static label text — these labels are empty in the Designer
        self.lbl_logo_hint.text = (
            "Upload your business logo. Accepted: PNG, JPG, SVG."
        )
        self.lbl_colour_hint.text = "Enter hex values, e.g. #1A73E8"
        self.lbl_theme_deferred.text = (
            "Theme is saved and applied when the public website is built (Phase 2)."
        )
        self.lbl_stripe_secret_note.text = (
            "Secret key stored in The Vault (configured in next step)"
        )
        self.lbl_paystack_secret_note.text = (
            "Secret key stored in The Vault (configured in next step)"
        )
        self.lbl_paypal_secret_note.text = (
            "Secret stored in The Vault (configured in next step)"
        )

        # Dropdown items — empty in Designer
        self.dd_active_gateway.items = ["Stripe", "Paystack", "PayPal"]
        self.dd_font_family.items = [
            "Roboto", "Open Sans", "Lato", "Montserrat", "Poppins", "Inter"
        ]
        self.dd_header_style.items = ["Standard", "Minimal", "Bold"]

        # Default tab state — business tab active, all others hidden
        self._activate_tab('btn_tab_business')

        # Load all tab data from server
        self.load_business_profile()
        self.load_email_config()
        self.load_payment_config()
        self.load_theme_config()

    # --------------------------------------------------------------- tab nav

    def _activate_tab(self, active_btn_name: str) -> None:
        """Show the panel for active_btn_name; hide all others. Update button roles.

        Args:
            active_btn_name: Attribute name of the tab button being activated.
        """
        for btn_name, panel_name in _TABS.items():
            btn   = getattr(self, btn_name)
            panel = getattr(self, panel_name)
            if btn_name == active_btn_name:
                btn.role      = 'filled'
                panel.visible = True
            else:
                btn.role      = 'outlined'
                panel.visible = False

    def btn_tab_business_click(self, **event_args):
        self._activate_tab('btn_tab_business')

    def btn_tab_email_click(self, **event_args):
        self._activate_tab('btn_tab_email')

    def btn_tab_payments_click(self, **event_args):
        self._activate_tab('btn_tab_payments')

    def btn_tab_theme_click(self, **event_args):
        self._activate_tab('btn_tab_theme')

    # ------------------------------------------------ gateway panel visibility

    def dd_active_gateway_change(self, **event_args):
        self._show_gateway_panel(self.dd_active_gateway.selected_value)

    def _show_gateway_panel(self, gateway: str) -> None:
        """Show the ColumnPanel for the selected gateway; hide the other two.

        Args:
            gateway: Display name of the selected gateway, e.g. 'Stripe'.
        """
        for name, panel_name in _GATEWAY_PANELS.items():
            getattr(self, panel_name).visible = (name == gateway)

    # --------------------------------------------------------- load handlers

    def load_business_profile(self) -> None:
        """Load business profile from server and populate the Business tab fields."""
        result = anvil.server.call('get_business_profile')
        if not result['success']:
            alert(f"Could not load business profile: {result['error']}",
                  title="Load Error")
            return

        data = result['data'] or {}
        self.txt_business_name.text  = data.get('business_name', '')
        self.txt_tagline.text        = data.get('tagline', '')
        self.txt_description.text    = data.get('description', '')
        self.txt_contact_email.text  = data.get('contact_email', '')
        self.txt_contact_phone.text  = data.get('phone', '')
        self.txt_address_line_1.text = data.get('address_line_1', '')
        self.txt_address_line_2.text = data.get('address_line_2', '')
        self.txt_city.text           = data.get('city', '')
        self.txt_country.text        = data.get('country', '')
        self.txt_postal_code.text    = data.get('postal_code', '')
        self.txt_website_url.text    = data.get('website_url', '')
        self.txt_facebook.text       = data.get('social_facebook', '')
        self.txt_instagram.text      = data.get('social_instagram', '')
        self.txt_social_x.text       = data.get('social_x', '')
        self.txt_linkedin.text       = data.get('social_linkedin', '')

        logo = data.get('logo')
        if logo is not None:
            self.img_logo_preview.source  = logo
            self.img_logo_preview.visible = True
        else:
            self.img_logo_preview.visible = False

    def load_email_config(self) -> None:
        """Load email configuration from server and populate the Email tab fields."""
        result = anvil.server.call('get_email_config')
        if not result['success']:
            alert(f"Could not load email config: {result['error']}",
                  title="Load Error")
            return

        data = result['data'] or {}
        self.txt_smtp_host.text     = data.get('smtp_host', '')
        smtp_port                   = data.get('smtp_port')
        self.txt_smtp_port.text     = str(smtp_port) if smtp_port else ''
        self.txt_smtp_username.text = data.get('smtp_username', '')
        self.txt_smtp_password.text = data.get('smtp_password', '')
        self.txt_from_email.text    = data.get('from_email', '')
        self.txt_from_name.text     = data.get('from_name', '')

        configured = data.get('configured', False)
        self.lbl_config_status.text = "Configured" if configured else "Not configured"

    def load_payment_config(self) -> None:
        """Load payment configuration from server and populate the Payments tab fields."""
        result = anvil.server.call('get_payment_config')
        if not result['success']:
            alert(f"Could not load payment config: {result['error']}",
                  title="Load Error")
            return

        data    = result['data'] or {}
        gateway = data.get('active_gateway', 'Stripe')

        self.dd_active_gateway.selected_value = gateway
        self.cb_test_mode.checked             = data.get('test_mode', True)

        self.txt_stripe_pub.text   = data.get('stripe_publishable_key', '')
        self.txt_stripe_sk.text    = data.get('stripe_secret_key', '')
        self.txt_paystack_pub.text = data.get('paystack_public_key', '')
        self.txt_paystack_sk.text  = data.get('paystack_secret_key', '')
        self.txt_paypal_id.text    = data.get('paypal_client_id', '')
        self.txt_paypal_sk.text    = data.get('paypal_secret', '')

        self.lbl_stripe_status.text   = "Connected" if data.get('stripe_connected')   else "Not connected"
        self.lbl_paystack_status.text = "Connected" if data.get('paystack_connected') else "Not connected"
        self.lbl_paypal_status.text   = "Connected" if data.get('paypal_connected')   else "Not connected"

        # Show the panel matching the loaded gateway
        self._show_gateway_panel(gateway)

    def load_theme_config(self) -> None:
        """Load theme configuration from server and populate the Theme tab fields."""
        result = anvil.server.call('get_theme_config')
        if not result['success']:
            alert(f"Could not load theme config: {result['error']}",
                  title="Load Error")
            return

        data = result['data'] or {}
        self.txt_primary_color.text         = data.get('primary_color', '')
        self.txt_accent_color.text          = data.get('accent_color', '')
        self.dd_font_family.selected_value  = data.get('font_family', 'Roboto')
        self.dd_header_style.selected_value = data.get('header_style', 'Standard')

    # ---------------------------------------------------------- save handlers

    def btn_save_business_click(self, **event_args):
        self._save_business()

    def _save_business(self) -> None:
        """Validate and save the business profile."""
        if not self._validate_business():
            return

        logo_file = self.fu_logo.file  # None if no new file selected

        data = {
            'business_name':    self.txt_business_name.text,
            'tagline':          self.txt_tagline.text,
            'description':      self.txt_description.text,
            'contact_email':    self.txt_contact_email.text,
            'phone':            self.txt_contact_phone.text,
            'address_line_1':   self.txt_address_line_1.text,
            'address_line_2':   self.txt_address_line_2.text,
            'city':             self.txt_city.text,
            'country':          self.txt_country.text,
            'postal_code':      self.txt_postal_code.text,
            'website_url':      self.txt_website_url.text,
            'social_facebook':  self.txt_facebook.text,
            'social_instagram': self.txt_instagram.text,
            'social_x':         self.txt_social_x.text,
            'social_linkedin':  self.txt_linkedin.text,
        }

        result = anvil.server.call('save_business_profile', data, logo_file)
        if result['success']:
            Notification("Business profile saved.", style="success").show()
            if logo_file is not None:
                # Refresh preview to show the newly uploaded logo
                self.load_business_profile()
        else:
            alert(f"Save failed: {result['error']}", title="Save Error")

    def btn_save_email_click(self, **event_args):
        self._save_email()

    def _save_email(self) -> None:
        """Validate and save the email configuration."""
        if not self._validate_email():
            return

        data = {
            'smtp_host':     self.txt_smtp_host.text,
            'smtp_port':     int(self.txt_smtp_port.text.strip()),
            'smtp_username': self.txt_smtp_username.text,
            'smtp_password': self.txt_smtp_password.text,
            'from_email':    self.txt_from_email.text,
            'from_name':     self.txt_from_name.text,
        }

        result = anvil.server.call('save_email_config', data)
        if result['success']:
            Notification("Email configuration saved.", style="success").show()
            self.lbl_config_status.text = "Not tested"
        else:
            alert(f"Save failed: {result['error']}", title="Save Error")

    def btn_test_email_click(self, **event_args):
        self._test_email()

    def _test_email(self) -> None:
        """Validate fields then test the SMTP connection; display result in status label."""
        if not self._validate_email():
            return

        result = anvil.server.call('test_email_connection')
        if result['success']:
            self.lbl_config_status.text = result.get('data', 'Connection successful')
        else:
            self.lbl_config_status.text = result.get('error', 'Connection failed')

    def btn_save_payments_click(self, **event_args):
        self._save_payments()

    def _save_payments(self) -> None:
        """Save the payment gateway configuration."""
        # Secret key fields (txt_stripe_sk, txt_paystack_sk, txt_paypal_sk) display
        # masked '***' values loaded from the server and must never be sent back.
        # Secret keys are managed exclusively via The Vault (Stage 1.5).
        data = {
            'active_gateway':         self.dd_active_gateway.selected_value,
            'test_mode':              self.cb_test_mode.checked,
            'stripe_publishable_key': self.txt_stripe_pub.text,
            'paystack_public_key':    self.txt_paystack_pub.text,
            'paypal_client_id':       self.txt_paypal_id.text,
        }

        result = anvil.server.call('save_payment_config', data)
        if result['success']:
            Notification("Payment configuration saved.", style="success").show()
        else:
            alert(f"Save failed: {result['error']}", title="Save Error")

    def btn_save_theme_click(self, **event_args):
        self._save_theme()

    def _save_theme(self) -> None:
        """Validate hex colour fields and save the theme configuration."""
        if not self._validate_theme():
            return

        data = {
            'primary_color': self.txt_primary_color.text,
            'accent_color':  self.txt_accent_color.text,
            'font_family':   self.dd_font_family.selected_value,
            'header_style':  self.dd_header_style.selected_value,
        }

        result = anvil.server.call('save_theme_config', data)
        if result['success']:
            Notification("Theme configuration saved.", style="success").show()
        else:
            alert(f"Save failed: {result['error']}", title="Save Error")

    # ----------------------------------------------------------- validation

    def _set_field_error(self, field_name: str, message: str) -> None:
        """Mark a TextBox as invalid: outlined-error role + error message as placeholder.

        Args:
            field_name: Attribute name of the TextBox on this form.
            message:    Error message to display as placeholder text.
        """
        field             = getattr(self, field_name)
        field.role        = 'outlined-error'
        field.placeholder = message
        field.text        = ''

    def _clear_field_error(self, field_name: str) -> None:
        """Reset a TextBox to its default valid state.

        Args:
            field_name: Attribute name of the TextBox on this form.
        """
        field             = getattr(self, field_name)
        field.role        = 'outlined'
        field.placeholder = _PLACEHOLDERS.get(field_name, '')

    def _validate_hex(self, value: str) -> bool:
        """Return True if value is a valid CSS hex colour string.

        Accepts 3-digit (#RGB) and 6-digit (#RRGGBB) forms, case-insensitive.
        A blank/empty value is considered valid — the field is optional.

        Args:
            value: The string to validate, e.g. '#1A73E8'.

        Returns:
            True if value is empty or a valid hex colour; False otherwise.
        """
        value = value.strip()
        if not value:
            return True
        if not value.startswith('#'):
            return False
        hex_part = value[1:]
        if len(hex_part) not in (3, 6):
            return False
        return all(c in '0123456789abcdefABCDEF' for c in hex_part)

    def _validate_business(self) -> bool:
        """Validate required Business tab fields.

        Returns:
            True if all required fields are populated, False otherwise.
        """
        valid = True

        if not self.txt_business_name.text.strip():
            self._set_field_error('txt_business_name', 'Business name is required')
            valid = False
        else:
            self._clear_field_error('txt_business_name')

        if not self.txt_contact_email.text.strip():
            self._set_field_error('txt_contact_email', 'Contact email is required')
            valid = False
        else:
            self._clear_field_error('txt_contact_email')

        return valid

    def _validate_email(self) -> bool:
        """Validate all required Email tab fields.

        Returns:
            True if all required fields are populated and port is a valid integer.
        """
        valid = True

        required_fields = [
            ('txt_smtp_host',     'SMTP host is required'),
            ('txt_smtp_port',     'Port is required'),
            ('txt_smtp_username', 'Username is required'),
            ('txt_smtp_password', 'Password is required'),
            ('txt_from_email',    'From email is required'),
            ('txt_from_name',     'From name is required'),
        ]

        for field_name, message in required_fields:
            field = getattr(self, field_name)
            if not field.text.strip():
                self._set_field_error(field_name, message)
                valid = False
            else:
                self._clear_field_error(field_name)

        # Additional check — port must be a valid integer when populated
        if self.txt_smtp_port.text.strip():
            try:
                int(self.txt_smtp_port.text.strip())
            except ValueError:
                self._set_field_error('txt_smtp_port', 'Port must be a number')
                valid = False

        return valid

    def _validate_theme(self) -> bool:
        """Validate hex colour fields on the Theme tab.

        Returns:
            True if both colour fields are empty or valid hex values, False otherwise.
        """
        valid = True

        if not self._validate_hex(self.txt_primary_color.text):
            alert("Primary colour must be a valid hex value, e.g. #1A73E8",
                  title="Validation Error")
            valid = False

        if not self._validate_hex(self.txt_accent_color.text):
            alert("Accent colour must be a valid hex value, e.g. #FF5722",
                  title="Validation Error")
            valid = False

        return valid


# POLISH COMPLETE — SettingsForm client form
