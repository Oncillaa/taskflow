# TaskFlow - управление задачами для команд 
 
TaskFlow - это веб-приложение для управления задачами в команде. 
 
## Возможности 
 
- Регистрация и вход с JWT-токенами 
- Создание, редактирование, удаление задач 
- 4 статуса: ожидает - работе - проверке -
- Статистика задач 
- Тёмная тема 
- Docker 
 
## Как это работает 
 
1. Ты открываешь сайт в браузере 
2. Регистрируешься или входишь 
3. Создаёшь задачи, меняешь статусы 
4. Данные сохраняются в базе данных 
 
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
 
### 7. Открой сайт 
http://127.0.0.1:8000/static/index.html 
 
## Запуск через Docker 
docker-compose up --build 
 
## Авторы 
Oncillaa - фронтенд, авторизация, задачи, Docker, миграции 
ivan345234 - команды, комментарии, уведомления, тесты 
 
## Лицензия 
MIT 
