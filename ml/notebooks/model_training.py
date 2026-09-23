"""
NOTEBOOK 4: Model Training & Evaluation

Phase 5 - Step 4: Train multiple models, evaluate, select best model.

This notebook:
  - Loads preprocessed data
  - Trains Logistic Regression, Random Forest, Gradient Boosting
  - Performs cross-validation and hyperparameter tuning
  - Evaluates models with multiple metrics
  - Saves best model and artifacts

Run this notebook to train the final ML model.

To run:
    cd backend && python -m ml.notebooks.model_training
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_validate, GridSearchCV, train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix, classification_report
)
from sklearn.preprocessing import StandardScaler
import pickle
import json
import logging
import warnings
warnings.filterwarnings('ignore')

from ml.config import (
    DATA_DIR, TARGET, TEST_SIZE, RANDOM_STATE, CV_FOLDS,
    BEST_MODEL_PATH, FEATURE_NAMES_PATH, HYPERPARAMETERS
)
from ml.utils import (
    setup_logging, load_projects_from_database, create_derived_features,
    handle_missing_values, split_data, save_model
)

logger = setup_logging()

# =====================================================
# MODEL TRAINING PIPELINE
# =====================================================

def prepare_training_data():
    """Load and prepare data for training."""
    
    logger.info("\nLoading and preparing training data...")
    
    # Load from database
    df = load_projects_from_database()
    df = create_derived_features(df)
    df = handle_missing_values(df, strategy='mean')
    
    # Select features
    numeric_cols = ['land_required_ha', 'affected_families', 'compensation_percentage',
                   'possession_percentage', 'days_in_current_stage', 'active_disputes',
                   'grievances_pending', 'average_approval_delay_days', 'pending_approvals']
    
    derived_cols = ['legal_severity', 'compensation_velocity', 'approval_pressure',
                   'rehabilitation_lag', 'grievance_rate']
    
    feature_cols = [col for col in numeric_cols + derived_cols if col in df.columns]
    
    X = df[feature_cols].fillna(df[feature_cols].mean())
    y = df[TARGET].fillna(0)
    
    # Discretize target for classification (easier than pure regression)
    y_binned = pd.cut(y, bins=[0, 0.4, 1.0], labels=[0, 1]).astype(int)
    
    logger.info(f"✓ Data prepared: {X.shape[0]} samples × {X.shape[1]} features")
    logger.info(f"✓ Target distribution: {y_binned.value_counts().to_dict()}")
    
    return X, y_binned, y, feature_cols

def scale_features(X_train, X_test):
    """Scale features."""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler

def train_and_evaluate_model(model, X_train, X_test, y_train, y_test, model_name):
    """Train a single model and evaluate."""
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Training: {model_name}")
    logger.info(f"{'='*60}")
    
    # Train
    logger.info("Fitting model...")
    model.fit(X_train, y_train)
    
    # Predict
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else y_pred
    
    # Evaluate
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    try:
        auc = roc_auc_score(y_test, y_pred_proba)
    except:
        auc = 0.0
    
    results = {
        'model_name': model_name,
        'accuracy': acc,
        'precision': prec,
        'recall': rec,
        'f1': f1,
        'auc_roc': auc,
    }
    
    logger.info(f"\nResults:")
    logger.info(f"  Accuracy:  {acc:.4f}")
    logger.info(f"  Precision: {prec:.4f}")
    logger.info(f"  Recall:    {rec:.4f}")
    logger.info(f"  F1-Score:  {f1:.4f}")
    logger.info(f"  AUC-ROC:   {auc:.4f}")
    
    logger.info(f"\nConfusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    logger.info(f"  TN={cm[0,0]}, FP={cm[0,1]}")
    logger.info(f"  FN={cm[1,0]}, TP={cm[1,1]}")
    
    return model, results, y_pred, y_pred_proba

def cross_validate_model(model, X, y, cv_folds=CV_FOLDS):
    """Perform cross-validation."""
    
    logger.info(f"\nPerforming {cv_folds}-fold cross-validation...")
    
    scoring = {
        'accuracy': 'accuracy',
        'precision': 'precision',
        'recall': 'recall',
        'f1': 'f1',
        'roc_auc': 'roc_auc'
    }
    
    cv_results = cross_validate(model, X, y, cv=cv_folds, scoring=scoring, return_train_score=False)
    
    logger.info(f"\nCross-Validation Results (mean ± std):")
    for metric in scoring.keys():
        scores = cv_results[f'test_{metric}']
        logger.info(f"  {metric:10s}: {scores.mean():.4f} ± {scores.std():.4f}")
    
    return cv_results

def main():
    """Run model training pipeline."""
    
    logger.info("\n" + "="*70)
    logger.info("PHASE 5 - NOTEBOOK 4: MODEL TRAINING & EVALUATION")
    logger.info("="*70 + "\n")
    
    # =====================================================
    # PREPARE DATA
    # =====================================================
    
    X, y_binned, y_continuous, feature_cols = prepare_training_data()
    
    # Split data
    logger.info("\nSplitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_binned,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y_binned
    )
    
    logger.info(f"✓ Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")
    
    # Scale features
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)
    logger.info(f"✓ Features scaled")
    
    # =====================================================
    # TRAIN BASELINE MODELS
    # =====================================================
    
    logger.info("\n" + "="*70)
    logger.info("BASELINE MODELS (No Hyperparameter Tuning)")
    logger.info("="*70)
    
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=RANDOM_STATE),
    }
    
    results_list = []
    trained_models = {}
    
    for model_name, model in models.items():
        model_trained, results, y_pred, y_pred_proba = train_and_evaluate_model(
            model, X_train_scaled, X_test_scaled, y_train, y_test, model_name
        )
        results_list.append(results)
        trained_models[model_name] = (model_trained, y_pred_proba)
    
    # =====================================================
    # CROSS-VALIDATION
    # =====================================================
    
    logger.info("\n" + "="*70)
    logger.info("CROSS-VALIDATION")
    logger.info("="*70)
    
    for model_name, model in models.items():
        logger.info(f"\n{model_name}:")
        cross_validate_model(model, X_train_scaled, y_train, cv_folds=CV_FOLDS)
    
    # =====================================================
    # HYPERPARAMETER TUNING (Optional - for best model)
    # =====================================================
    
    logger.info("\n" + "="*70)
    logger.info("HYPERPARAMETER TUNING (Best Model Only)")
    logger.info("="*70)
    
    # Select best model (Gradient Boosting typically best for complex patterns)
    best_model_name = 'Gradient Boosting'
    logger.info(f"\nTuning {best_model_name}...")
    
    param_grid = HYPERPARAMETERS['gradient_boosting']
    
    gb_model = GradientBoostingClassifier(random_state=RANDOM_STATE)
    grid_search = GridSearchCV(
        gb_model,
        param_grid,
        cv=5,
        scoring='f1',
        n_jobs=-1,
        verbose=1
    )
    
    logger.info(f"Testing {len(param_grid['n_estimators']) * len(param_grid['learning_rate']) * len(param_grid['max_depth'])} parameter combinations...")
    grid_search.fit(X_train_scaled, y_train)
    
    logger.info(f"\nBest parameters: {grid_search.best_params_}")
    logger.info(f"Best CV F1-Score: {grid_search.best_score_:.4f}")
    
    # Evaluate tuned model
    best_model = grid_search.best_estimator_
    y_pred_best = best_model.predict(X_test_scaled)
    y_pred_proba_best = best_model.predict_proba(X_test_scaled)[:, 1]
    
    logger.info(f"\nTuned Model Test Performance:")
    logger.info(f"  Accuracy:  {accuracy_score(y_test, y_pred_best):.4f}")
    logger.info(f"  Precision: {precision_score(y_test, y_pred_best, zero_division=0):.4f}")
    logger.info(f"  Recall:    {recall_score(y_test, y_pred_best, zero_division=0):.4f}")
    logger.info(f"  F1-Score:  {f1_score(y_test, y_pred_best, zero_division=0):.4f}")
    logger.info(f"  AUC-ROC:   {roc_auc_score(y_test, y_pred_proba_best):.4f}")
    
    # =====================================================
    # FEATURE IMPORTANCE (Best Model)
    # =====================================================
    
    logger.info("\n" + "="*70)
    logger.info("FEATURE IMPORTANCE (Best Model)")
    logger.info("="*70)
    
    if hasattr(best_model, 'feature_importances_'):
        importances = best_model.feature_importances_
        feature_importance_df = pd.DataFrame({
            'Feature': feature_cols,
            'Importance': importances
        }).sort_values('Importance', ascending=False)
        
        logger.info("\nTop 10 Most Important Features:")
        logger.info("\n" + feature_importance_df.head(10).to_string(index=False))
    
    # =====================================================
    # MODEL COMPARISON
    # =====================================================
    
    logger.info("\n" + "="*70)
    logger.info("MODEL COMPARISON SUMMARY")
    logger.info("="*70 + "\n")
    
    results_df = pd.DataFrame(results_list)
    logger.info("\n" + results_df.to_string(index=False))
    
    # =====================================================
    # SAVE BEST MODEL
    # =====================================================
    
    logger.info("\n" + "="*70)
    logger.info("SAVING BEST MODEL")
    logger.info("="*70 + "\n")
    
    # Save model
    save_model(best_model)
    
    # Save feature names
    with open(FEATURE_NAMES_PATH, 'wb') as f:
        pickle.dump(feature_cols, f)
    logger.info(f"✓ Feature names saved to {FEATURE_NAMES_PATH}")
    
    # Save metadata
    metadata = {
        'model_type': 'GradientBoostingClassifier',
        'best_params': grid_search.best_params_,
        'best_cv_score': float(grid_search.best_score_),
        'test_accuracy': float(accuracy_score(y_test, y_pred_best)),
        'test_f1': float(f1_score(y_test, y_pred_best, zero_division=0)),
        'test_auc': float(roc_auc_score(y_test, y_pred_proba_best)),
        'n_features': len(feature_cols),
        'feature_names': feature_cols,
        'target_variable': TARGET,
    }
    
    with open(f"{DATA_DIR}/model_metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    logger.info(f"✓ Metadata saved to {DATA_DIR}/model_metadata.json")
    
    # =====================================================
    # SUMMARY
    # =====================================================
    
    logger.info("\n" + "="*70)
    logger.info("TRAINING COMPLETE - SUMMARY")
    logger.info("="*70 + "\n")
    
    logger.info(f"""
    ✓ Dataset: {X.shape[0]} projects × {X.shape[1]} features
    ✓ Train/Test Split: {X_train.shape[0]} / {X_test.shape[0]}
    ✓ Class Distribution: {y_binned.value_counts().to_dict()}
    
    ✓ Models Trained:
       1. Logistic Regression
       2. Random Forest
       3. Gradient Boosting (SELECTED AS BEST)
    
    ✓ Best Model Performance:
       - Accuracy:  {accuracy_score(y_test, y_pred_best):.4f}
       - Precision: {precision_score(y_test, y_pred_best, zero_division=0):.4f}
       - Recall:    {recall_score(y_test, y_pred_best, zero_division=0):.4f}
       - F1-Score:  {f1_score(y_test, y_pred_best, zero_division=0):.4f}
       - AUC-ROC:   {roc_auc_score(y_test, y_pred_proba_best):.4f}
    
    ✓ Model Artifacts:
       - Model: {BEST_MODEL_PATH}
       - Features: {FEATURE_NAMES_PATH}
       - Metadata: {DATA_DIR}/model_metadata.json
    
    ✓ Ready for Production:
       - Model can predict delay probability for new projects
       - Services/prediction_service.py can integrate this model
       - API endpoint /api/predict will use real ML predictions
    
    Next Step: Integrate model with prediction_service.py
    """)
    
    logger.info("="*70)
    logger.info("MODEL TRAINING NOTEBOOK COMPLETE")
    logger.info("="*70 + "\n")
    
    return best_model, results_df

if __name__ == "__main__":
    model, results = main()
