"""
Uplink Data Tables Access

Direct Data Tables access for data inspection and administrative tasks.
Configure the QUERY SECTION before running.

Usage:
    python scripts/uplink_data_tables.py
"""

import anvil.server
from anvil.tables import app_tables
import anvil.tables.query as q
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
        # =====================================================================
        # QUERY SECTION — add your query code here before running
        # Examples:
        #
        # rows = app_tables.users.search()
        # for row in rows:
        #     print(row['email'], row['role'])
        #
        # row = app_tables.users.get(email='test@example.com')
        # print(row)
        # =====================================================================

        print("Configure the QUERY SECTION in this script before running.")

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    finally:
        anvil.server.disconnect()


if __name__ == "__main__":
    main()
