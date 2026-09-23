"""
ML Pipeline Utilities

Helper functions for data loading, preprocessing, and evaluation.
"""

import pandas as pd
import numpy as np
import pickle
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
import logging

from ml.config import (
    DB_URL, TARGET, NUMERIC_FEATURES, CATEGORICAL_FEATURES,
    TEST_SIZE, RANDOM_STATE, SCALER_PATH, ENCODER_PATH,
    BEST_MODEL_PATH, FEATURE_NAMES_PATH, LOG_FILE, LOG_LEVEL
)

# =====================================================
# LOGGING
# =====================================================

def setup_logging():
    """Configure logging for ML pipeline."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# =====================================================
# DATA LOADING
# =====================================================

def load_projects_from_database():
    """
    Load projects from database and extract features.
    
    Returns:
        pd.DataFrame: Features and target variable
    """
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
        logger.info(f"Columns: {list(df.columns)}")
        
        return df
        
    except Exception as e:
        logger.error(f"✗ Failed to load data: {str(e)}")
        raise

# =====================================================
# FEATURE ENGINEERING
# =====================================================

def create_derived_features(df):
    """
    Create derived features from raw data.
    
    Args:
        df (pd.DataFrame): Raw project data
        
    Returns:
        pd.DataFrame: Data with derived features
    """
    logger.info("Creating derived features...")
    
    df = df.copy()
    
    # Legal severity (disputes per family)
    df['legal_severity'] = np.where(
        df['affected_families'] > 0,
        df['active_disputes'] / df['affected_families'],
        0
    )
    
    # Compensation velocity (progress per day in stage)
    df['compensation_velocity'] = np.where(
        df['days_in_current_stage'] > 0,
        df['compensation_percentage'] / df['days_in_current_stage'],
        0
    )
    
    # Approval pressure (pending approvals count)
    df['approval_pressure'] = df['pending_approvals'].fillna(0)
    
    # Rehabilitation lag (families not rehabilitated)
    df['rehabilitation_lag'] = np.where(
        df['affected_families'] > 0,
        (100 - df['rehabilitation_percentage'].fillna(0)) / 100 * df['affected_families'],
        0
    )
    
    # Grievance rate (per family)
    df['grievance_rate'] = np.where(
        df['affected_families'] > 0,
        df['grievances_pending'].fillna(0) / df['affected_families'],
        0
    )
    
    logger.info(f"✓ Created derived features: legal_severity, compensation_velocity, etc.")
    
    return df

# =====================================================
# PREPROCESSING
# =====================================================

def handle_missing_values(df, strategy='mean'):
    """
    Handle missing values in dataset.
    
    Args:
        df (pd.DataFrame): Input data
        strategy (str): 'mean', 'median', 'forward_fill'
        
    Returns:
        pd.DataFrame: Data with handled missing values
    """
    logger.info(f"Handling missing values with strategy: {strategy}")
    
    df = df.copy()
    
    if strategy == 'mean':
        for col in NUMERIC_FEATURES:
            if col in df.columns:
                df[col].fillna(df[col].mean(), inplace=True)
    
    elif strategy == 'median':
        for col in NUMERIC_FEATURES:
            if col in df.columns:
                df[col].fillna(df[col].median(), inplace=True)
    
    elif strategy == 'forward_fill':
        df.fillna(method='ffill', inplace=True)
        df.fillna(df.mean(), inplace=True)
    
    logger.info(f"✓ Missing values handled")
    
    return df

def scale_features(X_train, X_test=None):
    """
    Scale numeric features.
    
    Args:
        X_train (pd.DataFrame): Training features
        X_test (pd.DataFrame): Test features (optional)
        
    Returns:
        tuple: (X_train_scaled, X_test_scaled, scaler)
    """
    logger.info("Scaling features...")
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    if X_test is not None:
        X_test_scaled = scaler.transform(X_test)
    else:
        X_test_scaled = None
    
    logger.info(f"✓ Features scaled")
    
    return X_train_scaled, X_test_scaled, scaler

def encode_categorical(X_train, X_test=None, columns=None):
    """
    Encode categorical features using OneHotEncoder.
    
    Args:
        X_train (pd.DataFrame): Training features
        X_test (pd.DataFrame): Test features (optional)
        columns (list): Columns to encode
        
    Returns:
        tuple: (X_train_encoded, X_test_encoded, encoder, feature_names)
    """
    logger.info("Encoding categorical features...")
    
    if columns is None:
        columns = CATEGORICAL_FEATURES
    
    encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
    X_train_encoded = encoder.fit_transform(X_train[columns])
    
    feature_names = encoder.get_feature_names_out(columns)
    
    if X_test is not None:
        X_test_encoded = encoder.transform(X_test[columns])
    else:
        X_test_encoded = None
    
    logger.info(f"✓ Encoded {len(feature_names)} categorical features")
    
    return X_train_encoded, X_test_encoded, encoder, feature_names

# =====================================================
# TRAIN/TEST SPLIT
# =====================================================

def split_data(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE):
    """
    Split data into train and test sets.
    
    Args:
        X (pd.DataFrame): Features
        y (pd.Series): Target
        test_size (float): Test set proportion
        random_state (int): Random seed
        
    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    logger.info(f"Splitting data: {100*(1-test_size)}% train, {100*test_size}% test")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=pd.cut(y, bins=4, duplicates='drop')  # Stratify by risk level
    )
    
    logger.info(f"✓ Train: {len(X_train)}, Test: {len(X_test)}")
    
    return X_train, X_test, y_train, y_test

# =====================================================
# MODEL PERSISTENCE
# =====================================================

def save_model(model, scaler=None, encoder=None, feature_names=None):
    """
    Save trained model and preprocessing objects.
    
    Args:
        model: Trained sklearn model
        scaler: Fitted StandardScaler
        encoder: Fitted OneHotEncoder
        feature_names: Feature names used in training
    """
    logger.info("Saving model...")
    
    try:
        with open(BEST_MODEL_PATH, 'wb') as f:
            pickle.dump(model, f)
        
        if scaler:
            with open(SCALER_PATH, 'wb') as f:
                pickle.dump(scaler, f)
        
        if encoder:
            with open(ENCODER_PATH, 'wb') as f:
                pickle.dump(encoder, f)
        
        if feature_names is not None:
            with open(FEATURE_NAMES_PATH, 'wb') as f:
                pickle.dump(feature_names, f)
        
        logger.info(f"✓ Model saved to {BEST_MODEL_PATH}")
        
    except Exception as e:
        logger.error(f"✗ Failed to save model: {str(e)}")
        raise

def load_model(model_path=BEST_MODEL_PATH):
    """
    Load trained model.
    
    Args:
        model_path (str): Path to model file
        
    Returns:
        model: Trained sklearn model
    """
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
    logger.info(f"\nColumns: {list(df.columns)}")
    
    if y is not None:
        logger.info(f"\nTarget (delay_probability):")
        logger.info(f"  Mean: {y.mean():.4f}")
        logger.info(f"  Std:  {y.std():.4f}")
        logger.info(f"  Min:  {y.min():.4f}")
        logger.info(f"  Max:  {y.max():.4f}")
    
    logger.info("\nMissing values:")
    logger.info(df.isnull().sum())
    
    logger.info("\nData types:")
    logger.info(df.dtypes)
    logger.info("="*60 + "\n")
