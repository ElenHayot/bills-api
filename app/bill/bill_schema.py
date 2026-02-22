"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from decimal import Decimal
from datetime import datetime

# Bill common scheme
class BillBase(BaseModel):
    title: str = Field(..., max_length=150)
    amount: Decimal
    date: datetime | None = None
    category_id: int
    provider_id: int | None = None
    provider_name: str | None = Field("", max_length=150)
    comment: str | None = Field("", max_length=400)

    @field_validator("amount", mode="before")
    @classmethod
    def normalize_amount(cls, v):
        return Decimal(str(v))

# Bill reading scheme
class BillRead(BillBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes = True) 

# Bill updating scheme
class BillUpdate(BaseModel):
    title: str | None = None
    amount: Decimal | None = None
    date: datetime | None = None
    category_id: int | None = None
    comment: str | None = Field(None, max_length=400)
    provider_id: int | None = None
    provider_name: str | None = Field(None, max_length=150)

