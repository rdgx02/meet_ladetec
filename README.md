# 🏢 Sistema de Agendamento de Salas - MEET LADETEC

Este é um sistema web para **agendamento de salas no LADETEC**, desenvolvido em **Python (Flask)** no backend e **HTML + Tailwind + JavaScript** no frontend.

O sistema permite que usuários realizem agendamentos, consultem, cancelem por ticket e que o administrador gerencie as reservas com painel completo.

---

## 🚀 Funcionalidades

- ✅ Agendamento com nome, telefone, setor, sala, horário e duração
- 🔎 Tela pública de consulta com filtros (data, nome, setor, horário)
- ❌ Cancelamento com confirmação por ticket
- 🔐 Painel administrativo com login (usuário e senha fixos)
- 🗃 Cancelamento individual ou em massa
- 📅 Bloqueio dinâmico de horários já ocupados
- ✅ Integração com webhook (n8n)

---

## 🛠 Tecnologias utilizadas

- **Backend:** Python 3 + Flask
- **Frontend:** HTML5 + TailwindCSS + JavaScript
- **Banco de dados:** SQLite
- **APIs:** Fetch, Webhook (n8n)
- **Outros:** Cleave.js (máscara de telefone), Flatpickr (data/hora)

---

## 📁 Estrutura do Projeto
meet_ladetec/
├── app.py # Arquivo principal Flask
├── templates/
│ └── index.html # Frontend completo
├── static/ # (caso use assets locais)
├── database/
│ └── bookings.db # Banco de dados SQLite
├── .venv/ # Ambiente virtual (não subir no GitHub)
└── README.md # Este arquivo


---

## 💻 Como rodar localmente

### 1. Clone o repositório:

```bash
git clone https://github.com/rdgx02/meet_ladetec.git
cd meet_ladetec
python -m venv .venv
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
python app.py
📍 http://localhost:5000

🔑 Login Admin
Para acessar o painel de administração:

Usuário: admin
Senha: admin123

🧾 Licença
Este projeto é de uso interno do LADETEC/UFRJ.


