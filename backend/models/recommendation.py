from database import db
from datetime import datetime

class Recommendation(db.Model):
    """
    Stores recommendations tied to detected risk factors.
    Generated based on the major contributing factors identified by the ML model.
    """
    __tablename__ = 'recommendations'

    recommendation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.String(50), db.ForeignKey('projects.project_id'), nullable=False)
    
    # Recommendation details
    factor = db.Column(db.String(255), nullable=False)  # e.g., "Compensation delay", "Legal dispute"
    priority = db.Column(db.String(50), nullable=False)  # HIGH, MEDIUM, LOW
    recommendation_text = db.Column(db.Text, nullable=False)  # Action to take
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Recommendation {self.project_id}: {self.factor} ({self.priority})>'
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'recommendation_id': self.recommendation_id,
            'project_id': self.project_id,
            'factor': self.factor,
            'priority': self.priority,
            'recommendation_text': self.recommendation_text,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
