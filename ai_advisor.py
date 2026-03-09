# =============================================================================
# ai_advisor.py
#
# Author  : Jose M. Beato
# Created : March 9, 2026
# Built with the assistance of Claude (Anthropic) — claude.ai
#
# Description:
#   Queries the net-inventory-db SQLite database for offline devices,
#   generates AI-powered troubleshooting playbooks via the Gemini API,
#   and persists the recommendations back to the database. Each offline
#   device receives exactly 3 actionable recovery steps.
#
# Dependencies:
#   pip install google-generativeai python-decouple
#
# Environment Variables (.env file required):
#   GEMINI_API_KEY=your_key_here
#
# Project Setup (run in terminal before opening VS Code):
# ─────────────────────────────────────────────────────
#   1. cd /Users/jmb/PythonProjects
#   2. uv init ai-network-advisor
#   3. cd ai-network-advisor
#   4. code .
#   5. python3 -m venv .venv
#   6. source .venv/bin/activate
#   7. pip install google-generativeai python-decouple
#   # Create this file as: ai_advisor.py
#
# GitHub Commit (after completing):
# ──────────────────────────────────
#   git add ai_advisor.py
#   git commit -m "refactor: standardize ai_advisor.py header and structure"
#   git push origin main
# =============================================================================

import sqlite3           # Built-in: database access
from pathlib import Path # Built-in: cross-platform file paths
from google import genai # Third-party: Gemini AI API client
from decouple import config  # Third-party: load secrets from .env


# =============================================================================
# SECTION 1 — CONFIGURATION
# Best Practice: Never hardcode API keys or file paths. Load secrets from
# a .env file using python-decouple so they're never committed to GitHub.
# =============================================================================

DB_PATH = Path(__file__).parent.parent / "net-inventory-db" / "inventory.db"

# Best Practice: config() reads from .env — the API key is never in code.
client = genai.Client(api_key=config("GEMINI_API_KEY"))


# =============================================================================
# SECTION 2 — AI ADVICE GENERATION
# Best Practice: Separate the AI call from the database write. If the API
# changes, you only update this function. If the DB schema changes, you
# only update save_advice_to_db().
# =============================================================================


def get_ai_advice(hostname, model, status):
    """
    Calls the Gemini API to generate a 3-step troubleshooting playbook
    for an offline network device.

    Args:
        hostname (str): Device hostname (e.g., "NY-CORE-01").
        model    (str): Hardware model (e.g., "Cisco Nexus").
        status   (str): Current device status (e.g., "OFFLINE").

    Returns:
        str: AI-generated troubleshooting steps as plain text.
    """
    prompt = (
        f"You are a network engineer assistant.\n"
        f"A {model} device named '{hostname}' is currently {status}.\n"
        f"Provide exactly 3 concise troubleshooting steps to recover it."
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text


# =============================================================================
# SECTION 3 — DATABASE PERSISTENCE
# Best Practice: Always use parameterized queries (?) to prevent SQL injection.
# Wrap DB operations in try/except to handle connection and schema errors.
# =============================================================================


def save_advice_to_db(hostname, advice):
    """
    Persists the AI-generated troubleshooting recommendation to the database
    and updates the device status to NEEDS_REPAIR.

    Args:
        hostname (str): Device hostname to update.
        advice   (str): AI-generated troubleshooting text.

    Raises:
        sqlite3.Error: Re-raises database errors after logging them.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                """
                UPDATE devices
                SET ai_recommendation = ?, status = 'NEEDS_REPAIR'
                WHERE hostname = ?
                """,
                (advice, hostname),
            )
            conn.commit()
        print(f"[INFO] AI recommendation for '{hostname}' saved to database.")
    except sqlite3.Error as e:
        print(f"[ERROR] DB write failed for '{hostname}': {e}")
        raise


# =============================================================================
# SECTION 4 — SUMMARY PRINT
# Best Practice: Always print a human-readable summary to the console
# so you know what happened when you run the script.
# =============================================================================


def print_summary(processed, skipped):
    """
    Prints a formatted run summary to the console.

    Args:
        processed (int): Number of devices that received AI advice.
        skipped   (int): Number of devices skipped (none found or errors).
    """
    print()
    print("=" * 60)
    print("  AI NETWORK ADVISOR — SUMMARY REPORT")
    print("  Jose M. Beato | March 9, 2026")
    print("=" * 60)
    print(f"  Devices analyzed  : {processed}")
    print(f"  Devices skipped   : {skipped}")
    print(f"  Database          : {DB_PATH}")
    print("=" * 60)
    print()


# =============================================================================
# SECTION 5 — MAIN ENTRY POINT
# Best Practice: Always use `if __name__ == "__main__"` to protect your
# main logic. This allows other scripts to import get_ai_advice() without
# automatically running the whole pipeline.
# =============================================================================


def main():
    """
    Orchestrates the full pipeline:
    Query Offline Devices → Generate AI Advice → Save to DB → Print Summary
    """
    print()
    print("=" * 60)
    print("  ai_advisor.py — Starting...")
    print("=" * 60)
    print()

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT hostname, model, status FROM devices WHERE status = 'OFFLINE'"
        ).fetchall()

    if not rows:
        print("[INFO] No offline devices found. All systems green.")
        print_summary(0, 0)
        return

    processed = 0
    for device in rows:
        hostname = device["hostname"]
        print(f"[INFO] Analyzing '{hostname}' with AI advisor...")
        advice = get_ai_advice(hostname, device["model"], device["status"])
        save_advice_to_db(hostname, advice)
        processed += 1

    print_summary(processed, 0)


if __name__ == "__main__":
    main()

