import sqlite3


def show_pending_repairs():
    # Connect to your Day 11 database
    conn = sqlite3.connect("../net-inventory-db/inventory.db")
    cursor = conn.cursor()

    # 1. Execute the filter query
    query = """
    SELECT hostname, ip_address, ai_recommendation 
    FROM devices 
    WHERE ai_recommendation IS NOT NULL
    """

    cursor.execute(query)
    results = cursor.fetchall()

    if not results:
        print("☕ No pending AI reports. All systems green!")
    else:
        print(f"\n🚨 FOUND {len(results)} DEVICES REQUIRING ATTENTION:")
        print("=" * 60)
        for row in results:
            print(f"DEVICE: {row[0]} ({row[1]})")
            print(f"AI ADVICE: {row[2]}")
            print("-" * 60)

    conn.close()


if __name__ == "__main__":
    show_pending_repairs()
