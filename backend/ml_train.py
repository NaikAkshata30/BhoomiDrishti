"""
ML Pipeline - Complete Training Script

Phase 5: End-to-end ML pipeline
Trains Gradient Boosting model for delay prediction

Run: python ml_train.py
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import os
import pickle
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ml.config import (
    DB_URL, TARGET, NUMERIC_FEATURES, TEST_SIZE, RANDOM_STATE,
    BEST_MODEL_PATH, SCALER_PATH, FEATURE_NAMES_PATH, MODELS_DIR
)
from ml.utils import (
    setup_logging, load_projects_from_database, create_derived_features,
    handle_missing_values, scale_features, save_model, print_summary
)

logger = setup_logging()

# =====================================================
# MAIN PIPELINE
# =====================================================

def main():
    """Run complete ML training pipeline."""
    
    logger.info("\n" + "="*70)
    logger.info("PHASE 5: ML PIPELINE - COMPLETE TRAINING")
    logger.info("="*70 + "\n")
    
    try:
        # =====================================================
        # STEP 1: LOAD DATA
        # =====================================================
        
        logger.info("STEP 1: Loading Data from Database")
        logger.info("-"*70)
        
        df = load_projects_from_database()
        print_summary(df, y=df[TARGET] if TARGET in df.columns else None)
        
        # =====================================================
        # STEP 2: CREATE DERIVED FEATURES
        # =====================================================
        
        logger.info("\nSTEP 2: Creating Derived Features")
        logger.info("-"*70)
        
        df = create_derived_features(df)
        logger.info(f"✓ Data shape: {df.shape}")
        
        # =====================================================
        # STEP 3: HANDLE MISSING VALUES
        # =====================================================
        
        logger.info("\nSTEP 3: Handling Missing Values")
        logger.info("-"*70)
        
        df = handle_missing_values(df, strategy='mean')
        logger.info(f"✓ No more missing values")
        
        # =====================================================
        # STEP 4: PREPARE FEATURES & TARGET
        # =====================================================
        
        logger.info("\nSTEP 4: Preparing Features")
        logger.info("-"*70)
        
        # Select numeric features that exist
        numeric_cols = [col for col in NUMERIC_FEATURES if col in df.columns]
        
        # Select derived features
        derived_cols = [col for col in df.columns if col in [
            'legal_severity', 'compensation_velocity', 'approval_pressure', 'rehabilitation_lag'
        ]]
        
        feature_cols = numeric_cols + derived_cols
        
        X = df[feature_cols].fillna(df[feature_cols].mean())
        y = df[TARGET].fillna(0)
        
        logger.info(f"Features: {len(feature_cols)}")
        logger.info(f"  Numeric: {len(numeric_cols)}")
        logger.info(f"  Derived: {len(derived_cols)}")
        
        # Discretize target for classification
        y_binned = pd.cut(y, bins=[0, 0.4, 1.0], labels=[0, 1]).astype(int)
        
        logger.info(f"Target distribution: {y_binned.value_counts().to_dict()}")
        
        # =====================================================
        # STEP 5: TRAIN/TEST SPLIT
        # =====================================================
        
        logger.info("\nSTEP 5: Train/Test Split")
        logger.info("-"*70)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_binned,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE,
            stratify=y_binned
        )
        
        logger.info(f"Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")
        
        # =====================================================
        # STEP 6: SCALE FEATURES
        # =====================================================
        
        logger.info("\nSTEP 6: Scaling Features")
        logger.info("-"*70)
        
        X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)
        logger.info(f"✓ Features scaled")
        
        # =====================================================
        # STEP 7: TRAIN MODEL
        # =====================================================
        
        logger.info("\nSTEP 7: Training Gradient Boosting Model")
        logger.info("-"*70)
        
        model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=RANDOM_STATE
        )
        
        model.fit(X_train_scaled, y_train)
        logger.info(f"✓ Model trained")
        
        # =====================================================
        # STEP 8: EVALUATE MODEL
        # =====================================================
        
        logger.info("\nSTEP 8: Evaluating Model")
        logger.info("-"*70)
        
        y_pred = model.predict(X_test_scaled)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        auc = roc_auc_score(y_test, y_pred_proba)
        
        logger.info(f"\nModel Performance:")
        logger.info(f"  Accuracy:  {acc:.4f}")
        logger.info(f"  Precision: {prec:.4f}")
        logger.info(f"  Recall:    {rec:.4f}")
        logger.info(f"  F1-Score:  {f1:.4f}")
        logger.info(f"  AUC-ROC:   {auc:.4f}")
        
        # =====================================================
        # STEP 9: SAVE MODEL
        # =====================================================
        
        logger.info("\nSTEP 9: Saving Model Artifacts")
        logger.info("-"*70)
        
        # Ensure models directory exists
        os.makedirs(MODELS_DIR, exist_ok=True)
        
        # Save model
        with open(BEST_MODEL_PATH, 'wb') as f:
            pickle.dump(model, f)
        logger.info(f"✓ Model: {BEST_MODEL_PATH}")
        
        # Save scaler
        with open(SCALER_PATH, 'wb') as f:
            pickle.dump(scaler, f)
        logger.info(f"✓ Scaler: {SCALER_PATH}")
        
        # Save feature names
        with open(FEATURE_NAMES_PATH, 'wb') as f:
            pickle.dump(feature_cols, f)
        logger.info(f"✓ Features: {FEATURE_NAMES_PATH}")
        
        # =====================================================
        # COMPLETE
        # =====================================================
        
        logger.info("\n" + "="*70)
        logger.info("✓ ML PIPELINE COMPLETE")
        logger.info("="*70)
        logger.info(f"""
Model trained and saved!

Artifacts:
  ✓ {BEST_MODEL_PATH}
  ✓ {SCALER_PATH}
  ✓ {FEATURE_NAMES_PATH}

Performance:
  ✓ Accuracy: {acc:.4f}
  ✓ F1-Score: {f1:.4f}
  ✓ AUC-ROC:  {auc:.4f}

Ready for API predictions!
        """)
        
        return True
        
    except Exception as e:
        logger.error(f"\n✗ Pipeline failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
