# 📌 Changelog — MEET LADETEC

Todas as mudanças importantes neste projeto serão documentadas aqui.  
O formato segue o padrão [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/) e a numeração de versões [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [1.1.0] - 2025-08-23
### ✨ Adicionado
- Separação das páginas:
  - Público → `templates/index.html`
  - Admin → `static/admin.html`
  - Login do admin → `static/admin_login.html`
- Sessão persistente de **7 dias**
- Rota `/auth/me` para checagem da sessão
- Painel admin com **visualização de logs** (em modal)
- Cancelamento **em massa** com modal de confirmação
- `.gitignore` configurado para ignorar:
  - `database/bookings.db`
  - `venv/`, `__pycache__/`, arquivos temporários de IDE/SO

### 🔄 Alterado
- `/admin` agora decide automaticamente:
  - logado → painel admin
  - não logado → tela de login
- Endpoint `/api/logs` agora **oculta** registros de `login_success`
- Bloqueio dinâmico das opções de **duração** no agendamento conforme disponibilidade real

### 🗑️ Removido
- Exibição pública do **ticket** (agora só via WhatsApp/logs)

---

## [1.0.0] - 2025-07-20
### 🚀 Lançamento inicial
- Página pública de agendamento (`index.html`)  
  - agendamento com nome, setor, telefone, sala, data, horário e duração
  - repetição semanal/mensal
  - consulta com filtros (data, setor, horário, nome)
  - cancelamento com **ticket**
- Painel admin básico:
  - listagem de agendamentos
  - cancelamento individual
- Integração inicial com **n8n** (webhook para confirmação de agendamento)
