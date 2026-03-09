# =============================================================================
# ai_recommendation.py
#
# Author  : Jose M. Beato
# Created : March 9, 2026
# Built with the assistance of Claude (Anthropic) — claude.ai
#
# Description:
#   One-time database migration script. Adds the 'ai_recommendation' column
#   to the devices table in net-inventory-db. Safe to run multiple times —
#   skips silently if the column already exists.
#
#   Run this once before running ai_advisor.py for the first time.
#
# Project Setup (run in terminal before opening VS Code):
# ─────────────────────────────────────────────────────
#   1. cd /Users/jmb/PythonProjects
#   2. cd ai-network-advisor  (already initialized)
#   3. source .venv/bin/activate
#   # No extra packages — 100% Python standard library
#   # Create this file as: ai_recommendation.py
#
# GitHub Commit (after completing):
# ──────────────────────────────────
#   git add ai_recommendation.py
#   git commit -m "refactor: standardize ai_recommendation.py header and structure"
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
# SECTION 2 — MIGRATION LOGIC
# Best Practice: Schema migrations should be idempotent — safe to run
# more than once. Catching OperationalError on ALTER TABLE is the standard
# SQLite pattern for "add column if not exists".
# =============================================================================


def migrate_db():
    """
    Adds the 'ai_recommendation' TEXT column to the devices table.
    Skips silently if the column already exists.

    Best Practice: Always wrap schema changes in try/except so migration
    scripts can be re-run without causing errors.
    """
    with sqlite3.connect(DB_PATH) as conn:
        try:
            conn.execute("ALTER TABLE devices ADD COLUMN ai_recommendation TEXT")
            conn.commit()
            print("[INFO] Migration complete — 'ai_recommendation' column added.")
        except sqlite3.OperationalError:
            print("[INFO] Column 'ai_recommendation' already exists — skipping migration.")


# =============================================================================
# SECTION 3 — SUMMARY PRINT
# Best Practice: Always print a human-readable summary so you know what
# happened without opening the database file.
# =============================================================================


def print_summary():
    """
    Prints a formatted migration summary to the console.
    """
    print()
    print("=" * 60)
    print("  AI RECOMMENDATION MIGRATION — COMPLETE")
    print("  Jose M. Beato | March 9, 2026")
    print("=" * 60)
    print(f"  Database : {DB_PATH}")
    print(f"  Column   : ai_recommendation (TEXT)")
    print(f"  Status   : Ready for ai_advisor.py")
    print("=" * 60)
    print()


# =============================================================================
# SECTION 4 — MAIN ENTRY POINT
# Best Practice: Always use `if __name__ == "__main__"` to protect your
# main logic. This allows other scripts to import migrate_db() without
# automatically running the migration.
# =============================================================================


def main():
    """
    Runs the database migration and prints a summary.
    """
    print()
    print("=" * 60)
    print("  ai_recommendation.py — Starting...")
    print("=" * 60)
    print()

    migrate_db()
    print_summary()


if __name__ == "__main__":
    main()

