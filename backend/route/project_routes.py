"""
Project Routes

Endpoints for project information:
- GET /api/projects - List all projects
- GET /api/projects/<project_id> - Project details
- GET /api/projects/<project_id>/risk - Risk assessment
- GET /api/projects/<project_id>/recommendations - Recommendations
"""

from flask import Blueprint, jsonify, request
from models import EvidenceObservation, Project, Prediction, Recommendation
from database import db

bp = Blueprint('projects', __name__, url_prefix='/api/projects')


def evidence_summary(project_id):
    query = EvidenceObservation.query.filter_by(project_id=project_id)
    return {
        'observation_count': query.count(),
        'source_count': query.with_entities(EvidenceObservation.source_id).distinct().count(),
        'latest_observation_date': (
            query.order_by(EvidenceObservation.observation_date.desc()).first().observation_date.isoformat()
            if query.filter(EvidenceObservation.observation_date.isnot(None)).first()
            else None
        ),
        'conflicting_count': query.filter_by(conflict_flag=True).count(),
        'model_eligible_count': query.filter_by(ml_eligible=True).count(),
        'verification_statuses': {
            status: query.filter_by(verification_status=status).count()
            for status in ('official', 'verified_manual', 'public_snapshot', 'review_required', 'stale')
        },
    }


@bp.route('', methods=['GET'])
def list_projects():
    """
    Get list of all projects with basic information.
    
    Query Parameters:
        - state: Filter by state (optional)
        - risk_level: Filter by risk level (HIGH, MEDIUM, LOW, NO_RISK) (optional)
        - limit: Max results to return (default: 100)
        - offset: Skip N results (default: 0)
    
    Returns:
        {
            'projects': [
                {
                    'project_id': 'DEMO_001',
                    'project_name': 'Highway Project',
                    'state': 'Maharashtra',
                    'district': 'Nashik',
                    'risk_level': 'HIGH',
                    'delay_probability': 0.82,
                    'affected_families': 250
                }
            ],
            'total': 6,
            'limit': 100,
            'offset': 0
        }
    """
    try:
        # Get query parameters
        state = request.args.get('state', None)
        risk_level = request.args.get('risk_level', None)
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        
        # Build query
        query = Project.query
        
        # Apply filters
        if state:
            query = query.filter_by(state=state)
        if risk_level:
            # Filter by risk level via prediction
            query = query.join(Prediction).filter(Prediction.risk_level == risk_level)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply pagination
        projects = query.limit(limit).offset(offset).all()
        
        # Build response
        projects_data = []
        for project in projects:
            # Get latest prediction if available
            prediction = project.predictions[0] if project.predictions else None
            
            project_dict = {
                'project_id': project.project_id,
                'project_name': project.project_name,
                'project_type': project.project_type,
                'state': project.state,
                'district': project.district,
                'village': project.village,
                'affected_families': project.affected_families,
                'land_required_ha': project.land_required_ha,
                'current_stage': project.current_stage,
                'status': project.status,
                'source_name': project.source_name,
                'source_url': project.source_url,
                'source_document_url': project.source_document_url,
                'data_status': project.data_status,
                'barriers': [barrier.to_dict() for barrier in project.barriers],
                'evidence': evidence_summary(project.project_id),
            }
            
            if prediction:
                project_dict.update({
                    'delay_probability': float(prediction.delay_probability) if prediction.delay_probability is not None else None,
                    'risk_level': prediction.risk_level,
                    'risk_color': prediction.risk_color,
                })
            
            projects_data.append(project_dict)
        
        return jsonify({
            'projects': projects_data,
            'total': total,
            'limit': limit,
            'offset': offset,
            'success': True
        }), 200
        
    except ValueError as e:
        return jsonify({
            'error': 'Invalid query parameters',
            'message': str(e),
            'success': False
        }), 400
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e),
            'success': False
        }), 500


@bp.route('/<project_id>', methods=['GET'])
def get_project_details(project_id):
    """
    Get complete information for a single project.
    
    Returns:
        {
            'project': {
                'project_id': 'DEMO_001',
                'project_name': 'Highway Project',
                ...
            },
            'location': {
                'latitude': 20.0054,
                'longitude': 73.7898,
                'accuracy_level': 'project-level'
            },
            'progress': {
                'current_stage': 'Award',
                'overall_progress_percentage': 28,
                'possession_percentage': 15,
                'days_in_current_stage': 385
            },
            'compensation': {
                'total_amount': 75000000,
                'disbursed': 18750000,
                'percentage': 25,
                'families_eligible': 425,
                'families_paid': 95
            },
            'legal': {
                'active_disputes': 8,
                'court_cases': 3
            },
            'social_impact': {
                'rehabilitation_percentage': 30,
                'resettlement_percentage': 25
            },
            'approvals': {
                'pending_approvals': 2,
                'average_delay_days': 95
            },
            'risk': {
                'delay_probability': 0.82,
                'risk_level': 'HIGH',
                'risk_color': 'RED'
            },
            'recommendations': [...]
        }
    """
    try:
        project = Project.query.get(project_id)
        
        if not project:
            return jsonify({
                'error': 'Project not found',
                'project_id': project_id,
                'success': False
            }), 404
        
        # Get location (first location, usually only one)
        location = project.locations[0] if project.locations else None
        
        # Build response
        response = {
            'project': {
                'project_id': project.project_id,
                'project_name': project.project_name,
                'project_type': project.project_type,
                'agency': project.agency,
                'state': project.state,
                'district': project.district,
                'village': project.village,
                'land_required_ha': project.land_required_ha,
                'affected_families': project.affected_families,
                'current_stage': project.current_stage,
                'status': project.status,
                'source_name': project.source_name,
                'source_url': project.source_url,
                'source_document_url': project.source_document_url,
                'data_status': project.data_status,
                'created_at': project.created_at.isoformat() if project.created_at else None,
                'updated_at': project.updated_at.isoformat() if project.updated_at else None,
            },
            'location': None,
            'progress': None,
            'compensation': None,
            'legal': None,
            'social_impact': None,
            'approvals': None,
            'risk': None,
            'recommendations': [],
            'barriers': [],
            'climate': None,
            'evidence': evidence_summary(project_id),
            'success': True
        }
        
        # Add location data
        if location:
            response['location'] = {
                'latitude': location.latitude,
                'longitude': location.longitude,
                'location_source': location.location_source,
                'accuracy_level': location.accuracy_level,
            }
        
        # Add progress data
        if project.acquisition:
            response['progress'] = {
                'current_stage': project.acquisition.current_stage,
                'notification_status': project.acquisition.notification_status,
                'survey_status': project.acquisition.survey_status,
                'award_status': project.acquisition.award_status,
                'possession_status': project.acquisition.possession_status,
                'overall_progress_percentage': project.acquisition.overall_progress_percentage,
                'possession_percentage': project.acquisition.possession_percentage,
                'days_in_current_stage': project.acquisition.days_in_current_stage,
            }
        
        # Add compensation data
        if project.compensation:
            response['compensation'] = {
                'total_amount': project.compensation.total_compensation_amount,
                'disbursed': project.compensation.amount_disbursed,
                'percentage': project.compensation.compensation_percentage,
                'families_eligible': project.compensation.families_eligible,
                'families_paid': project.compensation.families_paid,
                'pending_cases': project.compensation.pending_cases,
                'average_payment_delay_days': project.compensation.average_payment_delay_days,
            }
        
        # Add legal data
        if project.legal:
            response['legal'] = {
                'active_disputes': project.legal.active_disputes,
                'dispute_count': project.legal.dispute_count,
                'court_cases': project.legal.court_cases,
                'legal_status': project.legal.legal_status,
                'average_case_age_days': project.legal.average_case_age_days,
            }
        
        # Add social impact data
        if project.social_impact:
            response['social_impact'] = {
                'affected_families': project.social_impact.affected_families,
                'rehabilitation_percentage': project.social_impact.rehabilitation_progress_percentage,
                'resettlement_percentage': project.social_impact.resettlement_progress_percentage,
                'relocation_completed_percentage': project.social_impact.relocation_completed_percentage,
                'grievances_pending': project.social_impact.grievances_pending,
                'stakeholder_responsiveness': project.social_impact.stakeholder_responsiveness,
            }
        
        # Add approvals data
        if project.approvals:
            response['approvals'] = {
                'environmental': project.approvals.environmental_approval_status,
                'administrative': project.approvals.administrative_approval_status,
                'financial': project.approvals.financial_approval_status,
                'other': project.approvals.other_approval_status,
                'pending_approvals': project.approvals.pending_approvals,
                'average_approval_delay_days': project.approvals.average_approval_delay_days,
            }
        
        # Add risk data
        if project.predictions:
            prediction = project.predictions[0]  # Latest prediction
            response['risk'] = {
                'delay_probability': float(prediction.delay_probability) if prediction.delay_probability is not None else None,
                'risk_level': prediction.risk_level,
                'risk_color': prediction.risk_color,
                'prediction_confidence': float(prediction.prediction_confidence) if prediction.prediction_confidence else None,
                'model_version': prediction.model_version,
                'prediction_date': prediction.prediction_date.isoformat() if prediction.prediction_date else None,
            }

            response['barriers'] = [barrier.to_dict() for barrier in project.barriers]
            if project.climate_observation:
                response['climate'] = project.climate_observation.to_dict()
        
        # Add recommendations
        response['recommendations'] = [
            {
                'factor': rec.factor,
                'priority': rec.priority,
                'recommendation': rec.recommendation_text,
            }
            for rec in project.recommendations
        ]
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e),
            'success': False
        }), 500


@bp.route('/<project_id>/evidence', methods=['GET'])
def get_project_evidence(project_id):
    """Return source-anchored evidence without replacing operational project fields."""
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found', 'project_id': project_id, 'success': False}), 404

    limit = min(max(int(request.args.get('limit', 100)), 1), 500)
    observations = EvidenceObservation.query.filter_by(project_id=project_id).order_by(
        EvidenceObservation.observation_date.desc(),
        EvidenceObservation.observation_id.desc(),
    ).limit(limit).all()
    return jsonify({
        'project_id': project_id,
        'summary': evidence_summary(project_id),
        'observations': [observation.to_dict() for observation in observations],
        'limit': limit,
        'success': True,
    }), 200


@bp.route('/<project_id>/risk', methods=['GET'])
def get_project_risk(project_id):
    """
    Get risk assessment for a project.
    
    Returns:
        {
            'project_id': 'DEMO_001',
            'project_name': 'Highway Project',
            'delay_probability': 0.82,
            'risk_level': 'HIGH',
            'risk_color': 'RED',
            'prediction_confidence': 0.88,
            'model_version': 'v1.0',
            'prediction_date': '2026-08-31T10:30:00',
            'contributing_factors': [
                'Compensation pending',
                'Legal dispute',
                'Approval delay'
            ]
        }
    """
    try:
        project = Project.query.get(project_id)
        
        if not project:
            return jsonify({
                'error': 'Project not found',
                'project_id': project_id,
                'success': False
            }), 404
        
        if not project.predictions:
            return jsonify({
                'error': 'No prediction available for this project',
                'project_id': project_id,
                'success': False
            }), 404
        
        prediction = project.predictions[0]  # Latest prediction
        
        # Build contributing factors from recommendations
        contributing_factors = [rec.factor for rec in project.recommendations]
        
        response = {
            'project_id': project.project_id,
            'project_name': project.project_name,
                'delay_probability': float(prediction.delay_probability) if prediction.delay_probability is not None else None,
            'risk_level': prediction.risk_level,
            'risk_color': prediction.risk_color,
            'prediction_confidence': float(prediction.prediction_confidence) if prediction.prediction_confidence else None,
            'model_version': prediction.model_version,
            'prediction_date': prediction.prediction_date.isoformat() if prediction.prediction_date else None,
            'contributing_factors': contributing_factors,
            'success': True
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e),
            'success': False
        }), 500


@bp.route('/<project_id>/recommendations', methods=['GET'])
def get_project_recommendations(project_id):
    """
    Get recommendations for a project.
    
    Returns:
        {
            'project_id': 'DEMO_001',
            'project_name': 'Highway Project',
            'recommendations': [
                {
                    'factor': 'Compensation delay',
                    'priority': 'HIGH',
                    'recommendation': 'Prioritize pending compensation verification...'
                }
            ]
        }
    """
    try:
        project = Project.query.get(project_id)
        
        if not project:
            return jsonify({
                'error': 'Project not found',
                'project_id': project_id,
                'success': False
            }), 404
        
        recommendations = [
            {
                'factor': rec.factor,
                'priority': rec.priority,
                'recommendation': rec.recommendation_text,
            }
            for rec in project.recommendations
        ]
        
        response = {
            'project_id': project.project_id,
            'project_name': project.project_name,
            'recommendations': recommendations,
            'count': len(recommendations),
            'success': True
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e),
            'success': False
        }), 500
