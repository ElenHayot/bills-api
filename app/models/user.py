from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

# User table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  #autoincrement implicite
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) #rempli une fois lors de la création
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())    #modifié à chaque update

    # Relation ships
    bills = relationship("Bill", back_populates="user")
    categories = relationship("Category", back_populates="user")
