🏢 Sistema de Agendamento de Salas - MEET LADETEC

Este é um sistema web para agendamento de salas no LADETEC, desenvolvido em Python (Flask) no backend e HTML + Tailwind + JavaScript no frontend.

O sistema permite que usuários realizem agendamentos, consultem, cancelem por ticket e que o administrador gerencie as reservas em um painel completo com login e sessão persistente.

🚀 Funcionalidades

✅ Agendamento com nome, telefone, setor, sala, horário e duração

📅 Bloqueio dinâmico de horários já ocupados (duração só habilita se houver espaço real)

🔎 Tela pública de consulta com filtros (data, nome, setor, horário)

❌ Cancelamento com confirmação por ticket

🔐 Painel administrativo com login (usuário/senha) e sessão persistente (7 dias)

🗃 Cancelamento individual ou em massa no painel admin

📜 Visualização de logs de ações no painel admin (excluindo login_success)

✅ Integração com webhook (n8n) para notificações automáticas

🛠 Tecnologias utilizadas

Backend: Python 3 + Flask

Frontend: HTML5 + TailwindCSS + JavaScript

Banco de dados: SQLite

APIs: Fetch, Webhook (n8n)

Outros: Cleave.js (máscara de telefone), Flatpickr (datas/horários)

📁 Estrutura do Projeto

meet_ladetec/
├── app.py                # Arquivo principal Flask
├── templates/
│   └── index.html        # Página pública (agendamento + consulta)
├── static/
│   ├── admin.html        # Painel admin (somente após login)
│   └── admin_login.html  # Tela de login do admin
├── models/
│   ├── database.py
│   ├── users.py
│   └── logs.py
├── database/
│   └── bookings.db       # Banco de dados SQLite (IGNORADO no Git)
├── .gitignore            # Ignora venv, db, caches etc.
└── README.md             # Este arquivo


💻 Como rodar localmente

1. Clone o repositório

git clone https://github.com/rdgx02/meet_ladetec.git
cd meet_ladetec


2. Crie um ambiente virtual e ative

python -m venv venv
venv\Scripts\activate     # Windows

3. Instale as dependências

pip install -r requirements.txt

Caso não exista requirements.txt, instale manualmente: pip install flask flask-cors requests


4. Inicie o servidor

python app.py


📍 Endereços:

Público: http://localhost:5000

Admin: http://localhost:5000/admin


🔑 Login Admin

Usuários administradores são pré-carregados no banco pelo seed_admins() em models/users.py.

Exemplo de logins (ajuste conforme configurado no seed):

Usuário: Vinícius
Usuário: Edimar
Usuário: Ana Maria
Usuário: Maíra
Senha: definida no seed (alterar em models/users.py)

A sessão é persistente por 7 dias.

🌐 Principais Rotas

| Rota                 | Método | Descrição                                            |
| -------------------- | ------ | ---------------------------------------------------- |
| `/`                  | GET    | Página pública de agendamento                        |
| `/admin`             | GET    | Se logado → `admin.html`; senão → `admin_login.html` |
| `/admin/login`       | POST   | Faz login do administrador                           |
| `/admin/logout`      | POST   | Faz logout                                           |
| `/auth/me`           | GET    | Retorna informações do usuário logado                |
| `/api/bookings`      | GET    | Lista todos agendamentos                             |
| `/api/bookings`      | POST   | Cria um novo agendamento (gera **ticket**)           |
| `/api/bookings/<id>` | DELETE | Cancela agendamento por ID                           |
| `/api/logs`          | GET    | Retorna logs (sem `login_success`)                   |


📦 Exemplo de uso da API

Criar agendamento
POST /api/bookings

{
  "name": "Fulano",
  "phone": "+55 21 99999-9999",
  "sector": "TI",
  "room": "203",
  "date": "23/08/2025",
  "startTime": "10:00",
  "duration": 60
}

Resposta:

{
  "id": 42,
  "name": "Fulano",
  "phone": "+55 21 99999-9999",
  "sector": "TI",
  "room": "203",
  "date": "23/08/2025",
  "start_time": "10:00",
  "duration": 60,
  "ticket": "ABC123"
}


🔗 Integração com n8n
Cada agendamento dispara um POST para o webhook configurado no app.py:

{
  "nome": "Fulano",
  "telefone": "+55 21 99999-9999",
  "setor": "TI",
  "sala": "203",
  "data": "23/08/2025",
  "inicio": "10:00",
  "fim": "11:00",
  "ticket": "ABC123"
}


🧾 Logs

Registram criação, cancelamento e falhas de login

Endpoint /api/logs retorna JSON filtrado

Painel admin possui modal de visualização de logs

Ação login_success é ocultada da listagem

🙈 .gitignore (já incluso)

# Ambiente virtual
venv/
.env

# Cache do Python
__pycache__/
*.pyc
*.pyo
*.pyd

# Banco local
database/bookings.db

# Logs
*.log

# IDE / SO
.vscode/
.idea/
.DS_Store
Thumbs.db

# Build
build/
dist/
*.egg-info/


📝 Licença

Este projeto é de uso interno do LADETEC/UFRJ.