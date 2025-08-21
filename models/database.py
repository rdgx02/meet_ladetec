import sqlite3
import os
from datetime import datetime

# Caminho do banco de dados
DB_PATH = os.path.join(os.path.dirname(__file__), '../database/bookings.db')

# Inicializa banco e tabelas
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabela de agendamentos
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

# Insere agendamento
def insert_booking(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings (name, phone, sector, room, date, start_time, duration, ticket)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['name'],
        data['phone'],
        data['sector'],
        data['room'],
        data['date'],
        data['startTime'],
        data['duration'],
        data['ticket']
    ))
    conn.commit()
    inserted_id = cursor.lastrowid
    conn.close()
    return inserted_id

# Retorna todos os agendamentos
def get_all_bookings():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Deleta agendamento e retorna dados para log
def delete_booking(booking_id, user=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # permite acessar como dicionário
    cursor = conn.cursor()

    # Obter dados do agendamento antes de deletar
    cursor.execute('SELECT * FROM bookings WHERE id = ?', (booking_id,))
    booking = cursor.fetchone()

    if not booking:
        conn.close()
        return None  # nada para deletar

    # Deletar agendamento
    cursor.execute('DELETE FROM bookings WHERE id = ?', (booking_id,))
    conn.commit()
    conn.close()

    # Retorna os dados do agendamento como dicionário
    return dict(booking)
