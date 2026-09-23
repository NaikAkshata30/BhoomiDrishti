"""Convert source-anchored reviewed recipes into auditable long-form observations."""
from common import *
from normalizers.values import normalize_number,normalize_date
from validators.rules import validate_fact,conflicts
def main():
    metas={read_json(p)['source_id']:(read_json(p),p) for p in (ROOT/'project_research').glob('*/*/*_metadata.json')}
    recipes=read_json(CONFIG/'reviewed_observations.json',[])+read_json(CONFIG/'table_observations.json',[]); rows=[]; rejected=[]
    for idx,f in enumerate(recipes,1):
        sid=f['source_id']
        if sid not in metas: rejected.append({**f,'reason':'source_not_found'}); continue
        m,path=metas[sid]; ex=read_json(path.with_name(sid+'_extracted.json'),{})
        page=f.get('pdf_page')
        evidence='\n'.join(p['text'] for p in ex.get('pages',[]) if page is None or p['page']==page)
        if f.get('source_cell'):
            c=f['source_cell']
            evidence='\n'.join(str(x['value_original']) for x in ex.get('cells',[]) if x.get('page')==page and all(x.get(k)==v for k,v in c.items()))
        errors=validate_fact(f,m,evidence)
        if errors: rejected.append({**f,'reason':';'.join(errors)}); continue
        try:
            if f.get('unit_original')=='text': value,unit,method=f['value_original'],'text','verbatim_category'
            else: value,unit,method=normalize_number(f['value_original'],f['unit_original'])
        except ValueError as exc: rejected.append({**f,'reason':str(exc)}); continue
        observation_date,precision=normalize_date(f.get('observation_date_original'),f.get('day_first_explicit',False))
        r={**f,'observation_id':f'OBS_{idx:05}','value_normalized':value,'unit':unit,'normalization_method':method,'observation_date':observation_date,'date_precision':precision,'source_sha256':m['sha256'],'source_url':m['url'],'local_file':m['local_file'],'retrieved_at':m['retrieved_at'],'verification_status':'official','identity_status':'matched_source_context','confidence':f.get('confidence',0.9),'confidence_basis':'heuristic evidence review; not a calibrated probability','conflict_flag':False,'ml_eligible':False,'ml_exclusion_reason':'Requires dated feature assembly, outcome labels and leakage review before training.','provenance_status':'anchor_checked_against_downloaded_raw_extraction'}
        if precision=='review_required': r['verification_status']='review_required'
        rows.append(r)
    disputed=conflicts(rows)
    write_json(MASTER/'normalized_observations.json',rows)
    fields=['observation_id','project_id','related_project_id','entity_id','parent_entity_id','record_scope','phase','corridor','package_number','state','district','tehsil','village','chainage_start','chainage_end','notification_number','proposal_number','case_number','field','value_original','unit_original','value_normalized','unit','measurement_type','land_tenure','observation_date_original','observation_date','observation_period','date_precision','source_id','source_sha256','source_url','local_file','retrieved_at','source_reference','pdf_page','anchor','normalization_method','verification_status','identity_status','confidence','confidence_basis','conflict_flag','ml_eligible','ml_exclusion_reason','notes']
    fields += ['package_name_as_source','district_original','accuracy_level','source_cell','provenance_status']
    write_csv(MASTER/'normalized_observations.csv',rows,fields)
    write_csv(MASTER/'conflicting_sources.csv',disputed,['project_id','entity_id','field','source_ids','values','reason','resolution'])
    write_json(ROOT/'data_processing/logs/rejected_observations.json',rejected)
    for pid in PROJECTS:
        subset=[r for r in rows if r['project_id']==pid or r.get('related_project_id')==pid]
        topics=read_json(CONFIG/'topics.json')
        for topic in topics:
            selected=[r for r in subset if r.get('topic','09_validation')==topic]
            if selected:
                write_csv(project_dir(pid)/topic/(pid+'_normalized.csv'),selected,fields)
                write_json(project_dir(pid)/topic/(pid+'_normalized.json'),selected)
    print(len(rows),'normalized observations;',len(rejected),'rejected;',len(disputed),'conflicts')
if __name__=='__main__': main()
