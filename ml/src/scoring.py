from __future__ import annotations


CREDIT_SCORE_MIN = 300
CREDIT_SCORE_MAX = 900
CREDIT_SCORE_RANGE = CREDIT_SCORE_MAX - CREDIT_SCORE_MIN


def probability_to_credit_score(default_probability: float) -> float:
    """
    Maps default probability [0,1] to a credit score [300,900].

    p = 0.0 -> 900
    p = 1.0 -> 300
    """
    p = max(0.0, min(1.0, float(default_probability)))
    score = CREDIT_SCORE_MIN + (1.0 - p) * CREDIT_SCORE_RANGE
    return round(score, 2)


def credit_score_to_risk_band(credit_score: float) -> str:
    """
    Simple risk banding for UI/business logic.
    """
    score = float(credit_score)

    if score >= 750:
        return "Low"
    if score >= 600:
        return "Medium"
    return "High"


def probability_to_risk_band(default_probability: float) -> str:
    """
    Optional probability-based banding.
    """
    p = max(0.0, min(1.0, float(default_probability)))

    if p < 0.30:
        return "Low"
    if p < 0.60:
        return "Medium"
    return "High"