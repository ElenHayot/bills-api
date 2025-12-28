from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.dependencies.auth import get_current_user
from app.services import user_service

user_router = APIRouter(tags=["Users"])

# POST : Create a user
@user_router.post("", response_model=UserRead,
                      summary="Create a user account")
def create(user_data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user_data)

# GET : Get all users - dev function
@user_router.get("/", response_model=list[UserRead],
                      summary="Returns all users data (excepted secret data)")
def read_all(db: Session = Depends(get_db)):
    return user_service.get_all_users(db)

# GET : Find a user by its email
@user_router.get("/{user_email}", response_model=UserRead,
                      summary="Find a user by its email",
                      description="Returns user data for a given email")
def read( user_email: str, db: Session = Depends(get_db)):
    return user_service.get_user_by_email(db, user_email)

# PUT : Update a user
@user_router.put("/{user_email}", response_model=UserRead,
                      summary="Update current user infos",
                      description="Update current user infos - returns updated data")
def update(user_email: str, updates: UserUpdate, current_user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    return user_service.update_user(db, current_user, updates, user_email)

# DELETE : Delete a user
@user_router.delete("/{user_email}",
                      summary="Delete account",
                      description="Delete current user's account - returns nothing")
def delete(user_email: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return user_service.delete_user(db, current_user, user_email)