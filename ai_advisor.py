import sqlite3
from pathlib import Path
from google import genai
from decouple import config

DB_PATH = Path(__file__).parent.parent / "net-inventory-db" / "inventory.db"

client = genai.Client(api_key=config("GEMINI_API_KEY"))


def save_advice_to_db(hostname, advice):
    """Saves the AI troubleshooting report into the SQL database."""
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
        print(f"💾 AI report for {hostname} persisted to database.")
    except sqlite3.Error as e:
        print(f"🚨 DB Save Failed: {e}")
        raise


def get_ai_advice(hostname, model, status):
    """Calls Gemini to generate a troubleshooting playbook for a device."""
    prompt = (
        f"You are a network engineer assistant.\n"
        f"A {model} device named '{hostname}' is currently {status}.\n"
        f"Provide exactly 3 concise troubleshooting steps to recover it."
    )
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
    )
    return response.text


def main():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT hostname, model, status FROM devices WHERE status = 'OFFLINE'"
        ).fetchall()

    if not rows:
        print("✅ No offline devices found.")
        return

    for device in rows:
        hostname = device["hostname"]
        print(f"🤖 AI Advisor is analyzing {hostname}...")
        advice = get_ai_advice(hostname, device["model"], device["status"])
        save_advice_to_db(hostname, advice)


if __name__ == "__main__":
    main()
