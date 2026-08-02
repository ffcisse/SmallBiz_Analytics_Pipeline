"""
Default Risk Prediction Model
Trains a logistic regression model to predict funding default risk.
"""

import os
import pickle
import duckdb
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score, confusion_matrix
import warnings
warnings.filterwarnings('ignore')


def load_data(conn):
    """Load feature engineering data from mart tables."""
    query = """
    SELECT
        funding_id,
        business_id,
        funding_amount,
        industry,
        state,
        employee_count,
        annual_revenue,
        decision,
        days_since_funding,
        is_defaulted,
        risk_segment
    FROM main_marts.fct_funding_decisions
    WHERE decision = 'approved'
    """
    return conn.execute(query).df()


def preprocess_features(df):
    """Preprocess and encode features."""
    df_model = df.copy()
    
    # Encode categorical variables
    le_industry = LabelEncoder()
    le_state = LabelEncoder()
    le_risk = LabelEncoder()
    
    df_model['industry_encoded'] = le_industry.fit_transform(df_model['industry'])
    df_model['state_encoded'] = le_state.fit_transform(df_model['state'])
    df_model['risk_segment_encoded'] = le_risk.fit_transform(df_model['risk_segment'])
    
    # Feature engineering
    df_model['funding_per_employee'] = df_model['funding_amount'] / (df_model['employee_count'] + 1)
    df_model['revenue_to_funding_ratio'] = df_model['annual_revenue'] / (df_model['funding_amount'] + 1)
    df_model['log_funding_amount'] = np.log1p(df_model['funding_amount'])
    df_model['log_revenue'] = np.log1p(df_model['annual_revenue'])
    
    # Select features
    feature_cols = [
        'funding_amount',
        'employee_count',
        'annual_revenue',
        'days_since_funding',
        'industry_encoded',
        'state_encoded',
        'funding_per_employee',
        'revenue_to_funding_ratio',
        'log_funding_amount',
        'log_revenue'
    ]
    
    return df_model, feature_cols, le_industry, le_state, le_risk


def train_model(X, y):
    """Train logistic regression model."""
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    metrics = {
        'auc': roc_auc_score(y_test, y_pred_proba),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred),
    }
    
    return model, scaler, metrics, X_train_scaled, X_test_scaled, y_train, y_test


def generate_predictions(conn, df, model, scaler, feature_cols, le_industry, le_state, le_risk):
    """Generate default risk predictions for all approved fundings."""
    df_pred = df.copy()
    
    # Encode features
    df_pred['industry_encoded'] = le_industry.transform(df_pred['industry'])
    df_pred['state_encoded'] = le_state.transform(df_pred['state'])
    df_pred['risk_segment_encoded'] = le_risk.transform(df_pred['risk_segment'])
    
    # Feature engineering
    df_pred['funding_per_employee'] = df_pred['funding_amount'] / (df_pred['employee_count'] + 1)
    df_pred['revenue_to_funding_ratio'] = df_pred['annual_revenue'] / (df_pred['funding_amount'] + 1)
    df_pred['log_funding_amount'] = np.log1p(df_pred['funding_amount'])
    df_pred['log_revenue'] = np.log1p(df_pred['annual_revenue'])
    
    # Get features
    X = df_pred[feature_cols]
    X_scaled = scaler.transform(X)
    
    # Predict
    predicted_default_risk = model.predict_proba(X_scaled)[:, 1]
    predicted_default = model.predict(X_scaled)
    
    df_pred['predicted_default_probability'] = predicted_default_risk
    df_pred['predicted_default'] = predicted_default
    df_pred['prediction_correct'] = (df_pred['predicted_default'] == df_pred['is_defaulted']).astype(int)
    
    return df_pred[['funding_id', 'business_id', 'industry', 'state', 'funding_amount', 
                     'predicted_default_probability', 'predicted_default', 'is_defaulted', 
                     'prediction_correct']]


def save_predictions_to_duckdb(conn, predictions_df):
    """Save predictions to DuckDB."""
    conn.execute("""
        DROP TABLE IF EXISTS main.model_predictions
    """)
    
    conn.execute("""
        CREATE TABLE main.model_predictions AS
        SELECT * FROM predictions_df
    """)
    
    print("✓ Predictions saved to DuckDB (model_predictions table)")


def main():
    """Main execution."""
    print("Training Default Risk Prediction Model...\n")
    
    # Connect to database
    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "funding_pipeline.duckdb")
    conn = duckdb.connect(db_path)
    
    # Load data
    print("Loading data...")
    df = load_data(conn)
    print(f"  • Loaded {len(df)} approved fundings")
    
    # Preprocess
    print("\nPreprocessing features...")
    df_model, feature_cols, le_industry, le_state, le_risk = preprocess_features(df)
    print(f"  • Created {len(feature_cols)} features")
    
    # Prepare training data
    X = df_model[feature_cols]
    y = df_model['is_defaulted']
    
    # Train model
    print("\nTraining logistic regression model...")
    model, scaler, metrics, X_train, X_test, y_train, y_test = train_model(X, y)
    
    print(f"\nModel Performance:")
    print(f"  • AUC:       {metrics['auc']:.4f}")
    print(f"  • Precision: {metrics['precision']:.4f}")
    print(f"  • Recall:    {metrics['recall']:.4f}")
    print(f"  • F1 Score:  {metrics['f1']:.4f}")
    
    # Generate predictions
    print("\nGenerating predictions for all fundings...")
    predictions_df = generate_predictions(conn, df, model, scaler, feature_cols, le_industry, le_state, le_risk)
    print(f"  • Generated predictions for {len(predictions_df)} fundings")
    
    # Save to DuckDB
    print("\nSaving to DuckDB...")
    save_predictions_to_duckdb(conn, predictions_df)
    
    # Save model artifacts
    model_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    os.makedirs(model_dir, exist_ok=True)
    
    with open(os.path.join(model_dir, "model.pkl"), "wb") as f:
        pickle.dump(model, f)
    
    with open(os.path.join(model_dir, "scaler.pkl"), "wb") as f:
        pickle.dump(scaler, f)
    
    print(f"✓ Model artifacts saved to models/")
    print(f"\n✓ Model training complete!")
    
    conn.close()


if __name__ == "__main__":
    main()
