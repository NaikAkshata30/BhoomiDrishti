"""Extract from saved raw files without network or changes to raw bytes."""
import argparse
from common import *
from extractors.documents import extract
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--ids',nargs='*'); ap.add_argument('--force',action='store_true'); args=ap.parse_args()
    for meta in sorted((ROOT/'project_research').glob('*/*/*_metadata.json')):
        m=read_json(meta)
        if m.get('download_status')!='downloaded' or (args.ids and m['source_id'] not in args.ids): continue
        out=meta.with_name(m['source_id']+'_extracted.json')
        if out.exists() and not args.force: continue
        path=ROOT/m['local_file']
        if sha(path.read_bytes())!=m['sha256']: raise ValueError('raw_checksum_mismatch')
        print('Extracting',m['source_id'],flush=True)
        try:
            obj=extract(path,m['source_format'],m['url'])
            obj.update(source_id=m['source_id'],sha256=m['sha256'],extracted_at=utc(),status='candidate_evidence_not_ML_features')
            write_json(out,obj)
            write_csv(meta.with_name(m['source_id']+'_table_cells.csv'),[{**c,'source_id':m['source_id'],'source_sha256':m['sha256'],'verification_status':'review_required'} for c in obj['cells']],['source_id','source_sha256','page','table','row','column','value_original','reference','verification_status'])
            write_csv(meta.with_name(m['source_id']+'_pages.csv'),obj['pages'],['page','reference','text'])
            print('Extracted',m['source_id'],len(obj['pages']),'pages',len(obj['cells']),'cells',flush=True)
        except Exception as exc:
            write_json(out,dict(source_id=m['source_id'],sha256=m['sha256'],status='extraction_failed',issues=[{'reason':str(exc)}],pages=[],cells=[],links=[]))
if __name__=='__main__': main()

