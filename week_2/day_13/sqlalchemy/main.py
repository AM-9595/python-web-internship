from fastapi import FastAPI
from database import engine, Base
from users_router import router as users_router
from tasks_router import router as tasks_router, task_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SQLAlchemy Users & Tasks API")

app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(task_router)

@app.get("/")
def root():
    return {"message": "SQLAlchemy API is running"}