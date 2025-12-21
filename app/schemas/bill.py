from pydantic import BaseModel, Field, Decimal
from datetime import datetime

# Bill common scheme
class BillBase(BaseModel):
    title: str = Field(..., max_length=150)
    amount: Decimal
    date: datetime | None = None
    category_id: int
    comment: str | None = Field(None, max_length=400)

# Bill reading scheme
class BillRead(BillBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:   
        from_attributes = True

# Bill updating scheme
class BillUpdate(BaseModel):
    title: str | None = None
    amount: Decimal | None = None
    date: datetime | None = None
    category_id: int | None = None
    comment: str | None = Field(None, max_length=400)