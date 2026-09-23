"""
Dashboard Routes

Endpoints for dashboard statistics:
- GET /api/dashboard - Dashboard summary statistics
"""

from flask import Blueprint, jsonify
from models import Project, Prediction
from database import db

bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


@bp.route('', methods=['GET'])
def get_dashboard_stats():
    """
    Get dashboard summary statistics.
    
    Returns:
        {
            'total_projects': 6,
            'risk_distribution': {
                'high': 2,
                'medium': 2,
                'low': 1,
                'no_risk': 1
            },
            'total_affected_families': 1264,
            'total_land_ha': 714.3,
            'average_delay_probability': 0.52,
            'state_distribution': {
                'Maharashtra': 1,
                'Kerala': 1,
                'Tamil Nadu': 1,
                'Uttar Pradesh': 1,
                'Rajasthan': 1,
                'Andhra Pradesh': 1
            },
            'project_stage_distribution': {
                'Notification': 0,
                'Survey': 1,
                'Award': 2,
                'Possession': 3
            },
            'average_compensation_percentage': 46.3,
            'average_possession_percentage': 48.1,
            'total_legal_disputes': 25,
            'total_pending_grievances': 85,
            'success': True
        }
    """
    try:
        # Get all projects and predictions
        projects = Project.query.all()
        predictions = Prediction.query.all()
        
        total_projects = len(projects)
        
        if total_projects == 0:
            return jsonify({
                'error': 'No projects in database',
                'success': False
            }), 404
        
        # Risk distribution
        risk_dist = db.session.query(
            Prediction.risk_level,
            db.func.count(Prediction.risk_level).label('count')
        ).group_by(Prediction.risk_level).all()
        
        risk_distribution = {
            'high': 0,
            'medium': 0,
            'low': 0,
            'no_risk': 0
        }
        
        for level, count in risk_dist:
            if level == 'HIGH':
                risk_distribution['high'] = count
            elif level == 'MEDIUM':
                risk_distribution['medium'] = count
            elif level == 'LOW':
                risk_distribution['low'] = count
            elif level == 'NO_RISK':
                risk_distribution['no_risk'] = count
        
        # State distribution
        state_dist = db.session.query(
            Project.state,
            db.func.count(Project.project_id).label('count')
        ).group_by(Project.state).all()
        
        state_distribution = {state: count for state, count in state_dist}
        
        # Project stage distribution
        stage_dist = db.session.query(
            Project.current_stage,
            db.func.count(Project.project_id).label('count')
        ).group_by(Project.current_stage).all()
        
        project_stage_distribution = {stage: count for stage, count in stage_dist}
        
        # Calculate aggregates
        total_affected_families = sum([p.affected_families or 0 for p in projects])
        total_land_ha = sum([p.land_required_ha or 0 for p in projects])
        
        # Average delay probability
        valid_probabilities = [float(p.delay_probability) for p in predictions if p.delay_probability is not None]
        avg_delay_prob = sum(valid_probabilities) / len(valid_probabilities) if valid_probabilities else 0
        
        # Average compensation percentage
        avg_comp_pct = 0
        if projects and projects[0].compensation:
            comp_values = [p.compensation.compensation_percentage or 0 for p in projects if p.compensation]
            avg_comp_pct = sum(comp_values) / len(comp_values) if comp_values else 0
        
        # Average possession percentage
        avg_poss_pct = 0
        if projects and projects[0].acquisition:
            poss_values = [p.acquisition.possession_percentage or 0 for p in projects if p.acquisition]
            avg_poss_pct = sum(poss_values) / len(poss_values) if poss_values else 0
        
        # Total legal disputes
        total_disputes = sum([p.legal.active_disputes or 0 for p in projects if p.legal])
        
        # Total pending grievances
        total_grievances = sum([p.social_impact.grievances_pending or 0 for p in projects if p.social_impact])
        
        response = {
            'total_projects': total_projects,
            'risk_distribution': risk_distribution,
            'total_affected_families': total_affected_families,
            'total_land_ha': round(total_land_ha, 1),
            'average_delay_probability': round(avg_delay_prob, 2),
            'state_distribution': state_distribution,
            'project_stage_distribution': project_stage_distribution,
            'average_compensation_percentage': round(avg_comp_pct, 1),
            'average_possession_percentage': round(avg_poss_pct, 1),
            'total_legal_disputes': total_disputes,
            'total_pending_grievances': total_grievances,
            'success': True
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e),
            'success': False
        }), 500
