"""
Feature engineering for gig worker credit scoring.

The model keeps the original 28 base features and adds only the five requested
gig-worker super-features.
"""

from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd


EPSILON = 1e-6


def _safe_divide(numerator: pd.Series, denominator: pd.Series | float) -> pd.Series:
    """Vectorized division that avoids inf values from zero denominators."""
    return numerator / np.maximum(denominator, EPSILON)


def engineer_features(X: pd.DataFrame) -> pd.DataFrame:
    """
    Return base features plus the five recommended engineered features.
    """
    X_eng = X.copy()

    X_eng["income_stability_buffer"] = _safe_divide(
        X_eng["avg_balance"] * X_eng["emergency_buffer"],
        X_eng["income_volatility"],
    ).round(4)

    X_eng["platform_earnings_density"] = _safe_divide(
        X_eng["avg_income"],
        X_eng["avg_hours"] * X_eng["avg_active_days"],
    ).round(4)

    X_eng["behavioral_discipline_score"] = (
        X_eng["rent_consistency_ratio"] * 0.7
        + X_eng["payment_behavior_consistency"] * 0.3
        - X_eng["delay_score"]
    ).round(4)

    X_eng["trust_growth_multiplier"] = (
        X_eng["earned_trust_score"] * (1.0 + X_eng["income_growth"])
    ).round(4)

    X_eng["liquidity_debt_stress_index"] = (
        (X_eng["fixed_emi_burden_ratio"] * X_eng["avg_income"])
        / (X_eng["avg_balance"] + 1.0)
    ).round(4)

    return X_eng


def get_engineered_feature_names() -> List[str]:
    """Return the five engineered feature names in training/inference order."""
    return [
        "income_stability_buffer",
        "platform_earnings_density",
        "behavioral_discipline_score",
        "trust_growth_multiplier",
        "liquidity_debt_stress_index",
    ]


def get_all_features_with_engineered(base_features: List[str]) -> List[str]:
    """Return original base features plus the five engineered features."""
    return base_features + get_engineered_feature_names()
