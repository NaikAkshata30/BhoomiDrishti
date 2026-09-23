"""
Database Testing Script

Tests the database schema and models.
Verifies that all tables are created correctly.

Usage:
    python -m pytest tests/test_database.py
    
Or manually:
    python
    >>> from app import create_app
    >>> app = create_app()
    >>> # Tables should be created automatically
"""

from app import create_app
from database import db, reset_db
from models import (
    Project, ProjectLocation, AcquisitionProgress, Compensation,
    Legal, SocialImpact, Approvals, Prediction, Recommendation
)
from datetime import datetime


def test_database_connection():
    """Test that database connection works"""
    app = create_app()
    with app.app_context():
        try:
            result = db.session.execute('SELECT 1')
            print("✓ Database connection successful")
            return True
        except Exception as e:
            print(f"✗ Database connection failed: {e}")
            return False


def test_model_creation():
    """Test creating and querying models"""
    app = create_app()
    
    with app.app_context():
        # Create a test project
        project = Project(
            project_id='TEST_001',
            project_name='Test Highway Project',
            project_type='Highway',
            agency='MoRTH',
            state='Maharashtra',
            district='Nashik',
            village='Test Village',
            land_required_ha=125.5,
            affected_families=250,
            current_stage='Notification',
            status='Active'
        )
        
        db.session.add(project)
        db.session.commit()
        
        # Create location for project
        location = ProjectLocation(
            project_id='TEST_001',
            latitude=20.0054,
            longitude=73.7898,
            location_source='Test Source',
            accuracy_level='project-level'
        )
        
        db.session.add(location)
        db.session.commit()
        
        # Create acquisition progress
        progress = AcquisitionProgress(
            project_id='TEST_001',
            current_stage='Survey',
            overall_progress_percentage=25.0,
            possession_percentage=10.0,
            days_in_current_stage=60
        )
        
        db.session.add(progress)
        db.session.commit()
        
        # Create compensation record
        comp = Compensation(
            project_id='TEST_001',
            total_compensation_amount=5000000,
            amount_disbursed=2700000,
            compensation_percentage=54.0,
            families_eligible=250,
            families_paid=135,
            pending_cases=10,
            average_payment_delay_days=15
        )
        
        db.session.add(comp)
        db.session.commit()
        
        # Create legal record
        legal = Legal(
            project_id='TEST_001',
            active_disputes=2,
            dispute_count=5,
            court_cases=1,
            legal_status='Pending',
            average_case_age_days=180
        )
        
        db.session.add(legal)
        db.session.commit()
        
        # Create social impact record
        social = SocialImpact(
            project_id='TEST_001',
            affected_families=250,
            rehabilitation_progress_percentage=40.0,
            resettlement_progress_percentage=35.0,
            relocation_completed_percentage=20.0,
            grievances_pending=8,
            stakeholder_responsiveness=65.0
        )
        
        db.session.add(social)
        db.session.commit()
        
        # Create approvals record
        approvals = Approvals(
            project_id='TEST_001',
            environmental_approval_status='Approved',
            administrative_approval_status='Pending',
            financial_approval_status='Approved',
            pending_approvals=1,
            average_approval_delay_days=45
        )
        
        db.session.add(approvals)
        db.session.commit()
        
        # Create prediction
        prediction = Prediction(
            project_id='TEST_001',
            delay_probability=0.82,
            prediction_confidence=0.88,
            risk_level='HIGH',
            risk_color='RED',
            model_version='v1.0'
        )
        
        db.session.add(prediction)
        db.session.commit()
        
        # Create recommendations
        rec1 = Recommendation(
            project_id='TEST_001',
            factor='Compensation delay',
            priority='HIGH',
            recommendation_text='Prioritize pending compensation verification and disbursement.'
        )
        
        rec2 = Recommendation(
            project_id='TEST_001',
            factor='Active legal disputes',
            priority='HIGH',
            recommendation_text='Prioritize unresolved legal cases and initiate legal review.'
        )
        
        db.session.add(rec1)
        db.session.add(rec2)
        db.session.commit()
        
        print("✓ Test data created successfully")
        
        # Query back
        proj = Project.query.get('TEST_001')
        if proj:
            print(f"✓ Project retrieved: {proj.project_name}")
            print(f"  - Locations: {len(proj.locations)}")
            print(f"  - Acquisition progress: {proj.acquisition}")
            print(f"  - Compensation: {proj.compensation.compensation_percentage}%")
            print(f"  - Predictions: {len(proj.predictions)}")
            print(f"  - Recommendations: {len(proj.recommendations)}")
            return True
        else:
            print("✗ Could not retrieve test project")
            return False


def print_schema_info():
    """Print database schema information"""
    app = create_app()
    
    with app.app_context():
        print("\n📊 Database Schema Information:\n")
        
        tables = [
            ('projects', Project),
            ('project_locations', ProjectLocation),
            ('acquisition_progress', AcquisitionProgress),
            ('compensation', Compensation),
            ('legal', Legal),
            ('social_impact', SocialImpact),
            ('approvals', Approvals),
            ('predictions', Prediction),
            ('recommendations', Recommendation),
        ]
        
        for table_name, model_class in tables:
            print(f"✓ {table_name}")
            columns = [c.name for c in model_class.__table__.columns]
            print(f"  Columns: {', '.join(columns)}\n")


if __name__ == '__main__':
    print("=" * 60)
    print("DATABASE SCHEMA TEST")
    print("=" * 60 + "\n")
    
    # Test connection
    if not test_database_connection():
        print("\n✗ Please check your database configuration in .env")
        exit(1)
    
    # Print schema
    print_schema_info()
    
    # Test model creation
    print("\nTesting model creation and relationships...\n")
    if test_model_creation():
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed")
