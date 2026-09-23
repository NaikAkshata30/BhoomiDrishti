# BhoomiDrishti Project Data Research Synopsis

## Purpose of this document

This document summarizes the BhoomiDrishti project and defines a controlled research process for collecting approximately 60% near-real-time data for ten real infrastructure projects.

It is designed to be pasted into another LLM together with screenshots, downloaded PDFs, CSV files, Excel files, API responses or website links. The other LLM should determine whether each item is suitable for the selected project, identify which fields can be extracted, detect duplicates or mismatches, and recommend how the data should be stored.

The research must be performed project by project. Do not combine all projects into one general dataset before project identity and authority references have been verified.

---

## 1. Project overview

BhoomiDrishti is a land-acquisition early-warning and risk-analysis application for infrastructure projects in India.

The application combines:

- Project identity and agency information
- Project location and map coordinates
- Land-acquisition stage and possession progress
- Compensation progress
- Rehabilitation and resettlement progress
- Legal disputes and court cases
- Environmental and other approvals
- Climate and weather conditions
- Terrain, landscape and access constraints
- Project-specific barriers
- ML-based delay-risk prediction
- Risk-reduction scenario simulation
- Source provenance, freshness and verification status

The backend is a Flask application with SQLAlchemy and MySQL. The frontend is a React/Vite/Vinext application with Leaflet map integration. The current backend and frontend are located in:

```text
backend/
frontend/
```

Important backend models include:

- `Project`
- `ProjectLocation`
- `AcquisitionProgress`
- `Compensation`
- `Legal`
- `SocialImpact`
- `Approvals`
- `Prediction`
- `Recommendation`
- `SourceSnapshot`
- `ProjectBarrier`
- `ClimateObservation`

---

## 2. Current implementation status

The current database contains ten real project identities with public source links and project-level map coordinates.

Current verified implementation results:

| Area | Current status |
| --- | ---: |
| Projects with source and map location | 10/10 = 100% |
| Projects with project-specific barrier records | 10/10 = 100% |
| Projects with climate observations | 10/10 = 100% after public weather refresh |
| Operational field coverage before climate observations | 15.5% |
| Operational field coverage including climate observations | 31.1% |
| Current realistic near-real-time operational coverage | Approximately 30-32% |
| Practical target after project-wise research and official records | Approximately 60-70% |

The current 30-32% does not mean that 30-32% of every project is officially live. It means the database has populated operational fields, including public weather observations. Some project barriers are currently contextual public snapshots and must be verified against project-specific records.

The remaining gap is mainly caused by missing official or district-level records for:

- Compensation amounts and payment status
- Land-acquisition notices and possession progress
- R&R and affected-family progress
- Approval identifiers and status history
- Project-specific legal disputes
- Verified project boundaries and parcels
- Official climate warnings and hazard intersections

---

## 3. The ten real projects

These are the current project identities in the real data catalog. The authority must be matched to the project before collecting data.

| Project ID | Project | Primary authority/source | Location represented in current database |
| --- | --- | --- | --- |
| `REAL_001` | Delhi-Mumbai Expressway | [NHAI](https://nhai.gov.in/) | Dausa, Rajasthan |
| `REAL_002` | Ganga Expressway | [UPEIDA](https://upeida.in/) | Meerut, Uttar Pradesh |
| `REAL_003` | Char Dham Highway Project | [MoRTH](https://morth.nic.in/) | Rudraprayag, Uttarakhand |
| `REAL_004` | Mumbai Metro Line 3 | [MMRCL](https://mmrcl.com/) | Mumbai, Maharashtra |
| `REAL_005` | Delhi Metro Phase IV | [DMRC](https://delhimetrorail.com/) | New Delhi, Delhi |
| `REAL_006` | Chennai Metro Rail Project | [CMRL](https://chennaimetrorail.org/) | Chennai, Tamil Nadu |
| `REAL_007` | Bharatmala Pariyojana | [NHAI](https://nhai.gov.in/) | Multi-state/multi-district programme |
| `REAL_008` | Zojila Tunnel Project | [NHIDCL](https://nhidcl.com/) | Ganderbal, Jammu and Kashmir |
| `REAL_009` | Mumbai-Nagpur Expressway | [MSRDC](https://www.msrdc.org/) | Nagpur corridor, Maharashtra |
| `REAL_010` | Eastern Dedicated Freight Corridor | [DFCCIL](https://dfccil.com/) | Prayagraj corridor, Uttar Pradesh |

### Important identity warning

Some records represent a corridor, package or programme rather than one parcel-level project. Before collecting detailed land or compensation information, split the project into package, district, tehsil or village units if the official source does so.

For example:

- Bharatmala is a programme, not one single project boundary.
- Delhi-Mumbai Expressway has multiple packages and districts.
- Metro projects may have multiple construction packages and stations.
- Freight corridors span many districts and must be researched package by package.

---

## 4. Meaning of 60% near-real-time coverage

The target is not that every value updates every second. The target is that the most important project conditions are populated from current or recently published records and each value has evidence.

A reasonable 60% target consists of:

| Data group | Target contribution |
| --- | ---: |
| Project identity, authority, location and package matching | 10% |
| Acquisition stage, notifications, awards and possession | 15% |
| Compensation and affected-family data | 10% |
| R&R and social-impact data | 8% |
| Legal disputes and court updates | 7% |
| Approvals and clearance status | 5% |
| Weather, climate and landscape barriers | 5% |
| **Total target** | **60%** |

A source is considered suitable only when it provides a current or dated value, a project/authority match, and a source document or official URL.

---

## 5. Source order for every project

Research each project using the following order. Do not start with a random general search.

### Step 1: Primary project authority

Start with the agency responsible for the project.

Examples:

- NHAI for Delhi-Mumbai Expressway and Bharatmala
- UPEIDA for Ganga Expressway
- MoRTH for Char Dham Highway
- MMRCL for Mumbai Metro Line 3
- DMRC for Delhi Metro Phase IV
- CMRL for Chennai Metro
- NHIDCL for Zojila Tunnel
- MSRDC for Mumbai-Nagpur Expressway
- DFCCIL for Eastern Dedicated Freight Corridor

Search terms:

```text
<Project name> project status
<Project name> land acquisition
<Project name> package
<Project name> compensation
<Project name> R&R
<Project name> progress report
<Project name> tender
<Project name> annual report
```

Capture the official project ID, package number, district, dates, documents and status.

### Step 2: State and district authority

Search the state department, district collector, Land Acquisition Officer, CALA, revenue department and R&R office.

Search terms:

```text
<Project name> <state> land acquisition
<Project name> <district> award notification
<Project name> <district> compensation
<Project name> <district> possession
<Project name> <district> rehabilitation resettlement
<Project name> <district> social impact assessment
```

This step is usually the most important for compensation, acquisition stage and R&R.

### Step 3: data.gov.in

Open [data.gov.in](https://www.data.gov.in/) and search using:

- Project name
- State
- District
- Department
- Rainfall
- Infrastructure
- Land records
- Population or affected-family context

Check whether the dataset actually contains project-level rows. A state-wide dataset is not automatically a project dataset.

### Step 4: PARIVESH and environmental clearance

Search [PARIVESH](https://parivesh.nic.in/) using:

- Project name
- Applicant/authority
- State
- District
- Proposal number
- Sector

Capture environmental, forest, wildlife and CRZ proposal IDs, status, dates, conditions and approval documents.

### Step 5: Legal sources

Search [eCourts](https://ecourts.gov.in/), [District Court Services](https://services.ecourts.gov.in/) and [eCourts judgments](https://judgments.ecourts.gov.in/).

Use:

- Official project name
- Authority name
- Land Acquisition Officer
- Collector
- Village
- Survey/khasra number
- CNR number
- Case number
- Party name

Do not assume that every case mentioning an authority relates to the selected project.

### Step 6: Climate and landscape

Use:

- [IMD](https://mausam.imd.gov.in/)
- [IMD district warnings](https://mausam.imd.gov.in/responsive/districtWiseWarningGIS.php)
- [IMD rainfall](https://mausam.imd.gov.in/responsive/rainfallinformation.php)
- [NDEM](https://ndem.nrsc.gov.in/)
- [Bhuvan](https://bhuvan.nrsc.gov.in/)
- [Open-Meteo API](https://open-meteo.com/en/docs)
- [IMD Climate Hazard Atlas](https://imdpune.gov.in/hazardatlas/index.html)

Match weather and hazards spatially to the project district, coordinates or verified boundary. A district warning is not automatically a project-specific warning.

### Step 7: procurement and contracts

Use [CPPP/eProcure](https://eprocure.gov.in/eprocure/app) to find tender, contractor, award, corrigendum and contract information.

Use contract/package identifiers to connect the procurement record to the project.

---

## 6. Project-wise dataset requirements

The following matrix identifies which datasets fit each project type. It is not enough to collect any file mentioning the project; the file must answer one of these project questions.

| Project type | Highest-priority datasets | Special matching risks |
| --- | --- | --- |
| Expressway/highway | Alignment and packages, land notifications, awards, compensation, possession, R&R, contractor progress, environmental/forest clearance, rainfall/flood/terrain | Multiple packages, many districts, repeated project names |
| Metro | Corridor/package, station/depots, utility and land parcels, resettlement, environmental/traffic permissions, construction progress, court cases | Project authority and construction package may differ |
| Tunnel/mountain road | Land parcels, forest/wildlife clearance, slope/geology, rainfall/snow/landslide, access roads, compensation, court cases | Hazard data must be spatially matched; corridor point is insufficient |
| Dedicated freight corridor | Package, railway/DFCCIL reference, village/parcel records, compensation, possession, R&R, contractor, crossing permissions | Corridor is too large for one project-level record |
| Multi-state programme | State/package/district subprojects, authority reference, land and compensation per package, approval per package | Programme-level data cannot be used as package-level truth |

---

## 7. Fields to extract from every selected dataset

### Project identity

```text
project_id
source_project_name
official_project_reference
project_type
agency
state
district
tehsil
village
package_number
corridor_or_alignment
```

### Location

```text
latitude
longitude
geometry
survey_or_khasra_reference
land_required_ha
coordinate_system
location_accuracy
```

### Acquisition progress

```text
notification_status
notification_date
survey_status
award_status
award_date
possession_status
possession_date
overall_progress_percentage
possession_percentage
days_in_current_stage
```

### Compensation

```text
families_eligible
families_paid
pending_cases
total_compensation_amount
amount_disbursed
compensation_percentage
average_payment_delay_days
award_reference
payment_date_or_period
```

### R&R and social impact

```text
affected_families
rehabilitation_progress_percentage
resettlement_progress_percentage
relocation_completed_percentage
grievances_pending
stakeholder_responsiveness
resettlement_site
```

### Legal

```text
case_number
cnr_number
court
parties
filing_date
next_hearing_date
case_status
active_disputes
court_cases
average_case_age_days
order_url
```

### Approvals

```text
proposal_number
approval_type
environmental_status
forest_status
wildlife_status
crz_status
administrative_status
financial_status
submission_date
decision_date
pending_approvals
conditions
```

### Climate, landscape and barriers

```text
observation_time
temperature_c
precipitation_mm
wind_speed_kmh
weather_warning
flood_status
landslide_status
terrain_type
land_use_type
forest_or_wildlife_overlap
waterbody_overlap
access_constraint
barrier_category
barrier_severity
barrier_description
mitigation
```

### Provenance

```text
source_name
source_url
direct_document_url
source_format
published_at
retrieved_at
source_page_or_row
verification_status
confidence
notes
```

---

## 8. Folder structure for each project

Create one folder per project. Use the official project or package reference in the folder name when available.

```text
project_research/
  REAL_001_delhi_mumbai_expressway/
    00_project_register/
      project_identity.csv
      project_aliases.csv
      project_references.csv
      manifest.csv
    01_authority/
      raw/
      processed/
      documents/
    02_state_district_land_acquisition/
      raw/
      processed/
      documents/
    03_compensation/
      raw/
      processed/
      documents/
    04_rr_social_impact/
      raw/
      processed/
      documents/
    05_legal/
      raw/
      processed/
      documents/
    06_approvals/
      raw/
      processed/
      documents/
    07_climate_landscape/
      raw/
      processed/
      gis/
    08_procurement_contracts/
      raw/
      processed/
      documents/
    09_validation/
      mismatch_log.csv
      missing_data_log.csv
      review_notes.md
```

Repeat the same structure for `REAL_002` through `REAL_010`.

### File naming convention

```text
<project_id>_<source>_<topic>_<publication-date>.<extension>
```

Examples:

```text
REAL_004_MMRCL_project-status_2025-06-30.pdf
REAL_004_PARIVESH_environmental-proposal_2026-08-15.pdf
REAL_004_eCourts_case-order_2026-09-02.pdf
REAL_004_IMD_district-warning_2026-09-04.json
REAL_004_compensation_award-package-3_2026-08-31.xlsx
```

---

## 9. Manifest file for every project

Every project folder must contain a `manifest.csv` with one row per source file or API response.

```csv
project_id,source_name,source_url,direct_file_url,source_format,authority_reference,package_number,publication_date,retrieved_at,local_file,fields_extracted,source_page_or_row,verification_status,confidence,match_notes
REAL_004,MMRCL,https://mmrcl.com/,https://example.gov.in/status.pdf,PDF,MMRCL-ML3,Package-3,2026-08-31,2026-09-04T12:00:00Z,01_authority/documents/status.pdf,current_stage;package;progress,4,verified_manual,0.95,Matched by MMRCL reference and Mumbai corridor
```

The manifest is essential because another person or LLM must be able to understand where every value came from.

---

## 10. How to decide whether a dataset fits a project

Accept a dataset only if most of the following are true:

1. It comes from an official authority, official government portal or clearly identified public provider.
2. It contains an official project, package, proposal, case or location reference.
3. Its state/district/village or coordinates match the selected project.
4. It has a publication date, observation date or retrieval date.
5. Its units are clear.
6. Its scope is clear: project, package, district, state or national.
7. It contains values that map to the BhoomiDrishti fields.
8. It can be preserved as a source document or complete API response.
9. It does not require bypassing access restrictions.
10. Any manually extracted values can be checked against the original page or document.

Reject or mark for review when:

- It mentions only a similar project name.
- It is a news article with no official supporting document.
- It has no date.
- It mixes packages or districts without separation.
- It contains only a general programme statistic.
- It provides a map screenshot without coordinates or metadata.
- It contains personal data that the project does not need.

---

## 11. What to give another LLM for verification

Paste this context together with the relevant screenshot, file, API response or URL:

```text
You are reviewing a dataset for the BhoomiDrishti land-acquisition early-warning project.

Selected project:
- Project ID: <REAL_001 to REAL_010>
- Project name: <exact selected project>
- Authority: <official authority>
- State/district/package: <scope>

Task:
1. Decide whether the supplied dataset belongs to this exact project, package or district.
2. Identify the official project/reference number and all project aliases.
3. Classify the dataset scope as project, package, village, district, state, national or unrelated.
4. Extract fields relevant to project identity, location, acquisition, compensation, R&R, legal, approvals, climate, landscape and barriers.
5. For every extracted value, provide the source page number, table row, API JSON path or screenshot region.
6. Identify the publication date, observation date and retrieval freshness.
7. Identify units, coordinate system and geographic assumptions.
8. Detect duplicate, conflicting or mismatched records.
9. Mark every value as official, verified_manual, public_snapshot, inferred, missing or stale.
10. Do not invent values for fields that are absent.
11. Return a normalized CSV/JSON proposal that can be imported into BhoomiDrishti.
12. Recommend the correct project folder and filename.
13. State whether this dataset improves the 60% near-real-time target and by which data category.

Output sections:
- Dataset suitability: ACCEPT / ACCEPT WITH REVIEW / REJECT
- Project match evidence
- Extracted structured fields
- Missing fields
- Conflicts or risks
- Freshness assessment
- Verification status
- Recommended local filename
- Recommended database destination
- Normalized JSON or CSV
```

---

## 12. Recommended project-by-project research workflow

For each of the ten projects:

1. Create the project folder.
2. Fill `project_identity.csv` using the official authority site.
3. Record all aliases, packages and authority reference numbers.
4. Search the primary authority website.
5. Search the relevant state and district websites.
6. Search data.gov.in for supporting datasets.
7. Search PARIVESH for clearances.
8. Search eCourts for project-linked legal records.
9. Search IMD and NDEM for current climate/disaster conditions.
10. Search Bhuvan or approved GIS sources for landscape and land-use conditions.
11. Search CPPP/eProcure for tender and contractor records.
12. Save every original file in the correct subfolder.
13. Create the manifest row immediately after saving each file.
14. Extract normalized records into the processed folder.
15. Use another LLM to verify project match, fields and contradictions.
16. Mark uncertain records for human review.
17. Import only validated records into the backend.
18. Run the data-quality check and confirm source freshness.
19. Recalculate risk predictions after verified operational fields are imported.
20. Update the project dashboard and simulator with the newly verified barriers.

Do not move to the next project until the current project has a complete identity record and a source manifest.

---

## 13. Expected contribution from each project folder

For each project, try to obtain at minimum:

| Dataset group | Minimum evidence |
| --- | --- |
| Identity/location | Official authority page plus coordinate or boundary evidence |
| Acquisition | Latest notification/award/possession record or official progress spreadsheet |
| Compensation | Latest award/payment table or official district export |
| R&R | Latest affected-family and rehabilitation/resettlement report |
| Legal | CNR/case reference and latest status/order where applicable |
| Approvals | Proposal number and latest approval/status document |
| Climate | Current weather observation plus official warning check |
| Landscape | Verified GIS layer or documented district/terrain intersection |
| Procurement | Tender/award/contract reference where applicable |

If a category has no reliable source, record `missing` with an explanation. Do not fill it with synthetic values.

---

## 14. Integration into the current project

After validation, normalized files should be mapped as follows:

| Dataset | Backend destination |
| --- | --- |
| Identity and authority | `projects` |
| Coordinates and boundaries | `project_locations` and GeoJSON API |
| Acquisition stage | `acquisition_progress` |
| Compensation | `compensation` |
| R&R and social impact | `social_impact` |
| Legal cases | `legal` |
| Environmental/administrative/financial approvals | `approvals` |
| Climate observations | `climate_observations` |
| Terrain, weather, access and clearance obstacles | `project_barriers` |
| Original pages, PDFs and API responses | `source_snapshots` and project research folder |
| Delay-risk output | `predictions` |
| Actions | `recommendations` |

Each imported value should preserve:

- Source URL
- Direct document URL where applicable
- Publication or observation date
- Retrieval date
- Verification status
- Confidence
- Page, row or API field path

---

## 15. Final objective

The final result should be ten project folders containing traceable, project-matched datasets. The application should show:

- Exact project and package identity
- Map location or verified project boundary
- Current acquisition and possession status
- Compensation and R&R progress
- Legal dispute references
- Approval status
- Current weather and climate barriers
- Terrain and landscape constraints
- Source links and last-updated time
- Data quality and verification label
- Risk-reduction simulator controls based on the project’s actual available factors

The target is approximately 60% near-real-time coverage using public sources, official documents, approved data exports, automated weather refreshes and verified manual updates. The system must show missing or stale data honestly rather than filling gaps with invented values.
