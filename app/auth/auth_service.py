"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from fastapi import  Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.auth.auth_schema import  RefreshRequest, RegisterResponse
from jose import jwt, JWTError
from datetime import datetime, timedelta

from app.core.security import SECRET_KEY, ALGORITHM
from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token, verify_password, REFRESH_TOKEN_EXPIRE_DAYS
from app.user.user_model import User
from app.auth.refresh_token import RefreshToken
from app.auth.blacklisted_token import BlacklistedToken
from app.user.user_schema import UserRead
from app.core.errors import InvalidCredentialsError, UnauthorizedError, AccountLockedError

# Log-in an existing user
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Check is user exists
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user :
        raise InvalidCredentialsError()

    # Check if user is not locked
    if user.locked_until and user.locked_until > datetime.now():
        raise AccountLockedError()
    
    # If wrong password
    if not verify_password(form_data.password, user.password_hash):
        # Lock user for 15 minutes after 5 attempts
        user.failed_login_attempts += 1
        if user.failed_login_attempts >= 5:
            timeLock = 15
            user.locked_until = datetime.now() + timedelta(minutes=timeLock)
            raise AccountLockedError()
        db.commit() 
        raise InvalidCredentialsError()

    # If login ok :
    user.failed_login_attempts = 0
    user.locked_until = None
    db.commit()

    # Create tokens
    access = create_access_token({"sub": str(user.id)})
    refresh = create_refresh_token({"sub": str(user.id)})

    # Add refresh token to db
    refresh_token = RefreshToken(
        user_id = user.id,
        token = refresh,
        expires_at = datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)

    response = RegisterResponse(
        access_token=access,
        refresh_token=refresh,
        token_type="bearer",
        current_user= UserRead.model_validate(user),
    )
    return response

# Refresh access_token if refresh_token is valid
def refresh_token(payload: RefreshRequest):
    try:
        decoded = jwt.decode(payload.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = decoded.get("sub")
        if not user_id:
            raise UnauthorizedError()
    except JWTError:
        raise UnauthorizedError(message="Invalid refresh token")

    return {
        "access_token": create_access_token({"sub": user_id}),
        "refresh_token": create_refresh_token({"sub": user_id}),
    }

# Logout user - delete associated refresh token and blacklist access token
def logout(db: Session, refresh_token: str, access_token: str = None):
    # Delete refresh token
    token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token
    ).first()

    if token:
        db.delete(token)

    # Blacklist access token if provided
    if access_token:
        try:
            decoded = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            exp_timestamp = decoded.get("exp")
            user_id = decoded.get("sub")
            
            if exp_timestamp and user_id:
                expires_at = datetime.fromtimestamp(exp_timestamp)
                
                # Only blacklist if token is not already expired
                if expires_at > datetime.now():
                    blacklisted_token = BlacklistedToken(
                        token=access_token,
                        expires_at=expires_at,
                        user_id=int(user_id)
                    )
                    db.add(blacklisted_token)
        except JWTError:
            pass  # Token is invalid, no need to blacklist

    db.commit()

# Check if a token is blacklisted
def is_token_blacklisted(db: Session, token: str) -> bool:
    blacklisted = db.query(BlacklistedToken).filter(
        BlacklistedToken.token == token
    ).first()
    
    if not blacklisted:
        return False
    
    # Remove expired tokens from blacklist and return False
    if blacklisted.expires_at <= datetime.utcnow():
        db.delete(blacklisted)
        db.commit()
        return False
    
    return True

# Clean up expired blacklisted tokens
def cleanup_expired_blacklisted_tokens(db: Session):
    expired_tokens = db.query(BlacklistedToken).filter(
        BlacklistedToken.expires_at <= datetime.utcnow()
    ).all()
    
    for token in expired_tokens:
        db.delete(token)
    
    if expired_tokens:
        db.commit()