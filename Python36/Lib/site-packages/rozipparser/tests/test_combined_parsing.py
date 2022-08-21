# coding=utf-8

import unittest

from rozipparser.codeparser import CodeParser


class TestBucharestParsing(unittest.TestCase):
    def test_number_of_codes(self):
        parser = CodeParser("rozipparser/tests/inputs/combined_input.xlsx")
        codes = parser.get_codes()

        self.assertEqual(len(codes), 3)

    def test_code_correctness(self):
        parser = CodeParser("rozipparser/tests/inputs/combined_input.xlsx")
        codes = parser.get_codes()

        bucharest_code = [x for x in codes if x.county == u"Bucuresti" and x.locality == u"Bucuresti"]
        self.assertEqual(len(bucharest_code), 1)
        bucharest_code = bucharest_code[0]
        self.assertEqual(bucharest_code.county, u"Bucuresti")
        self.assertEqual(bucharest_code.locality, u"Bucuresti")
        self.assertEqual(bucharest_code.sector, 1)
        self.assertEqual(bucharest_code.street, u"Mincu Ion, arh.")
        self.assertEqual(bucharest_code.house_number, u"nr. 21-T")
        self.assertEqual(bucharest_code.zip, u"011357")
        self.assertEqual(bucharest_code.street_type, u"Stradă")

        large_locality_code = [x for x in codes if x.county == u"Giurgiu" and x.locality == u"Giurgiu"]
        self.assertEqual(len(large_locality_code), 1)
        large_locality_code = large_locality_code[0]
        self.assertEqual(large_locality_code.county, u"Giurgiu")
        self.assertEqual(large_locality_code.locality, u"Giurgiu")
        self.assertIsNone(large_locality_code.sector)
        self.assertEqual(large_locality_code.street, u"Bucureşti")
        self.assertEqual(large_locality_code.house_number, u"bl. 54/2D, 61/2D-62/2D")
        self.assertEqual(large_locality_code.zip, u"080303")
        self.assertEqual(large_locality_code.street_type, u"Şosea")

        small_locality_code = [x for x in codes if x.county == u"Ilfov" and x.locality == u"Buftea"]
        self.assertEqual(len(small_locality_code), 1)
        small_locality_code = small_locality_code[0]
        self.assertEqual(small_locality_code.county, u"Ilfov")
        self.assertEqual(small_locality_code.locality, u"Buftea")
        self.assertIsNone(small_locality_code.sector)
        self.assertIsNone(small_locality_code.street)
        self.assertIsNone(small_locality_code.house_number)
        self.assertEqual(small_locality_code.zip, u"070000")
        self.assertIsNone(small_locality_code.street_type)
