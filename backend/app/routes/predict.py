from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..deps import get_db
from ..models.user import User
from ..schemas.prediction import PredictionResultResponse
from ..services.scoring_service import generate_prediction_for_user
from .auth import get_current_user


router = APIRouter(prefix="/predict", tags=["predict"])


@router.post("/", response_model=PredictionResultResponse)
def run_prediction(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        result = generate_prediction_for_user(db, current_user)
        return {
            "credit_score": result["credit_score"],
            "default_probability": result["default_probability"],
            "risk_level": result["risk_level"],
            "positive_factors": result["positive_factors"],
            "negative_factors": result["negative_factors"],
        }
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal prediction error: {str(exc)}",
        )