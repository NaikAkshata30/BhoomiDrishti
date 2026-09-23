"""Evidence extraction. Extracted text/table cells are NOT accepted ML facts."""
import csv, io, json, re
from lxml import html
from urllib.parse import urljoin

KEYWORDS=re.compile(r'land|acqui|compens|resettle|rehabil|affected|rainfall|progress|hectare|clearance|litig|award|hindrance|terrain|flood|slope',re.I)
def extract(path,format,source_url):
    pages=[]; cells=[]; links=[]; issues=[]
    if format=='pdf':
        from pypdf import PdfReader
        reader=PdfReader(str(path))
        for i,p in enumerate(reader.pages,1):
            try: text=p.extract_text() or ''
            except Exception as exc: text=''; issues.append({'page':i,'reason':'text_extraction_error','detail':str(exc)[:300]})
            pages.append(dict(page=i,reference=f'PDF page {i}',text=text))
            if len(text.strip())<50: issues.append({'page':i,'reason':'scanned_or_sparse_page_needs_visual_review'})
        # Tables are intentionally bounded in a first pass; every skipped page is explicit.
        candidates=[p['page'] for p in pages if KEYWORDS.search(p['text'])]
        selected=list(range(1,len(pages)+1)) if len(pages)<=40 else candidates[:30]
        if len(pages)>40 and len(candidates)>30: issues.append({'reason':'table_extraction_remaining_pages','pages':candidates[30:]})
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            for page_no in selected:
                try:
                    for ti,table in enumerate(pdf.pages[page_no-1].extract_tables(),1):
                        for ri,row in enumerate(table,1):
                            for ci,value in enumerate(row,1):
                                if value is not None:
                                    cells.append(dict(page=page_no,table=ti,row=ri,column=ci,value_original=value,reference=f'PDF page {page_no}; detected table {ti}; row {ri}; column {ci}'))
                except Exception as exc: issues.append({'page':page_no,'reason':'table_extraction_error','detail':str(exc)[:300]})
    elif format=='html':
        doc=html.fromstring(path.read_bytes())
        bases=doc.xpath('//base/@href')
        link_base=urljoin(source_url,bases[0]) if bases else source_url
        for el in doc.xpath('//script|//style|//noscript'): el.drop_tree()
        lines=[re.sub(r'\s+',' ',t).strip() for t in doc.xpath('//text()')]
        lines=[t for t in lines if t]
        pages=[dict(page=None,reference='HTML text segments (DOM order)',text='\n'.join(lines))]
        for ti,table in enumerate(doc.xpath('//table'),1):
            for ri,row in enumerate(table.xpath('.//tr'),1):
                for ci,cell in enumerate(row.xpath('./td|./th'),1):
                    value=re.sub(r'\s+',' ',cell.text_content()).strip()
                    cells.append(dict(page=None,table=ti,row=ri,column=ci,value_original=value,reference=f'HTML table {ti}; row {ri}; column {ci}'))
        for a in doc.xpath('//a[@href]'):
            parent=a
            for anc in a.iterancestors():
                if anc.tag in ('tr','li','p'): parent=anc; break
            links.append(dict(url=urljoin(link_base,a.get('href')),label=re.sub(r'\s+',' ',a.text_content()).strip(),context=re.sub(r'\s+',' ',parent.text_content()).strip()[:1500]))
    elif format in ('csv','tsv'):
        for ri,row in enumerate(csv.reader(io.StringIO(path.read_text(encoding='utf-8-sig')),delimiter='\t' if format=='tsv' else ','),1):
            for ci,value in enumerate(row,1): cells.append(dict(page=None,table=1,row=ri,column=ci,value_original=value,reference=f'row {ri}; column {ci}'))
    elif format in ('json','geojson'):
        obj=json.loads(path.read_text(encoding='utf-8-sig'))
        def walk(o,ptr=''):
            if isinstance(o,dict):
                for k,v in o.items(): walk(v,ptr+'/'+str(k).replace('~','~0').replace('/','~1'))
            elif isinstance(o,list):
                for i,v in enumerate(o): walk(v,ptr+'/'+str(i))
            else: cells.append(dict(value_original=o,reference='JSON pointer '+(ptr or '/')))
        walk(obj)
    elif format=='xlsx':
        from openpyxl import load_workbook
        wb=load_workbook(path,read_only=True,data_only=False)
        for sheet in wb:
            for row in sheet:
                for c in row:
                    if c.value is not None: cells.append(dict(value_original=str(c.value),reference=f'{sheet.title}!{c.coordinate}'))
        wb.close()
    else: issues.append({'reason':'unsupported_format_needs_manual_extractor'})
    return dict(pages=pages,cells=cells,links=links,issues=issues)
