from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse, PaginationParams, PaginatedResponse # <- Изменили импорт схем

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db) # <- Используем UserService
    user = service.create(user_data)
    return user

@router.get("/", response_model=PaginatedResponse)
def get_users(pagination: PaginationParams = Depends(), db: Session = Depends(get_db)):
    service = UserService(db) # <- Используем UserService
    users, total = service.get_all_active(pagination) # <- Вызов метода сервиса для User
    total_pages = (total + pagination.limit - 1) // pagination.limit
    return {
        "data": users, # <- Возвращаем пользователей
        "meta": {
            "total": total,
            "page": pagination.page,
            "limit": pagination.limit,
            "totalPages": total_pages,
        }
    }

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    service = UserService(db) # <- Используем UserService
    user = service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user_full(user_id: UUID, user_data: UserUpdate, db: Session = Depends(get_db)):
    service = UserService(db) # <- Используем UserService
    user = service.update(user_id, user_data, partial=False) # <- Указываем partial=False для полного обновления
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.patch("/{user_id}", response_model=UserResponse)
def update_user_partial(user_id: UUID, user_data: UserUpdate, db: Session = Depends(get_db)): # <- Изменили имя функции и тип данных
    service = UserService(db) # <- Используем UserService
    user = service.update(user_id, user_data, partial=True) # <- Указываем partial=True для частичного обновления
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") # <- Изменили сообщение об ошибке
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT) # <- Изменили путь
def delete_user(user_id: UUID, db: Session = Depends(get_db)): # <- Изменили имя функции и параметр
    service = UserService(db) # <- Используем UserService
    deleted = service.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found") # <- Изменили сообщение об ошибке
    return None
