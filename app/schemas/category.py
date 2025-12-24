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