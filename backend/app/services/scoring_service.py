from typing import Dict

from sqlalchemy.orm import Session

from ..models.platform import PlatformData
from ..models.prediction import Prediction
from ..models.user import User
from .explain_service import explain_prediction
from .feature_engineering import attach_numeric_flags, build_features
from .model_service import predict_default_probability


def probability_to_credit_score(probability: float) -> float:
    probability = max(0.0, min(1.0, float(probability)))
    return round(300 + (1.0 - probability) * 600, 2)


def credit_score_to_risk_level(score: float) -> str:
    if score >= 750:
        return "Low"
    if score >= 600:
        return "Medium"
    return "High"


def generate_prediction_for_user(db: Session, user: User) -> Dict:
    platforms = db.query(PlatformData).filter(PlatformData.user_id == user.id).all()

    if not platforms:
        raise ValueError("No connected platform data found for this user.")

    for platform in platforms:
        attach_numeric_flags(platform)

    features = build_features(platforms)

    default_probability, _ = predict_default_probability(features)
    credit_score = probability_to_credit_score(default_probability)
    risk_level = credit_score_to_risk_level(credit_score)

    positive_factors, negative_factors = explain_prediction(features)

    prediction = Prediction(
        user_id=user.id,
        credit_score=credit_score,
        default_probability=default_probability,
        risk_level=risk_level,
        positive_factors=positive_factors,
        negative_factors=negative_factors,
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return {
        "id": prediction.id,
        "user_id": prediction.user_id,
        "credit_score": prediction.credit_score,
        "default_probability": prediction.default_probability,
        "risk_level": prediction.risk_level,
        "positive_factors": prediction.positive_factors,
        "negative_factors": prediction.negative_factors,
        "created_at": prediction.created_at,
    }