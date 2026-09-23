"""Refresh the real-source catalog. Suitable for Windows Task Scheduler."""

import subprocess
import sys
from pathlib import Path


backend_dir = Path(__file__).resolve().parent
subprocess.run(
    [sys.executable, str(backend_dir / 'load_data.py'), '--source', 'real'],
    cwd=backend_dir,
    check=True,
)

sys.path.insert(0, str(backend_dir))
from app import create_app
from climate_service import refresh_climate_observations

with create_app().app_context():
    print(f'✓ Refreshed climate observations for {refresh_climate_observations()} projects')