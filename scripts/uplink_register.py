"""
Uplink Register

Registers local functions as callable from the Anvil app.
Connects and stays alive via wait_forever() so Anvil can call back.

Replace or extend the placeholder function with your real
@anvil.server.callable functions before connecting.

Usage:
    python scripts/uplink_register.py
"""

import anvil.server
import os
import sys


# =====================================================================
# REGISTER YOUR FUNCTIONS HERE
# Replace local_example with your real functions.
# =====================================================================

@anvil.server.callable
def local_example(data):
    """Example local function callable from Anvil. Replace with real implementation."""
    return {"received": data}

# =====================================================================


def main():
    key = os.environ.get("ANVIL_UPLINK_KEY")
    if not key:
        print("ERROR: ANVIL_UPLINK_KEY not set — see ref_anvil_uplink.md §4")
        sys.exit(1)
    if not key.startswith("server_"):
        print("ERROR: ANVIL_UPLINK_KEY is not a Server Uplink key — see ref_anvil_uplink.md §2")
        sys.exit(1)

    anvil.server.connect(key)
    print("Connected — local functions registered. Press Ctrl+C to stop.")
    anvil.server.wait_forever()


if __name__ == "__main__":
    main()
