#!/usr/bin/env python3
"""
Generate synthetic training dataset for gig worker credit scoring.

This script creates a balanced synthetic dataset with 5 new high-signal features
that have meaningful correlation with the default target variable.

Usage:
    python generate_dataset.py --n_samples 2000 --output_path ../data/final_dataset.csv
"""

import sys
import random
import argparse
from pathlib import Path
from typing import Tuple, List

import pandas as pd
import numpy as np

# Add backend to path for mock_data import
backend_path = Path(__file__).resolve().parent.parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.services.mock_data import generate_mock_platform_features, SUPPORTED_PLATFORMS


def calculate_recommended_feature_values(features: dict) -> dict:
    """Calculate the recommended super-features from a generated feature row."""
    income_volatility = max(float(features["income_volatility"]), 1e-6)
    activity_hours = max(float(features["avg_hours"]) * float(features["avg_active_days"]), 1e-6)

    return {
        "income_stability_buffer": (
            float(features["avg_balance"])
            * float(features["emergency_buffer"])
            / income_volatility
        ),
        "platform_earnings_density": float(features["avg_income"]) / activity_hours,
        "behavioral_discipline_score": (
            float(features["rent_consistency_ratio"]) * 0.7
            + float(features["payment_behavior_consistency"]) * 0.3
            - float(features["delay_score"])
        ),
        "trust_growth_multiplier": (
            float(features["earned_trust_score"]) * (1.0 + float(features["income_growth"]))
        ),
        "liquidity_debt_stress_index": (
            float(features["fixed_emi_burden_ratio"])
            * float(features["avg_income"])
            / (float(features["avg_balance"]) + 1.0)
        ),
    }


def calculate_default_risk_score(features: dict) -> float:
    """
    Generate a continuous default risk score based on features with meaningful correlation.
    
    Higher default risk is influenced by:
    - Lower gig_creditworthiness_score (earned less trust from platform)
    - Lower earned_trust_score (inconsistent quality work)
    - Lower income_reliability_ratio (volatile/declining income)
    - Lower payment_behavior_consistency (late payments)
    - Higher delay_score, credit_inquiries
    - Lower activity_stability, savings_ratio
    
    - Lower income stability buffer, lower behavioral discipline, lower trust growth
    - Higher liquidity-to-debt stress
    """
    
    # Calculate risk score from multiple factors
    # Each factor normalized to 0-1 range
    
    # Gig creditworthiness (0-100 score): lower score = higher risk
    creditworthiness_risk = (100.0 - features["gig_creditworthiness_score"]) / 100.0
    creditworthiness_risk = max(0.0, min(1.0, creditworthiness_risk))
    
    # Earned trust: lower trust = higher risk
    trust_risk = 1.0 - features["earned_trust_score"]
    
    # Income reliability: lower reliability = higher risk
    reliability_risk = 1.0 - features["income_reliability_ratio"]
    
    # Payment consistency: lower consistency = higher risk
    payment_risk = 1.0 - features["payment_behavior_consistency"]
    
    # Additional risk factors from original features
    delay_risk = features["delay_score"] / 5.0
    inquiry_risk = features["credit_inquiries"] / 10.0
    stability_risk = 1.0 - features["activity_stability"]
    volatility_risk = features["income_volatility"] / 0.9

    recommended = calculate_recommended_feature_values(features)
    income_stability_buffer_risk = 1.0 - min(
        recommended["income_stability_buffer"] / max(features["avg_income"], 1.0),
        1.0,
    )
    earnings_density_risk = 1.0 - min(recommended["platform_earnings_density"] / 250.0, 1.0)
    behavioral_discipline_risk = 1.0 - max(
        0.0,
        min((recommended["behavioral_discipline_score"] + 5.0) / 6.0, 1.0),
    )
    trust_growth_risk = 1.0 - max(
        0.0,
        min(recommended["trust_growth_multiplier"] / 1.8, 1.0),
    )
    liquidity_debt_stress_risk = min(recommended["liquidity_debt_stress_index"] / 3.0, 1.0)
    
    # Weighted combination of raw and engineered risk factors.
    total_risk = (
        creditworthiness_risk * 0.12 +
        trust_risk * 0.10 +
        reliability_risk * 0.10 +
        payment_risk * 0.10 +
        delay_risk * 0.08 +
        inquiry_risk * 0.06 +
        stability_risk * 0.04 +
        volatility_risk * 0.04 +
        income_stability_buffer_risk * 0.12 +
        earnings_density_risk * 0.05 +
        behavioral_discipline_risk * 0.16 +
        trust_growth_risk * 0.07 +
        liquidity_debt_stress_risk * 0.06
    )
    
    # Add modest noise so the task is realistic while preserving a clear signal.
    total_risk += random.gauss(0, 0.015)
    total_risk = max(0.0, min(1.0, total_risk))

    return total_risk


def generate_default_label(features: dict, threshold: float = 0.5) -> int:
    """Generate a default label from the continuous risk score."""
    return 1 if calculate_default_risk_score(features) > threshold else 0


def generate_synthetic_dataset(
    n_samples: int = 2000,
    random_state: int = 42,
    default_rate: float = 0.40,
) -> pd.DataFrame:
    """
    Generate synthetic gig worker dataset with strong predictive signals for mini project.
    
    Args:
        n_samples: Number of samples to generate
        random_state: Random seed for reproducibility
        default_rate: Target proportion of defaults (0-1)
    
    Returns:
        DataFrame with features and default target
    """
    
    random.seed(random_state)
    np.random.seed(random_state)
    
    records = []
    platforms = list(SUPPORTED_PLATFORMS)
    
    print(f"Generating {n_samples} synthetic samples...")
    
    for i in range(n_samples):
        if (i + 1) % 500 == 0:
            print(f"  Generated {i + 1} / {n_samples}")
        
        # Randomly select 1-3 platforms for this user
        n_platforms = random.randint(1, 3)
        selected_platforms = random.sample(platforms, n_platforms)
        
        # Aggregate features across platforms
        platform_features = []
        for platform in selected_platforms:
            features = generate_mock_platform_features(platform)
            platform_features.append(features)
        
        # Average features across platforms (for multi-platform users)
        aggregated = {}
        for key in platform_features[0].keys():
            if isinstance(platform_features[0][key], bool):
                # For boolean features, use logical OR (if any platform has it)
                aggregated[key] = any(f[key] for f in platform_features)
            else:
                # For numeric features, use mean
                aggregated[key] = np.mean([f[key] for f in platform_features])
        
        aggregated["default_risk_score"] = calculate_default_risk_score(aggregated)
        records.append(aggregated)
    
    df = pd.DataFrame(records)

    risk_threshold = float(df["default_risk_score"].quantile(1.0 - default_rate))
    df["default"] = (df["default_risk_score"] >= risk_threshold).astype(int)
    df = df.drop(columns=["default_risk_score"])
    
    # Check actual default rate
    actual_default_rate = df["default"].mean()
    print(f"\nActual default rate: {actual_default_rate:.2%}")
    print(f"Target default rate: {default_rate:.2%}")
    
    # Calculate feature correlations with default
    print("\nFeature correlations with default:")
    feature_cols = [c for c in df.columns if c != "default"]
    correlations = []
    for col in feature_cols:
        if df[col].dtype in [np.int64, np.float64]:
            corr = df[col].corr(df["default"])
            correlations.append((col, corr))
            if abs(corr) > 0.15:  # Print features with meaningful correlation
                print(f"  {col:30s}: {corr:7.4f}")
    
    correlations.sort(key=lambda x: abs(x[1]), reverse=True)
    print(f"\nTop 10 correlations:")
    for col, corr in correlations[:10]:
        print(f"  {col:30s}: {corr:7.4f}")
    
    return df


def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic gig worker credit scoring dataset"
    )
    parser.add_argument(
        "--n_samples",
        type=int,
        default=2000,
        help="Number of samples to generate (default: 2000)",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="../data/final_dataset.csv",
        help="Output CSV path (default: ../data/final_dataset.csv)",
    )
    parser.add_argument(
        "--random_state",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)",
    )
    
    args = parser.parse_args()
    
    # Generate dataset
    df = generate_synthetic_dataset(
        n_samples=args.n_samples,
        random_state=args.random_state,
    )
    
    # Create output directory if needed
    output_path = Path(args.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save dataset
    df.to_csv(output_path, index=False)
    print(f"\nDataset saved to: {output_path}")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")


if __name__ == "__main__":
    main()
