import unittest
from num_parse.NumParser import NumParser
from num_parse.RangeValue import RangeValue

class TestRangeValue(unittest.TestCase):

    def setUp(self):
        self.num_parser = NumParser()
        self.Q_ = self.num_parser.Quantity

    #######################################################
    # Comparison / Equality
    #######################################################

    def test_equality_dimensionless(self):
        rv = RangeValue(self.Q_(5), self.Q_(5))
        self.assertEqual(rv, 5)
        self.assertNotEqual(rv, 6)
        self.assertNotEqual(rv, -5)

    def test_range_greater_equal_than_dimensionless(self):
        rv = RangeValue(self.Q_(5), self.Q_(10))
        self.assertGreaterEqual(rv, 5)
        self.assertGreaterEqual(rv, 2)
        self.assertGreaterEqual(rv, -10)

    def test_range_greater_than_dimensionless(self):
        rv = RangeValue(self.Q_(5), self.Q_(10))
        self.assertGreaterEqual(rv, 4.9999)
        self.assertGreaterEqual(rv, 2)
        self.assertGreaterEqual(rv, -10)

    def test_range_less_equal_than_dimensionless(self):
        rv = RangeValue(self.Q_(5), self.Q_(10))
        self.assertLessEqual(rv, 10)
        self.assertLessEqual(rv, 10.00001)
        self.assertLessEqual(rv, 150)

    def test_range_less_than_dimensionless(self):
        rv = RangeValue(self.Q_(5), self.Q_(10))
        self.assertLess(rv, 10.000001)
        self.assertLess(rv, 150)

    def test_equality_meters(self):
        rv = RangeValue(self.Q_(5, 'meters'), self.Q_(5, 'meters'))
        self.assertEqual(rv, self.Q_(5, 'meters'))
        self.assertNotEqual(rv, self.Q_(6, 'meters'))
        self.assertNotEqual(rv, self.Q_(-5, 'meters'))

    def test_equality_different_units(self):
        rv = RangeValue(self.Q_(5, 'meters'), self.Q_(5, 'meters'))
        self.assertEqual(rv, self.Q_(500, 'cm'))
        self.assertEqual(rv, self.Q_(5000, 'mm'))
        self.assertNotEqual(rv, self.Q_(5, 'cm'))
        self.assertNotEqual(rv, self.Q_(5, 'mm'))

    def test_range_greater_equal_different_units(self):
        rv = RangeValue(self.Q_(5, 'meters'), self.Q_(10, 'meters'))
        self.assertGreaterEqual(rv, self.Q_(500, 'cm'))
        self.assertGreaterEqual(rv, self.Q_(5000, 'mm'))
        self.assertGreaterEqual(rv, self.Q_(-1000, 'cm'))

    def test_range_greater_than_different_units(self):
        rv = RangeValue(self.Q_(5, 'meters'), self.Q_(10, 'meters'))
        self.assertGreaterEqual(rv, self.Q_(4.999, 'm'))
        self.assertGreaterEqual(rv, self.Q_(499, 'cm'))
        self.assertGreaterEqual(rv, self.Q_(0, 'cm'))

    def test_range_less_equal_than_different_units(self):
        rv = RangeValue(self.Q_(5, 'meters'), self.Q_(10, 'meters'))
        self.assertLessEqual(rv, self.Q_(10, 'm'))
        self.assertLessEqual(rv, self.Q_(1000.011, 'cm'))
        self.assertLessEqual(rv, self.Q_(150000, 'mm'))

    def test_range_less_than_different_units(self):
        rv = RangeValue(self.Q_(5, 'meters'), self.Q_(10, 'meters'))
        self.assertLess(rv, self.Q_(10.00001, 'm'))
        self.assertLess(rv, self.Q_(1000.00001, 'cm'))
        self.assertLess(rv, self.Q_(100000.00001, 'mm'))

    #######################################################
    # Arithmetic
    #######################################################

    def test_range_addition_different_units(self):
        a = self.num_parser.parse_num("four")
        b = self.num_parser.parse_num("38 meters")
        c = self.num_parser.parse_num("42 meters")
        self.assertEqual(c, a + b)
        self.assertEqual(c, b + a)

    def test_range_subtraction_different_units(self):
        a = self.num_parser.parse_num("four")
        b = self.num_parser.parse_num("38 meters")
        c = self.num_parser.parse_num("-34 meters")
        d = self.num_parser.parse_num("34 meters")
        self.assertEqual(c, a - b)
        self.assertEqual(d, b - a)

    def test_range_multiplication_different_units(self):
        a = self.num_parser.parse_num("four")
        b = self.num_parser.parse_num("5 meters")
        c = self.num_parser.parse_num("20 meters")
        self.assertEqual(c, a * b)
        self.assertEqual(c, b * a)

    def test_range_addition_same_units(self):
        a = self.num_parser.parse_num("four meters")
        b = self.num_parser.parse_num("38 meters")
        c = self.num_parser.parse_num("42 meters")
        self.assertEqual(c, a + b)
        self.assertEqual(c, b + a)

    def test_range_subtraction_same_units(self):
        a = self.num_parser.parse_num("four meters")
        b = self.num_parser.parse_num("38 meters")
        c = self.num_parser.parse_num("-34 meters")
        d = self.num_parser.parse_num("34 meters")
        self.assertEqual(c, a - b)
        self.assertEqual(d, b - a)

    def test_range_multiplication_same_units(self):
        a = self.num_parser.parse_num("four meters")
        b = self.num_parser.parse_num("5 meters")
        c = self.num_parser.parse_num("20 square meters")
        self.assertEqual(c, a * b)
        self.assertEqual(c, b * a)
