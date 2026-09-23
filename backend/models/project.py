from database import db
from datetime import datetime

class Project(db.Model):
    """
    Core project information table.
    Central entity for all project-related data.
    """
    __tablename__ = 'projects'

    project_id = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    project_name = db.Column(db.String(255), nullable=False)
    project_type = db.Column(db.String(100), nullable=True)  # e.g., Highway, Railway, Dam
    agency = db.Column(db.String(255), nullable=True)  # Government agency
    state = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    village = db.Column(db.String(255), nullable=True)
    
    land_required_ha = db.Column(db.Float, nullable=True)  # Land area in hectares
    affected_families = db.Column(db.Integer, nullable=True)
    current_stage = db.Column(db.String(100), nullable=True)  # e.g., Notification, Survey, Award, etc.
    status = db.Column(db.String(50), nullable=True, default='Active')  # Active, Completed, etc.
    source_name = db.Column(db.String(255), nullable=True)
    source_url = db.Column(db.String(500), nullable=True)
    source_document_url = db.Column(db.String(500), nullable=True)
    data_status = db.Column(db.String(255), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    locations = db.relationship('ProjectLocation', backref='project', lazy=True, cascade='all, delete-orphan')
    acquisition = db.relationship('AcquisitionProgress', backref='project', uselist=False, cascade='all, delete-orphan')
    compensation = db.relationship('Compensation', backref='project', uselist=False, cascade='all, delete-orphan')
    legal = db.relationship('Legal', backref='project', uselist=False, cascade='all, delete-orphan')
    social_impact = db.relationship('SocialImpact', backref='project', uselist=False, cascade='all, delete-orphan')
    approvals = db.relationship('Approvals', backref='project', uselist=False, cascade='all, delete-orphan')
    predictions = db.relationship('Prediction', backref='project', lazy=True, cascade='all, delete-orphan')
    recommendations = db.relationship('Recommendation', backref='project', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Project {self.project_id}: {self.project_name}>'
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'project_id': self.project_id,
            'project_name': self.project_name,
            'project_type': self.project_type,
            'agency': self.agency,
            'state': self.state,
            'district': self.district,
            'village': self.village,
            'land_required_ha': self.land_required_ha,
            'affected_families': self.affected_families,
            'current_stage': self.current_stage,
            'status': self.status,
            'source_name': self.source_name,
            'source_url': self.source_url,
            'source_document_url': self.source_document_url,
            'data_status': self.data_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
