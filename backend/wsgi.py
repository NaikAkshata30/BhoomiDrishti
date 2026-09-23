"""Production WSGI entry point with idempotent demo-data seeding."""

from app import create_app
from database import db
from models import Project


app = create_app()

with app.app_context():
    if Project.query.count() == 0:
        from load_data import load_projects
        from synthetic_data import generate_synthetic_projects

        load_projects(generate_synthetic_projects(), fetch_source_snapshots=False)
        db.session.commit()
        print("✓ Seeded the production database with demo projects")
