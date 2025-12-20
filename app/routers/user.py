from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserRead
from app.dependencies.auth import get_current_user
from app.services import user_service

user_router = APIRouter(tags=["Users"])

# POST
@user_router.post("", response_model=UserRead)
def create(user_data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user_data)

# GET
@user_router.get("/{user_email}", response_model=UserRead)
def read( user_email: str, db: Session = Depends(get_db)):
    return user_service.get_user_by_email(db, user_email)

# PUT
@user_router.put("/{user_email}", response_model=UserRead)
def update( updates: UserCreate, logged_user: UserRead = Depends(get_current_user),  db: Session = Depends(get_db)):
    return user_service.update_user(db, logged_user, updates)

# DELETE
@user_router.delete("/{user_email}")
def delete(logged_user: UserRead = Depends(get_current_user), user_email: str = "", db: Session = Depends(get_db)):
    return user_service.delete_user(db, logged_user, user_email)