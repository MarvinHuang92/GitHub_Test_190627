# coding=utf-8

import unittest

from rozipparser.codeparser import CodeParser


class TestSmallLocalityParsing(unittest.TestCase):
    def test_number_of_codes(self):
        parser = CodeParser("rozipparser/tests/inputs/small_locality_input.xlsx")
        codes = parser.get_codes()

        self.assertEqual(len(codes), 9)

    def test_code_correctness(self):
        parser = CodeParser("rozipparser/tests/inputs/small_locality_input.xlsx")
        codes = parser.get_codes()

        first_code = codes[0]
        self.assertEqual(first_code.county, u"Ilfov")
        self.assertEqual(first_code.locality, u"Buftea")
        self.assertIsNone(first_code.sector)
        self.assertIsNone(first_code.street)
        self.assertIsNone(first_code.house_number)
        self.assertEqual(first_code.zip, u"070000")
        self.assertIsNone(first_code.street_type)
