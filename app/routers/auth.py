from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import Token, RefreshRequest
from app.services import auth_service

auth_router = APIRouter(tags=["auth"])

# POST - Login endpoint
@auth_router.post("/login", response_model=Token,
                    superummary="Log-in user",
                    description="Returns access token and refresh token for the user")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return auth_service.login(form_data, db)

# POST - Refresh endpoint
@auth_router.post("/refresh", response_model=Token,
                      description="Returns new access token for the current user")
def refresh_token(payload: RefreshRequest):
    return auth_service.refresh_token(payload)