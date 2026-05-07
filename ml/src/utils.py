from __future__ import annotations



from pathlib import Path
from typing import Tuple, List


import pandas as pd



PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "final_dataset.csv"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"


FEATURE_COLUMNS: List[str] = [
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
    # Phase 1: Gig-worker-specific credit assessment features
    "gig_creditworthiness_score",  # CORRECTED: Replaces CIBIL with gig-specific score (0-100)
    "earned_trust_score",           # How consistently worker delivered quality work (0-1)
    "income_reliability_ratio",     # Income stability + growth indicator (0-1)
    "payment_behavior_consistency", # Payment timeliness consistency (0-1)
]

TARGET_COLUMN = "default"


def ensure_artifacts_dir() -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)


def load_dataset(csv_path: Path | str = DATA_PATH) -> pd.DataFrame:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at: {path}")
    df = pd.read_csv(path)
    return df


def validate_dataset(df: pd.DataFrame) -> None:
    missing_cols = [c for c in FEATURE_COLUMNS + [TARGET_COLUMN] if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Dataset is missing required columns: {missing_cols}")

    if df[FEATURE_COLUMNS].isnull().any().any():
        null_cols = df[FEATURE_COLUMNS].columns[df[FEATURE_COLUMNS].isnull().any()].tolist()
        raise ValueError(f"Dataset has null values in feature columns: {null_cols}")

    if df[TARGET_COLUMN].isnull().any():
        raise ValueError("Target column contains null values.")

    unique_targets = sorted(df[TARGET_COLUMN].unique().tolist())
    if any(v not in [0, 1] for v in unique_targets):
        raise ValueError(f"Target must be binary (0/1). Found: {unique_targets}")


def get_X_y(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    validate_dataset(df)
    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].copy()
    return X, y