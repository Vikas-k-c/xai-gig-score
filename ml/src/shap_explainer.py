from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Any

import joblib
import numpy as np
import pandas as pd
import shap

from utils import ARTIFACTS_DIR, FEATURE_COLUMNS, ensure_artifacts_dir


def create_shap_explainer(model, background_data: np.ndarray | pd.DataFrame | None = None):
    """
    Creates the appropriate SHAP explainer based on model type.
    For tree models, TreeExplainer is efficient and accurate.
    For linear models, LinearExplainer needs background data.
    """
    model_name = model.__class__.__name__.lower()

    if "randomforest" in model_name or "xgb" in model_name or "boost" in model_name:
        return shap.TreeExplainer(model)

    if "logistic" in model_name or "linear" in model_name:
        if background_data is None:
            background_data = np.zeros((1, len(FEATURE_COLUMNS)))
        return shap.LinearExplainer(model, background_data)

    return shap.Explainer(model)


def save_explainer(explainer, path: Path | str | None = None) -> Path:
    ensure_artifacts_dir()
    out_path = Path(path) if path else ARTIFACTS_DIR / "explainer.pkl"
    joblib.dump(explainer, out_path)
    return out_path


def load_explainer(path: Path | str | None = None):
    explainer_path = Path(path) if path else ARTIFACTS_DIR / "explainer.pkl"
    return joblib.load(explainer_path)


def explain_single_instance(
    explainer,
    feature_row: pd.DataFrame,
    top_k: int = 3
) -> Dict[str, Any]:
    """
    feature_row must be a 1-row DataFrame with the same feature order as training.
    """
    if not isinstance(feature_row, pd.DataFrame):
        raise TypeError("feature_row must be a pandas DataFrame.")

    if feature_row.shape[0] != 1:
        raise ValueError("feature_row must contain exactly one row.")

    shap_values = explainer(feature_row)

    # For binary classification, SHAP returns one explanation row.
    values = shap_values.values[0]
    feature_names = feature_row.columns.tolist()

    contributions = list(zip(feature_names, values))
    positive = sorted([x for x in contributions if x[1] > 0], key=lambda x: x[1], reverse=True)
    negative = sorted([x for x in contributions if x[1] < 0], key=lambda x: x[1])

    return {
        "positive_factors": [
            {"feature": f, "contribution": float(v)} for f, v in positive[:top_k]
        ],
        "negative_factors": [
            {"feature": f, "contribution": float(v)} for f, v in negative[:top_k]
        ],
    }