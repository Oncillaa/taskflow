# 📋 TaskFlow — умная система управления задачами для команд

**TaskFlow** — это полноценное веб-приложение для управления задачами в команде.  
Оно помогает создавать задачи, назначать исполнителей, отслеживать статусы, обсуждать задачи в комментариях и получать уведомления.

Проект написан на **Python + FastAPI** с использованием **SQLite**, **JWT-авторизации** и **Docker**.  
Фронтенд — чистый **HTML + CSS + JS** с тёмной темой и адаптивным дизайном.

---

## 🎯 Для чего это

TaskFlow подходит для:

- 📌 Управления проектами в небольших командах
- 📋 Личного планирования задач и дедлайнов
- 🎓 Обучения современному веб-стеку
- 🧪 Портфолио для собеседований

---

## 🚀 Быстрый старт для новичков

### 1️⃣ Установи Python

Перейди на сайт: https://www.python.org/downloads/  
Скачай **Python 3.11** или выше.  
⚠️ **Важно:** при установке поставь галочку «Add Python to PATH».

### 2️⃣ Скачай проект с GitHub

Открой командную строку и выполни:

git clone https://github.com/Oncillaa/taskflow.git
cd taskflow

Если нет Git — скачай с https://git-scm.com/downloads

### 3️⃣ Создай виртуальное окружение

python -m venv venv

Активируй:

**Windows:**
venv\Scripts\activate

**Mac / Linux:**
source venv/bin/activate

### 4️⃣ Установи зависимости

pip install -r requirements.txt

### 5️⃣ Создай файл .env

В папке проекта создай файл .env и вставь:

SECRET_KEY=taskflow_secret_key_2026
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./taskflow.db

### 6️⃣ Запусти сервер

uvicorn app.main:app --reload

### 7️⃣ Открой сайт в браузере

http://127.0.0.1:8000/static/index.html

### 8️⃣ Зарегистрируйся и войди

- Username: например, oncyber
- Email: например, test@mail.com
- Password: например, qwerty123

---

## 🐳 Запуск через Docker

docker-compose up --build

Открой: http://127.0.0.1:8000/static/index.html

---

## 📁 Структура проекта

taskflow/
├── app/
│   ├── api/v1/endpoints/
│   │   ├── auth.py
│   │   ├── tasks.py
│   │   ├── users.py
│   │   ├── teams.py
│   │   ├── comments.py
│   │   └── notifications.py
│   ├── core/
│   │   ├── database.py
│   │   └── security.py
│   ├── models/
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── team.py
│   │   ├── comment.py
│   │   └── notification.py
│   ├── schemas/
│   ├── static/
│   │   └── index.html
│   └── main.py
├── migrations/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── .gitignore
├── README.md
└── LICENSE

---

## 📡 API-эндпоинты

Метод | Эндпоинт | Описание | Токен
POST | /api/v1/auth/register | Регистрация | ❌
POST | /api/v1/auth/login | Вход | ❌
GET | /api/v1/users/me | Профиль | ✅
POST | /api/v1/tasks/ | Создать задачу | ✅
GET | /api/v1/tasks/ | Список задач | ✅
GET | /api/v1/tasks/{id} | Получить задачу | ✅
PUT | /api/v1/tasks/{id} | Обновить задачу | ✅
DELETE | /api/v1/tasks/{id} | Удалить задачу | ✅
PATCH | /api/v1/tasks/{id}/status | Изменить статус | ✅

💡 Токен передаётся в заголовке: Authorization: Bearer <токен>

---

## 🛠️ Технологии

Технология | Назначение
Python 3.11+ | Язык программирования
FastAPI | Бэкенд-фреймворк
SQLAlchemy | ORM
SQLite | База данных
JWT | Авторизация
Alembic | Миграции
Docker | Контейнеризация
HTML + CSS + JS | Фронтенд

---

## 👥 Авторы

- **Oncillaa** — фронтенд, авторизация, задачи, Docker, миграции
- **ivan345234** — команды, комментарии, уведомления, тесты

---

## 📄 Лицензия

MIT. Подробнее в файле LICENSE.

---

## ❓ Частые вопросы

Ошибка: No module named '...'
pip install -r requirements.txt

Ошибка: unable to open database file
echo. > taskflow.db

Ошибка: порт 8000 занят
uvicorn app.main:app --reload --port 8001

Как остановить сервер?
Нажми Ctrl + C.

---
