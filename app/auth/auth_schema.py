from pydantic import BaseModel, EmailStr
from app.user.user_schema import UserRead

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

class RegisterResponse(BaseModel):
    access_token: str
    refresh_token: str
    current_user: UserRead
    token_type: str = "bearer"
