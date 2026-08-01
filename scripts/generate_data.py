"""
Generate synthetic small business funding and repayment data.
Creates realistic datasets for businesses, funding decisions, and repayment status.
"""

import os
import random
from datetime import datetime, timedelta
import duckdb
import pandas as pd
from faker import Faker

fake = Faker()
random.seed(42)
Faker.seed(42)

# Configuration
NUM_BUSINESSES = 500
NUM_FUNDING_DECISIONS = 800
NUM_REPAYMENTS = 600

INDUSTRIES = [
    "Technology",
    "Retail",
    "Healthcare",
    "Finance",
    "Manufacturing",
    "Hospitality",
    "Education",
    "Construction",
    "Real Estate",
    "Transportation",
]

STATES = ["CA", "NY", "TX", "FL", "IL", "PA", "OH", "GA", "NC", "MI"]

FUNDING_AMOUNTS = [50000, 100000, 150000, 250000, 500000, 750000, 1000000]

REPAYMENT_STATUSES = ["current", "30_days_late", "60_days_late", "90_days_late", "defaulted"]


def generate_businesses(n: int) -> pd.DataFrame:
    """Generate synthetic business data."""
    data = []
    for i in range(n):
        data.append(
            {
                "business_id": f"BUS_{i:06d}",
                "business_name": fake.company(),
                "industry": random.choice(INDUSTRIES),
                "state": random.choice(STATES),
                "founded_date": fake.date_between(start_date="-15y").isoformat(),
                "employee_count": random.randint(1, 500),
                "annual_revenue": random.randint(100000, 50000000),
                "created_at": datetime.now().isoformat(),
            }
        )
    return pd.DataFrame(data)


def generate_funding_decisions(businesses_df: pd.DataFrame, n: int) -> pd.DataFrame:
    """Generate synthetic funding decision data."""
    data = []
    for i in range(n):
        business_id = random.choice(businesses_df["business_id"].values)
        business = businesses_df[businesses_df["business_id"] == business_id].iloc[0]
        
        # Industry impacts approval likelihood
        industry_approval_rate = {
            "Technology": 0.85,
            "Retail": 0.65,
            "Healthcare": 0.80,
            "Finance": 0.90,
            "Manufacturing": 0.70,
            "Hospitality": 0.55,
            "Education": 0.75,
            "Construction": 0.68,
            "Real Estate": 0.72,
            "Transportation": 0.60,
        }
        
        approval_prob = industry_approval_rate.get(business["industry"], 0.70)
        approved = random.random() < approval_prob
        
        funding_amount = random.choice(FUNDING_AMOUNTS)
        funding_date = fake.date_between(
            start_date=datetime.fromisoformat(business["founded_date"]),
            end_date="-6m"
        )
        
        data.append(
            {
                "funding_id": f"FUN_{i:06d}",
                "business_id": business_id,
                "funding_amount": funding_amount,
                "decision": "approved" if approved else "denied",
                "decision_date": funding_date.isoformat(),
                "interest_rate": round(random.uniform(0.04, 0.15), 4) if approved else None,
                "created_at": datetime.now().isoformat(),
            }
        )
    return pd.DataFrame(data)


def generate_repayments(funding_df: pd.DataFrame, n: int) -> pd.DataFrame:
    """Generate synthetic repayment data."""
    approved_funding = funding_df[funding_df["decision"] == "approved"]
    
    data = []
    for i in range(min(n, len(approved_funding))):
        funding = approved_funding.iloc[i]
        funding_date = datetime.fromisoformat(funding["decision_date"])
        
        # Default rate increases over time
        months_since_funding = (datetime.now() - funding_date).days / 30
        default_prob = min(0.05 + (months_since_funding * 0.01), 0.25)
        
        # Determine repayment status based on default probability
        if random.random() < default_prob:
            status = "defaulted"
            last_payment_date = (funding_date + timedelta(days=random.randint(30, 180))).isoformat()
        else:
            # Stagger the payment status likelihood
            status_prob = random.random()
            if status_prob < 0.75:
                status = "current"
            elif status_prob < 0.85:
                status = "30_days_late"
            elif status_prob < 0.92:
                status = "60_days_late"
            elif status_prob < 0.98:
                status = "90_days_late"
            else:
                status = "defaulted"
            
            last_payment_date = (datetime.now() - timedelta(days=random.randint(0, 90))).isoformat()
        
        data.append(
            {
                "repayment_id": f"REP_{i:06d}",
                "funding_id": funding["funding_id"],
                "business_id": funding["business_id"],
                "status": status,
                "last_payment_date": last_payment_date,
                "total_paid": random.randint(0, int(funding["funding_amount"])),
                "created_at": datetime.now().isoformat(),
            }
        )
    return pd.DataFrame(data)


def save_to_duckdb(businesses_df, funding_df, repayments_df):
    """Save all dataframes to DuckDB."""
    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "funding_pipeline.duckdb")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = duckdb.connect(db_path)
    
    # Create and populate tables
    conn.execute("CREATE TABLE IF NOT EXISTS businesses AS SELECT * FROM businesses_df")
    conn.execute("CREATE TABLE IF NOT EXISTS funding_decisions AS SELECT * FROM funding_df")
    conn.execute("CREATE TABLE IF NOT EXISTS repayments AS SELECT * FROM repayments_df")
    
    conn.close()
    print(f"✓ Data saved to {db_path}")


def main():
    """Main execution."""
    print("Generating synthetic data...")
    
    print(f"  • Generating {NUM_BUSINESSES} businesses...")
    businesses_df = generate_businesses(NUM_BUSINESSES)
    
    print(f"  • Generating {NUM_FUNDING_DECISIONS} funding decisions...")
    funding_df = generate_funding_decisions(businesses_df, NUM_FUNDING_DECISIONS)
    
    print(f"  • Generating {NUM_REPAYMENTS} repayment records...")
    repayments_df = generate_repayments(funding_df, NUM_REPAYMENTS)
    
    print("\nSaving to DuckDB...")
    save_to_duckdb(businesses_df, funding_df, repayments_df)
    
    print("\n✓ Data generation complete!")
    print(f"  • Businesses: {len(businesses_df)}")
    print(f"  • Funding decisions: {len(funding_df)}")
    print(f"  • Repayments: {len(repayments_df)}")


if __name__ == "__main__":
    main()
