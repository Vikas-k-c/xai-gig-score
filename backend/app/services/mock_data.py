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

    data = {
        "age": random.randint(21, 50),
        "platform_tenure": random.randint(1, 60),
        "avg_active_days": round(random.uniform(*active_days), 2),
        "avg_hours": round(random.uniform(*avg_hours), 2),
        "task_completion_rate": round(random.uniform(0.70, 0.99), 3),
        "avg_rating": round(random.uniform(3.5, 5.0), 2),
        "activity_stability": round(random.uniform(0.20, 1.00), 3),
        "wallet_txn_freq": round(random.uniform(5, 100), 2),
        "inward_txn_freq": round(random.uniform(5, 60), 2),
        "avg_income": round(avg_income, 2),
        "income_volatility": round(random.uniform(0.05, 0.90), 3),
        "income_growth": round(random.uniform(-0.30, 0.80), 3),
        "savings_ratio": round(savings_ratio, 3),
        "avg_balance": round(avg_balance, 2),
        "has_insurance": random.choice([True, False]),
        "emergency_buffer": random.choice([True, False]),
        "loan_utilization": round(random.uniform(0.05, 0.95), 3),
        "fixed_emi_burden_ratio": round(random.uniform(0.00, 0.80), 3),
        "credit_inquiries": round(random.uniform(0, 10), 2),
        "delay_score": round(random.uniform(0, 5), 3),
        "recent_payment_delays_90": round(random.uniform(0, 6), 2),
        "utility_delay_score": round(random.uniform(0, 5), 3),
        "recent_missed_rent_3m": round(random.uniform(0, 3), 2),
        "rent_consistency_ratio": round(random.uniform(0.30, 1.00), 3),
    }

    return data