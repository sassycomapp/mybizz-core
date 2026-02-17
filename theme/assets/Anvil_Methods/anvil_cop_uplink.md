# Anvil Uplink Setup and Usage Guide

## Overview

Anvil Uplink allows external Python scripts to connect to your Anvil application, enabling automation, data processing, and integration with local systems. This document provides essential information for setting up, starting, using, and testing Anvil Uplink.

## Uplink Key
Enable Server Uplink.
For your use case — running Python scripts locally in VSCode that call your Anvil app's server functions — Server Uplink is correct.
Server Uplink means your local script connects as if it were a server module. It can call @anvil.server.callable functions, access Data Tables, and run server-side logic.
Client Uplink means your local script connects as if it were browser/client code. It cannot access Data Tables directly and has the same restrictions as client-side code — which is the opposite of what you need.
Your scripts/test_uplink.py and scripts/uplink.py are all written expecting Server Uplink. The key it generates goes into your ANVIL_UPLINK_KEY environment variable as documented in your anvil_cop_uplink.md.

Anvil uplink key has been deleted. I will create new anvil uplink:



The Server Uplink Key is: "server_JTC5YBCKEFJNKXLMOLXV3TNO-TUYORZGLGKI2HE4F"



Test the version of anvil-uplink or run : pip install anvil-uplink



Copy and paste this code into the top of your python program:



import anvil.server  anvil.server.connect("server_JTC5YBCKEFJNKXLMOLXV3TNO-TUYORZGLGKI2HE4F")



You can now use the uplink locally



https://anvil.works/docs/uplink

## Setup Configurations

### Prerequisites

1. An Anvil account with an active application
2. Python 3.7 or higher installed locally
3. Anvil Uplink package installed: `pip install anvil-uplink`

### Environment Configuration

Set your Uplink key as an environment variable:

**Windows (PowerShell):**
```powershell
$env:ANVIL_UPLINK_KEY = "your-uplink-key-here"
```

**Linux/macOS:**
```bash
export ANVIL_UPLINK_KEY="your-uplink-key-here"
```

**Important:** Never hardcode your Uplink key in scripts. Always use environment variables.

### Required Files

The following scripts are provided in your project:
- `scripts/uplink_connect.py` - Simple connection script
- `scripts/test_uplink.py` - Connection testing script
- `scripts/uplink.py` - Persistent connection script

## How to Start Uplink

### Method 1: Simple Connection

Run the simple connection script:
```bash
python scripts/uplink_connect.py
```

This will:
1. Connect to Anvil using your UPLINK_KEY environment variable
2. Display a success message
3. Wait for you to press Enter to disconnect

### Method 2: Persistent Connection

For long-running operations, use the persistent connection:
```bash
python scripts/uplink.py
```

This script:
1. Connects to Anvil
2. Registers a test function
3. Waits indefinitely for calls

### Method 3: Programmatic Connection

In your own scripts, use:
```python
import anvil.server
import os

uplink_key = os.environ.get('ANVIL_UPLINK_KEY')
anvil.server.connect(uplink_key)
# Your code here
anvil.server.disconnect()
```

## How to Use Uplink

### Calling Server Functions

Once connected, you can call server functions defined in your Anvil app:
```python
result = anvil.server.call('your_server_function', arg1, arg2)
```

### Registering Functions

Register functions that can be called from your Anvil app:
```python
@anvil.server.callable
def my_function(arg1, arg2):
    # Process data
    return result
```

### Working with Data Tables

Access Data Tables through server functions only:
```python
# In your Anvil app server module:
@anvil.server.callable
def get_contacts():
    return app_tables.contacts.search()

# In your Uplink script:
contacts = anvil.server.call('get_contacts')
```

## How to Run Tests

### Test Connection

Run the provided test script:
```bash
python scripts/test_uplink.py
```

This script will:
1. Connect to Anvil using your UPLINK_KEY
2. Call the `test_uplink_connection` server function
3. Display the results
4. Disconnect cleanly

### Manual Testing

You can also manually test your connection:
```python
import anvil.server
import os

uplink_key = os.environ.get('ANVIL_UPLINK_KEY')
anvil.server.connect(uplink_key)

try:
    result = anvil.server.call('test_uplink_connection')
    print(f"Test result: {result}")
finally:
    anvil.server.disconnect()
```

### Testing Your Own Functions

Create a test script for your functions:
```python
import anvil.server
import os

uplink_key = os.environ.get('ANVIL_UPLINK_KEY')
anvil.server.connect(uplink_key)

try:
    # Test your functions here
    result = anvil.server.call('your_function_name', test_args)
    print(f"Function result: {result}")
    
    # Verify results
    assert result == expected_value
    print("✅ Test passed")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    
finally:
    anvil.server.disconnect()
```

## Best Practices

1. **Always disconnect** after your operations complete
2. **Use environment variables** for your Uplink key
3. **Handle exceptions** properly to avoid hanging connections
4. **Test functions** before using them in production
5. **Log operations** for debugging and audit purposes

## Troubleshooting

### Common Issues

1. **"ANVIL_UPLINK_KEY environment variable not set"**
   - Solution: Set the environment variable as described in Setup Configurations

2. **Connection timeouts**
   - Solution: Check your internet connection and firewall settings

3. **Authentication errors**
   - Solution: Verify your Uplink key in the Anvil dashboard

### Debugging Tips

1. Add verbose logging to see connection details:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. Test with the simplest possible script first:
   ```python
   import anvil.server
   import os
   
   anvil.server.connect(os.environ.get('ANVIL_UPLINK_KEY'))
   print("Connected!")
   anvil.server.disconnect()
   ```

## Security Considerations

1. **Never commit Uplink keys** to version control
2. **Rotate keys regularly** through the Anvil dashboard
3. **Use least-privilege principles** - only expose necessary functions
4. **Monitor connection logs** for unauthorized access

