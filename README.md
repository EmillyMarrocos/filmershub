<div align="center">

# 🎬 FilmersHub

### A plataforma social e de negócios para a comunidade de videomakers

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)](https://djangoproject.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.4-3178C6?logo=typescript&logoColor=white)](https://typescriptlang.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-29-2496ED?logo=docker&logoColor=white)](https://docker.com)

[LinkedIn](https://www.linkedin.com/in/emilly-marrocos-mendon%C3%A7a-ciriaco-5751b1385/) · [Instagram](https://www.instagram.com/films.byemi/) · [Instagram Dev](https://www.instagram.com/emilly.codes/)

</div>

---

## 📖 Sobre o Projeto

O **FilmersHub** é uma plataforma full-stack desenvolvida como projeto de portfólio para conectar, apoiar e profissionalizar videomakers. Mais do que um agregador de portfólios, o sistema funciona como uma ferramenta de gestão e uma comunidade ativa.

Videomakers independentes frequentemente enfrentam dificuldades em três frentes:

- **Atração de Clientes** — Dependência exclusiva do Instagram, sem um portfólio web estruturado
- **Gestão do Negócio** — Dificuldade em precificar, montar orçamentos e redigir contratos
- **Comunidade** — Falta de um espaço focado para trocar experiências técnicas e de mercado

O FilmersHub centraliza a solução para essas dores.

---

## ✨ Funcionalidades

### 🔐 Autenticação
- Login e registro em 2 etapas (videomaker, cliente ou ambos)
- Senha visível/invisível, recuperação e redefinição via email
- JWT com refresh token automático

### 📰 Feed Social
- Criar, editar e excluir posts (optimistic updates)
- Reações com emoji picker
- Comentários em modal com tempo real
- Compartilhar (copiar link)
- Paginação com "Carregar mais"

### 🎬 Portfólio
- Upload de arquivos (vídeo/foto) e thumbnail
- Categorias filtráveis
- Menu 3-pontos: editar, publicar/rascunho, copiar link, excluir
- Modal de confirmação customizada

### 💬 Chat
- Salas de conversa 1-a-1
- Indicador de mensagens não lidas
- Marcar mensagens como lidas

### 📅 Agenda
- Criar e gerenciar eventos
- Visualização em lista

### 📄 Contratos
- Criação com resolução de cliente por email
- Assinatura digital com hash SHA-256
- Geração de PDF profissional (WeasyPrint)

### 🔔 Notificações
- Notificações in-app com ícones por tipo
- Contador de não lidas no header
- Marcar individual ou todas como lidas

### 👤 Perfil
- Editar dados, avatar e redes sociais
- Botão "Seguir" / "Mensagem" em perfis de outros
- Tabs: Trabalhos, Avaliações, Sobre
- Excluir conta com confirmação

### 🏠 Landing Page (Home)
- Hero com gradientes animados
- Contadores animados (IntersectionObserver)
- "Como funciona" (3 passos)
- Videomakers e trabalhos em destaque da API
- CTA, footer com 4 colunas

### 🔍 Explorar
- Busca por nome e cidade
- Grid de videomakers com paginação

---

## 🏗️ Arquitetura

```
filmershub/
├── backend/                    # Django 5 + DRF
│   ├── apps/
│   │   ├── accounts/           # Auth, perfis, follow
│   │   ├── feed/               # Posts, likes, comentários
│   │   ├── portfolio/          # Trabalhos, categorias, reviews
│   │   ├── chat/               # Salas e mensagens
│   │   ├── scheduling/         # Eventos e agenda
│   │   ├── contracts/          # Contratos e assinaturas
│   │   ├── payments/           # Mercado Pago (PIX/cartão)
│   │   ├── notifications/      # Notificações in-app + email
│   │   └── landing/            # Stats e dados da home
│   ├── config/                 # Settings (dev/test/prod)
│   ├── tests/                  # 103 testes (pytest-django)
│   └── requirements/           # Dependências por ambiente
├── frontend/                   # React 18 + TypeScript + Vite
│   └── src/
│       ├── pages/              # 15 páginas
│       ├── components/layout/  # Header, Sidebar, Layout
│       ├── api/                # Axios client + interceptors
│       ├── store/              # Zustand (authStore)
│       └── types/              # TypeScript interfaces
├── docker/                     # Dockerfiles
├── docker-compose.yml          # PostgreSQL, Redis, Backend, Frontend
└── .env.example                # Variáveis de ambiente
```

---

## 🚀 Stack Tecnológica

| Camada | Tecnologias |
|--------|------------|
| **Backend** | Python 3.13, Django 5.2, DRF, SimpleJWT, DRF Spectacular |
| **Frontend** | React 18, TypeScript 5, Vite 5, Tailwind CSS 3, Zustand, React Hook Form |
| **Banco de Dados** | PostgreSQL 16, Redis 7 |
| **Tempo Real** | Django Channels, Daphne, Channels-Redis |
| **Infraestrutura** | Docker, Docker Compose |
| **Pagamentos** | Mercado Pago (PIX + Cartão de crédito, split 85/15) |
| **Email** | SendGrid |
| **PDF** | WeasyPrint (contratos com 12 cláusulas) |
| **Testes** | pytest-django, factory-boy, SQLite in-memory |

---

## ⚙️ Como Executar

### Com Docker (Recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/EmillyMarrocos/filmershub.git
cd filmershub

# 2. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais

# 3. Suba os containers
docker-compose up -d

# 4. Acesse
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000
# API Docs: http://localhost:8000/api/docs/
```

### Desenvolvimento Local (Sem Docker)

**Pré-requisitos:** Python 3.13+, Node.js 24+

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate    # Linux/Mac

pip install -r requirements/development.txt

# Crie o .env (opcional para dev - usa SQLite por padrão)
python manage.py migrate
python manage.py runserver

# Frontend (em outro terminal)
cd frontend
npm install
npm run dev
```

---

## 📋 Variáveis de Ambiente

| Variável | Descrição | Padrão (dev) |
|----------|-----------|-------------|
| `DJANGO_SECRET_KEY` | Chave secreta do Django | `django-insecure-...` |
| `DJANGO_DEBUG` | Modo debug | `True` |
| `DATABASE_URL` | URL do PostgreSQL | `postgres://...localhost:5432/filmershub` |
| `REDIS_URL` | URL do Redis | `redis://localhost:6379/0` |
| `CORS_ALLOWED_ORIGINS` | Origens permitidas | `http://localhost:5173` |
| `MERCADOPAGO_ACCESS_TOKEN` | Token Mercado Pago | _(configurar depois)_ |
| `SENDGRID_API_KEY` | Chave SendGrid | _(configurar depois)_ |
| `EMAIL_BACKEND` | Backend de email | `console.EmailBackend` |

> **Nota:** Em desenvolvimento local sem PostgreSQL/Redis, o projeto usa SQLite + cache InMemory automaticamente.

---

## 🧪 Testes

```bash
cd backend
python -m pytest --tb=short -q
# 103 passed — accounts, chat, contracts, feed, notifications, payments, portfolio, scheduling
```

---

## 👨‍💻 Desenvolvido por

**Emilly Marrocos** — Estudante de Ciência da Computação (4º semestre) & Videomakers profissional

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Emilly%20Marrocos-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/emilly-marrocos-mendon%C3%A7a-ciriaco-5751b1385/)
[![Instagram](https://img.shields.io/badge/Instagram-%40films.byemi-E4405F?logo=instagram&logoColor=white)](https://www.instagram.com/films.byemi/)
[![Instagram Dev](https://img.shields.io/badge/Instagram-%40emilly.codes-E4405F?logo=instagram&logoColor=white)](https://www.instagram.com/emilly.codes/)

---

<div align="center">

Feito com 💜 para a comunidade de videomakers

</div>
