from ._anvil_designer import LoginFormTemplate
from anvil import *
import anvil.server
import anvil.users

from ..ui_helpers import navigate_by_role
from ..validation import is_basic_email, is_non_empty


class LoginForm(LoginFormTemplate):
    """Login form for email/password authentication.

    Layout: BlankLayout (Custom Form — no navigation, pre-authentication).
    Key user flows: sign in with email/password, navigate to forgot-password.
    Feature flag dependencies: none.
    M3 component choices: Card (appearance=outlined), TextBox (appearance=outlined),
    Button (appearance=filled). Validation uses M3 error=True/False boolean property.
    """

    def __init__(self, **properties):
        self.item = {'email': '', 'password': '', 'remember_me': False}
        self.txt_password.hide_text = True
        user = anvil.users.get_user()
        if user:
            navigate_by_role()
            return
        self.init_components(**properties)
        self._apply_m3_properties()

    # ── Programmatic M3 properties ────────────────────────────────────────────

    def _apply_m3_properties(self) -> None:
        """Set all programmatic M3 properties as specified in 1.2-ui-design.yaml."""
        self.card_login.appearance = 'outlined'

        self.lbl_title.style = 'headline'
        self.lbl_title.scale = 'large'
        self.lbl_title.text = 'Sign In'

        self.txt_email.appearance = 'outlined'
        self.txt_email.label = 'Email'
        self.txt_email.placeholder = 'Enter your email'

        self.txt_password.appearance = 'outlined'
        self.txt_password.label = 'Password'
        self.txt_password.placeholder = 'Enter your password'

        self.cb_remember_me.text = 'Remember me'

        self.btn_sign_in.appearance = 'filled'
        self.btn_sign_in.text = 'Sign In'

        self.link_forgot_password.text = 'Forgot password?'

        self.btn_reveal_password.icon = 'visibility_off'

    # ── Event handlers — zero logic ───────────────────────────────────────────

    def btn_sign_in_click(self, **event_args):
        self._handle_sign_in()

    def link_forgot_password_click(self, **event_args):
        open_form('PasswordResetForm')

    def btn_reveal_password_click(self, **event_args):
        self._toggle_password_visibility()

    # ── Business logic ────────────────────────────────────────────────────────

    def _toggle_password_visibility(self) -> None:
        """Toggle password field between masked and visible."""
        self.txt_password.hide_text = not self.txt_password.hide_text
        self.btn_reveal_password.icon = (
            'visibility_off' if self.txt_password.hide_text else 'visibility'
        )

    def _handle_sign_in(self) -> None:
        """Validate inputs, call authenticate_user, and navigate on success."""
        if not self.validate_form():
            return

        email = (self.item.get('email') or '').strip()
        password = self.item.get('password') or ''

        try:
            result = anvil.server.call('authenticate_user', email, password)
        except anvil.server.TimeoutError:
            Notification(
                "The request timed out. Please try again.", style="danger"
            ).show()
            return
        except anvil.server.AnvilWrappedError as err:
            self.txt_email.error = True
            self.txt_password.error = True
            Notification(str(err), style="danger").show()
            return

        if result.get('success'):
            navigate_by_role()
            return

        self.txt_email.error = True
        self.txt_password.error = True
        Notification(
            result.get('error', 'Sign in failed. Please try again.'),
            style="danger",
        ).show()

    def validate_form(self) -> bool:
        """Validate email and password fields.

        Returns:
            bool: True if all fields are valid, False otherwise.
        """
        email = (self.item.get('email') or '').strip()
        password = self.item.get('password') or ''
        is_valid = True

        if not is_basic_email(email):
            self.txt_email.error = True
            is_valid = False
        else:
            self.txt_email.error = False

        if not is_non_empty(password):
            self.txt_password.error = True
            is_valid = False
        else:
            self.txt_password.error = False

        return is_valid