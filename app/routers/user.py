from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserRead
from app.auth import get_current_user_or_open
from app.services import user_service

user_router = APIRouter(tags=["Users"])

# POST
@user_router.post("", response_model=UserRead)
def create(user_data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user_data)

# GET
@user_router.get("/{user_id}", response_model=UserRead)
def read( user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_by_id(db, user_id)

# PUT
@user_router.put("", response_model=UserRead)
def update( updates: UserCreate, logged_user: UserRead = Depends(get_current_user_or_open),  db: Session = Depends(get_db)):
    return user_service.update_user(db, user_id, updates, logged_user)

# DELETE
@user_router.delete("/{user_id}")
def delete(logged_user: UserRead = Depends(get_current_user_or_open), db: Session = Depends(get_db)):
    user_service.delete_user(db, user_id, logged_user)
    return {"detail": f"Utilisateur n°{user_id} supprimé"}