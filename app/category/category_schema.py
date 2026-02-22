"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

# Category common scheme
class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    color: str = Field(..., max_length=20)

# Category reading scheme
class CategoryRead(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes = True) 

# Category updating scheme
class CategoryUpdate(BaseModel):
    name: str | None = Field(..., max_length=100)
    color: str | None = Field(..., max_length=20)