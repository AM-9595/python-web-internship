from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, tasks

# Создаём таблицы в БД
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Simple Project Tracker", version="1.0")

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(tasks.task_router)

@app.get("/")
def root():
    return {"message": "Project Tracker API is running"}