from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import RegisterResponse, Token, RefreshRequest
from app.services import auth_service
from app.models.user import User
from app.dependencies.auth import get_current_user

auth_router = APIRouter(tags=["Auth"])

# POST - Login endpoint
@auth_router.post("/login/", response_model=RegisterResponse,
                    summary="Log-in user",
                    description="Returns access token and refresh token for the user")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(f"form_data.client_id: {form_data.client_id}")
    print(f"form_data.username: {form_data.username}")
    print(f"form_data.password: {form_data.password}")
    return auth_service.login(form_data, db)

# POST - Refresh endpoint
@auth_router.post("/refresh/", response_model=Token,
                      description="Returns new access token for the current user")
def refresh_token(payload: RefreshRequest):
    return auth_service.refresh_token(payload)

@auth_router.post("/logout/",
                  summary="Logout the current user",
                  description="Delete the current user's refresh token")
def logout(payload: RefreshRequest, db: Session = Depends(get_db)):
    auth_service.logout(db, payload.refresh_token)
    return {"message": "Logged out"}