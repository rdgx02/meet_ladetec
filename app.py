from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from models.database import init_db, insert_booking, get_all_bookings, delete_booking
import random
import string
import os
import requests

app = Flask(__name__, static_folder='static')
CORS(app)

# Inicializa o banco de dados
init_db()

# URL do webhook do n8n
N8N_WEBHOOK_URL = "https://n8n.ladetec.iq.ufrj.br/webhook/confirmar-agendamento"
API_KEY = "326E97B23199-47C5-9AB4-69B2B9B9C71A"

def enviar_para_n8n(dados):
    try:
        print("📤 Enviando os seguintes dados para o n8n:")
        print(dados)

        headers = {
            "apikey": API_KEY
        }

        resposta = requests.post(
            N8N_WEBHOOK_URL,
            json=dados,
            headers=headers
        )

        print("🔄 Status Code:", resposta.status_code)
        print("🔄 Resposta:", resposta.text)

        if resposta.status_code != 200:
            print("❌ Erro ao enviar para o n8n:", resposta.status_code, resposta.text)
        else:
            print("✅ Confirmação enviada com sucesso ao n8n.")
    except Exception as e:
        print("❌ Erro inesperado ao enviar para n8n:", e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    rows = get_all_bookings()
    bookings = []
    for r in rows:
        bookings.append({
            'id': r[0],
            'name': r[1],
            'phone': r[2],
            'sector': r[3],
            'room': r[4],
            'date': r[5],
            'start_time': r[6],
            'duration': r[7],
            'ticket': r[8]
        })
    return jsonify(bookings)

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    ticket = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    data['ticket'] = ticket

    # Corrige chave para compatibilidade com banco
    start_time = data.get('startTime')
    if not start_time:
        return jsonify({'error': 'Campo startTime é obrigatório'}), 400
    data['start_time'] = start_time

    # Garante que 'duration' seja um número inteiro
    data['duration'] = int(data.get('duration', 30))

    booking_id = insert_booking(data)

        # Calcula horário final com base em start_time e duration
    def calcular_fim(start_time, duration):
        hora, minuto = map(int, start_time.split(':'))
        total_minutos = hora * 60 + minuto + duration
        fim_hora = total_minutos // 60
        fim_minuto = total_minutos % 60
        return f"{fim_hora}:{str(fim_minuto).zfill(2)}"

    fim = calcular_fim(data['start_time'], data['duration'])

    enviar_para_n8n({
        'nome': data['name'],
        'telefone': data['phone'],
        'setor': data['sector'],
        'sala': data['room'],
        'data': data['date'],
        'inicio': data['start_time'],
        'fim': fim,
        'ticket': ticket
    })


    return jsonify({
        **data,
        'id': booking_id,
        'start_time': data['start_time'],
        'ticket': ticket
    })

@app.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
def remove_booking(booking_id):
    delete_booking(booking_id)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
