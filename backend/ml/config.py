"""
ML Pipeline Configuration

Settings for model training, feature engineering, and evaluation.
"""

import os

# =====================================================
# PATHS
# =====================================================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ML_DIR = os.path.join(PROJECT_ROOT, 'ml')
NOTEBOOKS_DIR = os.path.join(ML_DIR, 'notebooks')
MODELS_DIR = os.path.join(ML_DIR, 'models')
DATA_DIR = os.path.join(ML_DIR, 'data')

# Ensure directories exist
for directory in [MODELS_DIR, DATA_DIR, NOTEBOOKS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Model paths
BEST_MODEL_PATH = os.path.join(MODELS_DIR, 'best_model.pkl')
SCALER_PATH = os.path.join(MODELS_DIR, 'scaler.pkl')
ENCODER_PATH = os.path.join(MODELS_DIR, 'encoder.pkl')
FEATURE_NAMES_PATH = os.path.join(MODELS_DIR, 'feature_names.pkl')

# =====================================================
# DATABASE
# =====================================================

# Load from environment or use default
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', 3306)
DB_NAME = os.getenv('DB_NAME', 'land_acquisition_db')

# SQLAlchemy connection string
DB_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# =====================================================
# FEATURE ENGINEERING
# =====================================================

# Target variable
TARGET = 'delay_probability'

# Numeric features to extract from database
NUMERIC_FEATURES = [
    'land_required_ha',
    'affected_families',
    'compensation_percentage',
    'possession_percentage',
    'days_in_current_stage',
    'active_disputes',
    'pending_grievances',
    'average_approval_delay_days',
    'pending_approvals',
]

# Categorical features
CATEGORICAL_FEATURES = [
    'project_type',
    'state',
    'current_stage',
]

# Derived features (created from relationships)
DERIVED_FEATURES = [
    'legal_severity',
    'compensation_velocity',
    'approval_pressure',
    'rehabilitation_lag',
]

# All features used by model
ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES + DERIVED_FEATURES

# =====================================================
# MODEL TRAINING
# =====================================================

# Train/test split
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Cross-validation folds
CV_FOLDS = 5

# =====================================================
# PREPROCESSING
# =====================================================

# Handle missing values
MISSING_VALUE_STRATEGY = 'mean'

# Scale numeric features
SCALER_TYPE = 'standard'

# Encode categorical features
ENCODER_TYPE = 'onehot'

# =====================================================
# LOGGING
# =====================================================

LOG_LEVEL = 'INFO'
LOG_FILE = os.path.join(ML_DIR, 'training.log')
