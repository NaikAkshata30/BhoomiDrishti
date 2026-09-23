"""Download configured official sources; reruns reuse verified raw bytes."""
import argparse, concurrent.futures, json, mimetypes, threading
from urllib.parse import urlparse
from common import *
from collectors.public_http import fetch
persist_lock=threading.Lock()

def collect(seed):
    dest=project_dir(seed['project_id'])/seed['topic']
    record=dest/(seed['source_id']+'_metadata.json')
    old=read_json(record,{})
    if old.get('download_status')=='downloaded' and (ROOT/old['local_file']).exists():
        if sha((ROOT/old['local_file']).read_bytes())==old['sha256']: return old
        raise RuntimeError('Existing raw file checksum mismatch: '+old['local_file'])
    row={**seed,'retrieved_at':utc(),'download_status':'failed','verification_status':'review_required','sha256':None,'local_file':None,'publication_date':seed.get('publication_date'),'document_date':seed.get('document_date'),'fields_extracted':[]}
    try:
        if not seed.get('refresh',False):
            for candidate in (ROOT/'project_research').glob('*/*/*_metadata.json'):
                prior=read_json(candidate)
                if prior.get('url')==seed['url'] and prior.get('download_status')=='downloaded' and (ROOT/prior['local_file']).exists() and sha((ROOT/prior['local_file']).read_bytes())==prior['sha256']:
                    reused={**prior,**seed,'canonical_source_id':prior.get('canonical_source_id',prior['source_id']),'download_status':'downloaded','reused_existing_raw':True}
                    write_json(record,reused); return reused
        body,meta=fetch(seed['url']); row.update(meta)
        format='pdf' if body.startswith(b'%PDF-') else ('html' if 'html' in meta['content_type'] else seed.get('format','bin'))
        if seed.get('format')=='pdf' and format!='pdf': raise RuntimeError('expected_pdf_received_'+format)
        digest=sha(body)
        filename=f"{seed['project_id']}_{safe(seed['authority'])}_{safe(seed['label'])}_{seed.get('document_date') or seed.get('publication_date') or 'undated'}_{digest[:12]}.{format}"
        path=dest/filename
        with persist_lock:
            for candidate in (ROOT/'project_research').glob('*/*/*_metadata.json'):
                prior=read_json(candidate)
                if prior.get('sha256')==digest and prior.get('local_file') and (ROOT/prior['local_file']).exists():
                    path=ROOT/prior['local_file']; row['canonical_source_id']=prior.get('canonical_source_id',prior['source_id']); break
            if not path.exists(): path.write_bytes(body)
        row.update(download_status='downloaded',sha256=digest,local_file=relative(path),source_format=format,bytes=len(body),verification_status='official',identity_status='review_required',confidence=None)
    except Exception as exc: row['error']=f'{type(exc).__name__}: {exc}'[:1000]
    write_json(record,row)
    print(seed['source_id'],row['download_status'],row.get('bytes',''),row.get('error',''),flush=True)
    return row
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--ids',nargs='*'); args=ap.parse_args()
    seeds=read_json(CONFIG/'sources.json',[])
    if args.ids: seeds=[s for s in seeds if s['source_id'] in args.ids]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: list(pool.map(collect,seeds))
if __name__=='__main__': main()
