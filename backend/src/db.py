import datetime
import json
import sqlite3
from pathlib import Path

# Use a relative path from the script location so it stays in backend folder
DB_PATH = Path(__file__).parent.parent / "agent_data.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            language_preference TEXT,
            facts TEXT,
            last_interaction TIMESTAMP
        )
    """
    )
    conn.commit()
    conn.close()


def save_caller(name: str, facts: dict, language_preference: str = "English"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    user_id = name.lower().strip()
    facts_str = json.dumps(facts)
    now = datetime.datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO users (user_id, name, language_preference, facts, last_interaction)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            facts=excluded.facts,
            language_preference=excluded.language_preference,
            last_interaction=excluded.last_interaction
        """,
        (user_id, name, language_preference, facts_str, now),
    )
    conn.commit()
    conn.close()


def lookup_caller(name: str) -> dict | None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    user_id = name.lower().strip()

    cursor.execute(
        "SELECT name, language_preference, facts, last_interaction FROM users WHERE user_id = ?",
        (user_id,),
    )
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "name": row[0],
            "language_preference": row[1],
            "facts": json.loads(row[2]) if row[2] else {},
            "last_interaction": row[3],
        }
    return None


def forget_caller(name: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    user_id = name.lower().strip()

    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted
