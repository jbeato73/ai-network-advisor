import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "net-inventory-db" / "inventory.db"


def migrate_db():
    with sqlite3.connect(DB_PATH) as conn:
        try:
            conn.execute("ALTER TABLE devices ADD COLUMN ai_recommendation TEXT")
            conn.commit()
            print("✅ Database migrated: added 'ai_recommendation' column.")
        except sqlite3.OperationalError:
            print("ℹ️  Column already exists, skipping migration.")


if __name__ == "__main__":
    migrate_db()
