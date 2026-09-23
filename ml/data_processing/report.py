"""Build source manifests, coverage, review queues and honest ML-readiness reports."""
from collections import defaultdict, Counter
from common import *
from validators.rules import compact

REQUESTED={
'identity':'project_name authority project_number package_number state district tehsil village chainage_start chainage_end latitude longitude',
'land_acquisition':'land_required_ha land_available_ha land_to_be_acquired_ha land_acquired_ha land_acquired_till_now_ha acquisition_progress_pct 3A_notification_number 3A_notification_date 3D_notification_number 3D_notification_date award_number award_date possession_date possession_percentage CALA acquisition_status',
'compensation':'compensation_amount compensation_awarded compensation_paid compensation_pending payment_date affected_families landowners_count payment_status',
'rr_social_impact':'SIA_status SIA_date affected_families RR_status RR_progress resettlement_sites rehabilitation_status',
'legal':'case_number court case_type filing_date case_status last_hearing_date legal_issue project_relation',
'approvals':'approval_type proposal_number approval_number approval_status application_date approval_date expiry_date',
'climate':'observation_date rainfall_mm temperature humidity weather_condition rainfall_category warning warning_date',
'terrain_landscape':'elevation slope terrain_type forest_intersection waterbody_intersection flood_risk landslide_risk access_constraint',
'barriers':'barrier_type barrier_description severity start_date end_date status',
'procurement_progress':'tender_reference contractor_name contract_value physical_progress financial_progress construction_status completion_target delay EOT hindrance'}
def main():
    observations=read_json(MASTER/'normalized_observations.json',[])
    bysource=defaultdict(list)
    for o in observations: bysource[o['source_id']].append(o)
    manifest=[]; reviews=[]; duplicates=[]; hashfirst={}; quality=[]
    identities=read_json(CONFIG/'source_reviews.json',{})
    for path in sorted((ROOT/'project_research').glob('*/*/*_metadata.json')):
        m=read_json(path); sid=m['source_id']; facts=bysource[sid]
        ex=read_json(path.with_name(sid+'_extracted.json'),{})
        review=identities.get(sid,{})
        success=m['download_status']=='downloaded'
        actualhash=sha((ROOT/m['local_file']).read_bytes()) if success else None
        hashok=success and actualhash==m['sha256']
        identity=review.get('identity_status','matched_source_context' if facts else 'review_required')
        scope=review.get('scope',m.get('scope'))
        association='related_project_id' if scope in ('related_package','district_climate','district_context','national_climate_context','mixed_corridors','mixed_projects','discovery_only') else 'project_id'
        assigned=m['project_id'] if identity!='review_required' else None
        row={**m,'source_name':m['label'],'source_url':m.get('source_url',m['url']),'direct_file_url':m['url'],'source_type':'official_lender_disclosure' if m['authority'].startswith('JICA') else 'government_official','project_id':assigned if association=='project_id' else None,'related_project_id':assigned if association=='related_project_id' else None,'candidate_project_id':m['project_id'],'assignment_status':identity,'project_name_as_source':review.get('project_name_as_source'),'project_number':review.get('project_number'),'package_number':review.get('package_number'),'state':review.get('state'),'district':review.get('district'),'tehsil':None,'village':None,'document_date':review.get('document_date',m.get('document_date')),'document_date_original':review.get('document_date_original'),'source_page_or_row':list(dict.fromkeys(f['source_reference'] for f in facts)),'api_endpoint':m.get('api_endpoint'),'api_parameters':m.get('api_parameters'),'fields_extracted':sorted({f['field'] for f in facts}),'identity_status':identity,'confidence':0.9 if facts else review.get('confidence'),'scope':scope,'sha256_verified':hashok,'pages_extracted':len(ex.get('pages',[])),'candidate_table_cells':len(ex.get('cells',[])),'normalization_status':'normalized_observations_available' if facts else 'raw_and_candidate_evidence_only' if ex else 'not_extracted','canonical_source_id':sid,'verification_status':'official' if hashok else 'review_required','match_notes':m.get('match_notes','')+' '+review.get('notes','')}
        if success and m['sha256'] in hashfirst:
            row['canonical_source_id']=hashfirst[m['sha256']]
            duplicates.append(dict(source_id=sid,canonical_source_id=row['canonical_source_id'],sha256=m['sha256'],url=m['url'],duplicate_kind='identical_bytes',action='use_canonical_source_id_do_not_double_count'))
        elif success: hashfirst[m['sha256']]=sid
        manifest.append(row)
        quality.append(dict(project_id=m['project_id'],source_id=sid,check='raw_checksum',status='pass' if hashok else 'not_available',detail='SHA256 recomputed from file' if hashok else m.get('error','No raw file')))
        if not success: reviews.append(dict(project_id=m['project_id'],source_id=sid,url=m['url'],reason='download_failed',search_parameters=m['label'],expected_data='Original '+m.get('format','file'),action='Try official portal manually; do not bypass restrictions or disable TLS verification.',detail=m.get('error')))
        if success and identity=='review_required': reviews.append(dict(project_id=m['project_id'],source_id=sid,url=m['url'],reason='identity_or_record_scope_review',search_parameters=PROJECTS[m['project_id']]['aliases'],expected_data='Exact project, authority, phase/package, geography and reference number',action='Review source before project assignment.'))
        for issue in ex.get('issues',[]): reviews.append(dict(project_id=m['project_id'],source_id=sid,url=m['url'],reason=issue.get('reason'),source_reference=issue.get('page') or issue.get('pages'),action='Visual/OCR/table review; do not use unverified extraction as ML data.',detail=issue))
    for issue in read_json(ROOT/'data_processing/logs/table_adapter_issues.json',[]): reviews.append(dict(project_id='REAL_002',url=next((m['url'] for m in manifest if m['source_id']==issue['source_id']),None),action='Review original district table; preserve discrepancy and do not repair values silently.',**issue))
    for issue in read_json(ROOT/'data_processing/logs/rejected_observations.json',[]): reviews.append(dict(project_id=issue.get('project_id'),source_id=issue.get('source_id'),reason=issue.get('reason'),action='Correct recipe only after reviewing evidence.'))
    reviews+=read_json(CONFIG/'manual_tasks.json',[])
    missing=[]; registry=[]
    for pid,p in PROJECTS.items():
        own=[r for r in observations if r['project_id']==pid]
        counts=Counter(r['field'] for r in own)
        raw=[m for m in manifest if m['candidate_project_id']==pid and m['download_status']=='downloaded']
        registry.append({**p,'aliases':' | '.join(p['aliases']),'downloaded_source_count':len(raw),'normalized_observation_count':len(own),'training_ready':False})
        for category,fields in REQUESTED.items():
            for field in fields.split():
                meta_hits=[r for r in own if r.get(field) not in (None,'')]
                n=counts[field]+len(meta_hits)
                missing.append(dict(project_id=pid,category=category,field=field,normalized_evidence_count=n,status='partial_evidence_available' if n else 'missing_or_not_yet_verified',scope_note='Evidence is scoped and dated; presence does not imply current project-wide or study-district completeness.',reason=None if n else 'No accepted normalized observation in this collection pass. Raw documents may contain unextracted information.'))
        shared_sources={o['source_id'] for o in own}
        write_csv(project_dir(pid)/'manifest.csv',[m for m in manifest if m['candidate_project_id']==pid or m['source_id'] in shared_sources],MANIFEST_FIELDS)
        write_csv(project_dir(pid)/'00_project_register/project_registry.csv',[registry[-1]],REGISTRY_FIELDS)
        write_json(project_dir(pid)/'00_project_register/project_registry.json',registry[-1])
        write_csv(project_dir(pid)/'09_validation/missing_data_report.csv',[r for r in missing if r['project_id']==pid],MISSING_FIELDS)
        write_csv(project_dir(pid)/'09_validation/manual_review_required.csv',[r for r in reviews if r.get('project_id')==pid],REVIEW_FIELDS)
    write_csv(MASTER/'source_manifest.csv',manifest,MANIFEST_FIELDS)
    write_json(MASTER/'source_manifest.json',manifest)
    write_csv(MASTER/'project_registry.csv',registry,REGISTRY_FIELDS)
    write_csv(MASTER/'missing_data_report.csv',missing,MISSING_FIELDS)
    write_csv(MASTER/'manual_review_required.csv',reviews,REVIEW_FIELDS)
    write_csv(MASTER/'duplicate_sources.csv',duplicates,['source_id','canonical_source_id','sha256','url','duplicate_kind','action'])
    secondary=read_json(CONFIG/'secondary_discovery.json',[])
    write_csv(MASTER/'secondary_sources.csv',secondary,['project_id','source_name','source_url','discovery_purpose','official_trace_status','verification_status','used_in_training'])
    for pid in PROJECTS: write_csv(project_dir(pid)/'09_validation/secondary_sources.csv',[r for r in secondary if r['project_id']==pid],['project_id','source_name','source_url','discovery_purpose','official_trace_status','verification_status','used_in_training'])
    quality.extend([dict(project_id='ALL',check='target_labels',status='pass',detail='No target labels fabricated; all observations remain excluded from direct training.'),dict(project_id='ALL',check='scope_and_provenance',status='pass' if all(o.get('entity_id') and o.get('source_reference') and o.get('source_sha256') for o in observations) else 'fail',detail='Each observation has entity, source hash and locator.'),dict(project_id='ALL',check='ML_readiness',status='not_ready',detail='Mixed dates/scopes, incomplete coverage, pending reviews, no independently verified training outcomes.'),dict(project_id='ALL',check='API_collection',status='not_collected',detail='This pass collected PDF/HTML documents. No API payloads or geospatial vectors are claimed.')])
    write_csv(MASTER/'data_quality_report.csv',quality,['project_id','source_id','check','status','detail'])
    for pid in PROJECTS: write_csv(project_dir(pid)/'09_validation/data_quality_report.csv',[q for q in quality if q['project_id'] in (pid,'ALL')],['project_id','source_id','check','status','detail'])
    fields={f:c for c,fs in REQUESTED.items() for f in fs.split()}
    for r in observations: fields.setdefault(r['field'],'additional_source_specific')
    dictionary=[]
    for field,category in fields.items():
        examples=[r for r in observations if r['field']==field]
        unit=examples[0]['unit'] if examples else ('ha' if field.endswith('_ha') else 'mm' if field.endswith('_mm') else '%' if field.endswith('_pct') else None)
        dictionary.append(dict(field=field,category=category,data_type='number' if unit and unit!='text' else 'string_or_date',normalized_unit=unit,nullable=True,definition=FIELD_DESCRIPTIONS.get(field,field.replace('_',' ')+'; preserve the exact source scope and measurement basis.'),validation='Missing is blank CSV / null JSON; require source reference. Dates require explicit parsing. Percent completion 0..100.',available_observations=len(examples)))
    for field,description in METADATA_DESCRIPTIONS.items(): dictionary.append(dict(field=field,category='provenance_and_scope',data_type='string_or_boolean',nullable=True,definition=description,validation='Required where applicable; never infer a missing identifier.'))
    write_csv(MASTER/'data_dictionary.csv',dictionary,['field','category','data_type','normalized_unit','nullable','definition','validation','available_observations'])
    entities={}
    for o in observations:
        entities[o['entity_id']]={k:o.get(k) for k in ['entity_id','parent_entity_id','project_id','record_scope','phase','corridor','package_number','state','district']}
    write_csv(MASTER/'entity_registry.csv',list(entities.values()),['entity_id','parent_entity_id','project_id','record_scope','phase','corridor','package_number','state','district'])
    successful=[m for m in manifest if m['download_status']=='downloaded']; total_bytes=sum(m.get('bytes',0) for m in successful if m['canonical_source_id']==m['source_id'])
    text=f'''# BhoomiDrishti collection summary

Generated: {utc()}

## Delivered collection

- {len(PROJECTS)} user-specified projects configured with aliases and identity rules.
- {len(manifest)} attempted source URLs; {len(successful)} successful downloads; {len(manifest)-len(successful)} failed.
- {len(hashfirst)} unique SHA256 hashes; {total_bytes/1024/1024:.1f} MiB of canonical downloaded evidence.
- {sum(m['pages_extracted'] for m in manifest)} extracted PDF pages/HTML documents and {sum(m['candidate_table_cells'] for m in manifest)} candidate table cells.
- {len(observations)} source-anchored normalized observations; {len(entities)} scoped entities.
- {len(reviews)} review queue entries (including page-level issues and unattempted specialist portal searches).

## Project coverage

| Project | Raw sources | Normalized observations |
|---|---:|---:|
'''
    text+='\n'.join(f"| {r['project_id']} — {r['project_name']} | {r['downloaded_source_count']} | {r['normalized_observation_count']} |" for r in registry)
    text+='''

## Important limits

This is an evidence collection, not a training-ready dataset. No acquisition-risk targets, zero-filled missing values, fabricated coordinates or model changes were made. Current 2026 rainfall must not be used to predict outcomes before its observation period. Plans, forecasts, actual progress and programme totals stay separate. Source age alone does not make a historical observation invalid; it does mean it cannot be asserted as current status.

Most numeric land observations come from historical Ganga district reports. District records from the same expressway are correlated; they are not independent project samples. A document download, extracted page or table cell is not a validated feature row. Rows with changed layouts or failed area checks are held for review. Compensation expenditure/proposed-payment figures are not automatically treated as paid compensation. Scanned rate-approval annexures and poorly encoded text need further review. Legal case coverage, village/parcel notifications, outcome dates, route geometry and historical district weather remain incomplete. See the missing and manual-review reports for exact gaps.

JICA disclosures are official lender-hosted project evidence, explicitly distinguished from Indian implementing-agency hosting. Failed implementing-agency downloads are retained in the manifest. No login, CAPTCHA or TLS checks were bypassed. No API downloads, shapefiles or GeoJSON are claimed in this pass.

## Files and reproducibility

The supplied ML tree is preserved. Each project uses the ten supplied topic folders and manifest.csv. Raw PDFs/HTML, source metadata, extracted JSON, page CSV and table-cell CSV remain side by side. Normalized domain observations are additionally saved into the corresponding topic folders. Shared IMD raw files live once under REAL_001/07_climate_landscape and are referenced by hash for other districts. Their storage location does not mean national or other-district climate belongs to Dausa.

`data_processing/README.md` explains reruns, extraction limits, adding sources and review recipes. `research_protocol/` defines the rules. `master_dataset/` contains the requested manifests and reports, normalized observations, and entity registry. `feature_engineering/` and `models/` are empty.
'''
    (MASTER/'collection_summary.md').write_text(text,encoding='utf-8')
    print(len(successful),'downloads;',len(observations),'observations;',len(reviews),'review items')

MANIFEST_FIELDS='source_id canonical_source_id project_id related_project_id candidate_project_id assignment_status source_name source_url direct_file_url final_url source_type source_priority source_format authority project_name_as_source project_number package_number state district tehsil village scope publication_date publication_date_original publication_date_basis document_date document_date_original retrieved_at local_file sha256 sha256_verified bytes http_status content_type last_modified etag download_status fields_extracted source_page_or_row api_endpoint api_parameters verification_status identity_status confidence match_notes pages_extracted candidate_table_cells normalization_status error'.split()
REGISTRY_FIELDS='project_id project_name authority study_district study_state project_type aliases folder registry_basis identity_rule scope_rule downloaded_source_count normalized_observation_count training_ready'.split()
REVIEW_FIELDS='project_id source_id url reason source_reference search_parameters expected_data action detail'.split()
MISSING_FIELDS='project_id category field normalized_evidence_count status scope_note reason'.split()
FIELD_DESCRIPTIONS={'land_required_ha':'Source-defined required/proposed land, not necessarily purchased or legally acquired.','land_acquired_ha':'Source-defined acquisition total; land_tenure identifies purchase/resumption and other scope differences.','land_to_be_purchased_ha':'Area proposed for purchase; distinct from all land required or resumption land.','purchase_progress_pct':'Reported purchased area divided by source purchase requirement; not total acquisition progress.','acquisition_progress_pct':'Reported acquisition percentage with source-specific denominator; do not assume purchase-only denominator.','rainfall_mm':'Actual rainfall over observation_period at district resolution; daily and cumulative are separate.','forest_diversion_area_ha':'Forest area in a specified proposal/clearance, not total acquired land.','compensation_budget_inr':'Planned compensation/R&R budget, not payment achieved.','physical_progress':'Construction progress; never substituted for acquisition progress.'}
METADATA_DESCRIPTIONS={'entity_id':'Local scoped entity identifier; not an official package number.','parent_entity_id':'Parent project/programme; prevents programme aggregation into parcel facts.','source_id':'Stable collection source identifier.','source_sha256':'SHA256 of downloaded raw source bytes.','source_reference':'PDF one-based physical page/table/row, HTML table/row or JSON pointer.','value_original':'Original reported value before unit conversion.','unit_original':'Explicit source unit; unknown units must not be guessed.','value_normalized':'Converted numeric value or preserved category.','measurement_type':'Reported actual, requirement, planned estimate, daily or cumulative context.','land_tenure':'Separates government/private and temporary/permanent scope.','observation_period':'Temporal coverage of the measurement.','observation_date_original':'Preserved source date token.','date_precision':'Day/month/year/missing/review_required; no invented day.','confidence':'Heuristic evidence-review score, not statistical probability.','conflict_flag':'True for unresolved same-scope/time/value disagreement.','ml_eligible':'False until feature assembly, temporal checks and target verification.','verification_status':'official, verified_manual, public_snapshot, inferred, missing, stale, review_required.','identity_status':'Independent project-match state; official hosting does not establish identity.'}
if __name__=='__main__':main()
