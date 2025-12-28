from fastapi import  Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.auth import  RefreshRequest
from jose import jwt, JWTError
from datetime import datetime, timedelta

from app.core.security import SECRET_KEY, ALGORITHM
from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token, verify_password, REFRESH_TOKEN_EXPIRE_DAYS
from app.models.user import User
from app.models.refresh_token import RefreshToken

# Log-in an existing user
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Check is user exists
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user :
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Check if user is not locked
    if user.locked_until and user.locked_until > datetime.now():
        raise HTTPException(
            status_code=423,
            detail="Account locked. Try again later."
        )
    
    # If wrong password
    if not verify_password(form_data.password, user.password_hash):
        # Lock user for 15 minutes after 5 attempts
        user.failed_login_attempts += 1
        if user.failed_login_attempts >= 5:
            user.locked_until = datetime.now() + timedelta(minutes=15)
        db.commit() 
        raise HTTPException(status_code=401, detail="Invalid credentials")

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

    return {
        "access_token": access,
        "refresh_token": refresh,
    }

# Refresh access_token if refresh_token is valid
def refresh_token(payload: RefreshRequest):
    try:
        decoded = jwt.decode(payload.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = decoded.get("sub")
        if not user_id:
            raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    return {
        "access_token": create_access_token({"sub": user_id}),
        "refresh_token": create_refresh_token({"sub": user_id}),
    }

# Logout user - delete associated refresh token
def logout(db: Session, refresh_token: str):
    token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token
    ).first()

    if not token:
        return

    db.delete(token)
    db.commit()