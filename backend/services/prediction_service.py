"""
Prediction Service - Phase 5 Integration

Handles ML model loading and prediction generation.
Integrated with trained ML model from Phase 5.

Loads:
  - best_model.pkl - Trained Gradient Boosting model
  - scaler.pkl - StandardScaler for numeric features
  - encoder.pkl - OneHotEncoder for categorical features
  - feature_names.pkl - List of feature names in training order
"""

import os
import pickle
import numpy as np
import pandas as pd
from services.risk_service import RiskClassifier
from services.recommendation_service import RecommendationGenerator

class PredictionService:
    """
    Service for making predictions using the trained ML model (Phase 5).
    
    Loaded at Flask startup via initialize_prediction_service()
    """
    
    _model = None
    _scaler = None
    _encoder = None
    _feature_names = None
    _model_ready = False
    
    # Paths to model artifacts
    MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'ml', 'models', 'best_model.pkl')
    SCALER_PATH = os.path.join(os.path.dirname(__file__), '..', 'ml', 'models', 'scaler.pkl')
    ENCODER_PATH = os.path.join(os.path.dirname(__file__), '..', 'ml', 'models', 'encoder.pkl')
    FEATURE_NAMES_PATH = os.path.join(os.path.dirname(__file__), '..', 'ml', 'models', 'feature_names.pkl')
    
    # Features expected in input
    NUMERIC_FEATURES = [
        'land_required_ha', 'affected_families', 'compensation_percentage',
        'possession_percentage', 'days_in_current_stage', 'active_disputes',
        'grievances_pending', 'average_approval_delay_days', 'pending_approvals'
    ]
    
    CATEGORICAL_FEATURES = [
        'project_type', 'state', 'current_stage'
    ]

    DERIVED_FEATURES = [
        'legal_severity',
        'compensation_velocity',
        'approval_pressure',
        'rehabilitation_lag',
    ]
    
    @classmethod
    def load_model(cls):
        """
        Load the ML model and preprocessing artifacts from disk.
        Called once at Flask application startup.
        
        Returns:
            bool: True if model loaded successfully, False otherwise
        """
        if cls._model_ready:
            return True
        
        try:
            # Load trained model
            if os.path.exists(cls.MODEL_PATH):
                with open(cls.MODEL_PATH, 'rb') as f:
                    cls._model = pickle.load(f)
                print(f"✓ ML model loaded from {cls.MODEL_PATH}")
            else:
                print(f"⚠ Model not found at {cls.MODEL_PATH}")
                print("  Falling back to heuristic predictions")
                cls._model = None
            
            # Load scaler
            if os.path.exists(cls.SCALER_PATH):
                with open(cls.SCALER_PATH, 'rb') as f:
                    cls._scaler = pickle.load(f)
                print(f"✓ Feature scaler loaded")
            
            # Load encoder
            if os.path.exists(cls.ENCODER_PATH):
                with open(cls.ENCODER_PATH, 'rb') as f:
                    cls._encoder = pickle.load(f)
                print(f"✓ Categorical encoder loaded")
            
            # Load feature names
            if os.path.exists(cls.FEATURE_NAMES_PATH):
                with open(cls.FEATURE_NAMES_PATH, 'rb') as f:
                    cls._feature_names = pickle.load(f)
                print(f"✓ Feature names loaded ({len(cls._feature_names)} features)")
            
            cls._model_ready = cls._model is not None
            
            if cls._model_ready:
                print("✓ Prediction service ready with ML model (Phase 5)")
            else:
                print("⚠ Prediction service ready but using heuristics (no trained model)")
            
            return cls._model_ready
            
        except Exception as e:
            print(f"✗ Error loading ML model: {e}")
            print("  Falling back to heuristic predictions")
            cls._model_ready = False
            return False
    
    @classmethod
    def _prepare_features(cls, features_dict):
        """
        Prepare features for ML model prediction.
        
        Args:
            features_dict (dict): Dictionary with feature values
            
        Returns:
            np.ndarray: Features in correct format for model, or None if error
        """
        try:
            # Create a row with all expected feature names in the model order
            row = dict(features_dict)

            # Add missing numeric values with safe defaults
            row.setdefault('land_required_ha', 0.0)
            row.setdefault('affected_families', 0)
            row.setdefault('compensation_percentage', 0.0)
            row.setdefault('possession_percentage', 0.0)
            row.setdefault('days_in_current_stage', 0)
            row.setdefault('active_disputes', 0)
            row.setdefault('grievances_pending', 0)
            row.setdefault('average_approval_delay_days', 0)
            row.setdefault('pending_approvals', 0)

            # Derived features
            affected_families = float(row.get('affected_families', 0) or 0)
            days_in_stage = float(row.get('days_in_current_stage', 0) or 0)
            compensation_pct = float(row.get('compensation_percentage', 0) or 0)
            row['legal_severity'] = (float(row.get('active_disputes', 0) or 0) / (affected_families + 1))
            row['compensation_velocity'] = (compensation_pct / (days_in_stage + 1))
            row['approval_pressure'] = float(row.get('pending_approvals', 0) or 0)
            row['rehabilitation_lag'] = ((100.0 - float(row.get('rehabilitation_percentage', 0) or 0)) / 100.0) * affected_families

            # If the model was trained with a saved feature name list, respect that exact order.
            feature_names = cls._feature_names or cls.NUMERIC_FEATURES + cls.DERIVED_FEATURES
            feature_df = pd.DataFrame([row])
            for name in feature_names:
                if name not in feature_df.columns:
                    feature_df[name] = 0

            X = feature_df[feature_names].fillna(0).astype(float)

            if cls._scaler is not None:
                X = cls._scaler.transform(X)

            return X
            
        except Exception as e:
            print(f"✗ Error preparing features: {e}")
            return None
    
    @classmethod
    def predict_for_project(cls, features_dict):
        """
        Make a prediction for a project based on feature dictionary.
        
        Args:
            features_dict (dict): Dictionary with keys:
                - land_required_ha (float)
                - affected_families (int)
                - compensation_percentage (float)
                - possession_percentage (float)
                - days_in_current_stage (int)
                - active_disputes (int)
                - grievances_pending (int)
                - average_approval_delay_days (int)
                - pending_approvals (int)
                - project_type (str) - Highway, Railway, etc.
                - state (str) - State name
                - current_stage (str) - Survey, Award, Possession
            
            Returns:
                dict: Prediction result with delay_probability, risk_level, etc.
        """
        # Use heuristic fallback if model not available
        if not cls._model_ready:
            return cls._predict_heuristic(features_dict)
        
        try:
            # Prepare features
            X = cls._prepare_features(features_dict)
            
            if X is None:
                return cls._predict_heuristic(features_dict)
            
            # Make prediction
            prediction_proba = cls._model.predict_proba(X)[0]
            delay_probability = float(prediction_proba[1])  # Probability of high risk class
            
            # Classify risk
            risk_classification = RiskClassifier.classify(delay_probability)
            
            return {
                'delay_probability': risk_classification['delay_probability'],
                'risk_level': risk_classification['risk_level'],
                'risk_color': risk_classification['risk_color'],
                'prediction_confidence': 0.95,  # ML model confidence
                'model_version': 'v1.0-ml',
                'model_type': 'GradientBoostingClassifier',
            }
            
        except Exception as e:
            print(f"✗ ML prediction error: {e}")
            # Fall back to heuristic
            return cls._predict_heuristic(features_dict)
    
    @classmethod
    def _predict_heuristic(cls, features_dict):
        """
        Fallback heuristic prediction (when ML model not available).
        Uses rule-based approach based on feature values.
        
        Args:
            features_dict (dict): Dictionary with feature values
            
        Returns:
            dict: Prediction result
        """
        # Heuristic rules (from Phase 4)
        probability = 0.0
        
        # Rule 1: Low compensation (< 30%)
        if features_dict.get('compensation_percentage', 0) < 30:
            probability += 0.25
        
        # Rule 2: Active disputes (> 5)
        if features_dict.get('active_disputes', 0) > 5:
            probability += 0.20
        
        # Rule 3: High pending grievances (> 10)
        if features_dict.get('grievances_pending', 0) > 10:
            probability += 0.15
        
        # Rule 4: Low possession (< 20%)
        if features_dict.get('possession_percentage', 0) < 20:
            probability += 0.20
        
        # Rule 5: High approval delays (> 90 days)
        if features_dict.get('average_approval_delay_days', 0) > 90:
            probability += 0.15
        
        # Rule 6: Many pending approvals
        if features_dict.get('pending_approvals', 0) > 2:
            probability += 0.10
        
        # Rule 7: Large affected population (> 300 families)
        if features_dict.get('affected_families', 0) > 300:
            probability += 0.05
        
        # Normalize to [0, 1]
        delay_probability = min(max(probability, 0.0), 1.0)
        
        # Classify risk
        risk_classification = RiskClassifier.classify(delay_probability)
        
        return {
            'delay_probability': risk_classification['delay_probability'],
            'risk_level': risk_classification['risk_level'],
            'risk_color': risk_classification['risk_color'],
            'prediction_confidence': 0.60,  # Lower confidence for heuristic
            'model_version': 'v1.0-heuristic',
            'model_type': 'RuleBasedHeuristic',
        }
    
    @classmethod
    def predict_from_db_project(cls, project_obj):
        """
        Make a prediction for a project object from database.
        Extracts features from SQLAlchemy model instances.
        
        Args:
            project_obj (Project): SQLAlchemy Project model instance
            
        Returns:
            dict: Prediction result
        """
        try:
            # Extract features from related objects
            features_dict = {
                # From project
                'land_required_ha': float(project_obj.land_required_ha or 0),
                'affected_families': int(project_obj.affected_families or 0),
                'project_type': project_obj.project_type or 'unknown',
                'state': project_obj.state or 'unknown',
                
                # From acquisition_progress
                'current_stage': (project_obj.acquisition_progress.current_stage 
                                 if project_obj.acquisition_progress else 'Survey'),
                'possession_percentage': float(
                    project_obj.acquisition_progress.possession_percentage or 0
                    if project_obj.acquisition_progress else 0),
                'days_in_current_stage': int(
                    project_obj.acquisition_progress.days_in_current_stage or 0
                    if project_obj.acquisition_progress else 0),
                
                # From compensation
                'compensation_percentage': float(
                    project_obj.compensation.compensation_percentage or 0
                    if project_obj.compensation else 0),
                
                # From legal
                'active_disputes': int(
                    project_obj.legal.active_disputes or 0
                    if project_obj.legal else 0),
                
                # From social_impact
                'grievances_pending': int(
                    project_obj.social_impact.grievances_pending or 0
                    if project_obj.social_impact else 0),
                
                # From approvals
                'average_approval_delay_days': int(
                    project_obj.approvals.average_approval_delay_days or 0
                    if project_obj.approvals else 0),
                'pending_approvals': int(
                    project_obj.approvals.pending_approvals or 0
                    if project_obj.approvals else 0),
            }
            
            return cls.predict_for_project(features_dict)
            
        except Exception as e:
            print(f"✗ Error extracting features from project: {e}")
            return {
                'error': f'Prediction error: {str(e)}',
                'delay_probability': None,
                'risk_level': None,
                'risk_color': None,
            }


def initialize_prediction_service(app):
    """
    Initialize the prediction service when Flask app starts.
    Loads ML model and preprocessing artifacts (Phase 5).
    
    Args:
        app: Flask application instance
    """
    with app.app_context():
        print("\n" + "="*60)
        print("Initializing ML Prediction Service (Phase 5)")
        print("="*60)
        
        success = PredictionService.load_model()
        
        if success:
            print("✓ ML Prediction Service initialized successfully")
        else:
            print("⚠ ML Prediction Service using fallback heuristics")
        
        print("="*60 + "\n")
