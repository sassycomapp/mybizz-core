"""
Uplink Test Data Cleanup

Deletes all rows marked with sentinel value source='Test' or email prefix 'TEST_'.
Runs children before parents to avoid foreign key errors.
Always verify with DRY_RUN = True before committing a live deletion.

Usage:
    python scripts/uplink_cleanup.py

Configuration:
    Set DRY_RUN = False to perform actual deletion.
    Populate TABLE_DELETION_ORDER with actual Mybizz table names
    in child-before-parent order before running.
"""

import anvil.server
from anvil.tables import app_tables
import os
import sys

# =====================================================================
# CONFIGURATION
# =====================================================================

DRY_RUN = True  # Set to False to perform actual deletion

# Tables to clean in child-before-parent order.
# Populate with actual table names before running.
TABLE_DELETION_ORDER = [
    "tbl_audit_log",
    "tbl_rate_limits",
    "users",
]

# =====================================================================


def main():
    key = os.environ.get("ANVIL_UPLINK_KEY")
    if not key:
        print("ERROR: ANVIL_UPLINK_KEY not set — see ref_anvil_uplink.md §4")
        sys.exit(1)
    if not key.startswith("server_"):
        print("ERROR: ANVIL_UPLINK_KEY is not a Server Uplink key — see ref_anvil_uplink.md §2")
        sys.exit(1)

    if DRY_RUN:
        print("DRY RUN — no data will be deleted. Set DRY_RUN = False to commit deletion.")

    anvil.server.connect(key)
    try:
        total_deleted = 0

        for table_name in TABLE_DELETION_ORDER:
            try:
                table = getattr(app_tables, table_name)
            except AttributeError:
                print(f"  SKIP: {table_name} — table not found in schema")
                continue

            # Find sentinel rows
            rows_to_delete = []
            try:
                for row in table.search():
                    email = row['email'] if 'email' in row.keys() else None
                    source = row['source'] if 'source' in row.keys() else None
                    if (email and str(email).startswith("TEST_")) or source == "Test":
                        rows_to_delete.append(row)
            except Exception as e:
                print(f"  ERROR scanning {table_name}: {e}")
                continue

            print(f"  {table_name}: {len(rows_to_delete)} sentinel rows found")

            if not DRY_RUN:
                for row in rows_to_delete:
                    row.delete()
                    total_deleted += 1
                print(f"  {table_name}: {len(rows_to_delete)} rows deleted")

        if DRY_RUN:
            print("\nDry run complete. Review output above then set DRY_RUN = False to delete.")
        else:
            print(f"\nCleanup complete. {total_deleted} rows deleted.")

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    finally:
        anvil.server.disconnect()


if __name__ == "__main__":
    main()
