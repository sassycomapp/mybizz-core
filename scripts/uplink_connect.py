"""
Uplink Connect

Simple connect and wait — verifies the key is valid and connection is live.
Press Enter to disconnect.
Run before any integration work to confirm the environment is healthy.

Usage:
    python scripts/uplink_connect.py
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
    print("Connected to Anvil")

    input("\nPress Enter to disconnect...")

    anvil.server.disconnect()
    print("Disconnected")


if __name__ == "__main__":
    main()
