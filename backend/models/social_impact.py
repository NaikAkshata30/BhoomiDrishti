from database import db
from datetime import datetime

class SocialImpact(db.Model):
    """
    Tracks rehabilitation and resettlement (R&R) progress and social impact metrics.
    """
    __tablename__ = 'social_impact'

    social_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.String(50), db.ForeignKey('projects.project_id'), nullable=False, unique=True)
    
    # Affected families
    affected_families = db.Column(db.Integer, nullable=True)
    
    # Progress metrics
    rehabilitation_progress_percentage = db.Column(db.Float, nullable=True)
    resettlement_progress_percentage = db.Column(db.Float, nullable=True)
    relocation_completed_percentage = db.Column(db.Float, nullable=True)
    
    # Grievances and responsiveness
    grievances_pending = db.Column(db.Integer, nullable=True)
    stakeholder_responsiveness = db.Column(db.Float, nullable=True)  # 0-100 scale or 0-1
    
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<SocialImpact {self.project_id}: RR {self.rehabilitation_progress_percentage}%>'
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'social_id': self.social_id,
            'project_id': self.project_id,
            'affected_families': self.affected_families,
            'rehabilitation_progress_percentage': self.rehabilitation_progress_percentage,
            'resettlement_progress_percentage': self.resettlement_progress_percentage,
            'relocation_completed_percentage': self.relocation_completed_percentage,
            'grievances_pending': self.grievances_pending,
            'stakeholder_responsiveness': self.stakeholder_responsiveness,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
        }
