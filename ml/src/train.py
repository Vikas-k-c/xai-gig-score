from __future__ import annotations

import json
from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

from utils import (
    load_dataset,
    get_X_y,
    FEATURE_COLUMNS,
    ARTIFACTS_DIR,
    ensure_artifacts_dir,
)
from evaluate import evaluate_classifier
from shap_explainer import create_shap_explainer, save_explainer


RANDOM_STATE = 42
TEST_SIZE = 0.2


def save_json(data: dict, path: Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def build_random_forest() -> RandomForestClassifier:
    return RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        class_weight="balanced",
    )


def build_xgboost():
    if not XGBOOST_AVAILABLE:
        raise ImportError("xgboost is not installed.")

    return XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        objective="binary:logistic",
        eval_metric="logloss",
        random_state=RANDOM_STATE,
        reg_lambda=1.0,
        n_jobs=-1,
    )


def main() -> None:
    ensure_artifacts_dir()

    print("Loading dataset...")
    df = load_dataset()
    X, y = get_X_y(df)

    print(f"Dataset shape: {df.shape}")
    print(f"Feature count: {len(FEATURE_COLUMNS)}")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    candidates = {
        "random_forest": build_random_forest(),
    }

    if XGBOOST_AVAILABLE:
        candidates["xgboost"] = build_xgboost()
    else:
        print("xgboost not available, skipping XGBoost training.")

    results = {}
    trained_models = {}

    for name, model in candidates.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        metrics = evaluate_classifier(model, X_test, y_test)
        results[name] = metrics
        trained_models[name] = model

        print(f"{name} metrics:")
        print(json.dumps(
            {
                "accuracy": metrics["accuracy"],
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "f1": metrics["f1"],
                "roc_auc": metrics["roc_auc"],
            },
            indent=2
        ))

    # Primary selection criterion: ROC-AUC, then F1
    best_model_name = sorted(
        results.keys(),
        key=lambda name: (results[name]["roc_auc"], results[name]["f1"]),
        reverse=True
    )[0]

    best_model = trained_models[best_model_name]
    best_metrics = results[best_model_name]

    print(f"\nBest model selected: {best_model_name}")
    print(json.dumps(best_metrics, indent=2))

    model_path = ARTIFACTS_DIR / "model.pkl"
    features_path = ARTIFACTS_DIR / "features.pkl"
    metrics_path = ARTIFACTS_DIR / "metrics.json"

    print("\nSaving artifacts...")
    joblib.dump(best_model, model_path)
    joblib.dump(FEATURE_COLUMNS, features_path)

    metrics_payload = {
        "best_model": best_model_name,
        "all_results": results,
    }
    save_json(metrics_payload, metrics_path)

    print("Creating SHAP explainer...")
    explainer = create_shap_explainer(best_model)
    save_explainer(explainer)

    print("\nArtifacts saved successfully:")
    print(f"- {model_path}")
    print(f"- {features_path}")
    print(f"- {ARTIFACTS_DIR / 'explainer.pkl'}")
    print(f"- {metrics_path}")


if __name__ == "__main__":
    main()