from datetime import datetime
from pydantic import BaseModel


class PlatformConnectRequest(BaseModel):
    platform_name: str


class PlatformResponse(BaseModel):
    id: int
    user_id: int
    platform_name: str

    age: float
    platform_tenure: float
    avg_active_days: float
    avg_hours: float
    task_completion_rate: float
    avg_rating: float
    activity_stability: float
    wallet_txn_freq: float
    inward_txn_freq: float
    avg_income: float
    income_volatility: float
    income_growth: float
    savings_ratio: float
    avg_balance: float
    has_insurance: bool
    emergency_buffer: bool
    loan_utilization: float
    fixed_emi_burden_ratio: float
    credit_inquiries: float
    delay_score: float
    recent_payment_delays_90: float
    utility_delay_score: float
    recent_missed_rent_3m: float
    rent_consistency_ratio: float

    created_at: datetime

    class Config:
        from_attributes = True