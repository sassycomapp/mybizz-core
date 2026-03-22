from ._anvil_designer import PasswordResetFormTemplate
from anvil import *
import anvil.server

from ..validation import is_basic_email


class PasswordResetForm(PasswordResetFormTemplate):
    """Password reset form for email-based reset requests.

    Layout: BlankLayout (Custom Form — no navigation, unauthenticated context).
    Key user flows: request a password reset link by email, return to sign-in.
    Feature flag dependencies: none.
    M3 component choices: Card (appearance=outlined), TextBox (appearance=outlined),
    Button (appearance=filled). Validation uses M3 error=True/False boolean property.

    Security: always shows an identical success message regardless of whether
    the email is registered (OWASP A07:2021 — prevents user enumeration).

    """

    def __init__(self, **properties):
        self.item = {'email': ''}
        self.init_components(**properties)
        self._apply_m3_properties()

    # ── Programmatic M3 properties ────────────────────────────────────────────

    def _apply_m3_properties(self) -> None:
        """Set all programmatic M3 properties as specified in 1.2-ui-design.yaml."""
        self.card_reset.appearance = 'outlined'

        self.lbl_title.style = 'headline'
        self.lbl_title.scale = 'small'
        self.lbl_title.text = 'Reset Password'

        self.txt_email.appearance = 'outlined'
        self.txt_email.label = 'Email'
        self.txt_email.placeholder = 'Enter your email address'
        self.txt_email.error = False

        self.btn_send_reset.appearance = 'filled'
        self.btn_send_reset.text = 'Send Reset Link'

    # ── Event handlers — zero logic ───────────────────────────────────────────

    def btn_send_reset_click(self, **event_args):
        self._handle_send_reset()

    def link_back_to_sign_in_click(self, **event_args):
        open_form('LoginForm')

    # ── Business logic ────────────────────────────────────────────────────────

    def _handle_send_reset(self) -> None:
        """Validate email, call reset_password, always show identical message.

        The identical message on success and failure prevents user enumeration
        (OWASP A07:2021). The button is disabled immediately to prevent
        duplicate submissions.
        """
        if not self.validate_form():
            return

        self.btn_send_reset.enabled = False
        email = self.txt_email.text or self.item.get('email', '')

        try:
            anvil.server.call('reset_password', email)
        except anvil.server.TimeoutError:
            pass
        except anvil.server.AnvilWrappedError:
            pass
        except Exception:
            pass

        Notification(
            "If that email is registered, a reset link has been sent.",
            style="info",
        ).show()

    def validate_form(self) -> bool:
        """Validate that the email field contains a plausible address.

        Returns:
            bool: True if the email is non-empty and contains '@'.
        """
        email = (self.txt_email.text or '').strip()
        is_valid = is_basic_email(email)
        if is_valid:
            self.txt_email.error = False
            self.txt_email.placeholder = 'Enter your email address'
        else:
            self.txt_email.error = True
            self.txt_email.placeholder = 'Enter a valid email address'
        return is_valid