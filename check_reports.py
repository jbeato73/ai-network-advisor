# =============================================================================
# check_reports.py
#
# Author  : Jose M. Beato
# Created : March 9, 2026
# Built with the assistance of Claude (Anthropic) — claude.ai
#
# Description:
#   Queries the net-inventory-db SQLite database and displays all devices
#   with a status of NEEDS_REPAIR that have an AI recommendation on file.
#   Run this after ai_advisor.py to review pending remediation items.
#
# Project Setup (run in terminal before opening VS Code):
# ─────────────────────────────────────────────────────
#   1. cd /Users/jmb/PythonProjects
#   2. cd ai-network-advisor  (already initialized)
#   3. source .venv/bin/activate
#   # No extra packages — 100% Python standard library
#   # Create this file as: check_reports.py
#
# GitHub Commit (after completing):
# ──────────────────────────────────
#   git add check_reports.py
#   git commit -m "refactor: standardize check_reports.py header and structure"
#   git push origin main
# =============================================================================

import sqlite3           # Built-in: SQLite database access
from pathlib import Path # Built-in: cross-platform file paths


# =============================================================================
# SECTION 1 — CONFIGURATION
# Best Practice: Define the DB path once at the top. If the repo structure
# changes, you update it in one place only.
# =============================================================================

DB_PATH = Path(__file__).parent.parent / "net-inventory-db" / "inventory.db"


# =============================================================================
# SECTION 2 — QUERY LOGIC
# Best Practice: Separate database queries from display logic.
# If the schema changes, only this function needs updating.
# =============================================================================


def get_pending_repairs():
    """
    Retrieves all devices with status NEEDS_REPAIR and a non-null AI
    recommendation from the inventory database.

    Returns:
        list[tuple]: Rows of (hostname, ip_address, ai_recommendation).
    """
    with sqlite3.connect(DB_PATH) as conn:
        results = conn.execute(
            """
            SELECT hostname, ip_address, ai_recommendation
            FROM devices
            WHERE status = 'NEEDS_REPAIR' AND ai_recommendation IS NOT NULL
            """
        ).fetchall()
    return results


# =============================================================================
# SECTION 3 — DISPLAY LOGIC
# Best Practice: Separate display from data retrieval. This function can
# be replaced with a web view or CSV export without touching the query.
# =============================================================================


def display_pending_repairs(results):
    """
    Prints all pending repair devices with their AI recommendations.

    Args:
        results (list[tuple]): Rows of (hostname, ip_address, ai_recommendation).
    """
    if not results:
        print("[INFO] No pending AI reports. All systems green.")
        return

    print()
    print("=" * 60)
    print(f"  PENDING REPAIRS — {len(results)} DEVICE(S) REQUIRING ATTENTION")
    print("  Jose M. Beato | March 9, 2026")
    print("=" * 60)

    for hostname, ip_address, advice in results:
        print(f"\n  Device : {hostname} ({ip_address})")
        print(f"  {'─' * 56}")
        print(f"  AI Advice:\n  {advice.strip()}")
        print(f"  {'─' * 56}")

    print()


# =============================================================================
# SECTION 4 — MAIN ENTRY POINT
# Best Practice: Always use `if __name__ == "__main__"` to protect your
# main logic. This allows other scripts to import get_pending_repairs()
# without automatically running the pipeline.
# =============================================================================


def main():
    """
    Orchestrates the full pipeline:
    Query DB → Display Pending Repairs
    """
    print()
    print("=" * 60)
    print("  check_reports.py — Starting...")
    print("=" * 60)
    print()

    results = get_pending_repairs()
    display_pending_repairs(results)


if __name__ == "__main__":
    main()

