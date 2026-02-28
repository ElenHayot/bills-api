"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.auth_schema import RegisterResponse, Token, RefreshRequest, LogoutRequest
from app.auth import auth_service

auth_router = APIRouter(tags=["Auth"])

# POST - Login endpoint
@auth_router.post("/login/", response_model=RegisterResponse,
                    summary="Log-in user",
                    description="Returns access token and refresh token for the user")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth_service.login(form_data, db)

# POST - Refresh endpoint
@auth_router.post("/refresh/", response_model=Token,
                      description="Returns new access token for the current user")
def refresh_token(payload: RefreshRequest):
    return auth_service.refresh_token(payload)

@auth_router.post("/logout/",
                  summary="Logout the current user",
                  description="Delete the current user's refresh token and blacklist access token")
def logout(payload: LogoutRequest, db: Session = Depends(get_db)):
    auth_service.logout(db, payload.refresh_token, payload.access_token)
    return {"message": "Logged out successfully"}