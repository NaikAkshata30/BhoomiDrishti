"""
API DOCUMENTATION

Land Acquisition Predictive Analytics System - REST API

Base URL: http://localhost:5000

All responses use JSON format with a 'success' boolean field.
Error responses include an 'error' field and 'message' field.

===========================================================
PROJECT ENDPOINTS
===========================================================

1. LIST PROJECTS
   GET /api/projects
   
   Query Parameters (all optional):
     - state: Filter by state (e.g., "Maharashtra")
     - risk_level: Filter by risk level (HIGH, MEDIUM, LOW, NO_RISK)
     - limit: Max results (default: 100)
     - offset: Skip N results (default: 0)
   
   Response:
     {
       "projects": [
         {
           "project_id": "DEMO_HIGHRISE_001",
           "project_name": "Delhi-Mathura National Highway Expansion",
           "project_type": "Highway",
           "state": "Uttar Pradesh",
           "district": "Mathura",
           "village": "Bhuteshwar",
           "affected_families": 425,
           "land_required_ha": 250.5,
           "current_stage": "Award",
           "status": "Active",
           "delay_probability": 0.82,
           "risk_level": "HIGH",
           "risk_color": "RED"
         }
       ],
       "total": 6,
       "limit": 100,
       "offset": 0,
       "success": true
     }
   
   Status Codes:
     - 200: Success
     - 400: Invalid parameters
     - 500: Server error


2. GET PROJECT DETAILS
   GET /api/projects/<project_id>
   
   Example:
     GET /api/projects/DEMO_HIGHRISE_001
   
   Response:
     {
       "project": {
         "project_id": "DEMO_HIGHRISE_001",
         "project_name": "Delhi-Mathura National Highway Expansion",
         "project_type": "Highway",
         "agency": "MoRTH",
         "state": "Uttar Pradesh",
         "district": "Mathura",
         "village": "Bhuteshwar",
         "land_required_ha": 250.5,
         "affected_families": 425,
         "current_stage": "Award",
         "status": "Active",
         "created_at": "2026-08-31T10:30:00",
         "updated_at": "2026-08-31T10:30:00"
       },
       "location": {
         "latitude": 27.5089,
         "longitude": 77.6121,
         "location_source": "[SYNTHETIC/DEMO] Estimated coordinates",
         "accuracy_level": "village-level"
       },
       "progress": {
         "current_stage": "Award",
         "notification_status": "Completed",
         "survey_status": "Completed",
         "award_status": "Pending",
         "possession_status": "Pending",
         "overall_progress_percentage": 28.0,
         "possession_percentage": 15.0,
         "days_in_current_stage": 385
       },
       "compensation": {
         "total_amount": 75000000,
         "disbursed": 18750000,
         "percentage": 25.0,
         "families_eligible": 425,
         "families_paid": 95,
         "pending_cases": 45,
         "average_payment_delay_days": 120
       },
       "legal": {
         "active_disputes": 8,
         "dispute_count": 12,
         "court_cases": 3,
         "legal_status": "In Court",
         "average_case_age_days": 240
       },
       "social_impact": {
         "affected_families": 425,
         "rehabilitation_percentage": 30.0,
         "resettlement_percentage": 25.0,
         "relocation_completed_percentage": 12.0,
         "grievances_pending": 18,
         "stakeholder_responsiveness": 35.0
       },
       "approvals": {
         "environmental": "Approved",
         "administrative": "Pending",
         "financial": "Approved",
         "other": "Pending",
         "pending_approvals": 2,
         "average_approval_delay_days": 95
       },
       "risk": {
         "delay_probability": 0.82,
         "risk_level": "HIGH",
         "risk_color": "RED",
         "prediction_confidence": 0.88,
         "model_version": "v1.0",
         "prediction_date": "2026-08-31T10:30:00"
       },
       "recommendations": [
         {
           "factor": "Compensation delay",
           "priority": "HIGH",
           "recommendation": "Prioritize pending compensation verification and disbursement..."
         }
       ],
       "success": true
     }
   
   Status Codes:
     - 200: Success
     - 404: Project not found
     - 500: Server error


3. GET PROJECT RISK
   GET /api/projects/<project_id>/risk
   
   Example:
     GET /api/projects/DEMO_HIGHRISE_001/risk
   
   Response:
     {
       "project_id": "DEMO_HIGHRISE_001",
       "project_name": "Delhi-Mathura National Highway Expansion",
       "delay_probability": 0.82,
       "risk_level": "HIGH",
       "risk_color": "RED",
       "prediction_confidence": 0.88,
       "model_version": "v1.0",
       "prediction_date": "2026-08-31T10:30:00",
       "contributing_factors": [
         "Compensation delay",
         "Active legal disputes",
         "Approval delay",
         "Rehabilitation & Resettlement delay"
       ],
       "success": true
     }
   
   Status Codes:
     - 200: Success
     - 404: Project or prediction not found
     - 500: Server error


4. GET PROJECT RECOMMENDATIONS
   GET /api/projects/<project_id>/recommendations
   
   Example:
     GET /api/projects/DEMO_HIGHRISE_001/recommendations
   
   Response:
     {
       "project_id": "DEMO_HIGHRISE_001",
       "project_name": "Delhi-Mathura National Highway Expansion",
       "recommendations": [
         {
           "factor": "Compensation delay",
           "priority": "HIGH",
           "recommendation": "Prioritize pending compensation verification and disbursement..."
         },
         {
           "factor": "Active legal disputes",
           "priority": "HIGH",
           "recommendation": "Prioritize unresolved legal cases and initiate legal review..."
         }
       ],
       "count": 4,
       "success": true
     }
   
   Status Codes:
     - 200: Success
     - 404: Project not found
     - 500: Server error


===========================================================
MAP ENDPOINTS
===========================================================

5. GET GEOJSON (FOR LEAFLET MAP)
   GET /api/map/geojson
   
   Description:
     Returns all projects as a GeoJSON FeatureCollection.
     Designed for Leaflet map visualization.
     Uses Point geometry (fallback if polygon not available).
     Coordinate order: [longitude, latitude] (GeoJSON standard).
   
   Response:
     {
       "type": "FeatureCollection",
       "features": [
         {
           "type": "Feature",
           "properties": {
             "project_id": "DEMO_HIGHRISE_001",
             "project_name": "Delhi-Mathura National Highway Expansion",
             "project_type": "Highway",
             "state": "Uttar Pradesh",
             "district": "Mathura",
             "village": "Bhuteshwar",
             "affected_families": 425,
             "land_required_ha": 250.5,
             "location_source": "[SYNTHETIC/DEMO] Estimated coordinates",
             "accuracy_level": "village-level",
             "delay_probability": 0.82,
             "risk_level": "HIGH",
             "risk_color": "RED"
           },
           "geometry": {
             "type": "Point",
             "coordinates": [77.6121, 27.5089]
           }
         }
       ],
       "total_features": 6,
       "success": true
     }
   
   Status Codes:
     - 200: Success
     - 500: Server error
   
   Frontend Usage (Leaflet):
     fetch('/api/map/geojson')
       .then(res => res.json())
       .then(data => {
         L.geoJSON(data, {
           pointToLayer: (feature, latlng) => {
             return L.circleMarker(latlng, {
               color: feature.properties.risk_color
             });
           }
         }).addTo(map);
       });


===========================================================
DASHBOARD ENDPOINTS
===========================================================

6. GET DASHBOARD STATISTICS
   GET /api/dashboard
   
   Description:
     Returns overall dashboard statistics and summaries.
   
   Response:
     {
       "total_projects": 6,
       "risk_distribution": {
         "high": 2,
         "medium": 2,
         "low": 1,
         "no_risk": 1
       },
       "total_affected_families": 1264,
       "total_land_ha": 714.3,
       "average_delay_probability": 0.52,
       "state_distribution": {
         "Uttar Pradesh": 1,
         "Maharashtra": 1,
         "Kerala": 1,
         "Tamil Nadu": 1,
         "Rajasthan": 1,
         "Andhra Pradesh": 1
       },
       "project_stage_distribution": {
         "Survey": 1,
         "Award": 2,
         "Possession": 3
       },
       "average_compensation_percentage": 46.3,
       "average_possession_percentage": 48.1,
       "total_legal_disputes": 25,
       "total_pending_grievances": 85,
       "success": true
     }
   
   Status Codes:
     - 200: Success
     - 404: No projects in database
     - 500: Server error


===========================================================
PREDICTION ENDPOINTS
===========================================================

7. POST PREDICTION (PREDICT RISK)
   POST /api/predict
   
   Description:
     Generate a risk prediction for project data.
     Project does NOT need to exist in database.
     Uses heuristic rules (placeholder for ML model in Phase 5).
   
   Request Body:
     {
       "project_type": "Highway",
       "land_required_ha": 120,
       "affected_families": 340,
       "compensation_percentage": 62,
       "legal_disputes": 1,
       "approval_delay_days": 45,
       "rr_progress_percentage": 40,
       "possession_percentage": 30,
       "days_in_stage": 120
     }
   
   Response:
     {
       "delay_probability": 0.65,
       "risk_level": "MEDIUM",
       "risk_color": "ORANGE",
       "prediction_confidence": 0.75,
       "model_version": "v1.0",
       "contributing_factors": [
         "Low compensation progress",
         "Rehabilitation delay"
       ],
       "recommendations": [
         {
           "factor": "Compensation delay",
           "priority": "MEDIUM",
           "recommendation": "Accelerate compensation processing. Current progress: 62%"
         }
       ],
       "success": true
     }
   
   Status Codes:
     - 200: Success
     - 400: No JSON data provided
     - 500: Server error


===========================================================
HEALTH CHECK
===========================================================

8. HEALTH CHECK
   GET /api/health
   
   Response:
     {
       "status": "ok",
       "message": "Server is running"
     }
   
   Status: 200 (always, if server is running)


===========================================================
ERROR RESPONSES
===========================================================

All error responses follow this format:

  {
    "error": "Error type",
    "message": "Detailed error message",
    "success": false
  }

Common Error Codes:
  - 400: Bad Request (invalid parameters)
  - 404: Not Found (project/resource not found)
  - 500: Internal Server Error


===========================================================
FRONTEND INTEGRATION EXAMPLE
===========================================================

1. Load project list on dashboard:
   GET /api/projects
   
2. Display map with project locations:
   GET /api/map/geojson → Feed to Leaflet
   
3. On map click, show project details:
   GET /api/projects/{project_id}
   
4. Display risk summary:
   GET /api/projects/{project_id}/risk
   
5. Show recommendations:
   GET /api/projects/{project_id}/recommendations
   
6. Dashboard statistics:
   GET /api/dashboard
   
7. Test new project prediction:
   POST /api/predict with project features


===========================================================
NOTES FOR FRONTEND DEVELOPER
===========================================================

1. CORS is enabled - you can call from any frontend origin.

2. Coordinate System:
   - Database stores: latitude, longitude
   - GeoJSON returns: [longitude, latitude]
   - Leaflet expects: [latitude, longitude]
   
   Example for Leaflet:
     const feature = geoJsonData.features[0];
     const [lon, lat] = feature.geometry.coordinates;
     L.marker([lat, lon]).addTo(map);  // Note: reverse order!

3. Risk Colors:
   - RED: HIGH risk (0.70-1.0 probability)
   - ORANGE: MEDIUM risk (0.40-0.70 probability)
   - YELLOW: LOW risk (0.15-0.40 probability)
   - GREEN: NO_RISK (0.0-0.15 probability)

4. All projects are currently SYNTHETIC/DEMO data.
   Mark them clearly in the UI for user awareness.

5. The ML model will be integrated in Phase 5.
   Currently, predictions use heuristic rules.

6. Location accuracy_level explains precision:
   - "parcel-level": Exact parcel boundaries (GeoJSON polygon)
   - "project-level": Project coordinates (good accuracy)
   - "village-level": Village center (approximate)
   - "approximate": Best guess (low accuracy)
"""

if __name__ == '__main__':
    print(__doc__)
