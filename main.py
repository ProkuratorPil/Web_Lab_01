# main_fastapi.py
from fastapi import FastAPI
from app.routers import user_router # <- Роутер пользователей
from app.routers import file_router # <- Импортируем новый роутер файлов

app = FastAPI()

app.include_router(user_router.router)
app.include_router(file_router.router) # <- Подключаем новый роутер файлов

@app.get("/")
def read_root():
    return {"message": "Welcome to the User & File Management API"}