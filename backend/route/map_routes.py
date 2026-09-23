"""
Map Routes

Endpoints for geospatial data:
- GET /api/map/geojson - GeoJSON FeatureCollection for all projects
"""

from flask import Blueprint, jsonify
from models import Project, ProjectLocation, Prediction
import json

bp = Blueprint('map', __name__, url_prefix='/api/map')


@bp.route('/geojson', methods=['GET'])
def get_geojson():
    """
    Get all projects as GeoJSON FeatureCollection for Leaflet map.
    
    Returns:
        {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'properties': {
                        'project_id': 'DEMO_001',
                        'project_name': 'Highway Project',
                        'state': 'Maharashtra',
                        'district': 'Nashik',
                        'delay_probability': 0.82,
                        'risk_level': 'HIGH',
                        'risk_color': 'RED',
                        'location_source': 'Government records',
                        'accuracy_level': 'project-level'
                    },
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [73.7898, 20.0054]  # [lon, lat]
                    }
                }
            ]
        }
    """
    try:
        projects = Project.query.all()
        features = []
        
        for project in projects:
            # Get location (first one, usually only one)
            location = project.locations[0] if project.locations else None
            
            if not location:
                # Skip projects without location data
                continue
            
            # Get prediction for risk data
            prediction = project.predictions[0] if project.predictions else None
            
            # Build properties
            properties = {
                'project_id': project.project_id,
                'project_name': project.project_name,
                'project_type': project.project_type,
                'state': project.state,
                'district': project.district,
                'village': project.village,
                'affected_families': project.affected_families,
                'land_required_ha': project.land_required_ha,
                'location_source': location.location_source,
                'accuracy_level': location.accuracy_level,
                'source_name': project.source_name,
                'source_url': project.source_url,
                'source_document_url': project.source_document_url,
                'data_status': project.data_status,
                'barriers': [barrier.to_dict() for barrier in project.barriers],
                'climate': project.climate_observation.to_dict() if project.climate_observation else None,
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
            
            # Try to use polygon geometry first
            if location.geometry:
                try:
                    geometry = json.loads(location.geometry)
                except:
                    geometry = None
            
            # Fall back to point if no polygon
            if not geometry and location.latitude and location.longitude:
                geometry = {
                    'type': 'Point',
                    'coordinates': [location.longitude, location.latitude]  # GeoJSON: [lon, lat]
                }
            
            if geometry:
                feature = {
                    'type': 'Feature',
                    'properties': properties,
                    'geometry': geometry
                }
                features.append(feature)
        
        response = {
            'type': 'FeatureCollection',
            'features': features,
            'total_features': len(features),
            'success': True
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e),
            'success': False
        }), 500
