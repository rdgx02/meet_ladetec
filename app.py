from flask import Flask, request, jsonify, send_from_directory, render_template, session, redirect
from flask_cors import CORS
from models.database import init_db, insert_booking, get_all_bookings, delete_booking
import random
import string
import os
import requests
from datetime import timedelta

# 📌 IMPORTS ADICIONADOS PARA USUÁRIOS E LOGS
from models.users import create_users_table, seed_admins, get_user_by_username, verify_password
from models.logs import create_logs_table, get_all_logs, log_action

app = Flask(__name__, static_folder='static')
CORS(app)

app.secret_key = 'chave_super_segura_ladetec_2025'

# 🔐 Sessão persistente (7 dias)
app.permanent_session_lifetime = timedelta(days=7)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False  # coloque True se estiver servindo via HTTPS
)

# Helpers para identificar usuário logado
def current_actor_id():
    return session.get("user_id")

def current_actor_name():
    return session.get("user_name") or "PUBLICO"

# Inicializa banco e tabelas
init_db()
create_users_table()
create_logs_table()
seed_admins()

# Webhook n8n
N8N_WEBHOOK_URL = "https://n8n.ladetec.iq.ufrj.br/webhook/meet-cati"
API_KEY = "F25F310E71F6-4DAC-9615-16C76098B303"

def enviar_para_n8n(dados):
    try:
        print("📤 Enviando os seguintes dados para o n8n:")
        print(dados)

        headers = {"apikey": API_KEY}
        resposta = requests.post(N8N_WEBHOOK_URL, json=dados, headers=headers)

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

# ====== LOGIN/LOGOUT E SESSÃO ======
@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json(force=True)
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    user = get_user_by_username(username)
    if not user:
        log_action(
            None, "login_fail",
            entity="user",
            entity_id=username,
            details={"reason": "not_found"},
            ip=ip,
            user_name=username
        )
        return jsonify({"ok": False, "message": "Usuário ou senha inválidos."}), 401

    if not verify_password(password, user["password_hash"]):
        log_action(
            user["id"], "login_fail",
            entity="user",
            entity_id=username,
            details={"reason": "wrong_password"},
            ip=ip,
            user_name=user["name"]
        )
        return jsonify({"ok": False, "message": "Usuário ou senha inválidos."}), 401

    # Sucesso
    session.permanent = True
    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    session["role"] = user["role"]
    log_action(
        user["id"], "login_success",
        entity="user",
        entity_id=username,
        ip=ip,
        user_name=user["name"]
    )

    return jsonify({
        "ok": True,
        "name": user["name"],
        "role": user["role"]
    })

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    session.pop("user_id", None)
    session.pop("user_name", None)
    session.pop("role", None)
    return jsonify({"ok": True})

@app.route('/auth/me', methods=['GET'])
def auth_me():
    if 'user_id' in session:
        return jsonify({
            "ok": True,
            "id": session['user_id'],
            "name": session.get('user_name'),
            "role": session.get('role')
        })
    return jsonify({"ok": False}), 401

# ====== ENTRADA DO ADMIN (decide login/painel) ======
@app.route('/admin')
def admin_entry():
    """
    Se logado: serve o painel (static/admin.html)
    Se não logado: mostra tela de login (static/admin_login.html)
    """
    if 'user_id' in session:
        return send_from_directory('static', 'admin.html')
    return send_from_directory('static', 'admin_login.html')

# Compatibilidade para quem acessar /admin.html direto
@app.route('/admin.html')
def admin_html_direct():
    if 'user_id' not in session:
        return redirect('/admin')
    return send_from_directory('static', 'admin.html')

# ====== API DE AGENDAMENTOS ======
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

    # Corrigido: salvar com campo 'start_time' correto
    start_time = data.get('startTime')
    if not start_time:
        return jsonify({'error': 'Campo startTime é obrigatório'}), 400
    data['start_time'] = start_time
    data['duration'] = int(data.get('duration', 30))

    # Correção importante: o insert_booking espera 'start_time', não 'startTime'
    booking_id = insert_booking(data)

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

    try:
        log_action(
            user_id=current_actor_id(),
            action="booking_created",
            entity="booking",
            entity_id=str(booking_id),
            details={
                "nome": data['name'],
                "telefone": data['phone'],
                "setor": data['sector'],
                "sala": data['room'],
                "data": data['date'],
                "inicio": data['start_time'],
                "fim": fim,
                "ticket": ticket
            },
            ip=request.headers.get("X-Forwarded-For", request.remote_addr),
            user_name=current_actor_name()
        )
    except Exception as e:
        print("⚠️ Falha ao registrar log booking_created:", e)

    return jsonify({
        **data,
        'id': booking_id,
        'start_time': data['start_time'],
        'ticket': ticket
    })

@app.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
def remove_booking(booking_id):
    user_id = session.get("user_id")
    user_name = session.get("user_name", "admin")

    booking = delete_booking(booking_id, user=user_name)

    if booking:
        log_action(
            user_id=user_id,
            action="booking_deleted",
            entity="booking",
            entity_id=str(booking_id),
            details={
                "nome": booking["name"],
                "setor": booking["sector"],
                "sala": booking["room"],
                "data": booking["date"],
                "inicio": booking["start_time"],
                "ticket": booking["ticket"]
            },
            ip=request.remote_addr,
            user_name=user_name
        )

    return '', 204

# ====== API DE LOGS ======
@app.route('/api/logs', methods=['GET'])
def get_logs():
    logs = get_all_logs()
    logs = [l for l in logs if str(l.get("action", "")).lower() != "login_success"]
    return jsonify(logs)

# ✅ Rodar na rede para acesso via celular (Wi-Fi)
if __name__ == '__main__':
    print(">> Rodando app.py de:", os.path.abspath(__file__))
    app.run(host='0.0.0.0', port=5000, debug=True)
