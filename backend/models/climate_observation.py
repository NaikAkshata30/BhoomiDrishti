from datetime import datetime

from database import db


class ClimateObservation(db.Model):
    """Latest weather observation associated with a project coordinate."""

    __tablename__ = 'climate_observations'

    observation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.String(50), db.ForeignKey('projects.project_id'), nullable=False, unique=True)
    source_name = db.Column(db.String(255), nullable=False)
    source_url = db.Column(db.String(500), nullable=False)
    observed_at = db.Column(db.DateTime, nullable=False)
    temperature_c = db.Column(db.Float, nullable=True)
    precipitation_mm = db.Column(db.Float, nullable=True)
    wind_speed_kmh = db.Column(db.Float, nullable=True)
    weather_code = db.Column(db.Integer, nullable=True)
    warning_status = db.Column(db.String(50), nullable=True)
    verification_status = db.Column(db.String(50), nullable=False, default='public_snapshot')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    project = db.relationship('Project', backref=db.backref('climate_observation', uselist=False))

    def to_dict(self):
        return {
            'observation_id': self.observation_id,
            'project_id': self.project_id,
            'source_name': self.source_name,
            'source_url': self.source_url,
            'observed_at': self.observed_at.isoformat() if self.observed_at else None,
            'temperature_c': self.temperature_c,
            'precipitation_mm': self.precipitation_mm,
            'wind_speed_kmh': self.wind_speed_kmh,
            'weather_code': self.weather_code,
            'warning_status': self.warning_status,
            'verification_status': self.verification_status,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }