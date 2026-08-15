# TaskFlow — управление задачами для команд

**TaskFlow** — это веб-приложение для управления задачами в команде.  
Позволяет создавать задачи, назначать исполнителей, отслеживать статусы и получать уведомления.

---

## Возможности

- Регистрация и вход (JWT)
- Создание, редактирование, удаление задач
- 4 статуса: ожидает → в работе → на проверке → выполнена
- Статистика задач
- Тёмная тема
- Docker

---

## Как это работает

1. Ты открываешь сайт в браузере
2. Регистрируешься или входишь
3. Создаёшь задачи, меняешь статусы
4. Данные сохраняются в базе данных

---

## Быстрый старт

### 1. Установи Python 3.11+

Скачай с python.org

### 2. Склонируй проект

git clone https://github.com/Oncillaa/taskflow.git
cd taskflow

### 3. Создай виртуальное окружение

python -m venv venv

Активируй:

Windows: venv\Scripts\activate
Mac/Linux: source venv/bin/activate

### 4. Установи зависимости

pip install -r requirements.txt

### 5. Создай файл .env

SECRET_KEY=taskflow_secret_key_2026
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./taskflow.db

### 6. Запусти сервер

uvicorn app.main:app --reload

### 7. Открой в браузере

http://127.0.0.1:8000/static/index.html

---

## Запуск через Docker

docker-compose up --build

---

## Структура проекта

taskflow/
├── app/
│   ├── api/v1/endpoints/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── static/
│   └── main.py
├── migrations/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── README.md
└── LICENSE

---

## API-эндпоинты

POST /api/v1/auth/register — регистрация
POST /api/v1/auth/login — вход
GET /api/v1/users/me — профиль
POST /api/v1/tasks/ — создать задачу
GET /api/v1/tasks/ — список задач
GET /api/v1/tasks/{id} — получить задачу
PUT /api/v1/tasks/{id} — обновить задачу
DELETE /api/v1/tasks/{id} — удалить задачу
PATCH /api/v1/tasks/{id}/status — изменить статус

Токен передаётся в заголовке: Authorization: Bearer <токен>

---

## Технологии

Python 3.11+
FastAPI
SQLAlchemy
SQLite
JWT
Alembic
Docker
HTML + CSS + JS

---

## Авторы

Oncillaa — фронтенд, авторизация, задачи, Docker, миграции
ivan345234 — команды, комментарии, уведомления, тесты

---

## Лицензия

MIT

---
