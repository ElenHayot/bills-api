from pydantic import BaseModel, Field

# Category common scheme
class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    color: str = Field(..., max_length=20)

# Category reading scheme
class CategoryRead(CategoryBase):
    id: int

    class Config:
        from_attributes = True