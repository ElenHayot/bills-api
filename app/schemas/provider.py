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