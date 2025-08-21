import sqlite3
from pathlib import Path
import json

DB_PATH = Path(__file__).resolve().parents[1] / "database" / "bookings.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_logs_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            user_name TEXT,
            action TEXT NOT NULL,
            entity TEXT,
            entity_id TEXT,
            details TEXT,
            ip TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    conn.commit()
    conn.close()

def log_action(user_id, action, entity=None, entity_id=None, details=None, ip=None, user_name=None):
    if details is not None and not isinstance(details, str):
        details = json.dumps(details, ensure_ascii=False)

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO audit_logs (user_id, user_name, action, entity, entity_id, details, ip)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, user_name, action, entity, entity_id, details, ip))
    conn.commit()
    conn.close()

def get_all_logs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        l.id,
        l.action,
        l.entity,
        l.entity_id,
        l.details,
        l.created_at AS timestamp,
        l.ip,
        COALESCE(l.user_name, u.name) AS user_name
    FROM audit_logs l
    LEFT JOIN users u ON l.user_id = u.id
    WHERE l.action != 'login_success'
    ORDER BY l.created_at DESC
""")

    rows = cursor.fetchall()
    conn.close()

    logs = []
    for r in rows:
        logs.append({
            "id": r[0],
            "action": r[1],
            "entity": r[2],
            "entity_id": r[3],
            "details": r[4],
            "timestamp": r[5],
            "ip": r[6],
            "user_name": r[7] or "Desconhecido"
        })
    return logs

