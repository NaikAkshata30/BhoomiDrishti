# Data Source and Implementation Guide

## Purpose

This guide defines where BhoomiDrishti should obtain project data, what each source can provide, how the data should be saved, and how it should be imported into the backend.

The target is approximately 65-70% near-real-time coverage. This does not mean that every field is live every second. Each field must show its source, retrieval time, and verification status.

## Source Register

| Data category | Recommended source | Link | Useful information | Available format or access | Suggested refresh |
| --- | --- | --- | --- | --- | --- |
| Highway project status | National Highways Authority of India | [NHAI](https://nhai.gov.in/) | Highway projects, construction status, awarded and completed lengths, notices and documents | HTML, dashboards, PDF | Daily |
| National road schemes | Ministry of Road Transport and Highways | [MoRTH](https://morth.nic.in/) | Schemes, notifications, project documents and ministry updates | HTML, PDF | Daily or weekly |
| Government open datasets | Open Government Data Platform | [data.gov.in](https://www.data.gov.in/) | State, district, rainfall, infrastructure and administrative datasets | CSV, JSON, API, XLS | Daily or monthly |
| Project locations and GIS layers | ISRO/NRSC Bhuvan | [Bhuvan](https://bhuvan.nrsc.gov.in/) | Satellite maps, boundaries and thematic GIS layers | GIS layers, KML, GeoJSON, shapefile | Weekly or monthly |
| Flood and disaster barriers | National Database for Emergency Management | [NDEM](https://ndem.nrsc.gov.in/) | Floods, disasters, affected areas and emergency maps | GIS maps, PDF, raster or vector layers | Event-based |
| Weather and warnings | India Meteorological Department | [IMD](https://mausam.imd.gov.in/) | District warnings, rainfall, forecasts, nowcasts and cyclone information | Website, RSS, API subject to access, PDF, GIS | Hourly or daily |
| IMD data access | IMD Data Supply Portal | [IMD Data Supply Portal](https://dsp.imdpune.gov.in/) | Historical and station-based weather data | Portal or API subject to access | Daily |
| Climate hazard maps | IMD Climate Hazard Atlas | [Climate Hazard Atlas](https://imdpune.gov.in/hazardatlas/index.html) | Climate hazard and vulnerability information | Maps and reports | Monthly or annual |
| Environmental clearance | PARIVESH 2.0 | [PARIVESH](https://parivesh.nic.in/) | Environmental, forest, wildlife and CRZ proposal status | Search portal, HTML, PDF | Daily or weekly |
| Environmental monitoring | Ministry clearance portal | [Environment Clearance](https://environmentclearance.nic.in/) | Proposal status, clearance documents and monitoring reports | HTML, PDF | Daily or weekly |
| Legal disputes | eCourts | [eCourts](https://ecourts.gov.in/) | Court services, case statistics and links to case searches | Web portal, PDF | Daily |
| District case status | eCourts District Services | [District Court Services](https://services.ecourts.gov.in/) | Case status, orders and history using CNR or other search details | HTML, PDF; CAPTCHA may apply | Daily |
| Acts and rules | India Code | [India Code](https://www.indiacode.gov.in/) | Laws, rules, notifications and amendments | HTML, PDF | Monthly or when amended |
| Public grievances | CPGRAMS | [CPGRAMS](https://pgportal.gov.in/) | Public grievance registration and resolution information | Web portal; access may be restricted | Daily |
| Public tenders and contracts | Central Public Procurement Portal | [CPPP/eProcure](https://eprocure.gov.in/eprocure/app) | Tenders, contractors, award dates and contract documents | HTML, PDF | Daily |
| Project-specific authority data | State and project authority portals | See [existing real source catalogue](REAL_DATA_SOURCES.md) | Project identity, notices, progress and local documents | HTML, PDF, CSV or portal export | Daily or weekly |
| Land records and parcel data | State revenue, Bhulekh and GIS portals | Search the relevant state government portal | Survey numbers, parcels and land records where publicly available | Portal, PDF, GIS | Daily or weekly |
| Compensation and awards | District Collector or Land Acquisition Officer | Search by state and district | Awards, notices, eligible families and payment progress | PDF, Excel or portal | Weekly |
| R&R and social impact | District R&R and social welfare offices | Search by state and district | Affected families, rehabilitation, resettlement and grievances | PDF, Excel or portal | Weekly or monthly |

## Data-to-Application Mapping

| Application area | Fields to collect | Primary sources | Backend destination |
| --- | --- | --- | --- |
| Project identity | `project_id`, `project_name`, `project_type`, `agency`, `state`, `district`, `village`, `status` | Project authority, NHAI, MoRTH, state portals | `projects` |
| Location | Latitude, longitude, boundary, land area, coordinate system | Bhuvan, state GIS, revenue maps, project authority | `project_locations` and GeoJSON API |
| Acquisition progress | Current stage, notification, survey, award, possession, overall progress | Revenue department, Collector, LAO, project authority | `acquisition_progress` |
| Compensation | Total amount, amount disbursed, eligible families, paid families, pending cases, delay | LAO, Collector, treasury or payment records | `compensation` |
| R&R and social impact | Affected families, rehabilitation, resettlement, relocation, grievances and responsiveness | R&R office, SIA reports, district administration | `social_impact` |
| Legal disputes | Active disputes, total disputes, court cases, legal status and case age | eCourts, legal cell, court orders | `legal` |
| Approvals | Environmental, administrative, financial, forest, wildlife and CRZ status | PARIVESH, MoEFCC and state departments | `approvals` |
| Climate and project barriers | Hazard type, severity, rainfall, flood, landslide, terrain, access, clearance dependency and observation time | IMD, NDEM, Bhuvan, PARIVESH and project authorities | `project_barriers` |
| Current weather observation | Temperature, precipitation, wind speed, weather code and observation time | [Open-Meteo](https://open-meteo.com/) public coordinate API; verify warnings with [IMD](https://mausam.imd.gov.in/) | `climate_observations` |
| Risk prediction | Delay probability, risk level, confidence and model version | Combined verified data | `predictions` |

## Project Storage Layout

Create these directories under `backend/`:

```text
backend/
  data/
    raw/
      nhai/
      morth/
      imd/
      ndem/
      parivesh/
      ecourts/
      state_portals/
      district_documents/
    processed/
      projects/
      locations/
      acquisition/
      compensation/
      social_impact/
      legal/
      approvals/
      climate/
    archive/
    manifests/
  ingestion/
    source_registry.py
    download_sources.py
    parse_documents.py
    normalize_records.py
    validate_records.py
    import_to_database.py
```

| Location | What to save there |
| --- | --- |
| `data/raw/` | Untouched downloads from official sources |
| `data/processed/` | Clean CSV, JSON and GeoJSON files ready for import |
| `data/archive/` | Older versions retained for audit and comparison |
| `data/manifests/` | Source URL, retrieval time, publication time, hash and processing result |
| `ingestion/` | Download, parsing, validation and database import code |

Do not store source data in `frontend/public`. The frontend should receive it through the Flask API.

## Standard Record Format

Every record should contain project identity, source provenance and freshness information:

```json
{
  "project_id": "REAL_001",
  "source_name": "NHAI",
  "source_url": "https://nhai.gov.in/",
  "source_document_url": null,
  "published_at": "2026-09-03T00:00:00Z",
  "retrieved_at": "2026-09-04T10:30:00Z",
  "verification_status": "official",
  "confidence": 0.9,
  "data_status": "current",
  "data": {}
}
```

Use these values for `verification_status`:

| Value | Meaning |
| --- | --- |
| `official` | Taken directly from an official source |
| `verified_manual` | Entered or checked by an authorized person against an official document |
| `public_snapshot` | Public information that may be old or incomplete |
| `inferred` | Calculated from other values; never present as an official measurement |
| `missing` | No reliable value was found |
| `stale` | A value exists but is older than the permitted freshness window |

## Example Processed Files

### `projects.csv`

```csv
project_id,project_name,agency,state,district,village,land_required_ha,current_stage,status,source_name,source_url,observed_at
REAL_001,Delhi Mumbai Expressway,NHAI,Rajasthan,Alwar,,125.5,Possession,Active,NHAI,https://nhai.gov.in/,2026-09-04T10:30:00Z
```

### `compensation.csv`

```csv
project_id,total_compensation_amount,amount_disbursed,compensation_percentage,families_eligible,families_paid,pending_cases,average_payment_delay_days,source_url,observed_at
REAL_001,50000000,35000000,70,420,294,126,38,https://example.gov.in/document.pdf,2026-09-04T10:30:00Z
```

### `locations.geojson`

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [76.6346, 27.5530]
      },
      "properties": {
        "project_id": "REAL_001",
        "project_name": "Delhi Mumbai Expressway",
        "state": "Rajasthan",
        "district": "Alwar"
      }
    }
  ]
}
```

GeoJSON coordinates must be `[longitude, latitude]` and should use WGS84 / EPSG:4326.

## Collection Procedure

### API or official download

1. Open the source and locate its API, Web Services, Downloads or Open Data section.
2. Register for an access key if the source requires one.
3. Save the original JSON, CSV or Excel file under `data/raw/<source>/`.
4. Record the URL and timestamps in `data/manifests/`.
5. Normalize field names into the project format.
6. Validate project matching, dates, units and missing values.
7. Import only validated records into MySQL.
8. Preserve the original file and source URL.

### PDF or scanned document

1. Save the original PDF under `data/raw/<source>/`.
2. Record its publication date and URL.
3. Extract text with a PDF parser; use OCR only for scanned pages.
4. Convert extracted values into CSV or JSON.
5. Manually verify important amounts, family counts and statuses.
6. Mark the record `verified_manual` after checking it.
7. Keep the PDF as supporting evidence.

### GIS or satellite data

1. Download the original KML, GeoJSON, shapefile or GeoTIFF.
2. Save it under the appropriate `data/raw/` source directory.
3. Convert the layer to GeoJSON or a database GIS format.
4. Convert coordinates to WGS84 / EPSG:4326.
5. Intersect the project point or boundary with hazard layers.
6. Save derived results in `data/processed/climate/`.
7. Store the layer URL, observation date and processing method.

## Matching Projects Across Sources

Do not join records using project name alone. Maintain a cross-reference file:

```csv
project_id,source_name,source_project_name,authority_reference,match_method,match_confidence
REAL_001,NHAI,Delhi-Mumbai Expressway,DM-EXP-001,manual,1.0
REAL_001,PARIVESH,Delhi Mumbai Expressway Package 4,EC-12345,manual,0.95
REAL_001,eCourts,State vs Land Acquisition Officer,CASE-98765,manual,0.85
```

Use this matching order:

1. Official project ID.
2. Authority reference number.
3. Project name plus district.
4. Project name plus agency.
5. Geographic overlap.
6. Authorized manual confirmation.

## Refresh Schedule

| Collector | Recommended schedule |
| --- | --- |
| IMD weather and warnings | Every 1-3 hours |
| NDEM disaster information | Every 3-6 hours during an active event |
| Project authority status | Daily |
| PARIVESH approvals | Daily |
| eCourts references | Daily, subject to portal rules |
| Compensation | Daily or weekly |
| R&R and grievances | Weekly |
| Satellite imagery | Weekly or monthly |
| Government notifications | Daily |
| District manual updates | Whenever a verified update is received |

Use Windows Task Scheduler, APScheduler or Celery to run collectors. Keep API keys and database credentials in environment variables, never in source files.

## Source Snapshot and History

The existing `SourceSnapshot` model stores the right provenance fields: source URL, retrieval time, publication time, content hash, HTTP status and raw content. See `backend/models/source_snapshot.py`.

For historical field-level changes, add a separate observation table with:

```text
observation_id
project_id
category
field_name
field_value
source_name
source_url
source_document_url
published_at
retrieved_at
verification_status
confidence
raw_file_path
```

This allows the application to show trends, detect stale data, audit changes and retrain the prediction model using historical observations.

## Implementation Order

| Phase | Work | Expected result |
| --- | --- | --- |
| 1 | Create raw, processed, archive and manifest directories | Consistent storage |
| 2 | Create a source registry and project cross-reference | Reliable source and project matching |
| 3 | Import NHAI, MoRTH and project authority data | Better project status |
| 4 | Connect public weather and IMD/NDEM verification | Current climatic barriers |
| 5 | Import PARIVESH and environmental records | Approval monitoring |
| 6 | Add compensation and R&R CSV/PDF upload | Payment and resettlement coverage |
| 7 | Add verified eCourts references | Legal-risk coverage |
| 8 | Add historical observations | Time-series data and freshness checks |
| 9 | Expose source and freshness metadata in the Flask API | Transparent frontend |
| 10 | Recalculate predictions after verified updates | More useful early warnings |

## Rules for the Dashboard

- Show `source_name`, `source_url` and `retrieved_at` for every important metric.
- Show `Not available` for missing official values; do not replace them with invented values.
- Label calculated values as `Inferred`.
- Display a stale warning when data exceeds its category freshness window.
- Keep real project identity separate from synthetic demonstration values.
- Store all imported source documents and hashes so a value can be audited later.

## Expected Coverage

A practical 65-70% target can come from:

| Coverage contribution | Approximate contribution |
| --- | ---: |
| Official APIs, dashboards and downloads | 40-50% |
| GIS, satellite and weather information | 15-20% |
| PDF/OCR extraction with verification | 10-15% |
| Authorized manual district updates | 10-15% |

This target is realistic because compensation, R&R and litigation information is often delayed, fragmented, protected by login or published only in documents. The system should report freshness and confidence rather than claim that every project field is fully real-time.
