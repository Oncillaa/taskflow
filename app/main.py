from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.database import engine, Base
from app.api.v1.endpoints import (
    auth_router,
    users_router,
    tasks_router,
    teams_router,
    comments_router,
    notifications_router,
    links_router
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskFlow",
    description="Task management system for teams",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")
app.include_router(teams_router, prefix="/api/v1")
app.include_router(comments_router, prefix="/api/v1")
app.include_router(notifications_router, prefix="/api/v1")
app.include_router(links_router, prefix="/api/v1")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return {"message": "TaskFlow is running. Documentation: /docs"}