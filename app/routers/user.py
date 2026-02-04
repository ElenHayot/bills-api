from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.schemas.auth import RegisterResponse
from app.dependencies.auth import get_current_user
from app.services import user_service

user_router = APIRouter(tags=["Users"])

# POST : Create a user
@user_router.post("/", response_model=UserRead,
                      summary="Create a user account")
def create(user_data: UserCreate, db: Session = Depends(get_db)):
    print("Hello createUser router")
    return user_service.create_user(db, user_data)

# POST : Register a user and return tokens
@user_router.post("/register/", response_model=RegisterResponse,
                      summary="Register a new user and return access/refresh tokens")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return user_service.register_user(db, user_data)

# GET : Get all users - dev function
@user_router.get("/", response_model=list[UserRead],
                      summary="Returns all users data (excepted secret data)")
def read_all(db: Session = Depends(get_db)):
    return user_service.get_all_users(db)

# GET : Find a user by its id
@user_router.get("/{user_id}/", response_model=UserRead,
                      summary="Find a user by its id",
                      description="Returns user data for a given id")
def read(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_by_id(db, user_id)

# PUT : Update a user
@user_router.put("/{user_id}/", response_model=UserRead,
                      summary="Update current user infos",
                      description="Update current user infos - returns updated data")
def update(user_id: int, updates: UserUpdate, current_user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    return user_service.update_user(db, current_user, updates, user_id)

# DELETE : Delete a user
@user_router.delete("/{user_id}/",
                      summary="Delete account",
                      description="Delete current user's account - returns nothing")
def delete(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return user_service.delete_user(db, current_user, user_id)