"""
Uplink Smoke Test

Connects, calls uplink_smoketest_20260217_module, confirms server runtime
is responding, disconnects.
Run before every Level 2 test session.
Exits with code 1 on failure — do not proceed until this passes.

Usage:
    python scripts/test_uplink.py
"""

import anvil.server
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

    anvil.server.connect(key)
    try:
        print("Running smoke test...")
        result = anvil.server.call("uplink_smoketest_20260217_module")
        if result.get("status") == "success":
            print("PASSED: Server runtime is live and callable")
        else:
            print(f"FAILED: Unexpected response: {result}")
            sys.exit(1)
    except Exception as e:
        print(f"FAILED: {e}")
        sys.exit(1)
    finally:
        anvil.server.disconnect()


if __name__ == "__main__":
    main()
