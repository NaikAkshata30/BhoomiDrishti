# Data schema

master_dataset/normalized_observations.csv and .json are long-form source observations. A row contains project_id, optional related_project_id, entity_id, parent_entity_id, record_scope, geography/phase/package, field, value_original, unit_original, value_normalized, unit, measurement_type, land_tenure, observation_date_original, observation_date, observation_period, date_precision, source_id, source_sha256, source_reference, retrieved_at, verification_status, identity_status, confidence, conflict_flag and ml_eligible.

project_registry describes the user's ten requested research targets; it is not independent official evidence. entity_registry contains local identifiers for scoped records; these local IDs are never official package numbers. data_dictionary describes requested and observed fields. A field absent from observations remains missing, as enumerated in missing_data_report.

Land area is normalized to hectares only from explicit units (m2 * 0.0001, acres * 0.40468564224). INR lakh * 100000, INR crore * 10000000. Do not guess units. Dates retain original tokens and precision. An ambiguous date or year/month without a day is not silently made into a full date. Document dates, observation dates, upload dates and retrieval times differ.

Percent denominators are source-specific. Ganga purchase progress uses purchased / proposed purchase area. Its total acquisition percentage uses purchased plus resumed/exchanged area / proposed alignment area. Preserve reported percentages. Never apply one universal acquisition formula to all source records. No percent is derived with missing/zero denominator or mixed scope/time.

CSV is UTF-8 with BOM; missing values are empty cells. JSON preserves null and numeric types. Generic table cells are candidate evidence only. Page references are physical PDF pages, not printed folio numbers. API extraction support exists but this collection makes no claim to have downloaded any API payload.
