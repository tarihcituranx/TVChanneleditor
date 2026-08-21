import unittest
import os
import sys

# Add parent directory to path so we can import the core engines
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import scm_core
import lg_core
import sony_core
import tizen_core
import hisense_core

class TestRoundtrip(unittest.TestCase):
    def setUp(self):
        self.fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
        
    def test_samsung_scm_roundtrip(self):
        scm_path = os.path.join(self.fixtures_dir, 'samsung', 'test1.scm')
        if not os.path.exists(scm_path): self.skipTest("SCM fixture not found")
        orig_channels = scm_core.get_channels(scm_path)
        edited = {c['Slot']: c for c in orig_channels}
        out_path = os.path.join(self.fixtures_dir, 'samsung', 'out_test1.scm')
        scm_core.build_scm_direct(scm_path, out_path, edited)
        new_channels = scm_core.get_channels(out_path)
        self.assertEqual(len(orig_channels), len(new_channels))
        if os.path.exists(out_path): os.remove(out_path)

    def test_lg_tll_roundtrip(self):
        tll_path = os.path.join(self.fixtures_dir, 'lg', 'test2.tll')
        if not os.path.exists(tll_path): self.skipTest("TLL fixture not found")
        parser = lg_core.LgEditor(tll_path)
        parser.extract()
        orig_channels = parser.get_channels()
        out_path = os.path.join(self.fixtures_dir, 'lg', 'out_test2.tll')
        parser.update_channels(orig_channels, out_path)
        parser2 = lg_core.LgEditor(out_path)
        parser2.extract()
        new_channels = parser2.get_channels()
        self.assertEqual(len(orig_channels), len(new_channels))
        parser.cleanup(); parser2.cleanup()
        if os.path.exists(out_path): os.remove(out_path)

    def test_sony_sdb_roundtrip(self):
        xml_path = os.path.join(self.fixtures_dir, 'sony', 'test1.xml')
        if not os.path.exists(xml_path): self.skipTest("Sony fixture not found")
        parser = sony_core.SonyEditor(xml_path)
        parser.extract()
        orig_channels = parser.get_channels()
        out_path = os.path.join(self.fixtures_dir, 'sony', 'out_test1.xml')
        parser.update_channels(orig_channels, out_path)
        parser2 = sony_core.SonyEditor(out_path)
        parser2.extract()
        new_channels = parser2.get_channels()
        self.assertEqual(len(orig_channels), len(new_channels))
        parser.cleanup(); parser2.cleanup()
        if os.path.exists(out_path): os.remove(out_path)

    def test_tizen_zip_roundtrip(self):
        zip_path = os.path.join(self.fixtures_dir, 'tizen', 'test1.zip')
        if not os.path.exists(zip_path): self.skipTest("Tizen fixture not found")
        parser = tizen_core.TizenEditor(zip_path)
        parser.extract()
        orig_channels = parser.get_channels()
        out_path = os.path.join(self.fixtures_dir, 'tizen', 'out_test1.zip')
        parser.update_channels(orig_channels, out_path)
        parser2 = tizen_core.TizenEditor(out_path)
        parser2.extract()
        new_channels = parser2.get_channels()
        self.assertEqual(len(orig_channels), len(new_channels))
        parser.cleanup(); parser2.cleanup()
        if os.path.exists(out_path): os.remove(out_path)

    def test_hisense_2017_roundtrip(self):
        db_path = os.path.join(self.fixtures_dir, 'hisense', 'test_2017.db')
        if not os.path.exists(db_path): self.skipTest("Hisense 2017 fixture not found")
        parser = hisense_core.HisenseEditor(db_path)
        parser.extract()
        orig_channels = parser.get_channels()
        out_path = os.path.join(self.fixtures_dir, 'hisense', 'out_test_2017.db')
        parser.update_channels(orig_channels, out_path)
        parser2 = hisense_core.HisenseEditor(out_path)
        parser2.extract()
        new_channels = parser2.get_channels()
        self.assertEqual(len(orig_channels), len(new_channels))
        parser.cleanup(); parser2.cleanup()
        if os.path.exists(out_path): os.remove(out_path)

    def test_hisense_2021_roundtrip(self):
        db_path = os.path.join(self.fixtures_dir, 'hisense', 'test_2021.db')
        if not os.path.exists(db_path): self.skipTest("Hisense 2021 fixture not found")
        parser = hisense_core.HisenseEditor(db_path)
        parser.extract()
        orig_channels = parser.get_channels()
        out_path = os.path.join(self.fixtures_dir, 'hisense', 'out_test_2021.db')
        parser.update_channels(orig_channels, out_path)
        parser2 = hisense_core.HisenseEditor(out_path)
        parser2.extract()
        new_channels = parser2.get_channels()
        self.assertEqual(len(orig_channels), len(new_channels))
        parser.cleanup(); parser2.cleanup()
        if os.path.exists(out_path): os.remove(out_path)

if __name__ == '__main__':
    unittest.main()
