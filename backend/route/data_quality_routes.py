from datetime import datetime
from flask import Blueprint, jsonify
from models import EvidenceObservation, Project, SourceSnapshot

bp = Blueprint('data_quality', __name__, url_prefix='/api/data-quality')


@bp.route('', methods=['GET'])
def data_quality():
    projects = Project.query.all()
    total_fields = len(projects) * 7
    verified_fields = sum(
        sum(bool(value) for value in (
            project.project_name,
            project.agency,
            project.state,
            project.district,
            project.source_url,
            project.source_document_url,
            project.locations[0].latitude if project.locations else None,
        )) for project in projects
    )
    latest_snapshot = SourceSnapshot.query.order_by(SourceSnapshot.retrieved_at.desc()).first()
    age_hours = None
    if latest_snapshot:
        age_hours = round((datetime.utcnow() - latest_snapshot.retrieved_at).total_seconds() / 3600, 2)
    evidence_count = EvidenceObservation.query.count()
    current_evidence = EvidenceObservation.query.filter(
        EvidenceObservation.verification_status.in_(['official', 'verified_manual']),
        EvidenceObservation.ml_eligible.is_(False),
        EvidenceObservation.conflict_flag.is_(False),
    ).count()
    return jsonify({
        'success': True,
        'project_count': len(projects),
        'source_snapshot_count': SourceSnapshot.query.count(),
        'verified_identity_location_coverage_percent': round((verified_fields / total_fields) * 100, 2) if total_fields else 0,
        'latest_snapshot_retrieved_at': latest_snapshot.retrieved_at.isoformat() if latest_snapshot else None,
        'latest_snapshot_age_hours': age_hours,
        'evidence_observation_count': evidence_count,
        'evidence_project_count': EvidenceObservation.query.with_entities(EvidenceObservation.project_id).distinct().count(),
        'review_required_evidence_count': EvidenceObservation.query.filter(
            EvidenceObservation.verification_status == 'review_required'
        ).count(),
        'conflicting_evidence_count': EvidenceObservation.query.filter_by(conflict_flag=True).count(),
        'model_eligible_evidence_count': EvidenceObservation.query.filter_by(ml_eligible=True).count(),
        'source_backed_non_conflicting_evidence_count': current_evidence,
        'note': 'Coverage counts source-backed identity, agency, geography and provenance fields. Operational metrics are excluded until official records are ingested.',
    }), 200