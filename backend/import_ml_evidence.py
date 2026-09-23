"""Import the collected ML evidence without overwriting operational project data."""

import argparse
import csv
import os
from datetime import datetime

from app import create_app
from database import db
from models import EvidenceObservation, Project, SourceSnapshot


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ml', 'master_dataset'))


def parse_date(value):
    if not value:
        return None
    for fmt in ('%Y-%m-%d', '%Y-%m', '%Y'):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def as_float(value):
    try:
        return float(value) if value not in ('', None) else None
    except (TypeError, ValueError):
        return None


def read_rows(filename):
    with open(os.path.join(ROOT, filename), encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


def import_evidence(dry_run=False):
    projects = {project.project_id for project in Project.query.all()}
    observations = 0
    skipped_unknown = 0
    skipped_duplicate = 0
    sources = 0

    existing_keys = {
        (row.project_id, row.source_id, row.source_reference, row.field, row.entity_id)
        for row in EvidenceObservation.query.all()
    }
    existing_sources = {(row.content_hash, row.source_url) for row in SourceSnapshot.query.all()}

    for row in read_rows('normalized_observations.csv'):
        project_id = row.get('project_id', '').strip()
        if project_id not in projects:
            skipped_unknown += 1
            continue
        key = (project_id, row.get('source_id'), row.get('source_reference'), row.get('field'), row.get('entity_id') or None)
        if key in existing_keys:
            skipped_duplicate += 1
            continue
        normalized = as_float(row.get('value_normalized'))
        if not dry_run:
            db.session.add(EvidenceObservation(
                project_id=project_id,
                entity_id=row.get('entity_id') or None,
                field=row.get('field') or 'unknown',
                value_original=row.get('value_original') or None,
                value_normalized=normalized,
                value_text=row.get('value_normalized') if normalized is None else None,
                unit=row.get('unit') or None,
                measurement_type=row.get('measurement_type') or None,
                observation_date=parse_date(row.get('observation_date')),
                observation_period=row.get('observation_period') or None,
                source_id=row.get('source_id') or 'unknown',
                source_sha256=row.get('source_sha256') or None,
                source_url=row.get('source_url') or None,
                source_reference=row.get('source_reference') or None,
                verification_status=row.get('verification_status') or None,
                identity_status=row.get('identity_status') or None,
                confidence=as_float(row.get('confidence')),
                conflict_flag=(row.get('conflict_flag', '').lower() == 'true'),
                ml_eligible=(row.get('ml_eligible', '').lower() == 'true'),
            ))
        existing_keys.add(key)
        observations += 1

    for row in read_rows('source_manifest.csv'):
        source_id = row.get('source_id', '').strip()
        project_id = row.get('project_id', '').strip() or row.get('candidate_project_id', '').strip()
        source_url = row.get('source_url') or row.get('final_url') or 'unknown'
        source_hash = row.get('sha256') or source_id
        if not source_id or (source_hash, source_url) in existing_sources or project_id not in projects:
            continue
        if row.get('download_status') != 'downloaded':
            continue
        if not dry_run:
            db.session.add(SourceSnapshot(
                project_id=project_id,
                source_name=row.get('source_name') or source_id,
                source_url=source_url,
                published_at=parse_date(row.get('publication_date')),
                content_hash=source_hash,
                http_status=int(row['http_status']) if row.get('http_status', '').isdigit() else None,
            ))
        existing_sources.add((source_hash, source_url))
        sources += 1

    if not dry_run:
        db.session.commit()
    return {
        'observations_added': observations,
        'sources_added': sources,
        'skipped_unknown_projects': skipped_unknown,
        'skipped_duplicates': skipped_duplicate,
        'dry_run': dry_run,
    }


def main():
    parser = argparse.ArgumentParser(description='Import source-anchored ML evidence into the backend')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    app = create_app()
    with app.app_context():
        print(import_evidence(dry_run=args.dry_run))


if __name__ == '__main__':
    main()