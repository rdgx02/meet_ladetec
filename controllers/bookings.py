from flask import Blueprint, request, jsonify
from models.database import get_connection
from utils.helpers import generate_id, generate_ticket
from datetime import datetime

booking_routes = Blueprint('booking_routes', __name__)

@booking_routes.route('/api/bookings', methods=['GET'])
def list_bookings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings')
    rows = cursor.fetchall()
    conn.close()
    bookings = [dict(row) for row in rows]
    return jsonify(bookings)

@booking_routes.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.json

    booking = {
        'id': generate_id(),
        'name': data['name'],
        'phone': data['phone'],
        'sector': data['sector'],
        'room': data['room'],
        'date': data['date'],
        'start_time': data['startTime'],
        'duration': int(data['duration']),
        'ticket': generate_ticket(),
        'created_at': datetime.now().isoformat()
    }

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings (id, name, phone, sector, room, date, start_time, duration, ticket, created_at)
        VALUES (:id, :name, :phone, :sector, :room, :date, :start_time, :duration, :ticket, :created_at)
    ''', booking)
    conn.commit()
    conn.close()

    return jsonify(booking), 201

@booking_routes.route('/api/bookings/<booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM bookings WHERE id = ?', (booking_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})
