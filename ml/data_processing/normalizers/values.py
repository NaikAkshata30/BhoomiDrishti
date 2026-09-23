"""Explicit units only. No zero filling, implicit acres, date guessing or target labels."""
from decimal import Decimal, InvalidOperation
from datetime import datetime
import re
FACTORS={'ha':('ha',Decimal(1)),'m2':('ha',Decimal('0.0001')),'acre':('ha',Decimal('0.40468564224')),'INR':('INR',Decimal(1)),'INR_lakh':('INR',Decimal(100000)),'INR_crore':('INR',Decimal(10000000)),'mm':('mm',Decimal(1)),'km':('km',Decimal(1)),'%':('%',Decimal(1)),'count':('count',Decimal(1))}
def normalize_number(value,unit):
    if value is None or str(value).strip() in ('','-','NA','N/A','NULL'): return None,unit,'missing'
    if unit not in FACTORS: raise ValueError('unknown_unit:'+str(unit))
    token=str(value).strip().replace(',','').removesuffix('%').strip()
    if not re.fullmatch(r'-?\d+(?:\.\d+)?',token): raise ValueError('ambiguous_numeric_value:'+token)
    target,factor=FACTORS[unit]
    result=Decimal(token)*factor
    if result<0: raise ValueError('negative_measurement')
    if unit=='%' and result>100: raise ValueError('percentage_out_of_range')
    return float(result),target,'identity' if factor==1 else f'{unit} * {factor} -> {target}'
def normalize_date(value,day_first_explicit=False):
    if not value: return None,'missing'
    if re.fullmatch(r'\d{4}',value): return None,'year'
    if re.fullmatch(r'\d{4}-\d{2}',value): return None,'month'
    formats=['%Y-%m-%d','%d %B %Y','%d %b %Y']
    if day_first_explicit: formats+=['%d-%m-%Y','%d/%m/%Y','%d.%m.%Y']
    for fmt in formats:
        try: return datetime.strptime(value,fmt).date().isoformat(),'day'
        except ValueError: pass
    return None,'review_required'
def derived_progress(acquired,denominator,same_scope=False,same_date=False):
    if not same_scope or not same_date or acquired is None or denominator is None or denominator<=0 or acquired<0 or acquired>denominator: return None
    return 100*acquired/denominator

