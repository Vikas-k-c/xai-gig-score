from datetime import datetime
from typing import List
from pydantic import BaseModel


class PredictionResponse(BaseModel):
    id: int
    user_id: int
    credit_score: float
    default_probability: float
    risk_level: str
    positive_factors: List[str]
    negative_factors: List[str]
    created_at: datetime

    class Config:
        from_attributes = True


class PredictionResultResponse(BaseModel):
    credit_score: float
    default_probability: float
    risk_level: str
    positive_factors: List[str]
    negative_factors: List[str]