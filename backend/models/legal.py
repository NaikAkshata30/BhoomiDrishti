from database import db
from datetime import datetime

class Legal(db.Model):
    """
    Tracks legal disputes and court cases affecting the project.
    """
    __tablename__ = 'legal'

    legal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.String(50), db.ForeignKey('projects.project_id'), nullable=False, unique=True)
    
    # Dispute tracking
    active_disputes = db.Column(db.Integer, default=0, nullable=True)
    dispute_count = db.Column(db.Integer, default=0, nullable=True)  # Total disputes (active + resolved)
    court_cases = db.Column(db.Integer, default=0, nullable=True)
    
    # Status and timeline
    legal_status = db.Column(db.String(100), nullable=True)  # e.g., "Pending", "In Court", "Resolved"
    average_case_age_days = db.Column(db.Integer, nullable=True)  # Average age of pending cases
    
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Legal {self.project_id}: {self.active_disputes} active disputes>'
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'legal_id': self.legal_id,
            'project_id': self.project_id,
            'active_disputes': self.active_disputes,
            'dispute_count': self.dispute_count,
            'court_cases': self.court_cases,
            'legal_status': self.legal_status,
            'average_case_age_days': self.average_case_age_days,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
        }
