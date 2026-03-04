import sqlite3


def migrate_db():
    conn = sqlite3.connect("../net-inventory-db/inventory.db")  # Path to your Day 11 DB
    cursor = conn.cursor()
    try:
        # Adding a new column to an existing table
        cursor.execute("ALTER TABLE devices ADD COLUMN ai_recommendation TEXT")
        conn.commit()
        print("✅ Database migrated: added 'ai_recommendation' column.")
    except sqlite3.OperationalError:
        print("ℹ️  Column already exists, skipping migration.")
    finally:
        conn.close()


migrate_db()
