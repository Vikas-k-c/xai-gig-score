from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    pan_details = relationship(
        "PanDetails",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )
    platforms = relationship(
        "PlatformData",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    predictions = relationship(
        "Prediction",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    loans = relationship(
        "Loan",
        back_populates="user",
        cascade="all, delete-orphan",
    )