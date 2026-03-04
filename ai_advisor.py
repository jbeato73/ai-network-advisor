import sqlite3
from google import genai
from decouple import config

client = genai.Client(api_key=config("GEMINI_API_KEY"))


def save_advice_to_db(hostname, advice):
    """Saves the AI troubleshooting report into the SQL database."""
    try:
        conn = sqlite3.connect("../net-inventory-db/inventory.db")
        cursor = conn.cursor()

        # Updating the record based on hostname
        cursor.execute(
            """
            UPDATE devices 
            SET ai_recommendation = ?, status = 'NEEDS_REPAIR'
            WHERE hostname = ?
        """,
            (advice, hostname),
        )

        conn.commit()
        conn.close()
        print(f"💾 AI report for {hostname} persisted to database.")
    except Exception as e:
        print(f"🚨 DB Save Failed: {e}")


def main():
    device = {"name": "LON-BDR-02", "model": "Juniper MX", "status": "OFFLINE"}

    print(f"🤖 AI Advisor is analyzing {device['name']}...")

    # 1. Get AI Advice (from your previous working function)
    # response = client.models.generate_content(...)
    # advice = response.text
    advice = "1. Check SFP. 2. Verify VLAN. 3. Reload config."  # Simulated for example

    # 2. SAVE IT
    save_advice_to_db(device["name"], advice)


if __name__ == "__main__":
    main()
