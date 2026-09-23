"""
Data Loader Script

Loads project data into the database.

Usage:
    python load_data.py --source synthetic
    python load_data.py --source real
    
This will:
1. Clear existing data (development only)
2. Load all projects from the selected source
3. Display summary
"""

import argparse
import hashlib
import requests

from app import create_app
from database import db
from models import (
    Project, ProjectLocation, AcquisitionProgress, Compensation,
    Legal, SocialImpact, Approvals, Prediction, Recommendation
    ,SourceSnapshot, ProjectBarrier, ClimateObservation
)
from synthetic_data import generate_synthetic_projects
from real_data_source import build_real_project_records
from datetime import datetime


def clear_all_data():
    """
    Clear all data from database. Use with caution!
    Development only.
    """
    try:
        # Delete in reverse order of relationships
        Recommendation.query.delete()
        ProjectBarrier.query.delete()
        ClimateObservation.query.delete()
        SourceSnapshot.query.delete()
        Prediction.query.delete()
        Approvals.query.delete()
        SocialImpact.query.delete()
        Legal.query.delete()
        Compensation.query.delete()
        AcquisitionProgress.query.delete()
        ProjectLocation.query.delete()
        Project.query.delete()
        db.session.commit()
        print("✓ All existing data cleared")
    except Exception as e:
        db.session.rollback()
        print(f"✗ Error clearing data: {e}")
        raise


def load_projects(projects_data, fetch_source_snapshots=True):
    """
    Load synthetic projects into database.
    
    Args:
        projects_data (list): List of project dictionaries from synthetic_data
    """
    count = 0
    
    for proj_data in projects_data:
        try:
            # Create Project
            project = Project(
                project_id=proj_data['project']['project_id'],
                project_name=proj_data['project']['project_name'],
                project_type=proj_data['project']['project_type'],
                agency=proj_data['project']['agency'],
                state=proj_data['project']['state'],
                district=proj_data['project']['district'],
                village=proj_data['project']['village'],
                land_required_ha=proj_data['project']['land_required_ha'],
                affected_families=proj_data['project']['affected_families'],
                current_stage=proj_data['project']['current_stage'],
                status=proj_data['project']['status'],
                source_name=proj_data['project'].get('source_name'),
                source_url=proj_data['project'].get('source_url'),
                source_document_url=proj_data['project'].get('source_document_url'),
                data_status=proj_data['project'].get('data_status'),
            )
            db.session.add(project)
            db.session.flush()  # Get project_id for relationships

            source_url = proj_data['project'].get('source_document_url') or proj_data['project'].get('source_url')
            if source_url and fetch_source_snapshots:
                try:
                    source_response = requests.get(
                        source_url,
                        headers={'User-Agent': 'SIH-Land-Acquisition-DataBot/1.0'},
                        timeout=20,
                    )
                    raw_content = source_response.text[:60000]
                    db.session.add(SourceSnapshot(
                        project_id=project.project_id,
                        source_name=proj_data['project'].get('source_name', 'Unknown source'),
                        source_url=source_url,
                        content_hash=hashlib.sha256(raw_content.encode('utf-8')).hexdigest(),
                        http_status=source_response.status_code,
                        raw_content=raw_content,
                    ))
                except requests.RequestException as exc:
                    print(f"⚠ Source snapshot unavailable for {project.project_id}: {exc}")
            
            # Create ProjectLocation
            location = ProjectLocation(
                project_id=project.project_id,
                latitude=proj_data['location']['latitude'],
                longitude=proj_data['location']['longitude'],
                location_source=proj_data['location']['location_source'],
                accuracy_level=proj_data['location']['accuracy_level'],
            )
            db.session.add(location)
            
            # Create AcquisitionProgress
            acq = AcquisitionProgress(
                project_id=project.project_id,
                current_stage=proj_data['acquisition']['current_stage'],
                notification_status=proj_data['acquisition']['notification_status'],
                survey_status=proj_data['acquisition']['survey_status'],
                award_status=proj_data['acquisition']['award_status'],
                possession_status=proj_data['acquisition']['possession_status'],
                overall_progress_percentage=proj_data['acquisition']['overall_progress_percentage'],
                possession_percentage=proj_data['acquisition']['possession_percentage'],
                days_in_current_stage=proj_data['acquisition']['days_in_current_stage'],
            )
            db.session.add(acq)
            
            # Create Compensation
            comp = Compensation(
                project_id=project.project_id,
                total_compensation_amount=proj_data['compensation']['total_compensation_amount'],
                amount_disbursed=proj_data['compensation']['amount_disbursed'],
                compensation_percentage=proj_data['compensation']['compensation_percentage'],
                families_eligible=proj_data['compensation']['families_eligible'],
                families_paid=proj_data['compensation']['families_paid'],
                pending_cases=proj_data['compensation']['pending_cases'],
                average_payment_delay_days=proj_data['compensation']['average_payment_delay_days'],
            )
            db.session.add(comp)
            
            # Create Legal
            legal = Legal(
                project_id=project.project_id,
                active_disputes=proj_data['legal']['active_disputes'],
                dispute_count=proj_data['legal']['dispute_count'],
                court_cases=proj_data['legal']['court_cases'],
                legal_status=proj_data['legal']['legal_status'],
                average_case_age_days=proj_data['legal']['average_case_age_days'],
            )
            db.session.add(legal)
            
            # Create SocialImpact
            social = SocialImpact(
                project_id=project.project_id,
                affected_families=proj_data['social_impact']['affected_families'],
                rehabilitation_progress_percentage=proj_data['social_impact']['rehabilitation_progress_percentage'],
                resettlement_progress_percentage=proj_data['social_impact']['resettlement_progress_percentage'],
                relocation_completed_percentage=proj_data['social_impact']['relocation_completed_percentage'],
                grievances_pending=proj_data['social_impact']['grievances_pending'],
                stakeholder_responsiveness=proj_data['social_impact']['stakeholder_responsiveness'],
            )
            db.session.add(social)
            
            # Create Approvals
            approvals = Approvals(
                project_id=project.project_id,
                environmental_approval_status=proj_data['approvals']['environmental_approval_status'],
                administrative_approval_status=proj_data['approvals']['administrative_approval_status'],
                financial_approval_status=proj_data['approvals']['financial_approval_status'],
                other_approval_status=proj_data['approvals']['other_approval_status'],
                pending_approvals=proj_data['approvals']['pending_approvals'],
                average_approval_delay_days=proj_data['approvals']['average_approval_delay_days'],
            )
            db.session.add(approvals)
            
            # Create Prediction
            prediction = Prediction(
                project_id=project.project_id,
                delay_probability=proj_data['prediction']['delay_probability'],
                risk_level=proj_data['prediction']['risk_level'],
                risk_color=proj_data['prediction']['risk_color'],
                model_version=proj_data['prediction']['model_version'],
                prediction_confidence=proj_data['prediction'].get('prediction_confidence'),
            )
            db.session.add(prediction)
            
            # Create Recommendations
            for rec_data in proj_data['recommendations']:
                recommendation = Recommendation(
                    project_id=project.project_id,
                    factor=rec_data['factor'],
                    priority=rec_data['priority'],
                    recommendation_text=rec_data['text'],
                )
                db.session.add(recommendation)

            for barrier_data in proj_data.get('barriers', []):
                db.session.add(ProjectBarrier(
                    project_id=project.project_id,
                    category=barrier_data['category'],
                    title=barrier_data['title'],
                    severity=barrier_data.get('severity', 'MEDIUM'),
                    impact_score=barrier_data.get('impact_score'),
                    status=barrier_data.get('status'),
                    description=barrier_data.get('description'),
                    mitigation=barrier_data.get('mitigation'),
                    source_name=barrier_data.get('source_name'),
                    source_url=barrier_data.get('source_url'),
                    verification_status=barrier_data.get('verification_status', 'missing'),
                    observed_at=barrier_data.get('observed_at'),
                ))
            
            count += 1
            
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error loading project {proj_data['project']['project_id']}: {e}")
            raise
    
    # Commit all projects
    try:
        db.session.commit()
        print(f"✓ Loaded {count} projects into database")
    except Exception as e:
        db.session.rollback()
        print(f"✗ Error committing data: {e}")
        raise


def display_summary():
    """Display summary of loaded data"""
    print("\n" + "=" * 70)
    print("DATABASE SUMMARY")
    print("=" * 70)
    
    total_projects = Project.query.count()
    print(f"\n📊 Total Projects: {total_projects}")
    
    # Risk distribution
    high_risk = Prediction.query.filter_by(risk_level='HIGH').count()
    medium_risk = Prediction.query.filter_by(risk_level='MEDIUM').count()
    low_risk = Prediction.query.filter_by(risk_level='LOW').count()
    no_risk = Prediction.query.filter_by(risk_level='NO_RISK').count()
    
    print(f"\n🔴 HIGH RISK: {high_risk} projects")
    print(f"🟠 MEDIUM RISK: {medium_risk} projects")
    print(f"🟡 LOW RISK: {low_risk} projects")
    print(f"🟢 NO RISK: {no_risk} projects")
    
    print(f"\n📍 Locations: {ProjectLocation.query.count()}")
    print(f"💰 Compensation records: {Compensation.query.count()}")
    print(f"⚖️  Legal records: {Legal.query.count()}")
    print(f"🏘️  Social Impact records: {SocialImpact.query.count()}")
    print(f"✅ Approvals: {Approvals.query.count()}")
    print(f"🎯 Recommendations: {Recommendation.query.count()}")
    
    print("\n📋 Projects by State:")
    states = db.session.query(
        Project.state,
        db.func.count(Project.project_id).label('count')
    ).group_by(Project.state).all()
    
    for state, count in states:
        print(f"   {state}: {count}")
    
    print("\n" + "=" * 70)


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(description="Load project data into the database")
    parser.add_argument(
        "--source",
        choices=["synthetic", "real"],
        default="synthetic",
        help="Choose whether to load demo data or real public project data.",
    )
    args = parser.parse_args()

    print("=" * 70)
    print("DATA LOADER - Land Acquisition System")
    print("=" * 70)
    
    app = create_app()
    
    with app.app_context():
        if args.source == "real":
            print("\n⚙️  Loading real public project data...\n")
            projects_data = build_real_project_records()
        else:
            print("\n⚙️  Loading synthetic demo data...\n")
            projects_data = generate_synthetic_projects()
        
        # Clear existing data
        clear_all_data()
        
        # Load selected source data
        load_projects(projects_data)
        
        # Display summary
        display_summary()
        
        print("\n✅ Data loading complete!")
        print("\nYou can now:")
        print("  - Run the Flask server: python app.py")
        print("  - Test the API: GET http://localhost:5000/api/health")
        print("  - Query projects: GET http://localhost:5000/api/projects")


if __name__ == '__main__':
    main()
