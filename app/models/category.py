from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.core.database import Base

# Category table
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    color = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)


    # Two users can have a category named "Electricity", but one user should have it only once
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_user_category_name"),
    )