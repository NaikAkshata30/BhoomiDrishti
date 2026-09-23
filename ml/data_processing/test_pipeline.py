"""Offline safeguards and delivered evidence audit: python data_processing/test_pipeline.py."""
import unittest
from common import *
from normalizers.values import normalize_number, normalize_date, derived_progress
from validators.rules import validate_fact, conflicts

class Safeguards(unittest.TestCase):
    def test_units_and_missing(self):
        self.assertEqual(normalize_number('10000','m2')[0],1)
        self.assertIsNone(normalize_number(None,'ha')[0])
        for value,unit in [('101','%'),('12 approx','ha'),('5','unknown'),('-2','ha')]:
            with self.assertRaises(ValueError): normalize_number(value,unit)
    def test_dates_and_denominators(self):
        self.assertEqual(normalize_date('03/04/2022'),(None,'review_required'))
        self.assertEqual(normalize_date('03/04/2022',True),('2022-04-03','day'))
        self.assertEqual(normalize_date('2022-04'),(None,'month'))
        self.assertIsNone(derived_progress(1,0,True,True))
        self.assertIsNone(derived_progress(1,2,False,True))
        self.assertEqual(derived_progress(1,2,True,True),50)
    def test_anchor_and_programme(self):
        f=dict(entity_id='REAL_007',record_scope='project',project_id='REAL_007',source_reference='p1',anchor='missing')
        errors=validate_fact(f,{'download_status':'downloaded'},'actual evidence')
        self.assertIn('evidence_anchor_not_found',errors)
        self.assertIn('bharatmala_is_programme',errors)
    def test_conflicts_preserve_time(self):
        base=dict(entity_id='P/A',project_id='P',field='area',source_id='a',value_normalized=1,observation_date='2022-01-01',unit='ha')
        self.assertEqual(conflicts([base.copy(),dict(base,source_id='b',value_normalized=2,observation_date='2023-01-01')]),[])
        rows=[base.copy(),dict(base,source_id='b',value_normalized=2)]
        self.assertEqual(len(conflicts(rows)),1)
        self.assertTrue(all(r['conflict_flag'] and not r['ml_eligible'] for r in rows))
    def test_delivered_evidence(self):
        manifest=read_json(MASTER/'source_manifest.json')
        self.assertEqual(len(PROJECTS),10)
        byid={m['source_id']:m for m in manifest}
        for m in manifest:
            if m['download_status']=='downloaded':
                self.assertEqual(sha((ROOT/m['local_file']).read_bytes()),m['sha256'])
                self.assertGreater(m['pages_extracted'],0)
        for r in read_json(MASTER/'normalized_observations.json'):
            self.assertEqual(r['source_sha256'],byid[r['source_id']]['sha256'])
            self.assertTrue(r['source_reference'] and r['entity_id'])
            self.assertFalse(r['ml_eligible'])
        for name in 'source_manifest project_registry data_dictionary data_quality_report missing_data_report manual_review_required duplicate_sources conflicting_sources secondary_sources'.split():
            self.assertTrue((MASTER/(name+'.csv')).is_file())
        for pid in PROJECTS: self.assertTrue((project_dir(pid)/'manifest.csv').is_file())
        self.assertEqual(list((ROOT/'models').iterdir()),[])
        self.assertEqual(read_json(ROOT/'data_processing/logs/rejected_observations.json'),[])

if __name__=='__main__': unittest.main(verbosity=2)
