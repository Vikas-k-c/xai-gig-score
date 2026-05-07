import random


SUPPORTED_PLATFORMS = {
    "uber",
    "zomato",
    "swiggy",
    "rapido",
    "freelance",
    "delivery",
    "ride-hailing",
    "ola",
    "upwork",
}


def generate_mock_platform_features(platform_name: str) -> dict:
    platform = platform_name.strip().lower()

    if platform not in SUPPORTED_PLATFORMS:
        raise ValueError(f"Unsupported platform: {platform_name}")

    # Slight platform-specific tendencies
    if platform in {"uber", "rapido", "ride-hailing"}:
        income_base = (18000, 42000)
        active_days = (18, 29)
        avg_hours = (5.0, 11.0)
    elif platform in {"zomato", "swiggy", "delivery"}:
        income_base = (15000, 35000)
        active_days = (20, 30)
        avg_hours = (5.0, 12.0)
    else:  # freelance
        income_base = (12000, 50000)
        active_days = (10, 26)
        avg_hours = (3.0, 10.0)

    avg_income = random.uniform(*income_base)
    savings_ratio = random.uniform(0.05, 0.45)
    avg_balance = avg_income * random.uniform(0.10, 0.60)
    
    # Generate core features first
    task_completion_rate = round(random.uniform(0.70, 0.99), 3)
    avg_rating = round(random.uniform(3.5, 5.0), 2)
    activity_stability = round(random.uniform(0.20, 1.00), 3)
    avg_active_days = round(random.uniform(*active_days), 2)
    income_growth = round(random.uniform(-0.30, 0.80), 3)
    delay_score = round(random.uniform(0, 5), 3)
    income_volatility = round(random.uniform(0.05, 0.90), 3)
    loan_utilization = round(random.uniform(0.05, 0.95), 3)
    credit_inquiries = round(random.uniform(0, 10), 2)
    recent_payment_delays_90 = round(random.uniform(0, 6), 2)

    data = {
        "age": random.randint(21, 50),
        "platform_tenure": random.randint(1, 60),
        "avg_active_days": avg_active_days,
        "avg_hours": round(random.uniform(*avg_hours), 2),
        "task_completion_rate": task_completion_rate,
        "avg_rating": avg_rating,
        "activity_stability": activity_stability,
        "wallet_txn_freq": round(random.uniform(5, 100), 2),
        "inward_txn_freq": round(random.uniform(5, 60), 2),
        "avg_income": round(avg_income, 2),
        "income_volatility": income_volatility,
        "income_growth": income_growth,
        "savings_ratio": round(savings_ratio, 3),
        "avg_balance": round(avg_balance, 2),
        "has_insurance": random.choice([True, False]),
        "emergency_buffer": random.choice([True, False]),
        "loan_utilization": loan_utilization,
        "fixed_emi_burden_ratio": round(random.uniform(0.00, 0.80), 3),
        "credit_inquiries": credit_inquiries,
        "delay_score": delay_score,
        "recent_payment_delays_90": recent_payment_delays_90,
        "utility_delay_score": round(random.uniform(0, 5), 3),
        "recent_missed_rent_3m": round(random.uniform(0, 3), 2),
        "rent_consistency_ratio": round(random.uniform(0.30, 1.00), 3),
    }
    
    # NEW PHASE 1 FEATURES: High-signal features for gig worker credit assessment
    # These measure gig-worker-specific creditworthiness (not traditional CIBIL)
    
    # CORRECTED: gig_creditworthiness_score (replaces credit_bureau_score)
    # This is a GIG-WORKER-SPECIFIC credit score (0-100 scale)
    # Measures: "Has this gig worker earned trust through platform activities?"
    # Based on: task completion reliability, rating consistency, activity stability
    
    # Calculate from gig platform behavioral signals
    completion_quality = task_completion_rate * (avg_rating / 5.0)  # High completion + high rating = trustworthy
    activity_consistency = activity_stability * (avg_active_days / 30.0)  # Active + consistent = reliable
    
    # Composite: Trust earned from platform behavior (0-100 scale)
    gig_creditworthiness_score = round(
        (completion_quality * 0.5 + activity_consistency * 0.5) * 100,
        1
    )
    gig_creditworthiness_score = max(0.0, min(100.0, gig_creditworthiness_score))  # Clamp to 0-100
    data["gig_creditworthiness_score"] = gig_creditworthiness_score
    
    # earned_trust_score: How consistently has worker delivered quality work?
    # Range: 0-1, where 1 = perfect consistent high-quality work
    earned_trust_score = round(
        (task_completion_rate * 0.6 + (avg_rating - 3.5) / 1.5 * 0.4),
        3
    )
    earned_trust_score = max(0.0, min(1.0, earned_trust_score))
    data["earned_trust_score"] = earned_trust_score
    
    # income_reliability_ratio: How stable and growing is income?
    # Low volatility + positive growth = reliable earner
    # Range: 0-1, where higher = more reliable income
    growth_factor = max(0.0, min(1.0, (income_growth + 0.3) / 1.1))  # Normalize -0.3 to 0.8 range
    income_reliability_ratio = round(
        ((1.0 - income_volatility) * 0.6 + growth_factor * 0.4),
        3
    )
    data["income_reliability_ratio"] = income_reliability_ratio
    
    # payment_behavior_consistency: High consistency = lower default risk
    # Based on inverse of delays (consistent/low delays = high consistency)
    # Combine delay_score, recent_payment_delays, and utility_delay consistency
    consistency_value = 1.0 - (delay_score / 5.0) * 0.4 - (recent_payment_delays_90 / 6.0) * 0.6
    payment_behavior_consistency = round(max(0.0, min(1.0, consistency_value)), 3)
    data["payment_behavior_consistency"] = payment_behavior_consistency

    return data