from database import db
from datetime import datetime

class Compensation(db.Model):
    """
    Tracks compensation progress for affected families.
    """
    __tablename__ = 'compensation'

    compensation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.String(50), db.ForeignKey('projects.project_id'), nullable=False, unique=True)
    
    # Compensation amounts
    total_compensation_amount = db.Column(db.Float, nullable=True)  # Total amount to be disbursed
    amount_disbursed = db.Column(db.Float, nullable=True)  # Amount already paid
    compensation_percentage = db.Column(db.Float, nullable=True)  # % of total compensation
    
    # Family counts
    families_eligible = db.Column(db.Integer, nullable=True)
    families_paid = db.Column(db.Integer, nullable=True)
    
    # Pending cases
    pending_cases = db.Column(db.Integer, nullable=True)
    average_payment_delay_days = db.Column(db.Integer, nullable=True)
    
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Compensation {self.project_id}: {self.compensation_percentage}%>'
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'compensation_id': self.compensation_id,
            'project_id': self.project_id,
            'total_compensation_amount': self.total_compensation_amount,
            'amount_disbursed': self.amount_disbursed,
            'compensation_percentage': self.compensation_percentage,
            'families_eligible': self.families_eligible,
            'families_paid': self.families_paid,
            'pending_cases': self.pending_cases,
            'average_payment_delay_days': self.average_payment_delay_days,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
        }
