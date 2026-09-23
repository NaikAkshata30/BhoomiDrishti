# Real-Time and Near-Real-Time Data Source Extraction Guide

## Purpose

This document is designed to be shared with team members who will independently collect data for BhoomiDrishti. Each person can take one or more rows, download or request the relevant data, and return the original file plus the extracted structured record.

The target is near-real-time monitoring, not guaranteed live data for every field. Refresh frequency depends on how often the source publishes new information.

## Required output from every source

For every downloaded or extracted record, preserve:

- `project_id`
- Source name
- Source page URL
- Direct document, API or download URL
- Date published by the source
- Date and time retrieved
- Original file or response
- File format
- Official project/reference number
- Extracted fields
- Verification status
- Notes about missing or uncertain values

Use the following status values:

- `official`: copied directly from an official structured source
- `verified_manual`: extracted from an official document and checked by a person
- `public_snapshot`: publicly available but incomplete or not guaranteed current
- `inferred`: calculated from other values
- `missing`: no reliable value found
- `stale`: value exists but is older than the permitted refresh window

## Source extraction table

| Source name | Link to dataset, API, portal or document | Step-by-step instructions for finding and extracting data |
| --- | --- | --- |
| Open Government Data Platform India | [data.gov.in](https://www.data.gov.in/) · [Resources](https://www.data.gov.in/resources) · [APIs](https://www.data.gov.in/apis) · [Web services](https://www.data.gov.in/datasets_webservices) | 1. Open the portal and search using the project state, district, department and subject, for example `rainfall Rajasthan`, `infrastructure Maharashtra`, `land acquisition`, or `highway project`. 2. Open the dataset page and check the owning department, update date, geographic coverage and license. 3. Prefer resources marked API, JSON, CSV or XLS. 4. For an API, open the API details, copy the resource identifier and follow the documented request format. 5. For CSV/XLS, download the resource and preserve the original filename. 6. Record the department, resource ID, publication date and retrieval date. 7. Filter records using district, village, project name or official project ID. 8. Save original files under `backend/data/raw/data_gov_in/`; save normalized files under `backend/data/processed/`. |
| National Highways Authority of India (NHAI) | [NHAI portal](https://nhai.gov.in/) · [Bharatmala project map PDF](https://nhai.gov.in/assets/pdf/Bharatmala_NH_highlighted_2023_Project.pdf) · [NHAI Data Lake](https://nhai.gov.in/) | 1. Open NHAI and use the site search for the project name, package number, state, district, `project status`, `award`, `construction`, `land acquisition` or `Bharatmala`. 2. Check project overview pages, news, tenders, circulars, maps and downloadable documents. 3. For a PDF, download the original file and record its title, issue date and page number containing the value. 4. Extract project name, package, state, district, contractor, awarded length, completed length, construction status, land requirement and document dates. 5. Confirm that the project package belongs to the correct corridor; do not join only by similar names. 6. Save PDF files under `backend/data/raw/nhai/`. 7. Save verified rows as `nhai_projects_YYYY-MM-DD.csv`. 8. NHAI may expose public pages but not every operational metric as a public API; do not scrape protected dashboards or invent unavailable values. |
| Ministry of Road Transport and Highways (MoRTH) | [MoRTH](https://morth.nic.in/) | 1. Search the portal for the project name, highway number, state, district, scheme, notification, land acquisition, award or progress report. 2. Open the ministry page or document and verify the issuing department and publication date. 3. Download PDF notifications, reports, sanctions and progress documents. 4. Extract project reference number, road/highway number, package, state, district, sanctioned amount, status, dates, agency and land-acquisition references. 5. Record the exact page number for each extracted value. 6. Save originals under `backend/data/raw/morth/`; save structured results under `backend/data/processed/projects/`. 7. Treat ministerial announcements as public snapshots unless they include a dated official progress table. |
| State and project authority portals | [Existing project source catalogue](REAL_DATA_SOURCES.md) | 1. Identify the authority responsible for the project, such as UPEIDA, MMRCL, DMRC, CMRL, NHIDCL, MSRDC or DFCCIL. 2. Open the authority website and search by project name, package, corridor, tender, progress, land acquisition, rehabilitation or notice. 3. Check project-status pages, annual reports, board documents, tender pages, notices, press releases and PDFs. 4. Record the authority project ID and package ID. 5. Extract current stage, planned and completed work, contract dates, agency, project location, notices and approval dependencies. 6. Download the original PDF, Excel or CSV where available. 7. If the portal is blocked with login or returns HTTP 403, record the failed URL and request an official export instead of bypassing access controls. 8. Save each authority under its own directory in `backend/data/raw/state_portals/`. |
| IMD public weather and warning services | [IMD Mausam](https://mausam.imd.gov.in/) · [District warning GIS](https://mausam.imd.gov.in/responsive/districtWiseWarningGIS.php) · [District nowcast GIS](https://mausam.imd.gov.in/responsive/districtWiseNowcastGIS.php) · [Rainfall information](https://mausam.imd.gov.in/responsive/rainfallinformation.php) · [API documentation](https://mausam.imd.gov.in/Forecast/marquee_data/API_doc.pdf) · [CAP alerts RSS](https://cap-sources.s3.amazonaws.com/in-imd-en/rss.xml) | 1. Open the district warning or nowcast page. 2. Select the state and project district. 3. Record warning type, severity, issue time, validity period and affected district. 4. For rainfall, record observation period, rainfall amount, station/district and units. 5. For CAP/RSS, download or request the feed and parse alert title, area, severity, onset, expiry and source identifier. 6. Save PDF bulletins and RSS/API responses with retrieval time under `backend/data/raw/imd/`. 7. Match the alert to projects by district or project polygon. 8. Do not convert a district warning into a project-specific event without recording the geographic matching method. |
| IMD Data Supply Portal | [IMD Data Supply Portal](https://dsp.imdpune.gov.in/) | 1. Open the portal and review its registration and data-request requirements. 2. Select the required station, variable and date range. 3. Request temperature, rainfall, wind or historical observations. 4. Download the response in the format offered by the portal. 5. Record station ID, coordinates, variable, units, observation interval and quality flags. 6. Save the original response under `backend/data/raw/imd/`; convert it to the project climate schema. 7. Use the nearest station or a documented spatial interpolation method; record the distance from the project. 8. If access requires approval, request it from IMD instead of sharing credentials. |
| IMD Climate Hazard Atlas | [Climate Hazard Atlas](https://imdpune.gov.in/hazardatlas/index.html) | 1. Select the hazard type and geographic region. 2. Identify the state, district or map cell containing the project. 3. Download the available map, report or layer. 4. Record hazard type, time period, unit, classification and map resolution. 5. If only a map image or PDF is available, preserve it and manually record the project’s intersecting region. 6. Do not present historical hazard frequency as a current warning. 7. Save source layers/reports under `backend/data/raw/imd_hazard_atlas/` and derived project intersections under `backend/data/processed/climate/`. |
| IMD geospatial services | [IMD geospatial services](http://imdgeospatial.imd.gov.in/) | 1. Open the service and identify available map services or downloadable layers. 2. Check whether a WMS, WFS, GeoJSON, KML or raster download is provided. 3. Save the service URL and layer name. 4. Download only according to the published access method. 5. Convert project and layer data to WGS84 / EPSG:4326 when necessary. 6. Intersect the project point or boundary with the weather/hazard layer. 7. Store the layer date, coordinate system and processing method. |
| Open-Meteo public weather API | [Open-Meteo](https://open-meteo.com/) · [API documentation](https://open-meteo.com/en/docs) | 1. Obtain the project latitude and longitude. 2. Use the forecast endpoint with `latitude`, `longitude`, `current`, `hourly` or `daily` parameters. 3. Request current temperature, precipitation, wind speed and weather code. 4. Save the complete JSON response, not only selected values. 5. Record the API request URL, timezone, response time and observation time. 6. Store it as a public weather snapshot. 7. Use IMD for official Indian warnings; Open-Meteo should supplement operational weather context, not replace an official warning. |
| ISRO/NRSC Bhuvan | [Bhuvan](https://bhuvan.nrsc.gov.in/) | 1. Open the map and choose the relevant administrative, land-use, terrain, infrastructure or hazard layer. 2. Search or navigate to the project district and corridor. 3. Check whether the layer offers download, KML, WMS, WFS, GeoJSON or shapefile access. 4. Download the original layer where permitted. 5. Record layer name, date, source organization, coordinate system and resolution. 6. Convert to WGS84 / EPSG:4326 if needed. 7. Intersect the project point or polygon with land-use, terrain, water, forest or hazard features. 8. Save originals under `backend/data/raw/bhuvan/` and derived results under `backend/data/processed/locations/` or `climate/`. 9. A project-level point is not a parcel boundary; label its accuracy honestly. |
| National Database for Emergency Management (NDEM) | [NDEM](https://ndem.nrsc.gov.in/) | 1. Open the public disaster map and identify the relevant state/district. 2. Review flood, cyclone, landslide, fire and other disaster layers or published situation products. 3. Download linked PDF maps or available GIS products. 4. Record event type, affected area, issue time, source image date and geographic coverage. 5. Intersect the event footprint with the project coordinate or boundary. 6. Save original PDFs/maps under `backend/data/raw/ndem/`. 7. Save derived event records under `backend/data/processed/climate/`. 8. Some NDEM information is intended for authorized users; request access for restricted layers rather than bypassing the portal. |
| PARIVESH 2.0 | [PARIVESH](https://parivesh.nic.in/) · [Track your proposal](https://parivesh.nic.in/newupgrade/#/trackYourProposal/V1) · [Public land bank](https://parivesh.nic.in/admin/#/public/landbank?isPublic=true) · [Know Your Approval](https://parivesh.nic.in/kya/#/) | 1. Open Search, Track Your Proposal or Know Your Approval. 2. Search using project name, proposal number, state, district, applicant or sector. 3. Open the matching environmental, forest, wildlife or CRZ proposal. 4. Record proposal number, project name, authority, location, category, submission date, current stage, decision date and attached documents. 5. Download approval letters, meeting minutes, compliance reports and conditions. 6. Match the proposal to the BhoomiDrishti project using authority reference plus location; package names may differ. 7. Save HTML/PDF evidence under `backend/data/raw/parivesh/`. 8. Label a value `official` only when it comes directly from the proposal record or signed order. |
| Environment Clearance legacy portal | [Environment Clearance portal](https://environmentclearance.nic.in/) · [Track proposal](https://environmentclearance.nic.in/searchproposal.aspx) · [Monitoring reports](https://environmentclearance.nic.in/Monitoring_Report_Home.aspx) · [Compliance reports](https://environmentclearance.nic.in/Online_EC_Complience_Report.aspx) | 1. Open Track Proposal or Online Search. 2. Search by proposal number, project name, state, district, sector or approval type. 3. Open the proposal history and record every status transition with its date. 4. Download environmental clearance orders, EIA documents, minutes and compliance reports. 5. Extract approval type, status, conditions, validity, compliance date and responsible authority. 6. Preserve the original PDF and page references. 7. Store normalized values in the approvals table and document evidence in source snapshots. |
| eCourts main portal | [eCourts](https://ecourts.gov.in/) · [High Court Services](https://hcservices.ecourts.gov.in/) · [District Court Services](https://services.ecourts.gov.in/) · [Judgments](https://judgments.ecourts.gov.in/) | 1. Identify the state, district, court and parties connected to the land-acquisition dispute. 2. Search using CNR, case number, party name, advocate name or filing year. 3. Open the case record and record CNR, case type, parties, filing date, next hearing, current status and disposal status. 4. Download orders or judgments where available. 5. Match the case to the project using land village, survey number, authority, party and project reference. 6. Save case pages and orders under `backend/data/raw/ecourts/`. 7. CAPTCHA and access restrictions may prevent reliable automation; do not bypass them. 8. For a public dashboard, store case reference and source link rather than personal details not needed for risk analysis. |
| eCourts District Case Status | [District Court Services](https://services.ecourts.gov.in/) | 1. Choose Case Status if the CNR is not known. 2. Select state, district, court complex and search type. 3. Search by registration number, party name, advocate or filing year. 4. Complete CAPTCHA manually when requested. 5. Record CNR, case status, next hearing date, case stage and order links. 6. Download the latest order and record its date. 7. Store a manually verified case reference in the legal table. 8. Do not build an unattended CAPTCHA bypass. |
| India Code laws and rules | [India Code](https://www.indiacode.gov.in/) | 1. Search the Act or rule name, such as the Right to Fair Compensation and Transparency in Land Acquisition, Rehabilitation and Resettlement Act. 2. Open the current Act, rules or amendment. 3. Record title, section, effective date and amendment date. 4. Download the official PDF or preserve the HTML link. 5. Use this source for legal rules and obligations, not for the current status of an individual project dispute. 6. Save legal reference documents under `backend/data/raw/india_code/`. |
| CPGRAMS public grievances | [CPGRAMS](https://pgportal.gov.in/) | 1. Use the public grievance search or dashboard where available. 2. Filter by department, state, subject and time period. 3. Record only aggregated or authorized project-relevant information. 4. Do not collect personal complainant details unless legally authorized and necessary. 5. Save public reports or exports with their date and filters. 6. Map a grievance to a project only when project name, department and location provide a reliable match. 7. If the portal requires login or does not expose a dataset, request an authorized departmental report. |
| Central Public Procurement Portal | [CPPP/eProcure](https://eprocure.gov.in/eprocure/app) | 1. Search by department, organization, tender ID, project name, state or district. 2. Open the tender and record tender reference, work description, issuing authority, dates, estimated value, contractor/award status and corrigenda. 3. Download NIT, tender schedules, award notices and contract documents. 4. Link the tender to the project using authority reference and package number. 5. Save originals under `backend/data/raw/eprocure/`. 6. Do not treat a tender publication as proof that land acquisition or construction has started. |
| State revenue and land-record portals | State-specific portal; search [India.gov state services](https://www.india.gov.in/) or the relevant state government website | 1. Identify the state, district, tehsil, village and survey/khasra number. 2. Open the official Bhulekh, revenue, registration or GIS portal for that state. 3. Search by district, tehsil, village and survey number. 4. Download the available Record of Rights, mutation, parcel map, acquisition notice or land-use record. 5. Record the document number, issue date, parcel identifier, area, owner category if legally permitted and acquisition status. 6. Do not publish personal ownership data without authorization. 7. Save documents under `backend/data/raw/state_portals/<state>/`. 8. Request official bulk GIS/CSV exports where the portal does not permit automated downloads. |
| District Collector and Land Acquisition Officer records | [National Portal of India](https://www.india.gov.in/) for department discovery; relevant state/district websites | 1. Search the district website for `land acquisition`, `CALA`, `award`, `Section 3D`, `Section 3G`, `compensation`, `R&R`, `public notice` and the project name. 2. Check notices, award lists, hearing notices, village-wise annexures and progress reports. 3. Contact the Collector/LAO if the record is not public and request an official CSV, Excel export or signed report. 4. Extract eligible families, award amount, amount paid, pending cases, award date, possession date and village. 5. Verify totals against the source document and record page/annexure numbers. 6. Save PDFs/XLS under `backend/data/raw/district_documents/`. 7. These records are usually the most important manual input for compensation and acquisition coverage. |
| R&R and social-impact records | [MoRD](https://rural.gov.in/) · [National Portal of India](https://www.india.gov.in/) · relevant state social welfare/R&R department | 1. Search the state or district website for `rehabilitation`, `resettlement`, `R&R`, `social impact assessment`, `affected families`, `grievance` and the project name. 2. Download SIA reports, R&R plans, village-wise lists and monitoring reports. 3. Request an official spreadsheet from the R&R office if current progress is not publicly posted. 4. Extract affected families, eligible families, houses/assets, rehabilitation completed, relocation completed, resettlement sites, grievances and resolution dates. 5. Verify that percentages have a stated denominator. 6. Store the original report and normalized CSV under `backend/data/raw/district_documents/` and `backend/data/processed/social_impact/`. |
| Public project satellite/change monitoring | [Bhuvan](https://bhuvan.nrsc.gov.in/) · [Sentinel Hub](https://www.sentinel-hub.com/) · [Copernicus Data Space](https://dataspace.copernicus.eu/) | 1. Obtain a verified project boundary or corridor polygon first. 2. Select imagery dates before and after the monitoring period. 3. Download or request imagery according to the provider’s terms. 4. Compare land cover, construction footprint, waterlogging, vegetation loss or access changes. 5. Record image date, cloud cover, processing method and analyst confidence. 6. Save imagery metadata and derived GIS layers, not only screenshots. 7. Satellite evidence can indicate physical change but cannot prove compensation payment, legal resolution or R&R completion. |

## Format-specific extraction procedure

### API or JSON

1. Save the full response exactly as received.
2. Save the request URL without exposing API keys.
3. Record HTTP status, retrieval time, pagination and response schema.
4. Check units, timezone and observation timestamp.
5. Normalize into CSV or database rows.
6. Keep the raw JSON for audit.

Suggested files:

```text
backend/data/raw/<source>/<source>_YYYY-MM-DDTHH-mm-ssZ.json
backend/data/processed/<category>/<source>_YYYY-MM-DD.csv
```

### CSV, XLS or XLSX

1. Download the original file.
2. Never edit the original.
3. Check sheet name, header row, encoding, date format, units and merged cells.
4. Copy only the required columns into a normalized CSV.
5. Preserve the original row number as `source_row_number`.
6. Validate duplicate project IDs and totals.
7. Save the normalized file using UTF-8 CSV.

### PDF

1. Save the original PDF.
2. Record URL, title, publication date and page count.
3. Search extracted text for project name, package, village, `award`, `compensation`, `possession`, `R&R`, `court`, `approval` and `status`.
4. For scanned PDFs, run OCR.
5. Manually compare extracted values against the PDF page.
6. Record `source_page`, `source_table` and verifier name.
7. Use `verified_manual` only after checking the document.

### HTML portal

1. Record the page URL and retrieval time.
2. Save a PDF or permitted HTML export if available.
3. Record search filters used.
4. Capture the result identifier and status history.
5. Do not rely on a search result without saving the underlying document or reference.

### GIS, KML, GeoJSON, shapefile and GeoTIFF

1. Preserve the original layer and metadata.
2. Record coordinate reference system, date, resolution and source organization.
3. Convert to WGS84 / EPSG:4326 for web map use where appropriate.
4. Use GeoJSON for project points and small boundaries.
5. Use GeoPackage or PostGIS-compatible storage for large layers.
6. Use GeoTIFF for raster hazard and satellite data.
7. Record the spatial operation used to associate the layer with a project.

## File handover checklist

Every team member should return:

| Item | Required |
| --- | --- |
| Original file or complete API response | Yes |
| Source URL and direct document/API URL | Yes |
| Retrieval timestamp | Yes |
| Publication timestamp if available | Yes |
| Project/authority reference number | Yes |
| Normalized CSV or JSON | Yes |
| Page number, row number or API field path | Yes for extracted values |
| Units and coordinate system | Yes where applicable |
| Matching confidence | Yes |
| Missing-value explanation | Yes |
| Personal/sensitive data removed where required | Yes |

## What must not be done

- Do not bypass CAPTCHA, login, robots restrictions or access controls.
- Do not use a search-engine snippet as an official dataset.
- Do not treat a project name alone as proof that two records refer to the same project.
- Do not convert a district weather warning into a project-specific warning without spatial matching.
- Do not publish personal landowner, beneficiary or complainant information without authorization.
- Do not replace missing official metrics with synthetic values.
- Do not call a public snapshot fully real-time unless its publication and retrieval age are documented.

## Recommended shared handover structure

```text
source_handover/
  source_name/
    raw/
    processed/
    documents/
    manifest.csv
```

Recommended `manifest.csv` columns:

```csv
project_id,source_name,source_url,direct_file_url,source_format,publication_date,retrieved_at,official_reference,processed_file,verification_status,source_page_or_row,notes
```
