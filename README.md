# 📋 TaskFlow — умная система управления задачами для команд

**TaskFlow** — это полноценное веб-приложение для управления задачами в команде.  
Оно помогает создавать задачи, назначать исполнителей, отслеживать статусы, обсуждать задачи в комментариях и получать уведомления.

Проект написан на **Python + FastAPI** с использованием **SQLite**, **JWT-авторизации** и **Docker**.  
Фронтенд — чистый **HTML + CSS + JS** с тёмной темой и адаптивным дизайном.

---

## 🎯 Для чего это

TaskFlow подходит для:

- 📌 Управления проектами в небольших командах (до 20 человек)
- 📋 Личного планирования задач и дедлайнов
- 🎓 Обучения современному веб-стеку (Python, FastAPI, Docker, Git)
- 🧪 Портфолио для собеседований (показывает знание API, БД, авторизации, CI/CD)

---

## 🚀 Быстрый старт для новичков (пошагово)

Этот раздел для тех, кто **впервые видит командную строку**.

---

### 1️⃣ Установи Python

Перейди на сайт:  
👉 [https://www.python.org/downloads/](https://www.python.org/downloads/)

Скачай **Python 3.11** или выше.  

⚠️ **Важно:** во время установки **обязательно поставь галочку** «Add Python to PATH».  
Это позволит запускать Python из любой папки.

---

### 2️⃣ Скачай проект с GitHub

Открой **Командную строку** (Win + R → `cmd` → Enter) и выполни:
сли у тебя нет Git — скачай его с официального сайта.

3️⃣ Создай виртуальное окружение
Виртуальное окружение изолирует библиотеки проекта от других программ.

bash
python -m venv venv
Активируй окружение:

Windows:

bash
venv\Scripts\activate
Mac / Linux:

bash
source venv/bin/activate
Если в начале строки появилось (venv) — всё правильно.

4️⃣ Установи зависимости
bash
pip install -r requirements.txt
5️⃣ Создай файл .env с секретными настройками
В папке проекта создай файл .env (без расширения) и вставь:

env
SECRET_KEY=taskflow_secret_key_2026
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./taskflow.db
6️⃣ Запусти сервер
bash
uvicorn app.main:app --reload
Когда увидишь:

text
INFO: Uvicorn running on http://127.0.0.1:8000
значит сервер запущен.

7️⃣ Открой сайт в браузере
Перейди по адресу:

text
http://127.0.0.1:8000/static/index.html
8️⃣ Зарегистрируйся и войди
Username: придумай (например, oncyber)

Email: любой (например, test@mail.com)

Password: придумай (например, qwerty123)

После входа ты увидишь дашборд с задачами.
Можешь создавать, редактировать и удалять задачи, смотреть статистику.

🐳 Запуск через Docker (для продвинутых)
Если у тебя установлен Docker:

bash
docker-compose up --build
После сборки открой:

text
http://127.0.0.1:8000/static/index.html
📁 Структура проекта
text
taskflow/
├── app/
│   ├── api/v1/endpoints/   # API-эндпоинты (все запросы)
│   │   ├── auth.py         # Регистрация, логин, JWT
│   │   ├── tasks.py        # Работа с задачами (CRUD)
│   │   ├── users.py        # Профиль пользователя
│   │   ├── teams.py        # Команды (в разработке)
│   │   ├── comments.py     # Комментарии (в разработке)
│   │   └── notifications.py # Уведомления (в разработке)
│   ├── core/               # Ядро приложения
│   │   ├── database.py     # Подключение к SQLite
│   │   └── security.py     # Хэширование паролей и JWT
│   ├── models/             # Модели базы данных (SQLAlchemy)
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── team.py
│   │   ├── comment.py
│   │   └── notification.py
│   ├── schemas/            # Схемы Pydantic (валидация данных)
│   ├── static/             # Фронтенд (HTML, CSS, JS)
│   │   └── index.html      # Главная страница (тёмная тема)
│   └── main.py             # Точка входа (FastAPI приложение)
├── migrations/             # Миграции базы данных (Alembic)
├── Dockerfile              # Инструкция для сборки Docker-образа
├── docker-compose.yml      # Запуск проекта одной командой
├── requirements.txt        # Все Python-зависимости
├── .env                    # Переменные окружения (секреты)
├── .gitignore              # Что не заливать на GitHub
├── README.md               # Описание проекта (этот файл)
└── LICENSE                 # Лицензия MIT
📡 API-эндпоинты (для разработчиков)
Метод	Эндпоинт	Описание	Токен
POST	/api/v1/auth/register	Регистрация нового пользователя	❌
POST	/api/v1/auth/login	Вход, получение JWT-токена	❌
GET	/api/v1/users/me	Информация о текущем пользователе	✅
POST	/api/v1/tasks/	Создать задачу	✅
GET	/api/v1/tasks/	Список всех задач (с фильтрами)	✅
GET	/api/v1/tasks/{id}	Получить задачу по ID	✅
PUT	/api/v1/tasks/{id}	Обновить задачу	✅
DELETE	/api/v1/tasks/{id}	Удалить задачу	✅
PATCH	/api/v1/tasks/{id}/status	Изменить статус задачи	✅
GET	/api/v1/tasks/my/	Задачи, назначенные на меня	✅
GET	/api/v1/tasks/created/	Задачи, созданные мной	✅
POST	/api/v1/teams/	Создать команду	✅
POST	/api/v1/comments/	Добавить комментарий к задаче	✅
GET	/api/v1/notifications/	Получить уведомления	✅
PATCH	/api/v1/notifications/{id}/read	Отметить уведомление как прочитанное	✅
💡 Все эндпоинты, помеченные ✅, требуют заголовок:
Authorization: Bearer <ваш_токен>

🛠️ Используемые технологии
Технология	Назначение
Python 3.11+	Основной язык программирования
FastAPI	Современный бэкенд-фреймворк (асинхронный, с автоматической документацией)
SQLAlchemy	ORM для работы с базой данных
SQLite	Лёгкая файловая база данных (не требует установки)
JWT	Токен-авторизация (без сессий и кук)
Alembic	Управление миграциями базы данных
Docker	Контейнеризация (запуск на любом сервере)
HTML + CSS + JS	Фронтенд (чистый, без фреймворков, тёмная тема)
Git	Контроль версий
GitHub	Хостинг кода и совместная разработка
👥 Авторы
Oncillaa — фронтенд, авторизация, задачи, Docker, миграции, документация

[Друг] — команды, комментарии, уведомления, тесты (pytest), README

📄 Лицензия
Этот проект распространяется под лицензией MIT.
Это значит, что вы можете свободно использовать, изменять и распространять код, даже в коммерческих целях, с указанием авторства.
Подробнее: LICENSE

🤝 Как внести вклад
Форкни репозиторий (кнопка Fork на GitHub)

Создай ветку для своей фичи:
git checkout -b feature/имя-фичи

Сделай изменения и закоммить:
git commit -m "Описание изменений"

Запушь на GitHub:
git push origin feature/имя-фичи

Создай Pull Request в ветку dev

❓ Частые вопросы (FAQ)
❌ Ошибка: No module named '...'
Установи зависимости заново:

bash
pip install -r requirements.txt
❌ Ошибка: sqlite3.OperationalError: unable to open database file
Создай файл базы вручную:

bash
echo. > taskflow.db
Или просто запусти проект через uvicorn (без Docker).

❌ Ошибка: Address already in use (порт 8000 занят)
Используй другой порт:

bash
uvicorn app.main:app --reload --port 8001
И открой в браузере:

text
http://127.0.0.1:8001/static/index.html
❌ Как обновить проект после изменений?
bash
git pull origin dev
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
❌ Как остановить сервер?
Нажми Ctrl + C в терминале.

📬 Связь
GitHub: https://github.com/Oncillaa

Email: graevartem0@gmail.com

⭐ Если проект тебе помог — поставь звезду на GitHub!
Это поможет другим разработчикам найти его.
```bash
git clone https://github.com/Oncillaa/taskflow.git
cd taskflow
