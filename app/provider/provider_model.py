"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

# Provider table
class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)  #autoincrement implicite
    name = Column(String(150), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relation ships
    user = relationship("User", back_populates="providers")

    # Two users can have a provider named "EDF", but one user should have it only once
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_user_provider_name"),
    )