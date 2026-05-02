from datetime import datetime
from pydantic import BaseModel, Field


class PanSubmitRequest(BaseModel):
    pan_number: str = Field(..., min_length=10, max_length=10)


class PanResponse(BaseModel):
    id: int
    user_id: int
    pan_number: str
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True