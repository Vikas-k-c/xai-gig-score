from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score

try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

try:
    from imblearn.over_sampling import SMOTE
    SMOTE_AVAILABLE = True
except ImportError:
    SMOTE_AVAILABLE = False

from utils import (
    load_dataset,
    get_X_y,
    FEATURE_COLUMNS,
    ARTIFACTS_DIR,
    ensure_artifacts_dir,
)
from evaluate import evaluate_classifier
from shap_explainer import create_shap_explainer, save_explainer
from feature_engineering import engineer_features, get_all_features_with_engineered


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
        n_jobs=1,
        class_weight="balanced",
    )


def build_logistic_regression() -> LogisticRegression:
    return LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        solver="liblinear",
        random_state=RANDOM_STATE,
    )


def build_xgboost(scale_pos_weight: float = 1.0):
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
        scale_pos_weight=scale_pos_weight,  # PHASE 2: Weighted minority class
        n_jobs=1,
    )


def find_optimal_thresholds(model, X_test, y_test) -> dict:
    """
    Find optimal thresholds for three operating points:
    - conservative: maximize recall (catch defaults)
    - balanced: maximize F1 (balance precision and recall)
    - strict: maximize precision (minimize false positives)
    
    Returns dict with three threshold strategies and their metrics.
    """
    
    if not hasattr(model, "predict_proba"):
        raise ValueError("Model must support predict_proba()")
    
    y_prob = model.predict_proba(X_test)[:, 1]
    
    # Test 100 candidate thresholds
    thresholds = np.linspace(0.1, 0.9, 100)
    threshold_metrics = []
    
    for threshold in thresholds:
        y_pred = (y_prob >= threshold).astype(int)
        
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        threshold_metrics.append({
            "threshold": float(threshold),
            "precision": float(precision),
            "recall": float(recall),
            "f1": float(f1),
        })
    
    # Select three thresholds for different use cases
    # 1. Conservative: maximize recall at or above 0.75 recall
    conservative = max(
        [m for m in threshold_metrics if m["recall"] >= 0.75],
        key=lambda x: x["recall"],
        default=threshold_metrics[0]
    )
    
    # 2. Balanced: maximize F1 score
    balanced = max(threshold_metrics, key=lambda x: x["f1"])
    
    # 3. Strict: maximize precision at or above 0.70 precision
    strict = max(
        [m for m in threshold_metrics if m["precision"] >= 0.70],
        key=lambda x: x["precision"],
        default=min(threshold_metrics, key=lambda x: x["threshold"])
    )
    
    # 4. Operating points aligned with business targets
    best_precision_at_recall_75 = max(
        [m for m in threshold_metrics if m["recall"] >= 0.75],
        key=lambda x: x["precision"],
        default=threshold_metrics[0]
    )
    best_recall_at_precision_68 = max(
        [m for m in threshold_metrics if m["precision"] >= 0.68],
        key=lambda x: x["recall"],
        default=threshold_metrics[-1]
    )

    target_both = next((m for m in threshold_metrics if m["recall"] >= 0.75 and m["precision"] >= 0.68), None)

    def target_penalty(entry: dict) -> float:
        recall_gap = max(0.0, 0.75 - entry["recall"])
        precision_gap = max(0.0, 0.68 - entry["precision"])
        return recall_gap ** 2 + precision_gap ** 2

    best_compromise = min(threshold_metrics, key=target_penalty)
    best_compromise["distance_to_target"] = float(target_penalty(best_compromise))

    return {
        "conservative": conservative,
        "balanced": balanced,
        "strict": strict,
        "best_precision_at_recall_75": best_precision_at_recall_75,
        "best_recall_at_precision_68": best_recall_at_precision_68,
        "target_recall_precision_met": target_both is not None,
        "target_threshold_if_met": target_both,
        "best_compromise": best_compromise,
        "all_thresholds": threshold_metrics,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Train gig worker credit scoring models")
    parser.add_argument(
        "--random_state",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)",
    )
    parser.add_argument(
        "--use_smote",
        action="store_true",
        help="Apply SMOTE to the training data to balance classes when appropriate.",
    )
    args = parser.parse_args()

    ensure_artifacts_dir()

    print("Loading dataset...")
    df = load_dataset()
    X, y = get_X_y(df)

    print(f"Dataset shape: {df.shape}")
    print(f"Feature count: {len(FEATURE_COLUMNS)}")
    
    # PHASE 2: Class distribution analysis
    default_rate = y.mean()
    n_default = (y == 1).sum()
    n_non_default = (y == 0).sum()
    print(f"Default rate: {default_rate:.2%}")
    print(f"Class distribution: {n_non_default} non-default, {n_default} default")
    
    # Calculate scale_pos_weight for XGBoost (inverse of class ratio)
    scale_pos_weight = n_non_default / n_default if n_default > 0 else 1.0
    xgb_scale_pos_weight = 1.0 if args.use_smote else scale_pos_weight
    print(f"Scale_pos_weight for XGBoost: {scale_pos_weight:.2f}")
    if args.use_smote:
        if SMOTE_AVAILABLE:
            print("Using SMOTE; XGBoost scale_pos_weight will be set to 1.0 for balanced data.")
        else:
            print("Warning: --use_smote requested but imbalanced-learn is not installed.")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=args.random_state,
        stratify=y,
    )
    
    # PHASE 3: Feature Engineering - create interaction terms
    print("\nPhase 3: Applying feature engineering...")
    X_train = engineer_features(X_train)
    X_test = engineer_features(X_test)
    print(f"Features after engineering: {X_train.shape[1]} (was {len(FEATURE_COLUMNS)})")
    
    # Update feature list for later use
    all_feature_names = get_all_features_with_engineered(FEATURE_COLUMNS)
    print(f"Total feature count with engineered features: {len(all_feature_names)}")
    
    # PHASE 2: Apply SMOTE on training set only if explicitly requested
    if args.use_smote:
        if SMOTE_AVAILABLE:
            print("\nApplying SMOTE for class imbalance handling...")
            smote = SMOTE(random_state=args.random_state, k_neighbors=5)
            X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
            print(f"After SMOTE: {(y_train_resampled == 0).sum()} non-default, {(y_train_resampled == 1).sum()} default")
            X_train, y_train = X_train_resampled, y_train_resampled
        else:
            print("\nWarning: SMOTE requested but imbalanced-learn is not installed; proceeding without SMOTE.")

    X_train = X_train[all_feature_names]
    X_test = X_test[all_feature_names]

    candidates = {
        "random_forest": build_random_forest(),
        "logistic_regression": build_logistic_regression(),
    }

    if XGBOOST_AVAILABLE:
        candidates["xgboost"] = build_xgboost(scale_pos_weight=xgb_scale_pos_weight)
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
                "pr_auc": metrics["pr_auc"],  # NEW: Precision-Recall AUC
            },
            indent=2
        ))

    # Primary selection criterion: ROC-AUC (discrimination ability), then PR-AUC, then F1
    best_model_name = sorted(
        results.keys(),
        key=lambda name: (
            results[name]["roc_auc"],
            results[name].get("pr_auc", 0),
            results[name]["f1"]
        ),
        reverse=True
    )[0]

    best_model = trained_models[best_model_name]
    best_metrics = results[best_model_name]

    print(f"\nBest model selected: {best_model_name}")
    print(json.dumps({
        "accuracy": best_metrics["accuracy"],
        "precision": best_metrics["precision"],
        "recall": best_metrics["recall"],
        "f1": best_metrics["f1"],
        "roc_auc": best_metrics["roc_auc"],
        "pr_auc": best_metrics["pr_auc"],
    }, indent=2))

    # Find optimal thresholds for different operating points
    print("\nFinding optimal thresholds...")
    threshold_strategies = find_optimal_thresholds(best_model, X_test, y_test)
    
    print("\nThreshold strategies:")
    for strategy_name in ["conservative", "balanced", "strict"]:
        strat = threshold_strategies[strategy_name]
        print(f"\n  {strategy_name.upper()}:")
        print(f"    Threshold: {strat['threshold']:.3f}")
        print(f"    Precision: {strat['precision']:.3f}")
        print(f"    Recall:    {strat['recall']:.3f}")
        print(f"    F1 Score:  {strat['f1']:.3f}")
    best_precision_at_recall = threshold_strategies["best_precision_at_recall_75"]
    best_recall_at_precision = threshold_strategies["best_recall_at_precision_68"]
    print("\nBusiness-targeted thresholds:")
    print(f"  BEST PRECISION @ RECALL>=0.75: threshold={best_precision_at_recall['threshold']:.3f}, precision={best_precision_at_recall['precision']:.3f}, recall={best_precision_at_recall['recall']:.3f}")
    print(f"  BEST RECALL @ PRECISION>=0.68: threshold={best_recall_at_precision['threshold']:.3f}, precision={best_recall_at_precision['precision']:.3f}, recall={best_recall_at_precision['recall']:.3f}")
    if threshold_strategies["target_recall_precision_met"]:
        print("  TARGET MET: A threshold exists that meets both recall >= 0.75 and precision >= 0.68.")
    else:
        compromise = threshold_strategies["best_compromise"]
        print("  TARGET NOT MET: Best compromise threshold:")
        print(f"    threshold={compromise['threshold']:.3f}, precision={compromise['precision']:.3f}, recall={compromise['recall']:.3f}, distance_to_target={compromise['distance_to_target']:.4f}")

    model_path = ARTIFACTS_DIR / "model.pkl"
    features_path = ARTIFACTS_DIR / "features.pkl"
    metrics_path = ARTIFACTS_DIR / "metrics.json"
    thresholds_path = ARTIFACTS_DIR / "thresholds.json"

    print("\nSaving artifacts...")
    joblib.dump(best_model, model_path)

    metrics_payload = {
        "best_model": best_model_name,
        "all_results": results,
        "threshold_strategies": threshold_strategies,  # NEW: Store all threshold info
    }
    save_json(metrics_payload, metrics_path)
    
    # Also save thresholds separately for easy access by scoring service
    thresholds_only = {
        "conservative_threshold": threshold_strategies["conservative"]["threshold"],
        "balanced_threshold": threshold_strategies["balanced"]["threshold"],
        "strict_threshold": threshold_strategies["strict"]["threshold"],
        "best_precision_at_recall_75_threshold": threshold_strategies["best_precision_at_recall_75"]["threshold"],
        "best_recall_at_precision_68_threshold": threshold_strategies["best_recall_at_precision_68"]["threshold"],
        "target_recall_precision_met": threshold_strategies["target_recall_precision_met"],
    }
    if threshold_strategies["target_recall_precision_met"]:
        thresholds_only["target_threshold"] = threshold_strategies["target_threshold_if_met"]["threshold"]
    else:
        thresholds_only["best_compromise_threshold"] = threshold_strategies["best_compromise"]["threshold"]
    save_json(thresholds_only, thresholds_path)

    joblib.dump(all_feature_names, features_path)

    print("Creating SHAP explainer...")
    explainer = create_shap_explainer(best_model, background_data=X_train)
    save_explainer(explainer)

    print("\nArtifacts saved successfully:")
    print(f"- {model_path}")
    print(f"- {features_path}")
    print(f"- {ARTIFACTS_DIR / 'explainer.pkl'}")
    print(f"- {metrics_path}")
    print(f"- {thresholds_path} (NEW: Multi-threshold strategies)")


if __name__ == "__main__":
    main()
