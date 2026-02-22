"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.user.user_model import User
from app.user.user_schema import UserCreate, UserRead, UserUpdate
from app.auth.auth_schema import RegisterResponse
from app.dependencies.auth import get_current_user
from app.user import user_service

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
    print(f"in user router, on update, user_id: {user_id}, updates: {updates}, current_user: {current_user}")
    return user_service.update_user(db, current_user, updates, user_id)

# DELETE : Delete a user
@user_router.delete("/{user_id}/",
                      summary="Delete account",
                      description="Delete current user's account - returns nothing")
def delete(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return user_service.delete_user(db, current_user, user_id)