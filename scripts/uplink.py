"""
Uplink Keep-Alive

Connects and keeps connection alive via wait_forever().
Use during extended integration sessions or when Anvil needs to call local functions.
Ctrl+C to stop cleanly.

Usage:
    python scripts/uplink.py
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
    print("Connected to Anvil — waiting. Press Ctrl+C to stop.")
    anvil.server.wait_forever()


if __name__ == "__main__":
    main()
