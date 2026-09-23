# BhoomiDrishti collection summary

Generated: 2026-09-05T10:56:34+00:00

## Delivered collection

- 10 user-specified projects configured with aliases and identity rules.
- 81 attempted source URLs; 75 successful downloads; 6 failed.
- 75 unique SHA256 hashes; 193.3 MiB of canonical downloaded evidence.
- 2454 extracted PDF pages/HTML documents and 50126 candidate table cells.
- 4711 source-anchored normalized observations; 46 scoped entities.
- 384 review queue entries (including page-level issues and unattempted specialist portal searches).

## Project coverage

| Project | Raw sources | Normalized observations |
|---|---:|---:|
| REAL_001 — Delhi-Mumbai Expressway | 8 | 9 |
| REAL_002 — Ganga Expressway | 42 | 4602 |
| REAL_003 — Char Dham Highway Project | 4 | 11 |
| REAL_004 — Mumbai Metro Line 3 | 2 | 15 |
| REAL_005 — Delhi Metro Phase IV | 4 | 14 |
| REAL_006 — Chennai Metro Rail Project | 3 | 18 |
| REAL_007 — Bharatmala Pariyojana | 2 | 11 |
| REAL_008 — Zojila Tunnel Project | 5 | 14 |
| REAL_009 — Mumbai-Nagpur Expressway | 3 | 8 |
| REAL_010 — Eastern Dedicated Freight Corridor | 2 | 9 |

## Important limits

This is an evidence collection, not a training-ready dataset. No acquisition-risk targets, zero-filled missing values, fabricated coordinates or model changes were made. Current 2026 rainfall must not be used to predict outcomes before its observation period. Plans, forecasts, actual progress and programme totals stay separate. Source age alone does not make a historical observation invalid; it does mean it cannot be asserted as current status.

Most numeric land observations come from historical Ganga district reports. District records from the same expressway are correlated; they are not independent project samples. A document download, extracted page or table cell is not a validated feature row. Rows with changed layouts or failed area checks are held for review. Compensation expenditure/proposed-payment figures are not automatically treated as paid compensation. Scanned rate-approval annexures and poorly encoded text need further review. Legal case coverage, village/parcel notifications, outcome dates, route geometry and historical district weather remain incomplete. See the missing and manual-review reports for exact gaps.

JICA disclosures are official lender-hosted project evidence, explicitly distinguished from Indian implementing-agency hosting. Failed implementing-agency downloads are retained in the manifest. No login, CAPTCHA or TLS checks were bypassed. No API downloads, shapefiles or GeoJSON are claimed in this pass.

## Files and reproducibility

The supplied ML tree is preserved. Each project uses the ten supplied topic folders and manifest.csv. Raw PDFs/HTML, source metadata, extracted JSON, page CSV and table-cell CSV remain side by side. Normalized domain observations are additionally saved into the corresponding topic folders. Shared IMD raw files live once under REAL_001/07_climate_landscape and are referenced by hash for other districts. Their storage location does not mean national or other-district climate belongs to Dausa.

`data_processing/README.md` explains reruns, extraction limits, adding sources and review recipes. `research_protocol/` defines the rules. `master_dataset/` contains the requested manifests and reports, normalized observations, and entity registry. `feature_engineering/` and `models/` are empty.

## Validation

Five offline test groups passed: units and missing values; date and denominator safeguards; evidence anchors and programme scope; conflict/time separation; and the delivered-file audit. Every successful raw download was rehashed. District labels are also required to match the reviewed Ganga table baseline.
