from pydantic import BaseModel, DateTime, Field, Decimal

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

    class Config:
        from_attributes = True