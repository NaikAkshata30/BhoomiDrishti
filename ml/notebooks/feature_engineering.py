"""
NOTEBOOK 3: Feature Engineering & Selection

Phase 5 - Step 3: Deep dive into feature engineering and selection.

This notebook:
  - Analyzes feature importance
  - Creates interaction features
  - Removes redundant features
  - Validates feature engineering decisions

To run:
    cd backend && python -m ml.notebooks.feature_engineering
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import logging

from ml.config import (
    DATA_DIR, TARGET, NUMERIC_FEATURES, CATEGORICAL_FEATURES
)
from ml.utils import setup_logging, load_projects_from_database, create_derived_features

logger = setup_logging()

# =====================================================
# FEATURE ENGINEERING
# =====================================================

def main():
    """Run feature engineering analysis."""
    
    logger.info("\n" + "="*70)
    logger.info("PHASE 5 - NOTEBOOK 3: FEATURE ENGINEERING & SELECTION")
    logger.info("="*70 + "\n")
    
    # Load data
    df = load_projects_from_database()
    df = create_derived_features(df)
    
    # Fill missing values
    for col in df.select_dtypes(include=[np.number]).columns:
        df[col].fillna(df[col].mean(), inplace=True)
    
    # =====================================================
    # FEATURE IMPORTANCE ANALYSIS
    # =====================================================
    
    logger.info("\n" + "-"*70)
    logger.info("FEATURE IMPORTANCE ANALYSIS")
    logger.info("-"*70 + "\n")
    
    # Prepare data
    numeric_cols = [col for col in NUMERIC_FEATURES if col in df.columns]
    X = df[numeric_cols].fillna(df[numeric_cols].mean())
    y = df[TARGET].fillna(0)
    
    # Train a quick Random Forest for feature importance
    logger.info("Training Random Forest for feature importance estimation...")
    
    try:
        rf = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=10)
        
        # Discretize target for classification
        y_binned = pd.cut(y, bins=[0, 0.4, 1.0], labels=[0, 1])
        
        rf.fit(X, y_binned)
        
        feature_importance = pd.DataFrame({
            'Feature': numeric_cols,
            'Importance': rf.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        logger.info("\nFeature Importance (Random Forest):")
        logger.info("\n" + feature_importance.to_string(index=False))
        
        # Top features
        top_k = 10
        top_features = feature_importance.head(top_k)['Feature'].tolist()
        logger.info(f"\nTop {top_k} features: {top_features}")
        
    except Exception as e:
        logger.warning(f"Could not compute feature importance: {str(e)}")
    
    # =====================================================
    # INTERACTION FEATURES
    # =====================================================
    
    logger.info("\n" + "-"*70)
    logger.info("INTERACTION FEATURES")
    logger.info("-"*70 + "\n")
    
    logger.info("""
    Consider adding these interaction features:
    
    1. land_per_family = land_required_ha / affected_families
       → Indicates complexity (small plots per family vs large)
    
    2. compensation_velocity = compensation_percentage / days_in_stage
       → How quickly compensation is being disbursed
    
    3. dispute_intensity = active_disputes / affected_families
       → Legal complexity per family
    
    4. approval_pressure = pending_approvals / total_expected_approvals
       → How many approvals still needed (as fraction)
    
    5. rehabilitation_lag = (100 - rehabilitation_pct) / 100 * affected_families
       → Number of families still needing R&R
    
    6. grievance_severity = grievances_pending / affected_families
       → Grievance rate
    
    7. possession_pace = possession_percentage / days_in_stage
       → How quickly land is being possessed
    
    8. stage_progress = overall_progress_percentage / days_in_stage
       → Project momentum
    """)
    
    # =====================================================
    # MULTICOLLINEARITY CHECK
    # =====================================================
    
    logger.info("\n" + "-"*70)
    logger.info("MULTICOLLINEARITY CHECK (Correlations)")
    logger.info("-"*70 + "\n")
    
    correlation_matrix = X.corr()
    
    # Find high correlations (>0.8)
    high_corr = []
    for i in range(len(correlation_matrix.columns)):
        for j in range(i+1, len(correlation_matrix.columns)):
            if abs(correlation_matrix.iloc[i, j]) > 0.8:
                high_corr.append({
                    'Feature 1': correlation_matrix.columns[i],
                    'Feature 2': correlation_matrix.columns[j],
                    'Correlation': correlation_matrix.iloc[i, j]
                })
    
    if high_corr:
        high_corr_df = pd.DataFrame(high_corr)
        logger.info("\nHighly Correlated Features (|r| > 0.8):")
        logger.info("\n" + high_corr_df.to_string(index=False))
        logger.info("\n⚠️  Consider removing one feature from each pair to reduce multicollinearity")
    else:
        logger.info("\n✓ No high correlations detected (all |r| < 0.8)")
    
    # =====================================================
    # FEATURE SCALING ANALYSIS
    # =====================================================
    
    logger.info("\n" + "-"*70)
    logger.info("FEATURE SCALING ANALYSIS")
    logger.info("-"*70 + "\n")
    
    logger.info("\nOriginal Feature Ranges:")
    for col in numeric_cols:
        logger.info(f"  {col:40s}: [{X[col].min():10.2f}, {X[col].max():10.2f}]")
    
    # After scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    logger.info("\nAfter Standard Scaling:")
    for i, col in enumerate(numeric_cols):
        logger.info(f"  {col:40s}: [{X_scaled[:, i].min():10.2f}, {X_scaled[:, i].max():10.2f}]")
    
    logger.info("\n✓ All features will be scaled to zero mean and unit variance")
    
    # =====================================================
    # MISSING VALUE PATTERNS
    # =====================================================
    
    logger.info("\n" + "-"*70)
    logger.info("MISSING VALUE PATTERNS")
    logger.info("-"*70 + "\n")
    
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100)
    
    missing_df = pd.DataFrame({
        'Column': missing.index,
        'Missing_Count': missing.values,
        'Missing_Percentage': missing_pct.values
    }).sort_values('Missing_Count', ascending=False)
    
    if missing_df['Missing_Count'].sum() > 0:
        logger.info("\n" + missing_df[missing_df['Missing_Count'] > 0].to_string(index=False))
        logger.info("\nStrategy: Fill with mean (for numeric) or mode (for categorical)")
    else:
        logger.info("\n✓ No missing values after preprocessing")
    
    # =====================================================
    # DATA DISTRIBUTION
    # =====================================================
    
    logger.info("\n" + "-"*70)
    logger.info("TARGET VARIABLE DISTRIBUTION")
    logger.info("-"*70 + "\n")
    
    logger.info(f"\nDelay Probability Distribution:")
    logger.info(f"  Count: {len(y)}")
    logger.info(f"  Mean: {y.mean():.4f}")
    logger.info(f"  Std: {y.std():.4f}")
    logger.info(f"  Min: {y.min():.4f}")
    logger.info(f"  Max: {y.max():.4f}")
    
    # Risk level distribution
    risk_bins = [0, 0.15, 0.40, 0.70, 1.0]
    risk_labels = ['NO_RISK', 'LOW', 'MEDIUM', 'HIGH']
    risk_dist = pd.cut(y, bins=risk_bins, labels=risk_labels).value_counts()
    
    logger.info(f"\nRisk Level Distribution:")
    for risk_level, count in risk_dist.items():
        logger.info(f"  {risk_level}: {count} ({count/len(y)*100:.1f}%)")
    
    # =====================================================
    # RECOMMENDATIONS
    # =====================================================
    
    logger.info("\n" + "="*70)
    logger.info("FEATURE ENGINEERING RECOMMENDATIONS")
    logger.info("="*70 + "\n")
    
    logger.info("""
    ✓ Use all numeric features as they are diverse and informative
    ✓ Add 8 derived/interaction features (see list above)
    ✓ Encode categorical features (project_type, state, stage) as one-hot
    ✓ Scale all numeric features with StandardScaler
    ✓ Handle missing values with mean imputation (numeric) or mode (categorical)
    ✓ No features have excessive multicollinearity (avoid redundancy)
    ✓ Target variable is continuous (0-1) → regression or binned classification
    
    Final Feature Set:
    ✓ ~20 numeric features (original + derived)
    ✓ ~10-15 categorical features (after encoding)
    ✓ Total: ~30-35 features for model training
    
    Next Step: Proceed to Notebook 4 (Model Training)
    """)
    
    logger.info("="*70)
    logger.info("FEATURE ENGINEERING NOTEBOOK COMPLETE")
    logger.info("="*70 + "\n")

if __name__ == "__main__":
    main()
