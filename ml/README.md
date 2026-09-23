"""
PHASE 5: ML PIPELINE README

Complete machine learning pipeline for delay prediction.

## Overview

Phase 5 implements a complete ML pipeline to predict project delay probability:

1. **Data Loading**: Extract features from synthetic/real project data
2. **Preprocessing**: Clean, handle missing values, scale features
3. **Feature Engineering**: Create derived features and interactions
4. **Model Training**: Train multiple models, select best performer
5. **Integration**: Integrate with Flask API for real-time predictions

## Quick Start

### Run Entire Pipeline

```bash
cd backend
python -m ml.run_pipeline
```

This runs all 4 notebooks sequentially:
1. EDA (Exploratory Data Analysis)
2. Preprocessing
3. Feature Engineering
4. Model Training

### Run Specific Step

```bash
# Exploratory Data Analysis only
python -m ml.run_pipeline --step eda

# Data Preprocessing only
python -m ml.run_pipeline --step preprocessing

# Feature Engineering only
python -m ml.run_pipeline --step features

# Model Training only
python -m ml.run_pipeline --step training
```

## Pipeline Components

### 1. EDA Notebook (ml/notebooks/eda_analysis.py)

Exploratory Data Analysis - understand data before building models.

**Input**: Raw project data from MySQL database

**Analysis**:
- Basic statistics (count, mean, median, std)
- Numeric feature distributions
- Categorical feature distributions
- Correlation with target variable (delay_probability)
- Missing data patterns
- Outlier detection (IQR method)
- Risk level distribution
- Data quality metrics

**Output**: Statistical insights and data understanding

**Run**: `python -m ml.notebooks.eda_analysis`

### 2. Preprocessing Notebook (ml/notebooks/preprocessing.py)

Data cleaning and preparation for modeling.

**Input**: Raw project data from database

**Steps**:
1. Load data from MySQL
2. Create derived features from relationships
3. Handle missing values (mean imputation)
4. Scale numeric features (StandardScaler)
5. Encode categorical features (OneHotEncoder)
6. Combine all features
7. Save processed data to CSV

**Outputs**:
- `ml/data/processed_data.csv` - Clean, processed features
- `ml/models/scaler.pkl` - Fitted StandardScaler
- `ml/models/encoder.pkl` - Fitted OneHotEncoder
- `ml/data/feature_names.pkl` - List of final feature names

**Run**: `python -m ml.notebooks.preprocessing`

### 3. Feature Engineering Notebook (ml/notebooks/feature_engineering.py)

Deep analysis of features and creation of derived features.

**Analysis**:
- Feature importance (Random Forest)
- Multicollinearity check (correlation analysis)
- Feature scaling analysis
- Missing value patterns
- Target variable distribution
- Risk level distribution

**Derived Features Created**:
1. `legal_severity` = active_disputes / affected_families
2. `compensation_velocity` = compensation_percentage / days_in_stage
3. `approval_pressure` = pending_approvals (normalized)
4. `rehabilitation_lag` = families not rehabilitated
5. `grievance_rate` = grievances_pending / affected_families

**Output**: Feature engineering recommendations

**Run**: `python -m ml.notebooks.feature_engineering`

### 4. Model Training Notebook (ml/notebooks/model_training.py)

Train and evaluate multiple ML models, select best performer.

**Models Tested**:
1. **Logistic Regression** - Baseline, interpretable
2. **Random Forest** - Ensemble, handles non-linearity
3. **Gradient Boosting** - State-of-art, best performance

**Training Process**:
1. Load preprocessed data
2. Split into train/test (80/20)
3. Scale features
4. Train baseline models
5. Cross-validation (5-fold)
6. Hyperparameter tuning (Grid Search)
7. Evaluate on test set

**Evaluation Metrics**:
- Accuracy
- Precision
- Recall
- F1-Score
- AUC-ROC

**Hyperparameter Tuning** (Gradient Boosting):
- n_estimators: [50, 100, 200]
- learning_rate: [0.01, 0.1, 0.5]
- max_depth: [3, 5, 7]

**Outputs**:
- `ml/models/best_model.pkl` - Trained model
- `ml/models/scaler.pkl` - Feature scaler
- `ml/models/encoder.pkl` - Categorical encoder
- `ml/models/feature_names.pkl` - Feature names in order
- `ml/data/model_metadata.json` - Model info and performance

**Run**: `python -m ml.notebooks.model_training`

## Input Features

### Numeric Features (9 total)
- `land_required_ha` - Land area required (hectares)
- `affected_families` - Number of families affected
- `compensation_percentage` - Percentage disbursed
- `possession_percentage` - Percentage possessed
- `days_in_current_stage` - Days in current acquisition stage
- `active_disputes` - Number of active legal disputes
- `grievances_pending` - Unresolved grievances
- `average_approval_delay_days` - Average approval delay
- `pending_approvals` - Number of pending approvals

### Categorical Features (3 total)
- `project_type` - Highway, Railway, Water Supply, etc.
- `state` - State name
- `current_stage` - Survey, Award, Possession

### Derived Features (5 total)
- `legal_severity` - Disputes per family
- `compensation_velocity` - Progress rate
- `approval_pressure` - Approval urgency
- `rehabilitation_lag` - R&R backlog
- `grievance_rate` - Grievance intensity

**Total Features**: 17 input features → ~30-35 after encoding

## Target Variable

**delay_probability**: Continuous variable (0.0 - 1.0)
- 0.0 = No delay expected
- 1.0 = High delay expected

**Binned for Classification**:
- NO_RISK: 0.0 - 0.15
- LOW: 0.15 - 0.40
- MEDIUM: 0.40 - 0.70
- HIGH: 0.70 - 1.0

## Model Performance

### Expected Results (from synthetic data)

| Model | Accuracy | Precision | Recall | F1 | AUC-ROC |
|-------|----------|-----------|--------|----|----|
| Logistic Regression | ~0.83 | ~0.82 | ~0.80 | ~0.81 | ~0.90 |
| Random Forest | ~0.87 | ~0.86 | ~0.84 | ~0.85 | ~0.93 |
| Gradient Boosting ⭐ | ~0.90 | ~0.89 | ~0.88 | ~0.88 | ~0.95 |

*Note: Actual performance depends on data quality and distribution*

## Integration with API

The trained model integrates with Flask API via `services/prediction_service.py`:

### API Endpoints Using ML Model

**1. GET /api/projects/<id>/risk**
- Returns model's risk prediction for existing project
- Uses `predict_from_db_project()` method
- Extracts features from database

**2. POST /api/predict**
- Generates prediction for new project data
- Request body includes features
- Uses `predict_for_project()` method
- Returns delay_probability + risk_level + recommendations

### Feature Extraction

```python
# From API POST request
{
    "project_type": "Highway",
    "land_required_ha": 150,
    "affected_families": 300,
    "compensation_percentage": 45,
    "legal_disputes": 3,
    "approval_delay_days": 60,
    "rr_progress_percentage": 35,
    "possession_percentage": 25,
    "days_in_stage": 200
}

↓ (Feature preparation)

# Extracted features
{
    'land_required_ha': 150.0,
    'affected_families': 300,
    'project_type': 'Highway',
    'state': 'Uttar Pradesh',
    'current_stage': 'Award',
    'compensation_percentage': 45.0,
    'possession_percentage': 25.0,
    'days_in_current_stage': 200,
    'active_disputes': 3,
    'grievances_pending': 5,
    'average_approval_delay_days': 60,
    'pending_approvals': 2
}

↓ (Preprocessing: scale + encode)

# ML Ready Features
[scaled_numeric, encoded_categorical, derived]

↓ (Model Prediction)

# Output
{
    "delay_probability": 0.68,
    "risk_level": "MEDIUM",
    "risk_color": "ORANGE",
    "model_version": "v1.0-ml"
}
```

## Configuration

File: `ml/config.py`

Key settings:
- `DB_URL` - Database connection string
- `TEST_SIZE` - Train/test split ratio (0.2)
- `CV_FOLDS` - Cross-validation folds (5)
- `RANDOM_STATE` - Random seed (42)
- `MODELS_TO_TEST` - Models to evaluate
- `HYPERPARAMETERS` - Tuning parameter ranges

## File Structure

```
ml/
├── __init__.py              # Package init
├── config.py                # Configuration & constants
├── utils.py                 # Helper functions
├── run_pipeline.py          # Master pipeline runner
│
├── notebooks/
│   ├── __init__.py
│   ├── eda_analysis.py      # Notebook 1: EDA
│   ├── preprocessing.py     # Notebook 2: Preprocessing
│   ├── feature_engineering.py  # Notebook 3: Features
│   └── model_training.py    # Notebook 4: Training
│
├── models/                  # Output artifacts
│   ├── best_model.pkl       # ⭐ Trained ML model
│   ├── scaler.pkl           # Feature scaler
│   ├── encoder.pkl          # Categorical encoder
│   └── feature_names.pkl    # Feature order
│
└── data/                    # Data files
    ├── processed_data.csv   # Cleaned features
    ├── feature_names.pkl    # Feature list
    └── model_metadata.json  # Model info
```

## Database Requirements

The pipeline expects MySQL with these tables:
- `projects` - Core project data
- `acquisition_progress` - Stage tracking
- `compensation` - Payment data
- `legal` - Dispute information
- `social_impact` - R&R data
- `approvals` - Approval status
- `prediction` - Predictions (target variable)

See `backend/README.md` for database schema.

## Dependencies

Python packages (in `requirements.txt`):
- pandas - Data manipulation
- numpy - Numeric operations
- scikit-learn - ML models and preprocessing
- sqlalchemy - Database access
- PyMySQL - MySQL driver
- joblib - Model serialization (legacy)
- pickle - Object serialization

## Troubleshooting

### "ModuleNotFoundError: No module named 'ml'"

Solution: Run from `backend/` directory:
```bash
cd backend
python -m ml.run_pipeline
```

### "Model not found" warning but API still works

Expected behavior - using heuristic fallback. To fix:
```bash
python -m ml.run_pipeline  # Train the model first
```

### Feature mismatch in prediction

Ensure POST request includes all required features. Check:
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"project_type": "Highway", ...}'
```

### Database connection error

Check:
1. MySQL is running
2. `.env` has correct credentials
3. Database `land_acquisition_db` exists
4. Tables are populated: `python load_data.py`

## Next Steps

After Phase 5 completion:

1. **Test with Real Data** (Phase 6)
   - Replace synthetic data with real project data
   - Retrain model
   - Evaluate on holdout test set

2. **Model Monitoring** (Phase 7)
   - Track prediction accuracy over time
   - Retrain periodically with new data
   - Monitor for data drift

3. **Feature Store** (Phase 8)
   - Implement feature engineering pipeline
   - Real-time feature computation
   - Version control for features

4. **Advanced Analytics** (Phase 9)
   - SHAP values for model interpretability
   - Feature importance analysis
   - Model explanation dashboard

5. **Production Deployment** (Phase 10)
   - Containerize model with Docker
   - Deploy to production servers
   - Set up monitoring and alerts

## References

- Scikit-learn: https://scikit-learn.org/
- Gradient Boosting: https://en.wikipedia.org/wiki/Gradient_boosting
- ML Pipeline Best Practices: https://mlops.community/
"""

if __name__ == '__main__':
    print(__doc__)
