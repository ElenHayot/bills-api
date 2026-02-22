"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.core.database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# Refresh tokens table
class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())

    # relation_ships
    user = relationship("User", back_populates="refresh_tokens")