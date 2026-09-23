"""Refresh project weather observations from a public coordinate-based API."""

from datetime import datetime

import requests

from database import db
from models import ClimateObservation, Project, ProjectBarrier


OPEN_METEO_URL = 'https://api.open-meteo.com/v1/forecast'
SOURCE_URL = 'https://open-meteo.com/'


def refresh_climate_observations():
    """Fetch current weather and update the climate context for each project."""
    refreshed = 0
    for project in Project.query.all():
        location = project.locations[0] if project.locations else None
        if not location or location.latitude is None or location.longitude is None:
            continue
        response = requests.get(
            OPEN_METEO_URL,
            params={
                'latitude': location.latitude,
                'longitude': location.longitude,
                'current': 'temperature_2m,precipitation,wind_speed_10m,weather_code',
                'timezone': 'UTC',
            },
            headers={'User-Agent': 'BhoomiDrishti/1.0'},
            timeout=20,
        )
        response.raise_for_status()
        current = response.json().get('current', {})
        observed_at = datetime.fromisoformat(str(current['time']).replace('Z', '+00:00')).replace(tzinfo=None)
        values = {
            'temperature_c': current.get('temperature_2m'),
            'precipitation_mm': current.get('precipitation'),
            'wind_speed_kmh': current.get('wind_speed_10m'),
            'weather_code': current.get('weather_code'),
        }
        observation = ClimateObservation.query.filter_by(project_id=project.project_id).first()
        if not observation:
            observation = ClimateObservation(project_id=project.project_id)
            db.session.add(observation)
        observation.source_name = 'Open-Meteo public weather API'
        observation.source_url = SOURCE_URL
        observation.observed_at = observed_at
        observation.warning_status = 'Monitor local official warning service'
        observation.verification_status = 'public_snapshot'
        for field, value in values.items():
            setattr(observation, field, value)

        barrier = next((item for item in project.barriers if item.category == 'climate'), None)
        if barrier:
            barrier.status = f"Observed {observed_at:%Y-%m-%d %H:%M} UTC"
            barrier.source_name = observation.source_name
            barrier.source_url = observation.source_url
            barrier.verification_status = observation.verification_status
            barrier.observed_at = observed_at
        refreshed += 1
    db.session.commit()
    return refreshed