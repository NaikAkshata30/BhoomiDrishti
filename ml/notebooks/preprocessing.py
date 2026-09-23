"""
NOTEBOOK 2: Data Preprocessing

Phase 5 - Step 2: Clean data, handle missing values, and prepare features.

This notebook:
  - Loads raw data from database
  - Handles missing values
  - Creates derived features
  - Scales numeric features
  - Encodes categorical features
  - Saves preprocessed data

Run this notebook second to prepare data for training.

To run:
    cd backend && python -m ml.notebooks.preprocessing
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pickle
import logging

from ml.config import (
    DB_URL, TARGET, NUMERIC_FEATURES, CATEGORICAL_FEATURES,
    DATA_DIR, SCALER_PATH, ENCODER_PATH, MISSING_VALUE_STRATEGY
)
from ml.utils import (
    setup_logging, load_projects_from_database, create_derived_features,
    handle_missing_values, scale_features, encode_categorical, print_summary
)

logger = setup_logging()

# =====================================================
# PREPROCESSING PIPELINE
# =====================================================

def main():
    """Run preprocessing pipeline."""
    
    logger.info("\n" + "="*70)
    logger.info("PHASE 5 - NOTEBOOK 2: DATA PREPROCESSING")
    logger.info("="*70 + "\n")
    
    # =====================================================
    # STEP 1: LOAD DATA
    # =====================================================
    
    logger.info("\n" + "-"*70)
    logger.info("STEP 1: LOADING DATA")
    logger.info("-"*70 + "\n")
    
    df = load_projects_from_database()
    print_summary(df, y=df[TARGET] if TARGET in df.columns else None)
    
    # =====================================================
    # STEP 2: CREATE DERIVED FEATURES
    # =====================================================
    
    logger.info("\n" + "-"*70)
    logger.info("STEP 2: CREATING DERIVED FEATURES")
    logger.info("-"*70 + "\n")
    
    df = create_derived_features(df)
    logger.info(f"✓ Data shape after feature engineering: {df.shape}")
    
    # =====================================================
    # STEP 3: HANDLE MISSING VALUES
    # =====================================================
    
    logger.info("\n" + "-"*70)
    logger.info("STEP 3: HANDLING MISSING VALUES")
    logger.info("-"*70 + "\n")
    
    logger.info(f"Missing values before:")
    missing_before = df.isnull().sum()
    logger.info(missing_before[missing_before > 0])
    
    df = handle_missing_values(df, strategy=MISSING_VALUE_STRATEGY)
    
    logger.info(f"Missing values after:")
    missing_after = df.isnull().sum()
    if missing_after.sum() == 0:
        logger.info("✓ No missing values remaining")
    else:
        logger.info(missing_after[missing_after > 0])
    
    # =====================================================
    # STEP 4: SEPARATE FEATURES AND TARGET
    # =====================================================
    
    logger.info("\n" + "-"*70)
    logger.info("STEP 4: SEPARATING FEATURES AND TARGET")
    logger.info("-"*70 + "\n")
    
    # Select only features that exist in data
    numeric_features = [col for col in NUMERIC_FEATURES if col in df.columns]
    categorical_features = [col for col in CATEGORICAL_FEATURES if col in df.columns]
    
    # Include derived features
    derived_features = [col for col in df.columns if col.startswith('derived_') or 
                       col in ['legal_severity', 'compensation_velocity', 
                              'approval_pressure', 'rehabilitation_lag', 'grievance_rate']]
    
    all_feature_cols = numeric_features + categorical_features + derived_features
    
    logger.info(f"Numeric features: {len(numeric_features)}")
    logger.info(f"  {numeric_features}")
    logger.info(f"\nCategorical features: {len(categorical_features)}")
    logger.info(f"  {categorical_features}")
    logger.info(f"\nDerived features: {len(derived_features)}")
    logger.info(f"  {derived_features}")
    
    X = df[all_feature_cols].copy()
    y = df[TARGET].copy() if TARGET in df.columns else None
    
    logger.info(f"\n✓ Features shape: {X.shape}")
    logger.info(f"✓ Target shape: {y.shape if y is not None else 'None'}")
    
    # =====================================================
    # STEP 5: SCALE NUMERIC FEATURES
    # =====================================================
    
    logger.info("\n" + "-"*70)
    logger.info("STEP 5: SCALING NUMERIC FEATURES")
    logger.info("-"*70 + "\n")
    
    X_numeric = X[numeric_features].copy()
    scaler = StandardScaler()
    X_numeric_scaled = scaler.fit_transform(X_numeric)
    X_numeric_scaled = pd.DataFrame(X_numeric_scaled, columns=numeric_features)
    
    logger.info(f"✓ Scaled numeric features")
    logger.info(f"  Mean: {X_numeric_scaled.mean().mean():.6f}")
    logger.info(f"  Std:  {X_numeric_scaled.std().mean():.6f}")
    
    # Save scaler
    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)
    logger.info(f"✓ Scaler saved to {SCALER_PATH}")
    
    # =====================================================
    # STEP 6: ENCODE CATEGORICAL FEATURES
    # =====================================================
    
    logger.info("\n" + "-"*70)
    logger.info("STEP 6: ENCODING CATEGORICAL FEATURES")
    logger.info("-"*70 + "\n")
    
    if len(categorical_features) > 0:
        X_categorical = X[categorical_features].copy()
        encoder = OneHotEncoder(sparse=False, handle_unknown='ignore', drop=None)
        X_categorical_encoded = encoder.fit_transform(X_categorical)
        feature_names_encoded = encoder.get_feature_names_out(categorical_features)
        X_categorical_encoded = pd.DataFrame(X_categorical_encoded, columns=feature_names_encoded)
        
        logger.info(f"✓ Encoded {len(categorical_features)} categorical features")
        logger.info(f"✓ Generated {len(feature_names_encoded)} binary features")
        logger.info(f"  Features: {list(feature_names_encoded)}")
        
        # Save encoder
        with open(ENCODER_PATH, 'wb') as f:
            pickle.dump(encoder, f)
        logger.info(f"✓ Encoder saved to {ENCODER_PATH}")
    else:
        X_categorical_encoded = pd.DataFrame()
        feature_names_encoded = []
        logger.info("No categorical features to encode")
    
    # =====================================================
    # STEP 7: COMBINE ALL FEATURES
    # =====================================================
    
    logger.info("\n" + "-"*70)
    logger.info("STEP 7: COMBINING ALL FEATURES")
    logger.info("-"*70 + "\n")
    
    # Add derived features (already scaled if from numeric origin)
    X_derived = X[derived_features].copy() if derived_features else pd.DataFrame()
    
    X_processed = pd.concat([
        X_numeric_scaled.reset_index(drop=True),
        X_categorical_encoded.reset_index(drop=True),
        X_derived.reset_index(drop=True)
    ], axis=1)
    
    logger.info(f"✓ Combined features shape: {X_processed.shape}")
    logger.info(f"✓ Total features: {X_processed.shape[1]}")
    
    # =====================================================
    # STEP 8: SAVE PREPROCESSED DATA
    # =====================================================
    
    logger.info("\n" + "-"*70)
    logger.info("STEP 8: SAVING PREPROCESSED DATA")
    logger.info("-"*70 + "\n")
    
    # Save processed features and target
    processed_data = pd.concat([
        X_processed.reset_index(drop=True),
        y.reset_index(drop=True) if y is not None else pd.DataFrame()
    ], axis=1)
    
    output_path = f"{DATA_DIR}/processed_data.csv"
    processed_data.to_csv(output_path, index=False)
    logger.info(f"✓ Processed data saved to {output_path}")
    
    # Save feature names
    feature_names = list(X_processed.columns)
    with open(f"{DATA_DIR}/feature_names.pkl", 'wb') as f:
        pickle.dump(feature_names, f)
    logger.info(f"✓ Feature names saved ({len(feature_names)} features)")
    
    # =====================================================
    # SUMMARY
    # =====================================================
    
    logger.info("\n" + "="*70)
    logger.info("PREPROCESSING SUMMARY")
    logger.info("="*70 + "\n")
    
    logger.info(f"""
    ✓ Raw Data: {df.shape[0]} projects × {df.shape[1]} columns
    ✓ Missing Values: Handled with '{MISSING_VALUE_STRATEGY}' strategy
    ✓ Derived Features: Created 5 new features from relationships
    ✓ Numeric Features: {len(numeric_features)} scaled using StandardScaler
    ✓ Categorical Features: {len(categorical_features)} encoded with {len(feature_names_encoded)} binary features
    ✓ Final Features: {X_processed.shape[1]} total
    ✓ Target Variable: delay_probability ({len(y)} samples)
    
    Outputs:
    ✓ Processed data: {output_path}
    ✓ Scaler: {SCALER_PATH}
    ✓ Encoder: {ENCODER_PATH}
    ✓ Feature names: {DATA_DIR}/feature_names.pkl
    
    Next Step: Proceed to Notebook 3 (Model Training)
    """)
    
    logger.info("="*70)
    logger.info("PREPROCESSING NOTEBOOK COMPLETE")
    logger.info("="*70 + "\n")
    
    return X_processed, y

if __name__ == "__main__":
    X, y = main()
