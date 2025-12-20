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
    date = Column(DateTime(timezone=True), server_default=func.now())
    comment = Column(String(400))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)

    # Relation ships
    user = relationship("User", back_populates="bills")