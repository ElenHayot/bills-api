"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime

# User common scheme
class UserBase(BaseModel):
    email: EmailStr

# Scheme to create user or update user's password
class UserCreate(UserBase):
    password: str = Field(min_length=8, strip_whitespace=True)

# User reading scheme - get all non-sensitive user infos
class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes = True) 

# User updating scheme
class UserUpdate(UserBase):
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8, strip_whitespace=True)
