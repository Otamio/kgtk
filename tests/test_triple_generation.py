import unittest
import os
from kgtk.generator import TripleGenerator
from pathlib import Path


class TestTripleGeneration(unittest.TestCase):
    def test_truthy_dates_generation(self):
        dates_tsv_file = Path('data/dates.tsv')
        wikidata_property_file = 'data/wikidata_properties.tsv'
        o = 'data/dates_truthy_tmp.ttl'
        generator = TripleGenerator(prop_file=wikidata_property_file, label_set='label', alias_set='aliases',
                                    description_set='descriptions', warning=True, n=100, truthy=True, use_id=True,
                                    dest_fp=o, log_path="data/date_warning.log", prop_declaration=False,
                                    prefix_path="NONE", input_file=dates_tsv_file, error_action='log')
        generator.process()

        f1 = open('data/dates_truthy.ttl')
        f2 = open('data/dates_truthy_tmp.ttl')

        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
        self.assertEqual(os.stat("data/date_warning.log").st_size, 0)

        p = Path("data/date_warning.log")
        p.unlink()
        p = Path('data/dates_truthy_tmp.ttl')
        p.unlink()

    def test_truthy_property_triple_generation(self):
        property_tsv_file = Path('data/P10.tsv')
        wikidata_property_file = 'data/wikidata_properties.tsv'
        o = 'data/P10_truthy_tmp.ttl'
        generator = TripleGenerator(prop_file=wikidata_property_file, label_set='label', alias_set='aliases',
                                    description_set='descriptions', warning=True, n=100, truthy=True, use_id=True,
                                    dest_fp=o, log_path="data/warning.log", prop_declaration=False, prefix_path="NONE",
                                    input_file=property_tsv_file, error_action='log')
        generator.process()

        f1 = open('data/P10_truthy.ttl')
        f2 = open('data/P10_truthy_tmp.ttl')
        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()

        self.assertEqual(os.stat("data/warning.log").st_size, 0)
        p = Path("data/warning.log")
        p.unlink()
        p = Path('data/P10_truthy_tmp.ttl')
        p.unlink()

    def test_property_triple_generation(self):
        property_tsv_file = Path('data/P10.tsv')
        wikidata_property_file = 'data/wikidata_properties.tsv'
        o = 'data/P10_not_truthy_tmp.ttl'
        generator = TripleGenerator(prop_file=wikidata_property_file, label_set='label', alias_set='aliases',
                                    description_set='descriptions', warning=True, n=100, truthy=False, use_id=True,
                                    dest_fp=o, log_path="data/warning.log", prop_declaration=False, prefix_path="NONE",
                                    input_file=property_tsv_file, error_action='log')
        generator.process()

        f1 = open('data/P10_not_truthy.ttl')
        f2 = open('data/P10_not_truthy_tmp.ttl')
        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
        self.assertEqual(os.stat("data/warning.log").st_size, 0)
        p = Path("data/warning.log")
        p.unlink()
        p = Path('data/P10_not_truthy_tmp.ttl')
        p.unlink()

    def test_truthy_qnode_triple_generation(self):
        qnode_tsv_file = Path('data/Q57160439.tsv')
        wikidata_property_file = 'data/wikidata_properties.tsv'
        o = 'data/Q57160439_truthy_tmp.ttl'
        generator = TripleGenerator(prop_file=wikidata_property_file, label_set='label', alias_set='aliases',
                                    description_set='descriptions', warning=True, n=100, truthy=True, use_id=True,
                                    dest_fp=o, log_path="data/warning.log", prop_declaration=False, prefix_path="NONE",
                                    input_file=qnode_tsv_file, error_action='log')
        generator.process()

        f1 = open('data/Q57160439_truthy.ttl')
        f2 = open('data/Q57160439_truthy_tmp.ttl')
        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
        self.assertEqual(os.stat("data/warning.log").st_size, 0)
        p = Path("data/warning.log")
        p.unlink()
        p = Path('data/Q57160439_truthy_tmp.ttl')
        p.unlink()

    def test_not_truthy_qnode_triple_generation(self):
        qnode_tsv_file = Path('data/Q57160439.tsv')
        wikidata_property_file = 'data/wikidata_properties.tsv'
        o = 'data/Q57160439_not_truthy_tmp.ttl'
        generator = TripleGenerator(prop_file=wikidata_property_file, label_set='label', alias_set='aliases',
                                    description_set='descriptions', warning=True, n=100, truthy=False, use_id=True,
                                    dest_fp=o, log_path="data/warning.log", prop_declaration=False, prefix_path="NONE",
                                    input_file=qnode_tsv_file, error_action='log')
        generator.process()

        f1 = open('data/Q57160439_not_truthy.ttl')
        f2 = open('data/Q57160439_not_truthy_tmp.ttl')

        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()

        self.assertEqual(os.stat("data/warning.log").st_size, 0)

        p = Path("data/warning.log")
        p.unlink()
        p = Path('data/Q57160439_not_truthy_tmp.ttl')
        p.unlink()

    def test_triple_small_values(self):
        small_values_file = Path('data/small_values.tsv')
        wikidata_property_file = 'data/wikidata_properties.tsv'
        o = 'data/small_values_tmp.ttl'
        generator = TripleGenerator(prop_file=wikidata_property_file, label_set='label', alias_set='aliases',
                                    description_set='descriptions', warning=True, n=100, truthy=True, use_id=True,
                                    dest_fp=o, log_path="data/warning.log", prop_declaration=False, prefix_path="NONE",
                                    input_file=small_values_file, error_action='log')
        generator.process()

        f1 = open('data/small_values.ttl')
        f2 = open('data/small_values_tmp.ttl')
        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
        self.assertEqual(os.stat("data/warning.log").st_size, 0)
        p = Path("data/warning.log")
        p.unlink()
        p = Path('data/small_values_tmp.ttl')
        p.unlink()

    def test_triple_corrupted_edges(self):
        corrupted_kgtk_file = Path('data/corrupted_kgtk.tsv')
        wikidata_property_file = 'data/wikidata_properties.tsv'
        o = 'data/corrupted_tmp.ttl'
        generator = TripleGenerator(prop_file=wikidata_property_file, label_set='label', alias_set='aliases',
                                    description_set='descriptions', warning=True, n=100, truthy=True, use_id=True,
                                    dest_fp=o, log_path="data/corrupted_warning_tmp.log", prop_declaration=False,
                                    prefix_path="NONE", input_file=corrupted_kgtk_file, error_action='log')
        generator.process()

        f1 = open('data/corrupted.ttl')
        f2 = open('data/corrupted_tmp.ttl')
        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
        f1 = open("data/corrupted_warning.log")
        f2 = open("data/corrupted_warning_tmp.log")
        self.assertEqual(f1.readlines(), f2.readlines())
        f1.close()
        f2.close()
        p = Path("data/corrupted_warning_tmp.log")
        p.unlink()
        p = Path('data/corrupted_tmp.ttl')
        p.unlink()