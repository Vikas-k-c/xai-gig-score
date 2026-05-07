from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class PlatformData(Base):
    __tablename__ = "platform_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    platform_name = Column(String(50), nullable=False)

    age = Column(Float, nullable=False)
    platform_tenure = Column(Float, nullable=False)
    avg_active_days = Column(Float, nullable=False)
    avg_hours = Column(Float, nullable=False)
    task_completion_rate = Column(Float, nullable=False)
    avg_rating = Column(Float, nullable=False)
    activity_stability = Column(Float, nullable=False)
    wallet_txn_freq = Column(Float, nullable=False)
    inward_txn_freq = Column(Float, nullable=False)
    avg_income = Column(Float, nullable=False)
    income_volatility = Column(Float, nullable=False)
    income_growth = Column(Float, nullable=False)
    savings_ratio = Column(Float, nullable=False)
    avg_balance = Column(Float, nullable=False)
    has_insurance = Column(Boolean, nullable=False, default=False)
    emergency_buffer = Column(Boolean, nullable=False, default=False)
    loan_utilization = Column(Float, nullable=False)
    fixed_emi_burden_ratio = Column(Float, nullable=False)
    credit_inquiries = Column(Float, nullable=False)
    delay_score = Column(Float, nullable=False)
    recent_payment_delays_90 = Column(Float, nullable=False)
    utility_delay_score = Column(Float, nullable=False)
    recent_missed_rent_3m = Column(Float, nullable=False)
    rent_consistency_ratio = Column(Float, nullable=False)

    gig_creditworthiness_score = Column(Float, nullable=False)
    earned_trust_score = Column(Float, nullable=False)
    income_reliability_ratio = Column(Float, nullable=False)
    payment_behavior_consistency = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="platforms")