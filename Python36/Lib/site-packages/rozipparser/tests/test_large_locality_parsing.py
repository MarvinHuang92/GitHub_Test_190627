# coding=utf-8

import unittest

from rozipparser.codeparser import CodeParser


class TestLargeLocalityParsing(unittest.TestCase):
    def test_number_of_codes(self):
        parser = CodeParser("rozipparser/tests/inputs/large_locality_input.xlsx")
        codes = parser.get_codes()

        self.assertEqual(len(codes), 8)

    def test_code_correctness(self):
        parser = CodeParser("rozipparser/tests/inputs/large_locality_input.xlsx")
        codes = parser.get_codes()

        first_code = codes[0]
        self.assertEqual(first_code.county, u"Giurgiu")
        self.assertEqual(first_code.locality, u"Giurgiu")
        self.assertIsNone(first_code.sector)
        self.assertEqual(first_code.street, u"Bucureşti")
        self.assertEqual(first_code.house_number, u"bl. 54/2D, 61/2D-62/2D")
        self.assertEqual(first_code.zip, u"080303")
        self.assertEqual(first_code.street_type, u"Şosea")
