import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = Path(__file__).resolve().parents[1] / "database" / "bookings.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_users_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'admin',
            is_active INTEGER NOT NULL DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

def seed_admins():
    admins = [
        ("Vinícius", "vinicius", "ladetec123"),
        ("Edimar", "edimar", "ladetec123"),
        ("Ana Maria", "anamaria", "ladetec123"),
        ("Maíra", "maira", "ladetec123"),
    ]
    conn = get_conn()
    cur = conn.cursor()
    for name, username, raw_pw in admins:
        cur.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        if not cur.fetchone():
            cur.execute("""
                INSERT INTO users (name, username, password_hash, role, is_active)
                VALUES (?, ?, ?, 'admin', 1)
            """, (name, username, generate_password_hash(raw_pw)))
    conn.commit()
    conn.close()

def get_user_by_username(username: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ? AND is_active = 1", (username,))
    row = cur.fetchone()
    conn.close()
    return row

def verify_password(password: str, hash_: str) -> bool:
    return check_password_hash(hash_, password)
