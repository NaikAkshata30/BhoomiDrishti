"""
Quick Start Guide - Phase 3

This guide helps you get started with the Land Acquisition Backend.

PREREQUISITES:
==============
- Python 3.8+
- MySQL Server running locally
- Virtual environment (optional but recommended)

SETUP STEPS:
============

1. CREATE VIRTUAL ENVIRONMENT (OPTIONAL)
   python -m venv venv
   
   On Windows:
   venv\Scripts\activate
   
   On Linux/Mac:
   source venv/bin/activate

2. INSTALL DEPENDENCIES
   pip install -r requirements.txt

3. CONFIGURE DATABASE
   Copy .env.example to .env:
   
   cp .env.example .env  (Linux/Mac)
   copy .env.example .env (Windows)
   
   Edit .env with your MySQL credentials:
   
   DB_USER=root
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=land_acquisition_db

4. CREATE DATABASE (in MySQL)
   
   Option A: Using MySQL command line
   mysql -u root -p
   > CREATE DATABASE land_acquisition_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   > EXIT;
   
   Option B: Using a tool like MySQL Workbench
   - Create new database named "land_acquisition_db"

5. LOAD SYNTHETIC DATA
   
   The synthetic data includes 6 projects with different risk profiles:
   
   python load_data.py
   
   This will:
   - Create all database tables
   - Load 6 sample projects (SYNTHETIC/DEMO DATA)
   - Display a summary
   
   Projects loaded:
   - DEMO_HIGHRISE_001: Delhi-Mathura Highway (HIGH RISK)
   - DEMO_MEDIUMRISK_001: Maharashtra Water Supply (MEDIUM RISK)
   - DEMO_LOWRISK_001: Kerala Coastal Road (LOW RISK)
   - DEMO_NORISK_001: Tamil Nadu Railway (NO RISK)
   - DEMO_HIGHRISE_002: Rajasthan Irrigation (HIGH RISK)
   - DEMO_MEDIUMRISK_002: Andhra Pradesh Metro (MEDIUM RISK)

6. START THE SERVER
   
   python app.py
   
   Server will start at: http://localhost:5000
   
   Health check endpoint:
   GET http://localhost:5000/api/health

VERIFICATION:
==============

Check database tables were created:
  python test_database.py

View all projects:
  In MySQL:
  USE land_acquisition_db;
  SELECT * FROM projects;

Next Phase:
===========
Once data is loaded, you can build Phase 4-5 APIs:
- GET /api/projects
- GET /api/projects/<project_id>
- GET /api/projects/<project_id>/risk
- GET /api/map/geojson
- POST /api/predict
- etc.

SYNTHETIC DATA DISCLAIMER:
==========================
The loaded projects are SYNTHETIC/DEMO data for development and testing.
They are NOT real government data.
Each project is clearly marked as SYNTHETIC/DEMO in its location source.
"""

if __name__ == '__main__':
    print(__doc__)
