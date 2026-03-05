from ._anvil_designer import SignupFormTemplate
from anvil import *
import anvil.server
import anvil.users
import re


class SignupForm(SignupFormTemplate):
    """Signup form for creating new owner accounts.

    Layout: BlankLayout (Custom Form — no navigation, pre-authentication).
    Key user flows: create account with email/password/business name,
    navigate to sign-in, terms, and privacy pages.
    Feature flag dependencies: none.
    M3 component choices: Card (appearance=outlined), TextBox (appearance=outlined),
    Button (appearance=filled). Validation uses M3 error=True/False boolean property.
    """

    def __init__(self, **properties):
        self.item = {
            'email': '',
            'password': '',
            'confirm_password': '',
            'business_name': '',
            'agree_terms': False,
        }
        self.txt_password.hide_text = True
        self.txt_confirm_password.hide_text = True
        self.init_components(**properties)
        self._apply_m3_properties()

    # ── Programmatic M3 properties ────────────────────────────────────────────

    def _apply_m3_properties(self) -> None:
        """Set all programmatic M3 properties as specified in 1.2-ui-design.yaml."""
        self.card_signup.appearance = 'outlined'

        self.lbl_title.style = 'headline'
        self.lbl_title.scale = 'large'
        self.lbl_title.text = 'Create Account'

        self.txt_email.appearance = 'outlined'
        self.txt_email.label = 'Email'
        self.txt_email.placeholder = 'Enter your email'

        self.txt_password.appearance = 'outlined'
        self.txt_password.label = 'Password'
        self.txt_password.placeholder = 'Create a password (min 8 chars)'

        self.txt_confirm_password.appearance = 'outlined'
        self.txt_confirm_password.label = 'Confirm Password'
        self.txt_confirm_password.placeholder = 'Re-enter your password'

        self.txt_business_name.appearance = 'outlined'
        self.txt_business_name.label = 'Business Name'
        self.txt_business_name.placeholder = 'Your business name'

        self.cb_agree_terms.text = 'I agree to the Terms & Conditions'

        self.btn_create_account.appearance = 'filled'
        self.btn_create_account.text = 'Create Account'

        self.btn_reveal_password.icon = 'visibility_off'
        self.btn_reveal_confirm_password.icon = 'visibility_off'

    # ── Event handlers — zero logic ───────────────────────────────────────────

    def btn_create_account_click(self, **event_args):
        self._handle_create_account()

    def link_sign_in_click(self, **event_args):
        open_form('LoginForm')

    def link_terms_click(self, **event_args):
        open_form('TermsConditionsPage')

    def link_privacy_click(self, **event_args):
        open_form('PrivacyPolicyPage')

    def btn_reveal_password_click(self, **event_args):
        self._toggle_password_visibility()

    def btn_reveal_confirm_password_click(self, **event_args):
        self._toggle_confirm_password_visibility()

    # ── Business logic ────────────────────────────────────────────────────────

    def _toggle_password_visibility(self) -> None:
        """Toggle password field between masked and visible."""
        self.txt_password.hide_text = not self.txt_password.hide_text
        self.btn_reveal_password.icon = (
            'visibility_off' if self.txt_password.hide_text else 'visibility'
        )

    def _toggle_confirm_password_visibility(self) -> None:
        """Toggle confirm password field between masked and visible."""
        self.txt_confirm_password.hide_text = not self.txt_confirm_password.hide_text
        self.btn_reveal_confirm_password.icon = (
            'visibility_off' if self.txt_confirm_password.hide_text else 'visibility'
        )

    def _handle_create_account(self) -> None:
        """Validate all inputs, then call create_user on the server."""
        if not self.validate_form():
            return

        password = self.item.get('password') or ''
        is_strong, message = self._validate_password_strength(password)
        if not is_strong:
            self.txt_password.error = True
            Notification(message, style="danger").show()
            return
        self.txt_password.error = False

        confirm_password = self.item.get('confirm_password') or ''
        if password != confirm_password:
            self.txt_confirm_password.error = True
            Notification("Passwords do not match.", style="danger").show()
            return
        self.txt_confirm_password.error = False

        if not self.item.get('agree_terms'):
            self.cb_agree_terms.error = True
            Notification(
                "You must agree to the Terms & Conditions.", style="danger"
            ).show()
            return
        self.cb_agree_terms.error = False

        email = (self.item.get('email') or '').strip()
        business_name = (self.item.get('business_name') or '').strip()

        try:
            result = anvil.server.call('create_user', email, password, business_name)
        except anvil.server.TimeoutError:
            Notification(
                "The request timed out. Please try again.", style="danger"
            ).show()
            return
        except anvil.server.AnvilWrappedError as err:
            Notification(str(err), style="danger").show()
            return

        if result.get('success'):
            Notification("Account created. Please sign in.", style="success").show()
            open_form('LoginForm')
            return

        Notification(
            result.get('error', 'Account creation failed. Please try again.'),
            style="danger",
        ).show()

    def _validate_password_strength(self, password: str) -> tuple:
        """Check password meets minimum strength requirements.

        Args:
            password: The candidate password string.

        Returns:
            tuple: (bool, str) — (is_valid, error_message).
                   error_message is empty string when is_valid is True.
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters."
        if not re.search(r'[A-Z]', password):
            return False, "Password must include an uppercase letter."
        if not re.search(r'[a-z]', password):
            return False, "Password must include a lowercase letter."
        if not re.search(r'[0-9]', password):
            return False, "Password must include a number."
        return True, ""

    def validate_form(self) -> bool:
        """Validate business name, email, and password fields.

        Returns:
            bool: True if all required fields are present and valid.
        """
        email = (self.item.get('email') or '').strip()
        business_name = (self.item.get('business_name') or '').strip()
        password = self.item.get('password') or ''
        is_valid = True

        if not business_name:
            self.txt_business_name.error = True
            is_valid = False
        else:
            self.txt_business_name.error = False

        if not email or '@' not in email:
            self.txt_email.error = True
            is_valid = False
        else:
            self.txt_email.error = False

        if not password:
            self.txt_password.error = True
            is_valid = False
        else:
            self.txt_password.error = False

        return is_valid