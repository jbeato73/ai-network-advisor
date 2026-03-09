import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "net-inventory-db" / "inventory.db"


def show_pending_repairs():
    with sqlite3.connect(DB_PATH) as conn:
        results = conn.execute(
            """
            SELECT hostname, ip_address, ai_recommendation
            FROM devices
            WHERE status = 'NEEDS_REPAIR' AND ai_recommendation IS NOT NULL
            """
        ).fetchall()

    if not results:
        print("☕ No pending AI reports. All systems green!")
    else:
        print(f"\n🚨 FOUND {len(results)} DEVICES REQUIRING ATTENTION:")
        print("=" * 60)
        for hostname, ip_address, advice in results:
            print(f"DEVICE: {hostname} ({ip_address})")
            print(f"AI ADVICE: {advice}")
            print("-" * 60)


if __name__ == "__main__":
    show_pending_repairs()
