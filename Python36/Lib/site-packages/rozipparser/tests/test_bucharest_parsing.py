# coding=utf-8

import unittest

from rozipparser.codeparser import CodeParser


class TestBucharestParsing(unittest.TestCase):
    def test_number_of_codes(self):
        parser = CodeParser("rozipparser/tests/inputs/bucharest_input.xlsx")
        codes = parser.get_codes()

        self.assertEqual(len(codes), 9)

    def test_code_correctness(self):
        parser = CodeParser("rozipparser/tests/inputs/bucharest_input.xlsx")
        codes = parser.get_codes()

        first_code = codes[0]
        self.assertEqual(first_code.county, u"Bucuresti")
        self.assertEqual(first_code.locality, u"Bucuresti")
        self.assertEqual(first_code.sector, 1)
        self.assertEqual(first_code.street, u"Mincu Ion, arh.")
        self.assertEqual(first_code.house_number, u"nr. 21-T")
        self.assertEqual(first_code.zip, u"011357")
        self.assertEqual(first_code.street_type, u"Stradă")
