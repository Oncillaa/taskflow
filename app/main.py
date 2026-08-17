from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import time

from app.api.v1.endpoints import auth, users, tasks, teams
from app.core.database import engine, Base
from app.utils.logger import setup_logger

# Настраиваем логирование
logger = setup_logger()
logger.info("🚀 TaskFlow запускается...")

Base.metadata.create_all(bind=engine)
logger.info("✅ База данных подключена")

app = FastAPI(
    title="TaskFlow",
    description="Task management system for teams",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Логирование всех запросов (middleware)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    return response

# Роутеры
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(teams.router, prefix="/api/v1")


# Статика
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    logger.info("🌐 Открыта главная страница")
    return FileResponse("static/index.html")

logger.info("✅ TaskFlow готов к работе!")