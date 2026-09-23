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
    'legal_severity',           # disputes / affected_families
    'compensation_velocity',    # compensation_percentage / days_in_stage
    'approval_pressure',        # pending_approvals / expected_approvals
    'rehabilitation_lag',       # affected_families - resettled_families
]

# All features used by model
ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES + DERIVED_FEATURES

# =====================================================
# MODEL TRAINING
# =====================================================

# Train/test split
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Model parameters
MODELS_TO_TEST = ['logistic_regression', 'random_forest', 'gradient_boosting']

# Hyperparameters for GridSearchCV
HYPERPARAMETERS = {
    'logistic_regression': {
        'C': [0.001, 0.01, 0.1, 1, 10],
        'max_iter': [1000, 2000],
    },
    'random_forest': {
        'n_estimators': [50, 100, 200],
        'max_depth': [5, 10, None],
        'min_samples_split': [2, 5],
    },
    'gradient_boosting': {
        'n_estimators': [50, 100, 200],
        'learning_rate': [0.01, 0.1, 0.5],
        'max_depth': [3, 5, 7],
    }
}

# Cross-validation folds
CV_FOLDS = 5

# =====================================================
# EVALUATION METRICS
# =====================================================

# Metrics to track
EVAL_METRICS = ['accuracy', 'precision', 'recall', 'f1', 'auc_roc']

# Thresholds for risk classification
RISK_THRESHOLDS = {
    'NO_RISK': (0.0, 0.15),
    'LOW': (0.15, 0.40),
    'MEDIUM': (0.40, 0.70),
    'HIGH': (0.70, 1.0),
}

# =====================================================
# PREPROCESSING
# =====================================================

# Handle missing values
MISSING_VALUE_STRATEGY = 'mean'  # 'mean', 'median', 'forward_fill'

# Scale numeric features
SCALER_TYPE = 'standard'  # 'standard', 'minmax', 'robust'

# Encode categorical features
ENCODER_TYPE = 'onehot'  # 'onehot', 'label'

# =====================================================
# LOGGING
# =====================================================

LOG_LEVEL = 'INFO'
LOG_FILE = os.path.join(ML_DIR, 'training.log')
