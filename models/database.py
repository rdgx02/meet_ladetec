import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../database/bookings.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            sector TEXT NOT NULL,
            room TEXT NOT NULL,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            duration INTEGER NOT NULL,
            ticket TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_booking(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings (name, phone, sector, room, date, start_time, duration, ticket)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['name'], data['phone'], data['sector'], data['room'], data['date'], data['startTime'], data['duration'], data['ticket']))
    conn.commit()
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

def get_all_bookings():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings')
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_booking(booking_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM bookings WHERE id = ?', (booking_id,))
    conn.commit()
    conn.close()
