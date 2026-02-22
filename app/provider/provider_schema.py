"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class ProviderBase(BaseModel):
    name: str = Field(..., max_length=150)

class ProviderRead(ProviderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    # Allows DB data reading
    model_config = ConfigDict(from_attributes=True)

class ProviderUpdate(BaseModel):
    name: str | None = Field(..., max_length=150)