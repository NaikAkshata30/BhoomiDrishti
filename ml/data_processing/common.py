"""Shared, portable paths and lossless CSV/JSON serialization."""
import csv, json, hashlib, re
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / 'data_processing/config'
MASTER = ROOT / 'master_dataset'
def read_json(path, default=None):
    return json.loads(Path(path).read_text(encoding='utf-8')) if Path(path).exists() else default
def write_json(path, value):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
def write_csv(path, rows, fields=None):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    fields=fields or list(dict.fromkeys(k for row in rows for k in row))
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore'); w.writeheader()
        for row in rows:
            w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in row.items()})
def utc(): return datetime.now(timezone.utc).isoformat(timespec='seconds')
def sha(data): return hashlib.sha256(data).hexdigest()
def relative(path): return Path(path).relative_to(ROOT).as_posix()
def safe(value): return re.sub(r'[^a-zA-Z0-9_-]+','_',value).strip('_')[:85]
PROJECTS={p['project_id']:p for p in read_json(CONFIG/'projects.json',[])}
def project_dir(pid): return ROOT/'project_research'/PROJECTS[pid]['folder']

