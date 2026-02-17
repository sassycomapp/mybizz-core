"""
Simple Anvil Uplink Connection Script

Usage:
    python scripts/uplink_connect.py

Environment:
    ANVIL_UPLINK_KEY - Your Anvil Uplink key (required)
"""

import anvil.server
import os
import sys


def connect():
    """Connect to Anvil via Uplink."""
    uplink_key = os.environ.get('ANVIL_UPLINK_KEY')
    
    if not uplink_key:
        print("Error: ANVIL_UPLINK_KEY environment variable not set")
        sys.exit(1)
    
    anvil.server.connect(uplink_key)
    print("✓ Connected to Anvil")


def disconnect():
    """Disconnect from Anvil."""
    anvil.server.disconnect()
    print("✓ Disconnected from Anvil")


if __name__ == "__main__":
    connect()
    
    # Keep connection alive until user presses Enter
    input("\nPress Enter to disconnect...")
    
    disconnect()
