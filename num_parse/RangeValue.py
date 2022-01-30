"""
Range Value
January 30, 2022

A class for modeling range values with units associated with them.

Author(s): Marko Sterbentz / C3
"""

import pint

class RangeValue:
    def __init__(self,
                 min_val: pint.Quantity,
                 max_val: pint.Quantity):
        # TODO: Ensure units are the same (also ensure if one is dimensionless, then that Quantity takes the units of the other)
        self.min_val = min_val
        self.max_val = max_val

    def __repr__(self):
        return '<RangeValue({}, {})>'.format(self.min_val.__repr__(), self.max_val.__repr__())

    def __str__(self):
        return self.__repr__()

    ########################################################
    # COMPARISON OPERATORS
    ########################################################
    def __eq__(self, other):
        return self.min_val == other and self.max_val == other

    def __ge__(self, other):
        return self.min_val >= other

    def __gt__(self, other):
        return self.min_val > other

    def __le__(self, other):
        return self.max_val <= other

    def __lt__(self, other):
        return self.max_val < other

    ########################################################
    # ARITHMETIC OPERATORS
    ########################################################

    def __add__(self, other):
        return RangeValue(self.min_val + other, self.max_val + other)

    def __sub__(self, other):
        return RangeValue(self.min_val - other, self.max_val - other)

    def __mul__(self, other):
        return RangeValue(self.min_val * other, self.max_val * other)

    def __neg__(self):
        return RangeValue(-self.max_val, -self.min_val)

    def __pos__(self):
        return RangeValue(self.min_val, self.max_val)
