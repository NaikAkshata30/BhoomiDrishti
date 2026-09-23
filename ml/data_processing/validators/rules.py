"""Reject unsupported identities and quarantine incompatible/conflicting observations."""
import re
from collections import defaultdict
def compact(text): return re.sub(r'\s+',' ',str(text)).strip().casefold()
def validate_fact(fact,meta,evidence):
    errors=[]
    if meta.get('download_status')!='downloaded': errors.append('raw_not_downloaded')
    if not fact.get('entity_id') or not fact.get('record_scope'): errors.append('missing_entity_scope')
    if not fact.get('source_reference'): errors.append('missing_source_reference')
    if not fact.get('anchor') or compact(fact['anchor']) not in compact(evidence): errors.append('evidence_anchor_not_found')
    if fact.get('record_scope') in ('package','corridor','phase') and fact.get('entity_id')==fact.get('project_id'): errors.append('scope_requires_child_entity')
    if fact.get('project_id')=='REAL_007' and fact.get('record_scope')=='project': errors.append('bharatmala_is_programme')
    if fact.get('project_id')=='REAL_008' and 'z-morh' in compact(fact.get('entity_id','')) and not fact.get('related_project_id'): errors.append('z_morh_not_zojila')
    if fact.get('field') in ('delay_risk_label','target','risk_label'): errors.append('target_labels_forbidden')
    if fact.get('field','').startswith(('3A_','3D_')) and fact.get('project_id') in ('REAL_004','REAL_005','REAL_006','REAL_010') and not fact.get('legal_basis'): errors.append('NH_sections_not_assumed_for_metro_rail')
    return errors
def conflicts(rows):
    groups=defaultdict(list); result=[]
    for r in rows:
        key=tuple(str(r.get(k) or '') for k in ('entity_id','field','observation_date','observation_period','measurement_type','land_tenure','unit'))
        groups[key].append(r)
    for group in groups.values():
        if len({str(r['value_normalized']) for r in group})<=1: continue
        for r in group:
            r['conflict_flag']=True; r['ml_eligible']=False
        result.append(dict(entity_id=group[0]['entity_id'],project_id=group[0]['project_id'],field=group[0]['field'],source_ids=[r['source_id'] for r in group],values=[r['value_normalized'] for r in group],reason='different_values_same_scope_time_and_measurement_basis' if group[0].get('observation_date') or group[0].get('observation_period') else 'potential_conflict_date_unknown',resolution='retained_all_values_manual_review'))
    return result

