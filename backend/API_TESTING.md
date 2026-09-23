"""
API TESTING GUIDE

Quick commands to test all endpoints using curl.
Copy and paste into PowerShell or terminal.

Prerequisites:
  1. Flask server running: python app.py
  2. Synthetic data loaded: python load_data.py
  3. curl available (Windows 10+ has it built-in)
"""

# ===================================================
# HEALTH CHECK
# ===================================================

# Test if server is running
curl http://localhost:5000/api/health


# ===================================================
# PROJECT ENDPOINTS
# ===================================================

# List all projects
curl http://localhost:5000/api/projects

# List projects with pagination
curl "http://localhost:5000/api/projects?limit=3&offset=0"

# Filter projects by state
curl "http://localhost:5000/api/projects?state=Maharashtra"

# Filter projects by risk level
curl "http://localhost:5000/api/projects?risk_level=HIGH"

# Get specific project details
curl http://localhost:5000/api/projects/DEMO_HIGHRISE_001

# Get project risk assessment
curl http://localhost:5000/api/projects/DEMO_HIGHRISE_001/risk

# Get project recommendations
curl http://localhost:5000/api/projects/DEMO_HIGHRISE_001/recommendations


# ===================================================
# MAP ENDPOINTS
# ===================================================

# Get GeoJSON for all projects (for Leaflet map)
curl http://localhost:5000/api/map/geojson


# ===================================================
# DASHBOARD ENDPOINTS
# ===================================================

# Get dashboard statistics
curl http://localhost:5000/api/dashboard


# ===================================================
# PREDICTION ENDPOINTS
# ===================================================

# Predict risk for new project (PowerShell format)
$body = @{
    project_type = "Highway"
    land_required_ha = 150
    affected_families = 300
    compensation_percentage = 45
    legal_disputes = 3
    approval_delay_days = 60
    rr_progress_percentage = 35
    possession_percentage = 25
    days_in_stage = 200
} | ConvertTo-Json

curl -X POST http://localhost:5000/api/predict `
  -Header "Content-Type: application/json" `
  -Body $body

# Alternative (bash/Linux format):
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "project_type": "Highway",
    "land_required_ha": 150,
    "affected_families": 300,
    "compensation_percentage": 45,
    "legal_disputes": 3,
    "approval_delay_days": 60,
    "rr_progress_percentage": 35,
    "possession_percentage": 25,
    "days_in_stage": 200
  }'


# ===================================================
# TESTING SCENARIOS
# ===================================================

# Scenario 1: Check HIGH RISK project
echo "=== HIGH RISK PROJECT ==="
curl http://localhost:5000/api/projects/DEMO_HIGHRISE_001/risk

# Scenario 2: Check LOW RISK project
echo "=== LOW RISK PROJECT ==="
curl http://localhost:5000/api/projects/DEMO_LOWRISK_001/risk

# Scenario 3: Get all projects by state
echo "=== MAHARASHTRA PROJECTS ==="
curl "http://localhost:5000/api/projects?state=Maharashtra"

# Scenario 4: Get map data
echo "=== MAP GEOJSON ==="
curl http://localhost:5000/api/map/geojson

# Scenario 5: Dashboard summary
echo "=== DASHBOARD STATS ==="
curl http://localhost:5000/api/dashboard


# ===================================================
# PYTHON TESTING (Alternative to curl)
# ===================================================

# Create test_api.py:

import requests
import json

BASE_URL = "http://localhost:5000"

def test_endpoints():
    # Health check
    print("Testing health check...")
    resp = requests.get(f"{BASE_URL}/api/health")
    print(f"Health: {resp.json()}\n")
    
    # List projects
    print("Testing project list...")
    resp = requests.get(f"{BASE_URL}/api/projects")
    data = resp.json()
    print(f"Total projects: {data['total']}\n")
    
    # Get specific project
    print("Testing project details...")
    resp = requests.get(f"{BASE_URL}/api/projects/DEMO_HIGHRISE_001")
    project = resp.json()
    print(f"Project: {project['project']['project_name']}")
    print(f"Risk: {project['risk']['risk_level']}\n")
    
    # Get risk
    print("Testing risk endpoint...")
    resp = requests.get(f"{BASE_URL}/api/projects/DEMO_HIGHRISE_001/risk")
    risk = resp.json()
    print(f"Delay probability: {risk['delay_probability']}\n")
    
    # Get recommendations
    print("Testing recommendations...")
    resp = requests.get(f"{BASE_URL}/api/projects/DEMO_HIGHRISE_001/recommendations")
    recs = resp.json()
    print(f"Recommendations: {recs['count']}\n")
    
    # Get GeoJSON
    print("Testing GeoJSON...")
    resp = requests.get(f"{BASE_URL}/api/map/geojson")
    geojson = resp.json()
    print(f"Features: {geojson['total_features']}\n")
    
    # Get dashboard
    print("Testing dashboard...")
    resp = requests.get(f"{BASE_URL}/api/dashboard")
    dashboard = resp.json()
    print(f"Total projects: {dashboard['total_projects']}")
    print(f"High risk: {dashboard['risk_distribution']['high']}\n")
    
    # Predict
    print("Testing prediction...")
    predict_data = {
        "project_type": "Highway",
        "land_required_ha": 120,
        "affected_families": 300,
        "compensation_percentage": 50,
        "legal_disputes": 2,
        "approval_delay_days": 45,
        "rr_progress_percentage": 45,
        "possession_percentage": 40,
        "days_in_stage": 150
    }
    resp = requests.post(f"{BASE_URL}/api/predict", json=predict_data)
    pred = resp.json()
    print(f"Predicted risk level: {pred['risk_level']}")
    print(f"Delay probability: {pred['delay_probability']}\n")
    
    print("✓ All tests completed!")

if __name__ == "__main__":
    test_endpoints()

# Run with: python test_api.py


# ===================================================
# POSTMAN/INSOMNIA IMPORT
# ===================================================

# Collection for Postman/Insomnia:

{
  "info": {
    "name": "Land Acquisition API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/api/health"
      }
    },
    {
      "name": "List Projects",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/api/projects"
      }
    },
    {
      "name": "Get Project Details",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/api/projects/DEMO_HIGHRISE_001"
      }
    },
    {
      "name": "Get Risk",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/api/projects/DEMO_HIGHRISE_001/risk"
      }
    },
    {
      "name": "Get Recommendations",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/api/projects/DEMO_HIGHRISE_001/recommendations"
      }
    },
    {
      "name": "Get GeoJSON",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/api/map/geojson"
      }
    },
    {
      "name": "Get Dashboard",
      "request": {
        "method": "GET",
        "url": "http://localhost:5000/api/dashboard"
      }
    },
    {
      "name": "Predict Risk",
      "request": {
        "method": "POST",
        "url": "http://localhost:5000/api/predict",
        "body": {
          "mode": "raw",
          "raw": "{\"project_type\":\"Highway\",\"land_required_ha\":120,\"affected_families\":300,\"compensation_percentage\":50,\"legal_disputes\":2,\"approval_delay_days\":45,\"rr_progress_percentage\":45,\"possession_percentage\":40,\"days_in_stage\":150}"
        }
      }
    }
  ]
}


# ===================================================
# EXPECTED RESPONSES
# ===================================================

# GET /api/projects
# Status: 200
# Response:
#   {
#     "projects": [...],
#     "total": 6,
#     "limit": 100,
#     "offset": 0,
#     "success": true
#   }

# GET /api/projects/DEMO_HIGHRISE_001
# Status: 200
# Response includes: project, location, progress, compensation, legal, social_impact, approvals, risk, recommendations

# GET /api/projects/DEMO_NONEXISTENT
# Status: 404
# Response:
#   {
#     "error": "Project not found",
#     "project_id": "DEMO_NONEXISTENT",
#     "success": false
#   }

# POST /api/predict
# Status: 200
# Response: delay_probability, risk_level, risk_color, recommendations, etc.


# ===================================================
# COMMON ISSUES & SOLUTIONS
# ===================================================

# Issue: curl: command not found
# Solution: 
#   - Windows 10+: Should be built-in. Try "wsl" for Linux subsystem.
#   - Otherwise: Install Git Bash or use Python requests instead.

# Issue: Connection refused
# Solution:
#   - Ensure Flask server is running: python app.py
#   - Check port 5000 is not blocked by firewall

# Issue: 404 Project not found
# Solution:
#   - Ensure synthetic data is loaded: python load_data.py
#   - Use correct project_id (case-sensitive)
#   - List projects first: curl http://localhost:5000/api/projects

# Issue: Empty data
# Solution:
#   - Check database connection in .env
#   - Verify synthetic data loaded successfully
#   - Check MySQL database has tables

# Issue: CORS errors in browser
# Solution:
#   - CORS is enabled on all routes
#   - Check browser console for specific error messages
#   - Verify frontend URL matches CORS settings
"""

if __name__ == '__main__':
    print(__doc__)
