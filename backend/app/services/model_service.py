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

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
ML_DIR = BASE_DIR / "ml"

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

    row = {feature: float(features_dict.get(feature, 0.0)) for feature in feature_order}
    X = pd.DataFrame([row], columns=feature_order)

    probability = float(model.predict_proba(X)[0][1])
    predicted_class = float(model.predict(X)[0])

    return probability, predicted_class