# app/api/routers/file_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.database import get_db
from app.services.file_service import FileService
from app.schemas.file import FileCreate, FileUpdate, FileResponse, PaginationParams, PaginatedResponse
from typing import Optional

router = APIRouter(prefix="/files", tags=["files"])

@router.post("/", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
def create_file(file_data: FileCreate, db: Session = Depends(get_db)):
    service = FileService(db)
    file_entry = service.create(file_data)
    return file_entry

@router.get("/", response_model=PaginatedResponse)
def get_files(
    pagination: PaginationParams = Depends(),
    user_id_filter: Optional[UUID] = None, # Позволяет фильтровать файлы конкретного пользователя
    db: Session = Depends(get_db)
):
    service = FileService(db)
    files, total, total_pages = service.get_all_active(pagination, user_id_filter=user_id_filter)
    return {
        "data": files,
        "meta": {
            "total": total,
            "page": pagination.page,
            "limit": pagination.limit,
            "totalPages": total_pages,
        }
    }

@router.get("/{file_id}", response_model=FileResponse)
def get_file(file_id: UUID, db: Session = Depends(get_db)):
    service = FileService(db)
    file_entry = service.get_by_id(file_id)
    if not file_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return file_entry

@router.put("/{file_id}", response_model=FileResponse)
def update_file_full(file_id: UUID, file_data: FileUpdate, db: Session = Depends(get_db)):
    service = FileService(db)
    file_entry = service.update(file_id, file_data)
    if not file_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return file_entry

@router.patch("/{file_id}", response_model=FileResponse)
def update_file_partial(file_id: UUID, file_data: FileUpdate, db: Session = Depends(get_db)):
    service = FileService(db)
    file_entry = service.update(file_id, file_data)
    if not file_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return file_entry

@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(file_id: UUID, db: Session = Depends(get_db)):
    service = FileService(db)
    deleted = service.delete(file_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return None