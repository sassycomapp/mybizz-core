"""
Simple Uplink Connection Test

This script tests if the Uplink connection is working properly.
"""

import anvil.server
import os
import sys


def main():
    try:
        # Get uplink key from environment
        uplink_key = os.environ.get('ANVIL_UPLINK_KEY')
        
        if not uplink_key:
            print("ERROR: ANVIL_UPLINK_KEY environment variable not set")
            return False
        
        print("Connecting to Anvil via Uplink...")
        
        # Connect to Anvil
        anvil.server.connect(uplink_key)
        print("SUCCESS: Connected to Anvil")
        
        # Test the function
        print("Testing server function call...")
        result = anvil.server.call('test_uplink_connection')
        
        print("SUCCESS: Server function call worked")
        print(f"Message: {result['message']}")
        print("Uplink is WORKING!")
        
        # Disconnect
        anvil.server.disconnect()
        print("SUCCESS: Disconnected from Anvil")
        
        return True
        
    except Exception as e:
        print(f"FAILED: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)