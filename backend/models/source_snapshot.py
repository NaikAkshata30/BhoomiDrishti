from datetime import datetime
from database import db


class SourceSnapshot(db.Model):
    __tablename__ = 'source_snapshots'

    snapshot_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.String(50), db.ForeignKey('projects.project_id'), nullable=True)
    source_name = db.Column(db.String(255), nullable=False)
    source_url = db.Column(db.String(500), nullable=False)
    retrieved_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    published_at = db.Column(db.DateTime, nullable=True)
    content_hash = db.Column(db.String(64), nullable=False)
    http_status = db.Column(db.Integer, nullable=True)
    raw_content = db.Column(db.Text, nullable=True)
