"""ML Pipeline Utilities - Helper functions"""

import pandas as pd
import numpy as np
import pickle
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import logging

from ml.config import (
    DB_URL, TARGET, NUMERIC_FEATURES, CATEGORICAL_FEATURES,
    SCALER_PATH, ENCODER_PATH, BEST_MODEL_PATH, FEATURE_NAMES_PATH, 
    LOG_FILE, LOG_LEVEL
)

# =====================================================
# LOGGING
# =====================================================

def setup_logging():
    """Configure logging for ML pipeline."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# =====================================================
# DATA LOADING
# =====================================================

def load_projects_from_database():
    """Load projects from database and extract features."""
    logger.info("Connecting to database...")
    
    try:
        engine = create_engine(DB_URL)
        
        # Load projects with all relationships
        query = """
        SELECT 
            p.project_id,
            p.project_type,
            p.state,
            p.land_required_ha,
            p.affected_families,
            
            ap.current_stage,
            ap.overall_progress_percentage,
            ap.possession_percentage,
            ap.days_in_current_stage,
            
            c.compensation_percentage,
            c.pending_cases,
            c.average_payment_delay_days,
            
            l.active_disputes,
            l.dispute_count,
            l.court_cases,
            
            si.grievances_pending,
            si.rehabilitation_percentage,
            si.resettlement_percentage,
            
            a.pending_approvals,
            a.average_approval_delay_days,
            
            pred.delay_probability
        FROM projects p
        LEFT JOIN acquisition_progress ap ON p.project_id = ap.project_id
        LEFT JOIN compensation c ON p.project_id = c.project_id
        LEFT JOIN legal l ON p.project_id = l.project_id
        LEFT JOIN social_impact si ON p.project_id = si.project_id
        LEFT JOIN approvals a ON p.project_id = a.project_id
        LEFT JOIN prediction pred ON p.project_id = pred.project_id
        ORDER BY p.project_id
        """
        
        df = pd.read_sql(query, engine)
        logger.info(f"✓ Loaded {len(df)} projects from database")
        
        return df
        
    except Exception as e:
        logger.error(f"✗ Failed to load data: {str(e)}")
        raise

# =====================================================
# FEATURE ENGINEERING
# =====================================================

def create_derived_features(df):
    """Create derived features from raw data."""
    logger.info("Creating derived features...")
    
    df = df.copy()
    
    # Legal severity
    df['legal_severity'] = np.where(
        df['affected_families'] > 0,
        df['active_disputes'] / df['affected_families'],
        0
    )
    
    # Compensation velocity
    df['compensation_velocity'] = np.where(
        df['days_in_current_stage'] > 0,
        df['compensation_percentage'] / df['days_in_current_stage'],
        0
    )
    
    # Approval pressure
    df['approval_pressure'] = df['pending_approvals'].fillna(0)
    
    # Rehabilitation lag
    df['rehabilitation_lag'] = np.where(
        df['affected_families'] > 0,
        (100 - df['rehabilitation_percentage'].fillna(0)) / 100 * df['affected_families'],
        0
    )
    
    logger.info(f"✓ Created derived features")
    
    return df

# =====================================================
# PREPROCESSING
# =====================================================

def handle_missing_values(df, strategy='mean'):
    """Handle missing values in dataset."""
    logger.info(f"Handling missing values with strategy: {strategy}")
    
    df = df.copy()
    
    if strategy == 'mean':
        for col in NUMERIC_FEATURES:
            if col in df.columns:
                df[col].fillna(df[col].mean(), inplace=True)
    
    logger.info(f"✓ Missing values handled")
    
    return df

def scale_features(X_train, X_test=None):
    """Scale numeric features."""
    logger.info("Scaling features...")
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    if X_test is not None:
        X_test_scaled = scaler.transform(X_test)
    else:
        X_test_scaled = None
    
    logger.info(f"✓ Features scaled")
    
    return X_train_scaled, X_test_scaled, scaler

# =====================================================
# MODEL PERSISTENCE
# =====================================================

def save_model(model, scaler=None, encoder=None, feature_names=None):
    """Save trained model and preprocessing objects."""
    logger.info("Saving model...")
    
    try:
        with open(BEST_MODEL_PATH, 'wb') as f:
            pickle.dump(model, f)
        
        if scaler:
            with open(SCALER_PATH, 'wb') as f:
                pickle.dump(scaler, f)
        
        if feature_names is not None:
            with open(FEATURE_NAMES_PATH, 'wb') as f:
                pickle.dump(feature_names, f)
        
        logger.info(f"✓ Model saved to {BEST_MODEL_PATH}")
        
    except Exception as e:
        logger.error(f"✗ Failed to save model: {str(e)}")
        raise

def load_model(model_path=BEST_MODEL_PATH):
    """Load trained model."""
    logger.info(f"Loading model from {model_path}...")
    
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        logger.info(f"✓ Model loaded")
        return model
        
    except Exception as e:
        logger.error(f"✗ Failed to load model: {str(e)}")
        raise

# =====================================================
# EVALUATION
# =====================================================

def print_summary(df, y=None):
    """Print data summary statistics."""
    logger.info("\n" + "="*60)
    logger.info("DATA SUMMARY")
    logger.info("="*60)
    logger.info(f"Shape: {df.shape}")
    
    if y is not None:
        logger.info(f"\nTarget (delay_probability):")
        logger.info(f"  Mean: {y.mean():.4f}")
        logger.info(f"  Std:  {y.std():.4f}")
        logger.info(f"  Min:  {y.min():.4f}")
        logger.info(f"  Max:  {y.max():.4f}")
    
    logger.info("="*60 + "\n")
