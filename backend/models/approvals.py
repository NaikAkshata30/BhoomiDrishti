from database import db
from datetime import datetime

class Approvals(db.Model):
    """
    Tracks various approvals required for the project.
    """
    __tablename__ = 'approvals'

    approval_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.String(50), db.ForeignKey('projects.project_id'), nullable=False, unique=True)
    
    # Approval status
    environmental_approval_status = db.Column(db.String(50), nullable=True)  # Pending, Approved, etc.
    administrative_approval_status = db.Column(db.String(50), nullable=True)
    financial_approval_status = db.Column(db.String(50), nullable=True)
    other_approval_status = db.Column(db.String(50), nullable=True)
    
    # Count and timing
    pending_approvals = db.Column(db.Integer, nullable=True)
    average_approval_delay_days = db.Column(db.Integer, nullable=True)
    
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Approvals {self.project_id}: {self.pending_approvals} pending>'
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'approval_id': self.approval_id,
            'project_id': self.project_id,
            'environmental_approval_status': self.environmental_approval_status,
            'administrative_approval_status': self.administrative_approval_status,
            'financial_approval_status': self.financial_approval_status,
            'other_approval_status': self.other_approval_status,
            'pending_approvals': self.pending_approvals,
            'average_approval_delay_days': self.average_approval_delay_days,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
        }
