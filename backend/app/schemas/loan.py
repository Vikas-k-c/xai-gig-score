from datetime import datetime
from pydantic import BaseModel, Field


class LoanApplyRequest(BaseModel):
    bank_name: str = Field(..., min_length=2, max_length=100)
    amount: float = Field(..., gt=0)


class LoanResponse(BaseModel):
    id: int
    user_id: int
    bank_name: str
    amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True