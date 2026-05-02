from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class PanDetails(Base):
    __tablename__ = "pan_details"
    __table_args__ = (
        UniqueConstraint("user_id", name="uq_pan_details_user_id"),
        UniqueConstraint("pan_number", name="uq_pan_details_pan_number"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    pan_number = Column(String(10), nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="pan_details")