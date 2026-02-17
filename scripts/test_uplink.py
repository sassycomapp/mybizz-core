"""
Test Uplink Connection

Tests the Uplink connection by calling a simple server function.
"""

import anvil.server
import os
import sys


def main():
    # Get uplink key
    uplink_key = os.environ.get('ANVIL_UPLINK_KEY')
    if not uplink_key:
        print("Error: ANVIL_UPLINK_KEY environment variable not set")
        sys.exit(1)
    
    print("Connecting to Anvil via Uplink...")
    
    try:
        # Connect
        anvil.server.connect(uplink_key)
        print("Connected to Anvil")
        
        # Test the function
        print("\nCalling uplink_smoketest_20260217_module()...")
        result = anvil.server.call('uplink_smoketest_20260217_module')
        
        print("\nTest successful!")
        print(f"   Status: {result['status']}")
        print(f"   Message: {result.get('message', '')}")
        print(f"   Timestamp: {result.get('timestamp', '')}")
        print(f"   Module: {result.get('server_module', '')}")
        
    except Exception as e:
        print(f"\nTest failed: {e}")
        sys.exit(1)
    
    finally:
        # Always disconnect
        print("\nDisconnecting...")
        anvil.server.disconnect()
        print("Disconnected")
    
    print("\nUplink test complete!")


if __name__ == "__main__":
    main()
