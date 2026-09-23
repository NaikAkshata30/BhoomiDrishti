# Backend - Land Acquisition Predictive Analytics System

## Overview
This is the Flask backend for the SIH 2026 Land Acquisition project. It handles:
- Database management (MySQL)
- ML model loading and predictions
- Risk classification and recommendations
- RESTful APIs for frontend consumption
- GeoJSON data generation for mapping

## Project Structure

```
backend/
├── app.py                    # Flask application factory
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
│
├── database/              # Database initialization
│   ├── __init__.py
│   └── db.py             # SQLAlchemy setup
│
├── models/               # SQLAlchemy ORM models
│   ├── __init__.py
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
├── routes/              # API endpoints
│   ├── __init__.py
│   ├── project_routes.py
│   ├── map_routes.py
│   ├── dashboard_routes.py
│   └── prediction_routes.py
│
├── services/           # Business logic
│   ├── __init__.py
│   ├── prediction_service.py
│   ├── risk_service.py
│   └── recommendation_service.py
│
└── ml/                # ML models (loaded at runtime)
    └── models/
        └── best_model.pkl
```

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- MySQL Server running
- pip or conda

### 2. Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy `.env.example` to `.env` and update with your database credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=land_acquisition_db
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
```

### 5. Create Database

```bash
# The database tables will be created automatically when you first run the app
python app.py
```

Or use the Flask CLI:

```bash
# Set up Flask environment
set FLASK_APP=app.py  # On Windows
export FLASK_APP=app.py  # On Linux/Mac

# Initialize database
flask shell
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
```

## Running the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

Health check: `GET http://localhost:5000/api/health`

## Development Phases

**Phase 1: ✓ Backend Foundation** (COMPLETE)
- Flask setup
- Configuration management
- Database connection

**Phase 2: Database Schema** (IN PROGRESS)
- Create SQLAlchemy models
- Define all tables (projects, locations, progress, etc.)

**Phase 3: Synthetic Test Data**
- Create sample projects
- Load test data for development

**Phase 4: ML Pipeline**
- EDA and data cleaning
- Feature engineering
- Model training
- Model evaluation

**Phase 5-7: APIs & Integration**
- Project, map, dashboard, and prediction routes
- Frontend integration

## API Endpoints (To be implemented)

- `GET /api/projects` - List all projects
- `GET /api/projects/<project_id>` - Project details
- `GET /api/projects/<project_id>/risk` - Risk assessment
- `GET /api/projects/<project_id>/recommendations` - Recommendations
- `GET /api/dashboard` - Dashboard statistics
- `GET /api/map/geojson` - GeoJSON for map
- `POST /api/predict` - Predict risk for new project

## Notes

- Never commit `.env` file to version control
- Database credentials should be in environment variables
- The ML model is loaded once at startup for performance
- All risk calculations are done by the backend, not the frontend
