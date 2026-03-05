"""
Uplink One-Shot Caller

Connects, calls a named server function with optional arguments,
prints the result, disconnects.

Usage:
    python scripts/uplink_call.py <function_name> [arg1] [arg2] ...

Arguments are JSON-parsed, so booleans, integers, and dicts can be passed
directly from the command line.

Examples:
    python scripts/uplink_call.py get_current_user_info
    python scripts/uplink_call.py authenticate_user '"test@example.com"' '"password123"'
    python scripts/uplink_call.py check_permission '"can_edit_contacts"'
"""

import anvil.server
import os
import sys
import json


def main():
    key = os.environ.get("ANVIL_UPLINK_KEY")
    if not key:
        print("ERROR: ANVIL_UPLINK_KEY not set — see ref_anvil_uplink.md §4")
        sys.exit(1)
    if not key.startswith("server_"):
        print("ERROR: ANVIL_UPLINK_KEY is not a Server Uplink key — see ref_anvil_uplink.md §2")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: python scripts/uplink_call.py <function_name> [args...]")
        sys.exit(1)

    fn_name = sys.argv[1]
    args = []
    for arg in sys.argv[2:]:
        try:
            args.append(json.loads(arg))
        except json.JSONDecodeError:
            args.append(arg)

    anvil.server.connect(key)
    try:
        result = anvil.server.call(fn_name, *args)
        print(json.dumps(result, indent=2, default=str))
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    finally:
        anvil.server.disconnect()


if __name__ == "__main__":
    main()
