from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

# User common scheme
class UserBase(BaseModel):
    email: EmailStr

# Scheme to create user or update user's password
class UserCreate(UserBase):
    password: str

# User reading scheme - get all non-sensitive user infos
class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes = True) 

# User updating scheme
class UserUpdate(UserBase):
    email: EmailStr | None = None
    password: str | None = None
