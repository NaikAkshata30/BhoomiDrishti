"""
COMPLETE STARTUP GUIDE - Phase 1-4

This guide walks you through setting up the entire backend system.

Total time: ~15-20 minutes
"""

# ===========================================================
# STEP 1: PREREQUISITES
# ===========================================================

# Required:
# - Python 3.8+
# - MySQL Server (running locally)
# - Git (optional, for version control)

# Check Python version:
python --version  # Should be 3.8 or higher

# Check MySQL is installed and running:
# - Windows: MySQL Server should be in Services
# - macOS: brew services list | grep mysql
# - Linux: sudo systemctl status mysql


# ===========================================================
# STEP 2: PROJECT SETUP (5 minutes)
# ===========================================================

# Navigate to backend directory:
cd c:\Users\admin\Desktop\SIH_Land-Acquisition\backend

# Create virtual environment:
python -m venv venv

# Activate virtual environment:
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

# Install dependencies:
pip install -r requirements.txt

# Should see: Successfully installed Flask, SQLAlchemy, etc.


# ===========================================================
# STEP 3: DATABASE SETUP (5 minutes)
# ===========================================================

# Create MySQL database:
mysql -u root -p

# When prompted for password, enter your MySQL password (or leave blank if no password)

# Inside MySQL shell, run:
CREATE DATABASE land_acquisition_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# Verify database created:
mysql -u root -p land_acquisition_db -e "SHOW TABLES;"
# Should show empty database (no tables yet - they'll be created by Flask)


# ===========================================================
# STEP 4: CONFIGURE ENVIRONMENT (2 minutes)
# ===========================================================

# Edit .env file:
# 1. Open backend\.env.example
# 2. Edit database credentials:
#    DB_USER=root
#    DB_PASSWORD=your_mysql_password
#    DB_HOST=localhost
#    DB_PORT=3306
#    DB_NAME=land_acquisition_db
# 3. Save as .env (copy .env.example if needed)

# Verify .env is in .gitignore (don't commit passwords!):
# - Check: .gitignore should include ".env"


# ===========================================================
# STEP 5: LOAD SYNTHETIC DATA (3 minutes)
# ===========================================================

# This creates all database tables and loads 6 sample projects:
python load_data.py

# Expected output:
# ✓ Database initialized successfully
# ✓ Tables created: projects, project_locations, ...
# ✓ Loaded 6 projects into database
# 🔴 HIGH RISK: 2 projects
# 🟠 MEDIUM RISK: 2 projects
# 🟡 LOW RISK: 1 projects
# 🟢 NO RISK: 1 projects

# Verify data loaded:
python test_database.py
# Should show all tables created and test data visible


# ===========================================================
# STEP 6: START FLASK SERVER (ongoing)
# ===========================================================

# Start the server:
python app.py

# Expected output:
# ✓ Database initialized successfully
# ✓ ML model loaded from ml/models/best_model.pkl
# WARNING: This is a development server. Do not use it in production.
# Running on http://127.0.0.1:5000

# Server is now running!
# Keep this terminal open while developing


# ===========================================================
# STEP 7: TEST THE API (5 minutes in another terminal)
# ===========================================================

# Open a NEW terminal/PowerShell window (keep server running in original)

# Test 1: Health check
curl http://localhost:5000/api/health
# Should return: {"status": "ok", "message": "Server is running"}

# Test 2: List projects
curl http://localhost:5000/api/projects
# Should return list of 6 projects

# Test 3: Get specific project
curl http://localhost:5000/api/projects/DEMO_HIGHRISE_001
# Should return full project details with risk info

# Test 4: Get GeoJSON (for map)
curl http://localhost:5000/api/map/geojson
# Should return GeoJSON FeatureCollection with all projects

# Test 5: Dashboard stats
curl http://localhost:5000/api/dashboard
# Should return statistics: total_projects, risk_distribution, etc.

# More examples in: API_TESTING.md


# ===========================================================
# STEP 8: INTEGRATION WITH FRONTEND (Next)
# ===========================================================

# Once frontend is ready:

# 1. Update frontend API base URL to:
#    http://localhost:5000 (development)
#    or https://your-server.com (production)

# 2. Frontend calls:
#    GET /api/projects              → Project list
#    GET /api/map/geojson            → Leaflet map data
#    GET /api/projects/<id>          → Project details
#    GET /api/projects/<id>/risk     → Risk info
#    GET /api/dashboard              → Dashboard stats

# 3. For interactive map:
#    - User clicks marker on map
#    - Frontend gets project_id from feature properties
#    - Frontend calls GET /api/projects/<project_id>
#    - Display project details page


# ===========================================================
# STEP 9: PRODUCTION DEPLOYMENT (Future)
# ===========================================================

# When ready for production:

# 1. Use production config:
#    export FLASK_ENV=production  (Linux/Mac)
#    set FLASK_ENV=production      (Windows)

# 2. Use production database server
#    Update .env with production credentials

# 3. Use production WSGI server (not Flask dev server):
#    pip install gunicorn
#    gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 4. Set up reverse proxy (nginx/Apache)

# 5. Enable HTTPS/SSL

# 6. Set up monitoring and logging


# ===========================================================
# FILE STRUCTURE RECAP
# ===========================================================

"""
backend/
├── app.py                      # Flask application
├── config.py                   # Configuration
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (GITIGNORE!)
├── .gitignore                  # Git ignore rules
│
├── database/
│   ├── __init__.py
│   └── db.py                   # SQLAlchemy setup
│
├── models/                     # 9 SQLAlchemy ORM models
│   ├── project.py
│   ├── project_location.py
│   ├── acquisition_progress.py
│   ├── compensation.py
│   ├── legal.py
│   ├── social_impact.py
│   ├── approvals.py
│   ├── prediction.py
│   └── recommendation.py
│
├── route/                      # API blueprints
│   ├── project_routes.py       # GET /api/projects/*
│   ├── map_routes.py           # GET /api/map/geojson
│   ├── dashboard_routes.py     # GET /api/dashboard
│   └── prediction_routes.py    # POST /api/predict
│
├── services/                   # Business logic
│   ├── risk_service.py         # Risk classification
│   ├── recommendation_service.py  # Recommendations
│   └── prediction_service.py   # ML predictions
│
├── synthetic_data.py           # Test data generator
├── load_data.py                # Data loader script
├── test_database.py            # Database tests
│
├── README.md                   # Backend documentation
├── QUICKSTART.md               # Quick setup guide
├── API_DOCUMENTATION.md        # API reference (detailed)
├── API_TESTING.md              # Testing commands
├── SYNTHETIC_DATA_INFO.md      # Data overview
└── COMPLETE_STARTUP.md         # This file
"""


# ===========================================================
# QUICK REFERENCE - MAIN ENDPOINTS
# ===========================================================

"""
All endpoints return JSON with "success": true/false

PROJECTS:
  GET /api/projects                           → List all
  GET /api/projects/<id>                      → Single project details
  GET /api/projects/<id>/risk                 → Risk assessment
  GET /api/projects/<id>/recommendations      → Recommendations

MAP:
  GET /api/map/geojson                        → GeoJSON for Leaflet

DASHBOARD:
  GET /api/dashboard                          → Statistics

PREDICT:
  POST /api/predict                           → New prediction

HEALTH:
  GET /api/health                             → Server status
"""


# ===========================================================
# COMMON COMMANDS
# ===========================================================

# Start server (in project directory):
python app.py

# Load/reload data:
python load_data.py

# Test database:
python test_database.py

# List all projects:
curl http://localhost:5000/api/projects

# Get specific project:
curl http://localhost:5000/api/projects/DEMO_HIGHRISE_001

# Get map data:
curl http://localhost:5000/api/map/geojson

# Get dashboard:
curl http://localhost:5000/api/dashboard


# ===========================================================
# TROUBLESHOOTING
# ===========================================================

# "Database connection failed"
# → Check MySQL is running
# → Verify credentials in .env
# → Verify database exists

# "ModuleNotFoundError: No module named 'flask'"
# → Activate virtual environment: venv\Scripts\activate
# → Install dependencies: pip install -r requirements.txt

# "Port 5000 already in use"
# → Kill existing Flask process
# → Or change port in app.py: app.run(port=5001)

# "404 Project not found"
# → Run: python load_data.py
# → Verify project_id is correct (case-sensitive)

# "Empty response from API"
# → Check database has data: python test_database.py
# → Check MySQL connection works

# See README.md for more troubleshooting


# ===========================================================
# NEXT STEPS
# ===========================================================

# Phase 4: ✓ COMPLETE - API endpoints built
# 
# Phase 5 (Optional - ML Training):
#   - Build ML training pipeline
#   - Train models with real data
#   - Replace placeholder predictions with real ML
#
# Phase 6+ (Integration):
#   - Connect frontend to API
#   - User authentication
#   - Advanced analytics
#   - More data sources


# ===========================================================
# CONTACT & SUPPORT
# ===========================================================

"""
Backend API is ready!

If you have questions:
1. Check API_DOCUMENTATION.md for detailed endpoint specs
2. Check API_TESTING.md for example calls
3. Check README.md for architecture overview

Frontend developer should integrate with:
- Base URL: http://localhost:5000
- All endpoints at /api/*
- CORS enabled for all origins
- GeoJSON data for Leaflet map

Good luck! 🚀
"""
