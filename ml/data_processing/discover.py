"""Discover relevant Ganga downloads from the saved official index, respecting base href."""
import re
from common import *
def main():
    seeds=read_json(CONFIG/'sources.json',[]); known={s['url'] for s in seeds}
    path=project_dir('REAL_002')/'01_authority/S002_extracted.json'
    for link in read_json(path,{})['links']:
        label=link['context']
        if not re.search('Land Acquisition Details of Ganga Expressway|Progress Report of Ganga Expressway|proposed rates',label,re.I): continue
        if '.pdf' not in link['url'].lower() or link['url'] in known: continue
        date=re.search(r'\b(\d{2})-(\d{2})-(\d{4})\b',label)
        stamp='-'.join(reversed(date.groups())) if date else None
        sid=f'G{len([s for s in seeds if s["source_id"].startswith("G")])+1:03}'
        seeds.append(dict(source_id=sid,project_id='REAL_002',topic='03_compensation' if 'proposed rates' in label else '02_state_district_land_acquisition',authority='UPEIDA',label='ganga_progress' if 'Progress Report' in label else 'ganga_land_status',url=link['url'],source_url=next(s['url'] for s in seeds if s['source_id']=='S002'),format='pdf',scope='project_and_district',publication_date=stamp,publication_date_original=date.group(0) if date else None,publication_date_basis='official_index_upload_date',document_date=None,match_notes=label,source_priority=1,discovery_method='saved_official_HTML_download_link'))
        known.add(link['url'])
    write_json(CONFIG/'sources.json',seeds)
    print('Configured',len(seeds),'source URLs')
if __name__=='__main__': main()
