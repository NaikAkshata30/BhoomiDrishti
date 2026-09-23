from datetime import datetime

from database import db


class EvidenceObservation(db.Model):
    """Append-only source observation imported from the ML evidence collection."""

    __tablename__ = 'evidence_observations'

    observation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.String(50), db.ForeignKey('projects.project_id'), nullable=False)
    entity_id = db.Column(db.String(255), nullable=True)
    field = db.Column(db.String(100), nullable=False)
    value_original = db.Column(db.Text, nullable=True)
    value_normalized = db.Column(db.Float, nullable=True)
    value_text = db.Column(db.Text, nullable=True)
    unit = db.Column(db.String(50), nullable=True)
    measurement_type = db.Column(db.String(100), nullable=True)
    observation_date = db.Column(db.DateTime, nullable=True)
    observation_period = db.Column(db.String(100), nullable=True)
    source_id = db.Column(db.String(50), nullable=False)
    source_sha256 = db.Column(db.String(64), nullable=True)
    source_url = db.Column(db.String(1000), nullable=True)
    source_reference = db.Column(db.String(1000), nullable=True)
    verification_status = db.Column(db.String(50), nullable=True)
    identity_status = db.Column(db.String(50), nullable=True)
    confidence = db.Column(db.Float, nullable=True)
    conflict_flag = db.Column(db.Boolean, nullable=False, default=False)
    ml_eligible = db.Column(db.Boolean, nullable=False, default=False)
    imported_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    project = db.relationship('Project', backref=db.backref('evidence_observations', lazy=True))

    def to_dict(self):
        return {
            'observation_id': self.observation_id,
            'project_id': self.project_id,
            'entity_id': self.entity_id,
            'field': self.field,
            'value_original': self.value_original,
            'value_normalized': self.value_normalized,
            'value_text': self.value_text,
            'unit': self.unit,
            'measurement_type': self.measurement_type,
            'observation_date': self.observation_date.isoformat() if self.observation_date else None,
            'observation_period': self.observation_period,
            'source_id': self.source_id,
            'source_sha256': self.source_sha256,
            'source_url': self.source_url,
            'source_reference': self.source_reference,
            'verification_status': self.verification_status,
            'identity_status': self.identity_status,
            'confidence': self.confidence,
            'conflict_flag': self.conflict_flag,
            'ml_eligible': self.ml_eligible,
            'imported_at': self.imported_at.isoformat() if self.imported_at else None,
        }