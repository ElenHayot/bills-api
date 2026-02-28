"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.user import user_db
from app.user.user_schema import UserCreate, UserUpdate
from app.core.security import hash_password, create_access_token, create_refresh_token, REFRESH_TOKEN_EXPIRE_DAYS
from app.user.user_model import User
from app.auth.refresh_token import RefreshToken
from app.category import category_service
from app.core.errors import UnauthorizedError, ForbiddenError, UserNotFoundError, EmailAlreadyExistsError

# Create a new user
def create_user(db: Session, user: UserCreate) -> User:
    # Check email unicity
    existing_user = user_db.get_user_by_email(db, user.email)
    if existing_user:
        raise EmailAlreadyExistsError()
    
    # Password hash before creating
    hashed_password = hash_password(user.password)
    # User db model to create
    user_to_create = User(
        **user.model_dump(exclude={'password'}),
        password_hash = hashed_password
    )

    created_user = user_db.create_user(db, user_to_create)

    # Create default associated category for the created user
    category_service.create_default(db, created_user)

    return created_user

# Register a new user and return tokens
def register_user(db: Session, user: UserCreate):
    # Create the user
    created_user = create_user(db, user)
    
    # Create tokens
    access = create_access_token({"sub": str(created_user.id)})
    refresh = create_refresh_token({"sub": str(created_user.id)})

    # Add refresh token to db
    refresh_token = RefreshToken(
        user_id = created_user.id,
        token = refresh,
        expires_at = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)

    return {
        "access_token": access,
        "refresh_token": refresh,
        "current_user": created_user
    }

# Get all users
def get_all_users(db: Session) -> list[User]:
    return user_db.get_all_users(db)

# Find a user by its id
def get_user_by_id(db: Session, user_id: int) -> User:
    user = user_db.get_user_by_id(db, user_id)
    if not user:
        raise UserNotFoundError()
    return user

# Find a user by its email
def get_user_by_email(db: Session, email: str) -> User:
    user = user_db.get_user_by_email(db, email)
    if not user:
        raise UserNotFoundError()
    return user

# Update the logged user
def update_user(db: Session, current_user: User, updates: UserUpdate, user_id: int) -> User:
    if not current_user :
        raise UnauthorizedError("Vous devez être connecté pour cette opération")
        #raise HTTPException(status_code=401, detail=f"Il faut être connecté pour pouvoir exécuter cette opération")
    
    # Verify if can update
    if current_user.id != user_id:
        raise ForbiddenError(resource='user', message="Vous ne pouvez pas modifier cet utilisateur")
        #raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Vous ne pouvez pas modifier cet utilisateur.")
    
    # Verify email validity if changed
    if updates.email:
        user = user_db.get_user_by_email(db, updates.email)  
        if user:
            raise EmailAlreadyExistsError(email=updates.email)
            #raise HTTPException(status_code=404, detail=f"Erreur : email déjà utilisé")

    # Generate update datas
    update_data = updates.model_dump(exclude_unset=True, exclude={'password'})
    if updates.password and updates.password != "":
        update_data['password'] = hash_password(updates.password)

    return user_db.update_user(db, current_user, update_data)

# Delete an account
def delete_user(db: Session, current_user: User, user_id: int):
    if not current_user:
        raise UnauthorizedError(message="Il faut être connecté pour pouvoir exécuter cette opération")
    
    user = get_user_by_id(db, user_id)
    if not user:
        raise UserNotFoundError()
    
     # Verify if the user can update
    if current_user.id != user.id:
        raise ForbiddenError(message="Vous ne pouvez pas supprimer cet utilisateur.")
    
    return user_db.delete_user(db, user)