"""
Uplink Context Manager

Reusable context manager for clean connect/disconnect.
Import uplink_session from this into any script that needs it.

Usage:
    from scripts.uplink_context import uplink_session

    with uplink_session():
        result = anvil.server.call("some_function")
"""

import anvil.server
import os
from contextlib import contextmanager


@contextmanager
def uplink_session():
    key = os.environ.get("ANVIL_UPLINK_KEY")
    if not key:
        raise RuntimeError("ANVIL_UPLINK_KEY not set — see ref_anvil_uplink.md §4")
    if not key.startswith("server_"):
        raise RuntimeError("ANVIL_UPLINK_KEY is not a Server Uplink key — see ref_anvil_uplink.md §2")
    anvil.server.connect(key)
    try:
        yield
    finally:
        anvil.server.disconnect()
