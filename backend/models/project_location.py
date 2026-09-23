from database import db
from datetime import datetime

class ProjectLocation(db.Model):
    """
    Geographic location data for projects.
    Supports both point (latitude/longitude) and polygon (GeoJSON) representations.
    Tracks location source and accuracy level.
    """
    __tablename__ = 'project_locations'

    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.String(50), db.ForeignKey('projects.project_id'), nullable=False)
    
    # Point location
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    # Polygon/geometry (stored as GeoJSON string)
    # For use with actual geometry, can be extended to PostGIS or similar
    geometry = db.Column(db.Text, nullable=True)  # JSON string of GeoJSON geometry
    
    # Metadata
    location_source = db.Column(db.String(255), nullable=True)  # e.g., "MoRTH project document", "BhoomiRashi"
    accuracy_level = db.Column(db.String(50), nullable=True)  # parcel-level, project-level, village-level, approximate
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<ProjectLocation {self.location_id} for {self.project_id}>'
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'location_id': self.location_id,
            'project_id': self.project_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'geometry': self.geometry,
            'location_source': self.location_source,
            'accuracy_level': self.accuracy_level,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def to_geojson_feature(self):
        """
        Convert to GeoJSON Feature for Leaflet map.
        Preference: polygon > point
        """
        import json
        
        # Start with project data
        project = self.project
        prediction = project.predictions[0] if project.predictions else None
        
        properties = {
            'project_id': self.project_id,
            'project_name': project.project_name,
            'location_source': self.location_source,
            'accuracy_level': self.accuracy_level,
        }
        
        # Add risk data if available
        if prediction:
            properties.update({
                'delay_probability': float(prediction.delay_probability) if prediction.delay_probability is not None else None,
                'risk_level': prediction.risk_level,
                'risk_color': prediction.risk_color,
            })
        
        # Determine geometry type
        geometry = None
        if self.geometry:
            # Try to use polygon geometry if available
            try:
                geometry = json.loads(self.geometry)
            except:
                geometry = None
        
        if not geometry and self.latitude and self.longitude:
            # Fall back to point
            geometry = {
                'type': 'Point',
                'coordinates': [self.longitude, self.latitude]  # GeoJSON: [lon, lat]
            }
        
        return {
            'type': 'Feature',
            'properties': properties,
            'geometry': geometry
        }
