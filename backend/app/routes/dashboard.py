from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..deps import get_db
from ..models.loan import Loan
from ..models.pan import PanDetails
from ..models.platform import PlatformData
from ..models.prediction import Prediction
from ..models.user import User
from .auth import get_current_user


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pan_record = (
        db.query(PanDetails)
        .filter(PanDetails.user_id == current_user.id)
        .first()
    )

    platforms = (
        db.query(PlatformData)
        .filter(PlatformData.user_id == current_user.id)
        .order_by(PlatformData.created_at.desc())
        .all()
    )

    latest_prediction = (
        db.query(Prediction)
        .filter(Prediction.user_id == current_user.id)
        .order_by(Prediction.created_at.desc())
        .first()
    )

    prediction_history = (
        db.query(Prediction)
        .filter(Prediction.user_id == current_user.id)
        .order_by(Prediction.created_at.desc())
        .limit(5)
        .all()
    )

    loans = (
        db.query(Loan)
        .filter(Loan.user_id == current_user.id)
        .order_by(Loan.created_at.desc())
        .all()
    )

    platform_summary = {
        "connected_count": len(platforms),
        "platform_names": [p.platform_name for p in platforms],
        "avg_income": round(sum(p.avg_income for p in platforms) / len(platforms), 2) if platforms else 0.0,
        "avg_rating": round(sum(p.avg_rating for p in platforms) / len(platforms), 2) if platforms else 0.0,
        "avg_active_days": round(sum(p.avg_active_days for p in platforms) / len(platforms), 2) if platforms else 0.0,
    }

    return {
        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
        },
        "pan": {
            "submitted": pan_record is not None,
            "is_verified": pan_record.is_verified if pan_record else False,
            "pan_number": pan_record.pan_number if pan_record else None,
        },
        "platform_summary": platform_summary,
        "latest_prediction": {
            "credit_score": latest_prediction.credit_score,
            "default_probability": latest_prediction.default_probability,
            "risk_level": latest_prediction.risk_level,
            "positive_factors": latest_prediction.positive_factors,
            "negative_factors": latest_prediction.negative_factors,
            "created_at": latest_prediction.created_at,
        } if latest_prediction else None,
        "prediction_history": [
            {
                "id": p.id,
                "credit_score": p.credit_score,
                "default_probability": p.default_probability,
                "risk_level": p.risk_level,
                "created_at": p.created_at,
            }
            for p in prediction_history
        ],
        "loans": [
            {
                "id": loan.id,
                "bank_name": loan.bank_name,
                "amount": loan.amount,
                "status": loan.status,
                "created_at": loan.created_at,
            }
            for loan in loans
        ],
    }