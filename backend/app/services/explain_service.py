# from pathlib import Path
# from typing import Dict, List, Tuple

# import joblib
# import pandas as pd

# BASE_DIR = Path(__file__).resolve().parent.parent
# ML_DIR = BASE_DIR / "ml"

# EXPLAINER_PATH = ML_DIR / "explainer.pkl"
# FEATURES_PATH = ML_DIR / "features.pkl"

# _explainer = None
# _features = None


# FEATURE_LABELS = {
#     "age": "Age",
#     "platform_tenure": "Platform tenure",
#     "avg_active_days": "Active working days",
#     "avg_hours": "Average working hours",
#     "task_completion_rate": "Task completion rate",
#     "avg_rating": "Customer rating",
#     "activity_stability": "Activity stability",
#     "wallet_txn_freq": "Wallet transaction frequency",
#     "inward_txn_freq": "Incoming transaction frequency",
#     "avg_income": "Average income",
#     "income_volatility": "Income volatility",
#     "income_growth": "Income growth",
#     "savings_ratio": "Savings ratio",
#     "avg_balance": "Average balance",
#     "has_insurance": "Insurance coverage",
#     "emergency_buffer": "Emergency buffer",
#     "loan_utilization": "Loan utilization",
#     "fixed_emi_burden_ratio": "Fixed EMI burden ratio",
#     "credit_inquiries": "Credit inquiries",
#     "delay_score": "Payment delay score",
#     "recent_payment_delays_90": "Recent payment delays (90 days)",
#     "utility_delay_score": "Utility delay score",
#     "recent_missed_rent_3m": "Recent missed rent (3 months)",
#     "rent_consistency_ratio": "Rent consistency ratio",
# }


# def load_explainer_artifacts():
#     global _explainer, _features

#     if _explainer is None:
#         _explainer = joblib.load(EXPLAINER_PATH)

#     if _features is None:
#         _features = joblib.load(FEATURES_PATH)

#     return _explainer, _features


# def explain_prediction(features_dict: Dict[str, float], top_k: int = 3) -> Tuple[List[str], List[str]]:
#     explainer, feature_order = load_explainer_artifacts()

#     row = {feature: float(features_dict.get(feature, 0.0)) for feature in feature_order}
#     X = pd.DataFrame([row], columns=feature_order)

#     explanation = explainer(X)
#     values = explanation.values[0]

#     contributions = list(zip(feature_order, values))

#     positive = sorted([item for item in contributions if item[1] > 0], key=lambda x: x[1], reverse=True)
#     negative = sorted([item for item in contributions if item[1] < 0], key=lambda x: x[1])

#     positive_factors = [
#         f"{FEATURE_LABELS.get(feature, feature)} increased the predicted risk"
#         for feature, _ in positive[:top_k]
#     ]
#     negative_factors = [
#         f"{FEATURE_LABELS.get(feature, feature)} reduced the predicted risk"
#         for feature, _ in negative[:top_k]
#     ]

#     return positive_factors, negative_factors

# from pathlib import Path
# from typing import Dict, List, Tuple

# import joblib
# import pandas as pd

# BASE_DIR = Path(__file__).resolve().parent.parent
# ML_DIR = BASE_DIR / "ml"

# EXPLAINER_PATH = ML_DIR / "explainer.pkl"
# FEATURES_PATH = ML_DIR / "features.pkl"

# _explainer = None
# _features = None


# FEATURE_LABELS = {
#     "age": "Age",
#     "platform_tenure": "Platform tenure",
#     "avg_active_days": "Active working days",
#     "avg_hours": "Average working hours",
#     "task_completion_rate": "Task completion rate",
#     "avg_rating": "Customer rating",
#     "activity_stability": "Activity stability",
#     "wallet_txn_freq": "Wallet transaction frequency",
#     "inward_txn_freq": "Incoming transaction frequency",
#     "avg_income": "Average income",
#     "income_volatility": "Income volatility",
#     "income_growth": "Income growth",
#     "savings_ratio": "Savings ratio",
#     "avg_balance": "Average balance",
#     "has_insurance": "Insurance coverage",
#     "emergency_buffer": "Emergency buffer",
#     "loan_utilization": "Loan utilization",
#     "fixed_emi_burden_ratio": "Fixed EMI burden ratio",
#     "credit_inquiries": "Credit inquiries",
#     "delay_score": "Payment delay score",
#     "recent_payment_delays_90": "Recent payment delays (90 days)",
#     "utility_delay_score": "Utility delay score",
#     "recent_missed_rent_3m": "Recent missed rent (3 months)",
#     "rent_consistency_ratio": "Rent consistency ratio",
# }


# def load_explainer_artifacts():
#     global _explainer, _features

#     if _explainer is None:
#         _explainer = joblib.load(EXPLAINER_PATH)

#     if _features is None:
#         _features = joblib.load(FEATURES_PATH)

#     return _explainer, _features


# def explain_prediction(features_dict: Dict[str, float], top_k: int = 3) -> Tuple[List[str], List[str]]:
#     explainer, feature_order = load_explainer_artifacts()

#     row = {feature: float(features_dict.get(feature, 0.0)) for feature in feature_order}
#     X = pd.DataFrame([row], columns=feature_order)

#     shap_values = explainer.shap_values(X)

#     # For binary classification, TreeExplainer may return a list of 2 arrays
#     if isinstance(shap_values, list):
#         values = shap_values[1][0]
#     else:
#         values = shap_values[0]

#     contributions = list(zip(feature_order, values))

#     positive = sorted(
#         [(feature, value) for feature, value in contributions if value > 0],
#         key=lambda x: x[1],
#         reverse=True,
#     )
#     negative = sorted(
#         [(feature, value) for feature, value in contributions if value < 0],
#         key=lambda x: x[1],
#     )

#     positive_factors = [
#         f"{FEATURE_LABELS.get(feature, feature)} increased the predicted risk"
#         for feature, _ in positive[:top_k]
#     ]
#     negative_factors = [
#         f"{FEATURE_LABELS.get(feature, feature)} reduced the predicted risk"
#         for feature, _ in negative[:top_k]
#     ]

#     return positive_factors, negative_factors


from pathlib import Path
from typing import Dict, List, Tuple

import joblib
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
ML_DIR = BASE_DIR / "ml"

EXPLAINER_PATH = ML_DIR / "explainer.pkl"
FEATURES_PATH = ML_DIR / "features.pkl"

_explainer = None
_features = None


FEATURE_LABELS = {
    "age": "Age",
    "platform_tenure": "Platform tenure",
    "avg_active_days": "Active working days",
    "avg_hours": "Average working hours",
    "task_completion_rate": "Task completion rate",
    "avg_rating": "Customer rating",
    "activity_stability": "Activity stability",
    "wallet_txn_freq": "Wallet transaction frequency",
    "inward_txn_freq": "Incoming transaction frequency",
    "avg_income": "Average income",
    "income_volatility": "Income volatility",
    "income_growth": "Income growth",
    "savings_ratio": "Savings ratio",
    "avg_balance": "Average balance",
    "has_insurance": "Insurance coverage",
    "emergency_buffer": "Emergency buffer",
    "loan_utilization": "Loan utilization",
    "fixed_emi_burden_ratio": "Fixed EMI burden ratio",
    "credit_inquiries": "Credit inquiries",
    "delay_score": "Payment delay score",
    "recent_payment_delays_90": "Recent payment delays (90 days)",
    "utility_delay_score": "Utility delay score",
    "recent_missed_rent_3m": "Recent missed rent (3 months)",
    "rent_consistency_ratio": "Rent consistency ratio",
}


def load_explainer_artifacts():
    global _explainer, _features

    if _explainer is None:
        _explainer = joblib.load(EXPLAINER_PATH)

    if _features is None:
        _features = joblib.load(FEATURES_PATH)

    return _explainer, _features


def _extract_1d_shap_values(shap_values) -> np.ndarray:
    """
    Normalize SHAP output to a 1D array of length n_features.
    Handles different SHAP versions / model output formats.
    """
    arr = np.array(shap_values)

    # Common cases:
    # (1, n_features)
    if arr.ndim == 2 and arr.shape[0] == 1:
        return arr[0]

    # (1, n_features, 2) or (1, 2, n_features)
    if arr.ndim == 3:
        # Case: (1, n_features, 2) -> choose class 1
        if arr.shape[0] == 1 and arr.shape[2] == 2:
            return arr[0, :, 1]

        # Case: (1, 2, n_features) -> choose class 1
        if arr.shape[0] == 1 and arr.shape[1] == 2:
            return arr[0, 1, :]

    # Fallback
    return arr.flatten()


def explain_prediction(features_dict: Dict[str, float], top_k: int = 3) -> Tuple[List[str], List[str]]:
    explainer, feature_order = load_explainer_artifacts()

    row = {feature: float(features_dict.get(feature, 0.0)) for feature in feature_order}
    X = pd.DataFrame([row], columns=feature_order)

    shap_values = explainer.shap_values(X)
    values = _extract_1d_shap_values(shap_values)

    contributions = list(zip(feature_order, values.tolist()))

    positive = sorted(
        [(feature, float(value)) for feature, value in contributions if float(value) > 0],
        key=lambda x: x[1],
        reverse=True,
    )
    negative = sorted(
        [(feature, float(value)) for feature, value in contributions if float(value) < 0],
        key=lambda x: x[1],
    )

    positive_factors = [
        f"{FEATURE_LABELS.get(feature, feature)} increased the predicted risk"
        for feature, _ in positive[:top_k]
    ]
    negative_factors = [
        f"{FEATURE_LABELS.get(feature, feature)} reduced the predicted risk"
        for feature, _ in negative[:top_k]
    ]

    return positive_factors, negative_factors