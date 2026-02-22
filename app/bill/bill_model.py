"""
Copyright (c) 2026 Elen Hayot
All rights reserved.

This software is the confidential and proprietary information of Elen Hayot.
You shall not disclose such Confidential Information and shall use it only in 
accordance with the terms of the license agreement.
"""

from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

# Bill table
class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)  #autoincrement implicite
    title = Column(String(150), nullable=False, index=True)
    amount = Column(Numeric(10,2), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False, index=True)
    provider_id = Column(Integer, ForeignKey("providers.id", ondelete="SET NULL"), nullable=True, index=True)
    provider_name = Column(String(150), nullable = True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    comment = Column(String(400))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # PREVISIONNEL
    # devise/currency = Column(String, nullable=False)   # enum : $, €, ¥, £, ...

    # Relation ships
    user = relationship("User", back_populates="bills")