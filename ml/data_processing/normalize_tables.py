"""Source-specific table adapters with structural checks; recipes remain auditable."""
import re
from collections import defaultdict
from common import *

def ganga():
    observations=[]; issues=[]
    baseline_path=next(project_dir('REAL_002').glob('*/G002_extracted.json'),None)
    if baseline_path is None: return [],[dict(source_id='G002',reason='reviewed_district_label_baseline_missing')]
    baseline=read_json(baseline_path)['cells']; district_labels={}
    for cell in baseline:
        if cell.get('column')==1 and cell['value_original'].isdigit() and 1<=int(cell['value_original'])<=12:
            label=next((x['value_original'] for x in baseline if x.get('table')==cell.get('table') and x.get('row')==cell.get('row') and x.get('column')==2),None)
            district_labels[int(cell['value_original'])]=label
    names=['Meerut','Hapur','Bulandshahar','Amroha','Sambhal','Badaun','Shahjahanpur','Hardoi','Unnao','Rae Bareli','Pratapgarh','Prayagraj','Total']
    # Mapping reviewed against original PDF G002 page 1, including numbered columns.
    columns={3:('affected_villages_count','count'),4:('land_required_ha','ha'),5:('land_to_be_purchased_ha','ha'),8:('land_to_be_resumed_ha','ha'),11:('sale_deeds_count','count'),12:('land_purchased_ha','ha'),17:('farmers_count','count'),18:('land_resumed_exchanged_ha','ha'),19:('purchase_progress_pct','%'),20:('land_acquired_ha','ha'),21:('acquisition_progress_pct','%'),22:('land_purchase_remaining_ha','ha')}
    for path in sorted(project_dir('REAL_002').glob('*/G*_extracted.json')):
        sid=path.name.split('_')[0]; ex=read_json(path); tables=defaultdict(dict)
        for cell in ex['cells']:
            tables[(cell.get('table'),cell.get('row'))][cell.get('column')]=cell
        date=re.search(r'Updated till\s+(\d{2}-\d{2}-\d{4})',ex['pages'][0]['text']) if ex['pages'] else None
        if not date:
            if sid!='G001': issues.append(dict(source_id=sid,reason='no_unambiguous_asof_date_or_adapter_not_applicable'))
            continue
        rows=[]
        for (table,row),cols in tables.items():
            serial=cols.get(1,{}).get('value_original','')
            if (serial.isdigit() and 1<=int(serial)<=12 and cols.get(2,{}).get('value_original','') not in ('','2')) or (len(cols)==22 and cols.get(2,{}).get('value_original','')==''):
                rows.append((table,row,cols))
        # Require exact district sequence; do not apply positional schema to a changed layout.
        data_rows=[r for r in rows if r[2].get(1,{}).get('value_original','').isdigit()]
        if [r[2][1]['value_original'] for r in data_rows]!=[str(i) for i in range(1,13)]:
            issues.append(dict(source_id=sid,reason='district_table_layout_requires_review')); continue
        for table,row,cols in data_rows:
            idx=int(cols[1]['value_original'])-1; district=names[idx]
            if cols[2]['value_original']!=district_labels.get(idx+1):
                issues.append(dict(source_id=sid,row=row,district=district,reason='district_label_differs_from_reviewed_baseline')); continue
            try:
                nums={c:float(cols[c]['value_original']) for c in [4,5,8,12,18,19,20,21,22]}
                checks=[abs(nums[4]-nums[5]-nums[8])<0.02,abs(nums[12]+nums[18]-nums[20])<0.02,abs(nums[5]-nums[12]-nums[22])<0.02,nums[5]>0,nums[4]>0]
                checks += [abs(nums[12]/nums[5]*100-nums[19])<0.06,abs(nums[20]/nums[4]*100-nums[21])<0.06]
                if not all(checks): raise ValueError('land_accounting_or_percentage_inconsistency')
            except (KeyError,ValueError,ZeroDivisionError) as exc:
                issues.append(dict(source_id=sid,row=row,district=district,reason=str(exc))); continue
            for col,(field,unit) in columns.items():
                if col not in cols: continue
                cell=cols[col]; value=cell['value_original']
                if not value.strip(): continue
                observations.append(dict(project_id='REAL_002',source_id=sid,entity_id='REAL_002/DISTRICT/'+safe(district),parent_entity_id='REAL_002',record_scope='district',district=district,district_original=cols[2]['value_original'],state='Uttar Pradesh',field=field,value_original=value,unit_original=unit,source_reference=cell['reference']+'; source printed column '+str(col),pdf_page=1,source_cell=dict(table=table,row=row,column=col),anchor=value,observation_date_original=date.group(1),day_first_explicit=True,measurement_type='reported_actual' if col in (11,12,17,18,19,20,21) else 'reported_requirement_or_remaining',land_tenure='purchase_plus_resumption' if col in (4,20,21) else 'as_defined_in_source_column',topic='02_state_district_land_acquisition',notes='Numbered Hindi table column mapping visually reviewed on G002. Same-layout rows require district sequence and area/percentage identities. Reported percentages retained; no imposed denominator.'))
    return observations,issues

def rainfall():
    paths=list((ROOT/'project_research').glob('*/*/S037_extracted.json'))
    if not paths:return [],[]
    ex=read_json(paths[0]); rows=[]; issues=[]
    mapping={'DAUSA':('REAL_001','Rajasthan'),'MEERUT':('REAL_002','Uttar Pradesh'),'RUDRAPRAYAG':('REAL_003','Uttarakhand'),'MUMBAI CITY':('REAL_004','Maharashtra'),'MUMBAI SUBURBAN':('REAL_004','Maharashtra'),'NEW DELHI':('REAL_005','Delhi'),'CHENNAI':('REAL_006','Tamil Nadu'),'GANDERBAL':('REAL_008','Jammu & Kashmir'),'NAGPUR':('REAL_009','Maharashtra'),'PRAYAGRAJ':('REAL_010','Uttar Pradesh')}
    for p in ex['pages']:
        stamp=re.search(r'DAY:\s*(\d{2}-\d{2}-\d{4})\s+PERIOD:\s*(\d{2}-\d{2}-\d{4})\s+to\s+(\d{2}-\d{2}-\d{4})',p['text'])
        if not stamp: continue
        for line_no,line in enumerate(p['text'].splitlines(),1):
            for district,(pid,state) in mapping.items():
                match=re.fullmatch(r'\s*\d+\s+'+district+r'\s+([\d.]+)\s+([\d.]+)\s+(-?\d+)%\s+(\w+)\s+([\d.]+)\s+([\d.]+)\s+(-?\d+)%\s+(\w+)\s*',line)
                if not match: continue
                vals=match.groups()
                for field,index,unit,period in [('rainfall_mm',0,'mm','daily'),('rainfall_normal_mm',1,'mm','daily'),('rainfall_category',3,'text','daily'),('rainfall_mm',4,'mm','cumulative'),('rainfall_normal_mm',5,'mm','cumulative'),('rainfall_category',7,'text','cumulative')]:
                    rows.append(dict(project_id=pid,source_id='S037',entity_id=pid+'/CLIMATE/'+safe(district),parent_entity_id=pid,record_scope='district_climate',district=district,state=state,accuracy_level='district',field=field,value_original=vals[index],unit_original=unit,source_reference=f'PDF page {p["page"]}; text row {line_no}; district {district}; {period} {field}',pdf_page=p['page'],anchor=line.strip(),observation_date_original=stamp.group(1),day_first_explicit=True,observation_period=stamp.group(1) if period=='daily' else stamp.group(2)+' to '+stamp.group(3),measurement_type=period,topic='07_climate_landscape',notes='District context only; no route intersection or coordinates inferred. Current 2026 observation must not be joined to earlier targets. Category codes retained as printed.'))
    return rows,issues
def main():
    rows,issues=ganga(); climate,ci=rainfall()
    write_json(CONFIG/'table_observations.json',rows+climate)
    write_json(ROOT/'data_processing/logs/table_adapter_issues.json',issues+ci)
    print(len(rows),'Ganga observations;',len(climate),'climate observations;',len(issues),'review items')
if __name__=='__main__':main()
