"""
ML Pipeline Test - Standalone (No Database Required)

Creates synthetic data and trains ML model
for testing purposes without MySQL dependency.

Run: python ml_test_standalone.py
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import os
import pickle

# Set random seed for reproducibility
np.random.seed(42)

# =====================================================
# GENERATE SYNTHETIC DATA
# =====================================================

def generate_synthetic_features(n_projects=50):
    """Generate synthetic project features for testing."""
    
    print("\n" + "="*70)
    print("GENERATING SYNTHETIC DATA")
    print("="*70 + "\n")
    
    data = {
        'project_id': [f'TEST_PROJECT_{i:03d}' for i in range(n_projects)],
        'project_type': np.random.choice(['Highway', 'Railway', 'Water Supply'], n_projects),
        'state': np.random.choice(['Maharashtra', 'Uttar Pradesh', 'Kerala', 'Tamil Nadu'], n_projects),
        'land_required_ha': np.random.uniform(50, 500, n_projects),
        'affected_families': np.random.randint(100, 600, n_projects),
        'compensation_percentage': np.random.uniform(0, 100, n_projects),
        'possession_percentage': np.random.uniform(0, 100, n_projects),
        'days_in_current_stage': np.random.randint(30, 800, n_projects),
        'active_disputes': np.random.randint(0, 15, n_projects),
        'grievances_pending': np.random.randint(0, 20, n_projects),
        'average_approval_delay_days': np.random.randint(0, 180, n_projects),
        'pending_approvals': np.random.randint(0, 5, n_projects),
    }
    
    df = pd.DataFrame(data)
    
    # Create derived features
    df['legal_severity'] = df['active_disputes'] / (df['affected_families'] + 1)
    df['compensation_velocity'] = df['compensation_percentage'] / (df['days_in_current_stage'] + 1)
    df['approval_pressure'] = df['pending_approvals']
    df['rehabilitation_lag'] = (100 - df['compensation_percentage']) / 100 * df['affected_families']
    
    # Create target variable (with some correlation to features)
    base_prob = np.full(n_projects, 0.5)  # Start at 0.5 for all
    
    # Adjust based on factors
    base_prob -= (df['compensation_percentage'] / 100) * 0.4  # More compensation = less delay
    base_prob += (df['active_disputes'] / 20) * 0.2  # More disputes = more delay
    base_prob += (df['days_in_current_stage'] / 1000) * 0.2  # More days = slight delay
    base_prob += (df['grievances_pending'] / 30) * 0.2  # More grievances = more delay
    
    # Add some noise
    noise = np.random.normal(0, 0.15, n_projects)
    df['delay_probability'] = np.clip(base_prob + noise, 0, 1)
    
    print(f"✓ Generated {n_projects} synthetic projects")
    print(f"  Shape: {df.shape}")
    print(f"\nTarget Distribution:")
    print(f"  Mean: {df['delay_probability'].mean():.4f}")
    print(f"  Std:  {df['delay_probability'].std():.4f}")
    print(f"  Min:  {df['delay_probability'].min():.4f}")
    print(f"  Max:  {df['delay_probability'].max():.4f}")
    
    return df

# =====================================================
# TRAIN MODEL
# =====================================================

def train_model(df):
    """Train ML model on synthetic data."""
    
    print("\n" + "="*70)
    print("TRAINING MODEL")
    print("="*70 + "\n")
    
    # Select features
    numeric_cols = [
        'land_required_ha', 'affected_families', 'compensation_percentage',
        'possession_percentage', 'days_in_current_stage', 'active_disputes',
        'grievances_pending', 'average_approval_delay_days', 'pending_approvals'
    ]
    
    derived_cols = [
        'legal_severity', 'compensation_velocity', 'approval_pressure', 'rehabilitation_lag'
    ]
    
    feature_cols = numeric_cols + derived_cols
    
    X = df[feature_cols].fillna(0)
    y = df['delay_probability'].fillna(0)
    
    # Discretize for classification
    y_binned = pd.cut(y, bins=[0, 0.4, 1.0], labels=[0, 1]).astype(int)
    
    print(f"Features: {len(feature_cols)}")
    print(f"Target distribution: {y_binned.value_counts().to_dict()}")
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_binned,
        test_size=0.2,
        random_state=42,
        stratify=y_binned
    )
    
    print(f"\nTrain/Test split: {len(X_train)} / {len(X_test)}")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("✓ Features scaled")
    
    # Train model
    print("\nTraining Gradient Boosting...")
    model = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )
    
    model.fit(X_train_scaled, y_train)
    print("✓ Model trained")
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    print("\nModel Performance:")
    print(f"  Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"  Precision: {precision_score(y_test, y_pred, zero_division=0):.4f}")
    print(f"  Recall:    {recall_score(y_test, y_pred, zero_division=0):.4f}")
    print(f"  F1-Score:  {f1_score(y_test, y_pred, zero_division=0):.4f}")
    print(f"  AUC-ROC:   {roc_auc_score(y_test, y_pred_proba):.4f}")
    
    return model, scaler, feature_cols

# =====================================================
# SAVE ARTIFACTS
# =====================================================

def save_artifacts(model, scaler, feature_cols):
    """Save model and preprocessing artifacts."""
    
    print("\n" + "="*70)
    print("SAVING ARTIFACTS")
    print("="*70 + "\n")
    
    # Create models directory
    models_dir = os.path.join(os.path.dirname(__file__), 'ml', 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    # Save model
    model_path = os.path.join(models_dir, 'best_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"✓ Model saved: {model_path}")
    
    # Save scaler
    scaler_path = os.path.join(models_dir, 'scaler.pkl')
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)
    print(f"✓ Scaler saved: {scaler_path}")
    
    # Save feature names
    feature_path = os.path.join(models_dir, 'feature_names.pkl')
    with open(feature_path, 'wb') as f:
        pickle.dump(feature_cols, f)
    print(f"✓ Features saved: {feature_path}")
    
    print(f"\n✓ Model is ready for API predictions!")

# =====================================================
# MAIN
# =====================================================

def main():
    """Run complete test."""
    
    print("\n" + "="*70)
    print("ML PIPELINE - STANDALONE TEST")
    print("="*70)
    
    # Generate data
    df = generate_synthetic_features(n_projects=50)
    
    # Train model
    model, scaler, feature_cols = train_model(df)
    
    # Save artifacts
    save_artifacts(model, scaler, feature_cols)
    
    # Summary
    print("\n" + "="*70)
    print("✓ TEST COMPLETE")
    print("="*70)
    print("""
Next Steps:
1. Start Flask server: python app.py
2. Test predictions: curl http://localhost:5000/api/predict
3. Check if model loads correctly at startup
    """)

if __name__ == "__main__":
    main()
