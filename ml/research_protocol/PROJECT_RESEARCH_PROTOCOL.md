# BhoomiDrishti research protocol

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
