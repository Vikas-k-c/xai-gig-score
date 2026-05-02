from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    credit_score = Column(Float, nullable=False)
    default_probability = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)

    positive_factors = Column(ARRAY(String), nullable=False, default=list)
    negative_factors = Column(ARRAY(String), nullable=False, default=list)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="predictions")