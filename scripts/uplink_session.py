"""
Uplink Authenticated Session

Connects using init_session to pre-authenticate a user before any calls.
Required for server functions that internally call anvil.users.get_user().

Environment variables required:
    ANVIL_UPLINK_KEY      — Server Uplink key
    TEST_USER_EMAIL       — Email of the test user to authenticate as
    TEST_USER_PASSWORD    — Password of the test user

Usage:
    python scripts/uplink_session.py
"""

import anvil.server
import anvil.users
import os
import sys


def main():
    key = os.environ.get("ANVIL_UPLINK_KEY")
    if not key:
        print("ERROR: ANVIL_UPLINK_KEY not set — see ref_anvil_uplink.md §4")
        sys.exit(1)
    if not key.startswith("server_"):
        print("ERROR: ANVIL_UPLINK_KEY is not a Server Uplink key — see ref_anvil_uplink.md §2")
        sys.exit(1)

    test_email = os.environ.get("TEST_USER_EMAIL")
    test_password = os.environ.get("TEST_USER_PASSWORD")
    if not test_email or not test_password:
        print("ERROR: TEST_USER_EMAIL and TEST_USER_PASSWORD must be set")
        sys.exit(1)

    def authenticate():
        anvil.users.login_with_email(test_email, test_password)
        print(f"Authenticated as {test_email}")

    anvil.server.connect(key, init_session=authenticate)
    try:
        # =====================================================================
        # CALL SECTION — add your authenticated server calls here
        # Examples:
        #
        # result = anvil.server.call("get_current_user_info")
        # print(result)
        #
        # result = anvil.server.call("check_permission", "can_edit_contacts")
        # print(result)
        # =====================================================================

        print("Configure the CALL SECTION in this script before running.")

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    finally:
        anvil.server.disconnect()


if __name__ == "__main__":
    main()
