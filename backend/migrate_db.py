import sqlite3
import os

db_paths = ["guardianai.db", "backend/guardianai.db"]

for path in db_paths:
    if not os.path.exists(path):
        continue
    try:
        conn = sqlite3.connect(path)
        cursor = conn.cursor()

        # Get existing columns
        cursor.execute("PRAGMA table_info(users)")
        existing_cols = {row[1] for row in cursor.fetchall()}

        required_cols = [
            ("full_name", "VARCHAR(255)"),
            ("role", "VARCHAR(50) DEFAULT 'user'"),
            ("subscription_tier", "VARCHAR(32) DEFAULT 'free'"),
            ("is_active", "BOOLEAN DEFAULT 1"),
            ("is_verified", "BOOLEAN DEFAULT 0"),
            ("updated_at", "DATETIME"),
            ("deleted_at", "DATETIME"),
        ]

        for col_name, col_type in required_cols:
            if col_name not in existing_cols:
                try:
                    cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type};")
                    print(f"Added column {col_name} to {path}")
                except Exception as e:
                    print(f"Note on {col_name} for {path}: {e}")

        conn.commit()
        conn.close()
        print(f"Migration completed for {path}")
    except Exception as err:
        print(f"Error migrating {path}: {err}")
