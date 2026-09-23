from database import db
from datetime import datetime

class AcquisitionProgress(db.Model):
    """
    Tracks progress of land acquisition through various stages.
    """
    __tablename__ = 'acquisition_progress'

    progress_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.String(50), db.ForeignKey('projects.project_id'), nullable=False, unique=True)
    
    # Stage tracking
    current_stage = db.Column(db.String(100), nullable=True)  # Notification, Survey, Award, Possession, etc.
    notification_status = db.Column(db.String(50), nullable=True)  # Pending, Completed, etc.
    survey_status = db.Column(db.String(50), nullable=True)
    award_status = db.Column(db.String(50), nullable=True)
    possession_status = db.Column(db.String(50), nullable=True)
    
    # Progress percentage
    overall_progress_percentage = db.Column(db.Float, nullable=True)  # 0-100%
    possession_percentage = db.Column(db.Float, nullable=True)  # % of land possessed
    
    # Timeline
    days_in_current_stage = db.Column(db.Integer, nullable=True)  # Days spent in current stage
    
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<AcquisitionProgress {self.project_id}: {self.overall_progress_percentage}%>'
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'progress_id': self.progress_id,
            'project_id': self.project_id,
            'current_stage': self.current_stage,
            'notification_status': self.notification_status,
            'survey_status': self.survey_status,
            'award_status': self.award_status,
            'possession_status': self.possession_status,
            'overall_progress_percentage': self.overall_progress_percentage,
            'possession_percentage': self.possession_percentage,
            'days_in_current_stage': self.days_in_current_stage,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
        }
