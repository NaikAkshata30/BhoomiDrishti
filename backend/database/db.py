from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """
    Initialize the database with the Flask app.
    
    Args:
        app: Flask application instance
    """
    db.init_app(app)
    
    with app.app_context():
        # Import all models to register them with SQLAlchemy
        # This ensures all model classes are loaded before creating tables
        from models import (
            Project,
            ProjectLocation,
            AcquisitionProgress,
            Compensation,
            Legal,
            SocialImpact,
            Approvals,
            Prediction,
            Recommendation
            ,SourceSnapshot
            ,EvidenceObservation
        )
        
        # Create all tables
        db.create_all()
        from sqlalchemy import inspect, text
        if db.engine.dialect.name != 'mysql':
            print(f"✓ Database initialized using {db.engine.dialect.name}")
            return
        project_columns = {column['name'] for column in inspect(db.engine).get_columns('projects')}
        for column_name in ('source_name', 'source_url', 'source_document_url', 'data_status'):
            if column_name not in project_columns:
                db.session.execute(text(f'ALTER TABLE projects ADD COLUMN `{column_name}` VARCHAR(500) NULL'))
        nullable_columns = (
            ('acquisition_progress', 'overall_progress_percentage', 'FLOAT NULL'),
            ('acquisition_progress', 'possession_percentage', 'FLOAT NULL'),
            ('compensation', 'amount_disbursed', 'FLOAT NULL'),
            ('compensation', 'compensation_percentage', 'FLOAT NULL'),
            ('compensation', 'families_paid', 'INT NULL'),
            ('compensation', 'pending_cases', 'INT NULL'),
            ('approvals', 'pending_approvals', 'INT NULL'),
            ('social_impact', 'rehabilitation_progress_percentage', 'FLOAT NULL'),
            ('social_impact', 'resettlement_progress_percentage', 'FLOAT NULL'),
            ('social_impact', 'relocation_completed_percentage', 'FLOAT NULL'),
            ('social_impact', 'grievances_pending', 'INT NULL'),
            ('predictions', 'delay_probability', 'FLOAT NULL'),
            ('predictions', 'risk_level', 'VARCHAR(50) NULL'),
            ('predictions', 'risk_color', 'VARCHAR(20) NULL'),
        )
        for table_name, column_name, definition in nullable_columns:
            db.session.execute(text(f'ALTER TABLE `{table_name}` MODIFY COLUMN `{column_name}` {definition}'))
        db.session.execute(text('ALTER TABLE source_snapshots MODIFY COLUMN raw_content LONGTEXT NULL'))
        db.session.commit()
        print("✓ Database initialized successfully")
        print("✓ Tables created: projects, project_locations, acquisition_progress, compensation,")
        print("                 legal, social_impact, approvals, predictions, recommendations")


def reset_db(app):
    """
    Drop all tables and recreate them.
    Use with caution in development only!
    
    Args:
        app: Flask application instance
    """
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database reset successfully")
