# from pathlib import Path
# from typing import Dict, Tuple

# import joblib
# import numpy as np

# from .feature_engineering import FEATURE_COLUMNS


# BASE_DIR = Path(__file__).resolve().parent.parent
# ML_DIR = BASE_DIR / "ml"

# MODEL_PATH = ML_DIR / "model.pkl"
# FEATURES_PATH = ML_DIR / "features.pkl"


# _model = None
# _features = None


# def load_model_artifacts():
#     global _model, _features

#     if _model is None:
#         _model = joblib.load(MODEL_PATH)

#     if _features is None:
#         _features = joblib.load(FEATURES_PATH)

#     return _model, _features


# def predict_default_probability(features_dict: Dict[str, float]) -> Tuple[float, float]:
#     model, feature_order = load_model_artifacts()

#     row = [float(features_dict.get(feature, 0.0)) for feature in feature_order]
#     X = np.array(row, dtype=float).reshape(1, -1)

#     probability = float(model.predict_proba(X)[0][1])
#     predicted_class = float(model.predict(X)[0])

#     return probability, predicted_class

from pathlib import Path
from typing import Dict, Tuple
import sys

import joblib
import pandas as pd

from .feature_engineering import FEATURE_COLUMNS as BASE_FEATURE_COLUMNS

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent.parent
ML_DIR = PROJECT_ROOT / "ml" / "artifacts"
ML_SRC_DIR = PROJECT_ROOT / "ml" / "src"
if str(ML_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(ML_SRC_DIR))

try:
    from feature_engineering import engineer_features as engineer_ml_features
except ImportError as exc:
    raise ImportError(
        f"Unable to import the ML feature engineering module from {ML_SRC_DIR}. "
        "Ensure the ml/src folder exists and contains feature_engineering.py."
    ) from exc

MODEL_PATH = ML_DIR / "model.pkl"
FEATURES_PATH = ML_DIR / "features.pkl"

_model = None
_features = None


def load_model_artifacts():
    global _model, _features

    if _model is None:
        _model = joblib.load(MODEL_PATH)

    if _features is None:
        _features = joblib.load(FEATURES_PATH)

    return _model, _features


def predict_default_probability(features_dict: Dict[str, float]) -> Tuple[float, float]:
    model, feature_order = load_model_artifacts()

    base_row = {feature: float(features_dict.get(feature, 0.0)) for feature in BASE_FEATURE_COLUMNS}
    X_base = pd.DataFrame([base_row], columns=BASE_FEATURE_COLUMNS)
    X = engineer_ml_features(X_base)
    X = X[feature_order]

    probability = float(model.predict_proba(X)[0][1])
    predicted_class = float(model.predict(X)[0])

    return probability, predicted_class
