"""
Prediction Routes

Endpoints for ML predictions:
- POST /api/predict - Generate prediction for project data
"""

from flask import Blueprint, jsonify, request
from services.risk_service import classify_risk
from services.recommendation_service import generate_recommendations
from services.prediction_service import PredictionService

bp = Blueprint('predictions', __name__, url_prefix='/api/predict')


@bp.route('', methods=['POST'])
def predict():
    """
    Generate a risk prediction for project data (not necessarily in database).
    
    Request body:
        {
            "project_type": "Highway",
            "land_required_ha": 120,
            "affected_families": 340,
            "compensation_percentage": 62,
            "legal_disputes": 1,
            "approval_delay_days": 45,
            "rr_progress_percentage": 40,
            "possession_percentage": 30,
            "days_in_stage": 120
        }
    
    Returns:
        {
            'delay_probability': 0.65,
            'risk_level': 'MEDIUM',
            'risk_color': 'ORANGE',
            'prediction_confidence': 0.78,
            'model_version': 'v1.0',
            'contributing_factors': [
                'Low compensation progress',
                'Rehabilitation delay'
            ],
            'recommendations': [
                {
                    'factor': 'Compensation delay',
                    'priority': 'MEDIUM',
                    'recommendation': 'Accelerate compensation processing...'
                }
            ],
            'success': True
        }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'error': 'No JSON data provided',
                'success': False
            }), 400

        PredictionService.load_model()

        feature_dict = {
            'land_required_ha': float(data.get('land_required_ha', data.get('land_required', 0) or 0)),
            'affected_families': int(data.get('affected_families', 0) or 0),
            'compensation_percentage': float(data.get('compensation_percentage', 0) or 0),
            'possession_percentage': float(data.get('possession_percentage', 0) or 0),
            'days_in_current_stage': int(data.get('days_in_current_stage', data.get('days_in_stage', 0) or 0)),
            'active_disputes': int(data.get('active_disputes', data.get('legal_disputes', 0) or 0)),
            'grievances_pending': int(data.get('grievances_pending', 0) or 0),
            'average_approval_delay_days': int(data.get('average_approval_delay_days', data.get('approval_delay_days', 0) or 0)),
            'pending_approvals': int(data.get('pending_approvals', 0) or 0),
            'project_type': data.get('project_type', 'Highway'),
            'state': data.get('state', 'Unknown'),
            'current_stage': data.get('current_stage', 'Survey'),
            'rehabilitation_percentage': float(data.get('rehabilitation_percentage', data.get('rr_progress_percentage', 0) or 0)),
        }

        result = PredictionService.predict_for_project(feature_dict)

        compensation_pct = feature_dict['compensation_percentage']
        legal_disputes = feature_dict['active_disputes']
        approval_delay = feature_dict['average_approval_delay_days']
        rr_progress = feature_dict.get('rehabilitation_percentage', 0)
        possession_pct = feature_dict['possession_percentage']
        days_in_stage = feature_dict['days_in_current_stage']

        contributing_factors = []
        if compensation_pct < 60:
            contributing_factors.append('Low compensation progress')
        if legal_disputes > 2:
            contributing_factors.append('Active legal disputes')
        if approval_delay > 45:
            contributing_factors.append('Approval delays')
        if rr_progress < 60:
            contributing_factors.append('Rehabilitation delay')
        if possession_pct < 50:
            contributing_factors.append('Low possession progress')
        if days_in_stage > 200:
            contributing_factors.append('Extended stage duration')

        recommendations = []
        if compensation_pct < 60:
            recommendations.append({
                'factor': 'Compensation delay',
                'priority': 'HIGH' if compensation_pct < 30 else 'MEDIUM',
                'recommendation': f'Accelerate compensation processing. Current progress: {compensation_pct}%'
            })
        if legal_disputes > 2:
            recommendations.append({
                'factor': 'Legal disputes',
                'priority': 'HIGH' if legal_disputes > 5 else 'MEDIUM',
                'recommendation': f'Prioritize resolution of {legal_disputes} active disputes.'
            })
        if approval_delay > 45:
            recommendations.append({
                'factor': 'Approval delay',
                'priority': 'MEDIUM',
                'recommendation': f'Escalate pending approvals. Average delay: {approval_delay} days.'
            })
        if rr_progress < 60:
            recommendations.append({
                'factor': 'R&R progress',
                'priority': 'MEDIUM',
                'recommendation': f'Accelerate rehabilitation and resettlement. Current: {rr_progress}%'
            })

        response = {
            'delay_probability': result['delay_probability'],
            'risk_level': result['risk_level'],
            'risk_color': result['risk_color'],
            'prediction_confidence': result['prediction_confidence'],
            'model_version': result['model_version'],
            'model_type': result.get('model_type'),
            'contributing_factors': contributing_factors,
            'recommendations': recommendations,
            'success': True
        }

        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Prediction error',
            'message': str(e),
            'success': False
        }), 500
