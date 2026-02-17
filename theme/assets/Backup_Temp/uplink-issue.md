# Uplink Issue Report

## Summary
We can establish an Anvil Uplink connection successfully, but any attempt to call a server function from the Uplink script fails with the error:

```
Too many nested anvil.server.call()s
```

This indicates the server function call is being executed while already in an Anvil server call context, which should not happen for a simple test function.

## Environment & Context
- **App:** Mybizz_core_v1_2_dev
- **Environment:** Default Environment (per uplink connect log)
- **Uplink key used:** `server_JTC5YBCKEFJNKXLMOLXV3TNO-TUYORZGLGKI2HE4F`
- **Uplink library:** `anvil-uplink 0.6.0`
- **OS/Terminal:** Windows PowerShell

## Steps Taken
1. **Uplink connection confirmed** (connect succeeds).
2. **Test call fails** with nested call error.
3. **Server test function verified** (simple callable returning a dict; no nested calls).
4. **App restarted** to ensure fresh runtime.
5. **Test script updated** to call a new function name (`test_uplink_connection_v2`).
6. **Failure persisted** with the same error.

## Logs (Example)
```
Connecting to wss://anvil.works/uplink
Anvil websocket open
Connected to "Default Environment" as SERVER
Connecting to Anvil via Uplink...
Connected to Anvil

Calling test_uplink_connection_v2()...

Test failed: Too many nested anvil.server.call()s

Disconnecting...
Disconnected
```

## Expected Behavior
Calling a simple server function from the Uplink should return a dict response such as:

```python
{
  "status": "success",
  "message": "Uplink connection is working!",
  "timestamp": "2026-02-17T16:45:00",
  "server_module": "server_shared.utilities"
}
```

## Observed Behavior
- The function call fails immediately with:
  - `Too many nested anvil.server.call()s`

## Possible Causes (Hypotheses)
1. **Environment mismatch**
   - The Uplink key might be tied to a different environment (e.g., Production), while the server function was edited in Default.
   - Evidence: connect log shows "Default Environment", but function behavior doesn’t match local code.

2. **Name collision in another server module**
   - Another server module in the live app might define a function with the same name that *does* contain nested calls.
   - This could be hidden if the module is not in this repo or is from a previous version.

3. **Server call triggered on import/startup**
   - If a server module executes `anvil.server.call()` on import or during startup, then any subsequent call could be considered nested.
   - This could happen in a server module not shown in the repo or in the live app environment.

4. **Incorrect key type / invalid key state**
   - The Uplink key might be stale or mis-associated despite connecting.
   - The Anvil runtime could accept the connection but behave inconsistently when calling server functions.

## Diagnostic Examples to Narrow Down
**Example A: Unique function name**
```python
@anvil.server.callable
def uplink_smoketest_20260217():
    return {"status": "success"}
```
If this still fails, it strongly suggests environment mismatch or startup nested call issue.

**Example B: Call a minimal function from a brand-new module**
Create a new server module and define only a single callable returning a static dict. If that fails, the issue is likely environmental or runtime-related, not code-related.

## Recommended Next Steps
1. **Confirm environment alignment**
   - Ensure the Server Uplink key is generated from the **same environment** where the function was updated.

2. **Create a uniquely named test function**
   - Use a new function name with a unique suffix (date/time) to avoid collisions.

3. **Check for startup or import-time server calls**
   - Review any server modules that might run code at import time in the live Anvil app.

4. **Regenerate the Uplink key**
   - Generate a new Server Uplink key from the correct environment and retest.

## Files Touched Locally
- `scripts/test_uplink.py` (updated to remove emoji output and changed test function name during diagnostics)

## Note
This issue persists even after updating the server function and restarting the app, which indicates the problem is likely environmental or runtime-related rather than purely local code changes.
