# Reproduce or extend this collection

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
