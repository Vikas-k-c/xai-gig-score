from typing import Dict, List

from ..models.platform import PlatformData


FEATURE_COLUMNS = [
    "age",
    "platform_tenure",
    "avg_active_days",
    "avg_hours",
    "task_completion_rate",
    "avg_rating",
    "activity_stability",
    "wallet_txn_freq",
    "inward_txn_freq",
    "avg_income",
    "income_volatility",
    "income_growth",
    "savings_ratio",
    "avg_balance",
    "has_insurance",
    "emergency_buffer",
    "loan_utilization",
    "fixed_emi_burden_ratio",
    "credit_inquiries",
    "delay_score",
    "recent_payment_delays_90",
    "utility_delay_score",
    "recent_missed_rent_3m",
    "rent_consistency_ratio",
]


def _bool_to_float(value: bool) -> float:
    return 1.0 if value else 0.0


def build_features(platforms: List[PlatformData]) -> Dict[str, float]:
    if not platforms:
        raise ValueError("No platform data available to build features.")

    count = len(platforms)

    def avg(attr: str) -> float:
        return float(sum(getattr(p, attr) for p in platforms) / count)

    features = {
        "age": avg("age"),
        "platform_tenure": avg("platform_tenure"),
        "avg_active_days": avg("avg_active_days"),
        "avg_hours": avg("avg_hours"),
        "task_completion_rate": avg("task_completion_rate"),
        "avg_rating": avg("avg_rating"),
        "activity_stability": avg("activity_stability"),
        "wallet_txn_freq": avg("wallet_txn_freq"),
        "inward_txn_freq": avg("inward_txn_freq"),
        "avg_income": avg("avg_income"),
        "income_volatility": avg("income_volatility"),
        "income_growth": avg("income_growth"),
        "savings_ratio": avg("savings_ratio"),
        "avg_balance": avg("avg_balance"),
        "has_insurance": avg("_has_insurance_numeric"),
        "emergency_buffer": avg("_emergency_buffer_numeric"),
        "loan_utilization": avg("loan_utilization"),
        "fixed_emi_burden_ratio": avg("fixed_emi_burden_ratio"),
        "credit_inquiries": avg("credit_inquiries"),
        "delay_score": avg("delay_score"),
        "recent_payment_delays_90": avg("recent_payment_delays_90"),
        "utility_delay_score": avg("utility_delay_score"),
        "recent_missed_rent_3m": avg("recent_missed_rent_3m"),
        "rent_consistency_ratio": avg("rent_consistency_ratio"),
    }

    return features


def attach_numeric_flags(platform: PlatformData) -> None:
    platform._has_insurance_numeric = _bool_to_float(platform.has_insurance)
    platform._emergency_buffer_numeric = _bool_to_float(platform.emergency_buffer)