from datetime import datetime

from database import db


class ProjectBarrier(db.Model):
    """Project-specific condition that can obstruct acquisition or delivery."""

    __tablename__ = 'project_barriers'

    barrier_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.String(50), db.ForeignKey('projects.project_id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    severity = db.Column(db.String(20), nullable=False, default='MEDIUM')
    impact_score = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    mitigation = db.Column(db.Text, nullable=True)
    source_name = db.Column(db.String(255), nullable=True)
    source_url = db.Column(db.String(500), nullable=True)
    verification_status = db.Column(db.String(50), nullable=False, default='missing')
    observed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    project = db.relationship('Project', backref=db.backref('barriers', lazy=True, cascade='all, delete-orphan'))

    def to_dict(self):
        return {
            'barrier_id': self.barrier_id,
            'project_id': self.project_id,
            'category': self.category,
            'title': self.title,
            'severity': self.severity,
            'impact_score': self.impact_score,
            'status': self.status,
            'description': self.description,
            'mitigation': self.mitigation,
            'source_name': self.source_name,
            'source_url': self.source_url,
            'verification_status': self.verification_status,
            'observed_at': self.observed_at.isoformat() if self.observed_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }