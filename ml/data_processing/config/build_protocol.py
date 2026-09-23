"""Build collection documentation, planned searches and explicit manual follow-ups."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from common import *
protocols={
'PROJECT_RESEARCH_PROTOCOL.md':'''# BhoomiDrishti research protocol

Canonical structure: the standalone ML tree supplied by the user on 2026-09-05. This collection does not touch their main project. Existing project files must not be deleted. feature_engineering and models remain empty.

Collection architecture: project/alias configuration -> official source discovery -> public download -> byte-level SHA256 -> page/table extraction -> identity and scope review -> explicit normalization -> conflicts/coverage/review reports. Collectors, extractors, validators and normalizers live in data_processing, not a replacement dataset tree. Reports are generated under master_dataset and project 09_validation folders.

Per project, populate exactly these topic folders:

| Folder | Contents |
|---|---|
| 00_project_register | User-supplied identity/aliases, scope rules, registry |
| 01_authority | Authority reports and construction progress; source identity |
| 02_state_district_land_acquisition | Land requirements, purchase/acquisition and notifications |
| 03_compensation | Compensation/R&R budgets, awards, payment evidence and rate approvals |
| 04_rr_social_impact | SIA, RAP, rehabilitation and social impacts |
| 05_legal | Project-linked court records with exact case/application identifiers |
| 06_approvals | Environmental/forest/wildlife documents with approval stage |
| 07_climate_landscape | District rainfall, terrain, hazards and access constraints |
| 08_procurement_contracts | Package, contractor, tender and contract evidence |
| 09_validation | Missing-data and manual-review reports; quarantined conflicting observations |

Raw files remain unchanged and carry a hash. Extracted JSON, page CSV and table-cell CSV are separate files. Each source has metadata and a manifest entry, including failures. HTML is used for genuine page evidence or download discovery; actual linked PDFs are preferred. Shared national climate sources are stored once and referenced by hash in other projects.

Every value needs an exact physical PDF page (one-based), detected table/row/column, HTML table/row/anchor, or API endpoint/parameters/JSON pointer. Detected table indices are extractor indices, not printed table numbers unless explicitly stated. Downloaded, extracted and accepted observations are different states. Missing is blank CSV / null JSON, never zero. A reported zero can be retained with provenance.

The collection is bounded to discovered priority documents. Coverage gaps and remaining searches are explicit. Do not claim exhaustive coverage or ML readiness from file counts.
''',
'DATA_SCHEMA.md':'''# Data schema

master_dataset/normalized_observations.csv and .json are long-form source observations. A row contains project_id, optional related_project_id, entity_id, parent_entity_id, record_scope, geography/phase/package, field, value_original, unit_original, value_normalized, unit, measurement_type, land_tenure, observation_date_original, observation_date, observation_period, date_precision, source_id, source_sha256, source_reference, retrieved_at, verification_status, identity_status, confidence, conflict_flag and ml_eligible.

project_registry describes the user's ten requested research targets; it is not independent official evidence. entity_registry contains local identifiers for scoped records; these local IDs are never official package numbers. data_dictionary describes requested and observed fields. A field absent from observations remains missing, as enumerated in missing_data_report.

Land area is normalized to hectares only from explicit units (m2 * 0.0001, acres * 0.40468564224). INR lakh * 100000, INR crore * 10000000. Do not guess units. Dates retain original tokens and precision. An ambiguous date or year/month without a day is not silently made into a full date. Document dates, observation dates, upload dates and retrieval times differ.

Percent denominators are source-specific. Ganga purchase progress uses purchased / proposed purchase area. Its total acquisition percentage uses purchased plus resumed/exchanged area / proposed alignment area. Preserve reported percentages. Never apply one universal acquisition formula to all source records. No percent is derived with missing/zero denominator or mixed scope/time.

CSV is UTF-8 with BOM; missing values are empty cells. JSON preserves null and numeric types. Generic table cells are candidate evidence only. Page references are physical PDF pages, not printed folio numbers. API extraction support exists but this collection makes no claim to have downloaded any API payload.
''',
'SOURCE_PRIORITY.md':'''# Source priority

1. Implementing agencies and Indian official government sources: NHAI, MoRTH/Bhoomi Rashi, UPEIDA, DMRC, MMRCL, CMRL, MSRDC, NHIDCL, DFCCIL, district/state portals, Supreme Court/eCourts, PARIVESH/MoEFCC, IMD, Bhuvan/NDEM and official procurement.
2. Government/public data and official project lender disclosures. JICA is a Japanese government agency and financing/disclosure institution, not a newspaper mirror. Its role and host are explicitly recorded; it is not represented as an Indian implementing agency URL.
3. Reputable secondary reporting is discovery/cross-checking only. Trace to the official record whenever possible; retain secondary discovery separately as public_snapshot and never include it in training.

Approved hosts are explicitly allowlisted. Redirect hosts are checked. TLS remains verified. On 401/403/429 or an access challenge, stop that host for the run. No credentials, CAPTCHA solving or bypass, proxy rotation, stealth headers or disabled certificate verification. The Windows transport fallback uses Schannel verification and does not disable trust/revocation checks. Restricted or unavailable URLs go to manual_review_required with exact searches and expected data.
''',
'PROJECT_TYPE_RULES.md':'''# Project and package hierarchy

REAL_001: Delhi-Mumbai/Delhi-Vadodara aliases help discovery. Dausa is a study location, not the extent of all expressway records. Bandikui-Jaipur spur is related and separate. NH-148 is not NH-148N; Delhi-Meerut must not be confused with DME.

REAL_002: Ganga district records are retained for all districts in official tables, with Meerut explicit. Package/group labels and district boundaries are different dimensions.

REAL_003: Char Dham road programme includes multiple highways and packages. Highway, shrine management and helicopter-operation cases must not be mixed. Court case/application status is recorded only as of a dated order.

REAL_004/005/006: Metro phase, corridor, station and depot scopes, private/government and temporary/permanent land remain distinct. NH Act 3A/3D/3G must not be assumed applicable. Delhi priority Phase IV and Phase IV-2 are separate. Chennai shared land must not be double counted across corridors. MMRCL's approval/design packages and construction packages need explicit identifiers.

REAL_007: Bharatmala is a programme. Programme/state totals are context; project/package records have child entity IDs. Never build a parcel-level training example from a programme total.

REAL_008: Z-Morh is NOT a Zojila alias. Zojila plus connecting-road contracts and historical designs have separate scopes. ROW available percentage is not acquired percentage. Do not derive completion by dividing current excavation by an older design length.

REAL_009: Approval package numbers may not match EPC civil package numbers. Aurangabad/named historical districts remain as source. Do not substitute Nagpur for another district.

REAL_010: Eastern and Western DFC are different. EDFC I/II/III and direct-purchase-policy requirements stay separate. Railway sections remain as printed, never relabeled as NH sections.

District weather is contextual, not route-measured. No coordinates, slopes, intersections or hazard scores are invented. No overall rainfall value is assigned to multi-state Bharatmala.
''',
'VERIFICATION_RULES.md':'''# Verification and ML-readiness rules

Allowed verification_status: official, verified_manual, public_snapshot, inferred, missing, stale, review_required. Official hosting indicates provenance, not correct project matching or extraction. identity_status is independent. Unknown matches remain candidate_project_id / review_required. Confidence is heuristic and explicitly not a calibrated probability.

Check downloaded bytes against SHA256; validate format by content, not suffix. PDF text and detected table cells remain candidate evidence. Accepted recipes require the original source hash, page/cell locator and matching text anchor. Ganga adapters require the known table layout, district sequence and land-accounting/percentage identities. An accounting failure is review_required, never silently corrected. Changed layouts are not filled by positional guesswork. Scans, undecodable labels and unprocessed tables stay in the review log.

Deduplicate URLs and hashes; compare source titles/names for potential duplicates without treating similarity as proof. One canonical raw file per checksum; duplicate URLs refer to it. Conflicts compare entity, field, date/period, measurement type, land tenure and units. Retain all differing values and mark conflict_flag. Different dated progress snapshots are not automatically conflicts. Unknown dates require review. Prefer a newer value only after establishing comparable scope and genuine temporal change.

No risk labels are manufactured. Outcomes require independently verified acquisition targets and actual possession/completion dates. Do not use post-outcome information for earlier predictions. Documents from the same project/packages and adjacent snapshots are correlated; group temporal splits accordingly. All present observations have ml_eligible=false until downstream dated feature assembly, label verification, conflict resolution and leakage review. Do not modify model architecture, prediction logic, backend or frontend.
'''}
for name,text in protocols.items():(ROOT/'research_protocol'/name).write_text(text,encoding='utf-8')
tasks=[]; plans=[]
for pid,p in PROJECTS.items():
    base={'project':p['project_name'],'authority':p['authority'],'state':p['study_state'],'district':p['study_district'],'aliases':p['aliases'],'package_number':'must be confirmed before parcel matching'}
    portals=[('https://services.ecourts.gov.in/','legal_case_search_not_completed','Case number, CNR, court, case status, dated order, project relation'),('https://parivesh.nic.in/','approval_search_not_completed','Proposal number, package, state/district, clearance stage and dated letter'),('https://bhuvan.nrsc.gov.in/','route_geometry_hazard_search_not_completed','Public route/terrain layers, metadata, CRS, licence and spatial resolution'),('https://eprocure.gov.in/','tender_archive_search_not_completed','Tender reference, package, award and contract PDFs'),('https://dsp.imdpune.gov.in/data_request_form_rainfall.php','historical_weather_request_not_completed','District daily historical rainfall for the acquisition observation period; public or authorized access only')]
    if pid in ('REAL_001','REAL_003','REAL_007','REAL_008'):portals.append(('https://bhoomirashi.gov.in/auth/revamp/login1.cshtml','manual_portal_workflow','Exact project/package, NH number, state/district, 3A/3D/award and CALA records; never use dashboard totals as project facts'))
    for url,reason,wanted in portals:tasks.append(dict(project_id=pid,url=url,reason=reason,search_parameters=base,expected_data=wanted,action='Use public search where available; if CAPTCHA/login is required use authorized manual access. No assertion is made that every portal is CAPTCHA-gated.'))
    for topic in ('land acquisition','3A 3D notification award','compensation R&R SIA','legal disputes','environment forest clearance','rainfall terrain flood','tender contract progress'):
        plans.append(dict(project_id=pid,query=f'{p["project_name"]} {p["authority"]} {p["study_district"]} {topic}',status='followup_search_plan_not_claimed_executed'))
tasks.extend([
dict(project_id='REAL_006',source_id='S008',reason='internal_corridor_header_conflict',source_reference='Cover and pages 4/14: Corridor 5; later pages including 78: Corridor 4',action='Retain page-specific scope. Verify appendix ownership with CMRL before using later-page figures.',expected_data='Corrected authoritative corridor attribution'),
dict(project_id='REAL_006',source_id='S008',reason='conflicting_station_counts',source_reference='PDF pages 4 and 14',action='Review 29 versus 30 station count; both values retained and conflict-flagged.'),
dict(project_id='REAL_002',reason='compensation_units_and_payment_basis',source_reference='Ganga district reports columns 13-16',action='Verify currency unit and proposed-versus-paid meaning before numeric compensation normalization. Scanned rate orders G040/G041 also require review.'),
dict(project_id='REAL_002',url='https://drive.google.com/file/d/1eO-RZ9nUiSjV4NbMoMRNQqT3m-knVqNu/view?usp=sharing',reason='official_index_external_hydrological_file_not_collected',search_parameters='UPEIDA Ganga Expressway Hydrological Report, index date 04-06-2021',expected_data='Hydrological report PDF',action='Follow official UPEIDA link in a browser; download only if publicly accessible.'),
dict(project_id='REAL_002',url='https://drive.google.com/file/d/1GdsDxxkMxogd9plXhKsKgZXYS0YpBc-q/view?usp=sharing',reason='official_index_external_coordinates_file_not_collected',search_parameters='UPEIDA Interchange Coordinates of Ganga Expressway, index date 04-06-2021',expected_data='Interchange coordinates with coordinate reference system',action='Follow official UPEIDA link; verify package/coordinate system; do not invent points.')])
write_json(CONFIG/'manual_tasks.json',tasks)
write_csv(ROOT/'data_processing/logs/search_plan.csv',plans,['project_id','query','status'])
write_json(CONFIG/'secondary_discovery.json',[
dict(project_id='REAL_003',source_name='Indian Kanoon judgment discovery',source_url='https://indiankanoon.org/doc/161682615/',discovery_purpose='Identify case and judgment date for official Supreme Court retrieval',official_trace_status='Official Supreme Court PDF downloaded as S038',verification_status='public_snapshot',used_in_training=False)])
readme='''# Reproduce or extend this collection

Use Python 3.11+ and install requirements.txt in your preferred environment. The delivered package is portable; all paths are resolved relative to ML. From the ML folder run:

```text
python data_processing/collect.py
python data_processing/extract.py
python data_processing/normalize_tables.py
python data_processing/config/build_reviewed_recipes.py
python data_processing/config/build_protocol.py
python data_processing/normalize.py
python data_processing/report.py
python data_processing/test_pipeline.py
```

collect.py reads config/sources.json. Existing hash-verified raw downloads are reused, not re-downloaded; a failed source is retried on rerun. Use --ids S037 etc. to select a source. Source metadata preserve retrieval time and original URLs. To collect a new snapshot of a mutable URL, add a NEW source_id and specify an intentional refresh workflow; do not replace an earlier raw snapshot. Public downloading is rate-limited per host and stops a host on access restrictions. The collector verifies TLS. On Windows only, certificate-chain failures may use Windows Schannel with verification still enabled.

extract.py processes saved evidence offline. --force re-extracts derived files without changing raw files. All PDF pages are text-extracted. Tables in short PDFs (<=40 pages) are attempted on all pages; longer PDFs use the first 30 keyword-relevant pages. Unprocessed relevant tables are explicitly reported. This first pass is not full OCR; sparse or scanned pages require manual review. Legacy Hindi font strings remain unaltered in raw/extracted output.

normalize_tables.py contains guarded Ganga and IMD adapters. Unknown layouts and arithmetic inconsistencies are quarantined. config/build_reviewed_recipes.py records additional reviewed source anchors and units. A successful anchor check proves traceability, not universal interpretation accuracy. Update recipes only after reviewing original evidence. normalize.py preserves conflicting observations; direct training eligibility is deliberately false.

source_manifest.csv is the audit entry point. normalized_observations.csv is the machine-readable fact collection. *_table_cells.csv and *_extracted.json are candidate evidence and must not be treated as validated features. Missing reports record requested fields that have not been normalized; a field may still exist in unreviewed raw material. No API payloads or vector datasets were collected in this pass.
'''
(ROOT/'data_processing/README.md').write_text(readme,encoding='utf-8')
print('Built protocols and manual follow-ups')
