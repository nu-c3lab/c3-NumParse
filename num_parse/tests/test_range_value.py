import unittest
from pint import UnitRegistry
from num_parse.RangeValue import RangeValue

class TestRangeValue(unittest.TestCase):

    def setUp(self):
        self.ureg = UnitRegistry()

    def test_equality_dimensionless(self):
        rv = RangeValue(self.ureg.Quantity(5), self.ureg.Quantity(5))
        self.assertEqual(rv, 5)
        self.assertNotEqual(rv, 6)
        self.assertNotEqual(rv, -5)

    def test_range_greater_equal_than_dimensionless(self):
        rv = RangeValue(self.ureg.Quantity(5), self.ureg.Quantity(10))
        self.assertGreaterEqual(rv, 5)
        self.assertGreaterEqual(rv, 2)
        self.assertGreaterEqual(rv, -10)

    def test_range_greater_than_dimensionless(self):
        rv = RangeValue(self.ureg.Quantity(5), self.ureg.Quantity(10))
        self.assertGreaterEqual(rv, 4.9999)
        self.assertGreaterEqual(rv, 2)
        self.assertGreaterEqual(rv, -10)

    def test_range_less_equal_than_dimensionless(self):
        rv = RangeValue(self.ureg.Quantity(5), self.ureg.Quantity(10))
        self.assertLessEqual(rv, 10)
        self.assertLessEqual(rv, 10.00001)
        self.assertLessEqual(rv, 150)

    def test_range_less_than_dimensionless(self):
        rv = RangeValue(self.ureg.Quantity(5), self.ureg.Quantity(10))
        self.assertLess(rv, 10.000001)
        self.assertLess(rv, 150)

    def test_equality_meters(self):
        rv = RangeValue(self.ureg.Quantity(5, 'meters'), self.ureg.Quantity(5, 'meters'))
        self.assertEqual(rv, self.ureg.Quantity(5, 'meters'))
        self.assertNotEqual(rv, self.ureg.Quantity(6, 'meters'))
        self.assertNotEqual(rv, self.ureg.Quantity(-5, 'meters'))

    def test_equality_different_units(self):
        rv = RangeValue(self.ureg.Quantity(5, 'meters'), self.ureg.Quantity(5, 'meters'))
        self.assertEqual(rv, self.ureg.Quantity(500, 'cm'))
        self.assertEqual(rv, self.ureg.Quantity(5000, 'mm'))
        self.assertNotEqual(rv, self.ureg.Quantity(5, 'cm'))
        self.assertNotEqual(rv, self.ureg.Quantity(5, 'mm'))

    def test_range_greater_equal_different_units(self):
        rv = RangeValue(self.ureg.Quantity(5, 'meters'), self.ureg.Quantity(10, 'meters'))
        self.assertGreaterEqual(rv, self.ureg.Quantity(500, 'cm'))
        self.assertGreaterEqual(rv, self.ureg.Quantity(5000, 'mm'))
        self.assertGreaterEqual(rv, self.ureg.Quantity(-1000, 'cm'))

    def test_range_greater_than_different_units(self):
        rv = RangeValue(self.ureg.Quantity(5, 'meters'), self.ureg.Quantity(10, 'meters'))
        self.assertGreaterEqual(rv, self.ureg.Quantity(4.999, 'm'))
        self.assertGreaterEqual(rv, self.ureg.Quantity(499, 'cm'))
        self.assertGreaterEqual(rv, self.ureg.Quantity(0, 'cm'))

    def test_range_less_equal_than_different_units(self):
        rv = RangeValue(self.ureg.Quantity(5, 'meters'), self.ureg.Quantity(10, 'meters'))
        self.assertLessEqual(rv, self.ureg.Quantity(10, 'm'))
        self.assertLessEqual(rv, self.ureg.Quantity(1000.011, 'cm'))
        self.assertLessEqual(rv, self.ureg.Quantity(150000, 'mm'))

    def test_range_less_than_different_units(self):
        rv = RangeValue(self.ureg.Quantity(5, 'meters'), self.ureg.Quantity(10, 'meters'))
        self.assertLess(rv, self.ureg.Quantity(10.00001, 'm'))
        self.assertLess(rv, self.ureg.Quantity(1000.00001, 'cm'))
        self.assertLess(rv, self.ureg.Quantity(100000.00001, 'mm'))
