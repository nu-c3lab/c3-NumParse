"""
Range Value
January 30, 2022

A class for modeling range values with units associated with them.

Author(s): Marko Sterbentz / C3

TODO: Add function to convert to other units (e.g. 5 to 10 cm ==> 1.97 to 3.94 inches)
TODO: Improve handling of temperature units (e.g. 5 degrees Fahrenehit

"""

import pint

class RangeValue:
    def __init__(self,
                 min_val: pint.Quantity,
                 max_val: pint.Quantity = None):
        self.min_val = min_val
        self.max_val = max_val if max_val is not None else min_val

        # If either one of the Quantities is unitless, then add the units of the other Quantity to it
        if self.max_val is not None and self.max_val.unitless:
            self.max_val._units = self.min_val._units

        if self.min_val.unitless and self.max_val is not None and self.max_val.units:
            # self.min_val *= self.max_val.units
            self.min_val._units = self.max_val._units

        # Ensure units of the two values are the same
        assert self.min_val.is_compatible_with(self.max_val)

        # Ensure the min and max values are in the appropriate order
        if self.min_val > self.max_val:
            self.min_val, self.max_val = self.max_val, self.min_val

    def __repr__(self):
        return '<RangeValue({}, {})>'.format(self.min_val.__repr__(), self.max_val.__repr__())

    def __str__(self):
        if self.min_val == self.max_val:
            if self.min_val.unitless:
                return str(self.min_val.m)
            else:
                return str(self.min_val.m) + ' ' + str(self.min_val.units)
        else:
            if self.min_val.unitless:
                return str(self.min_val.m) + ' to ' + str(self.max_val.m)
            else:
                return str(self.min_val.m) + ' to ' + str(self.max_val.m) + ' ' + str(self.min_val.units)

    ########################################################
    # COMPARISON OPERATORS
    ########################################################
    # TODO: Add unit tests for the RangeValue vs RangeValue cases
    # TODO: Might need to special case this for integer/floats vs. pint.Quantity so we look at just the min_val.magnitude when comparing
    def __eq__(self, other):
        if type(other) == RangeValue:
            return self.min_val == other.min_val and self.max_val == other.max_val
        else:
            return self.min_val == other and self.max_val == other

    def __ge__(self, other):
        if type(other) == RangeValue:
            return self.min_val >= other.min_val and self.max_val >= other.max_val
        else:
            return self.min_val >= other

    def __gt__(self, other):
        if type(other) == RangeValue:
            return self.min_val > other.min_val and self.max_val > other.max_val
        else:
            return self.min_val > other

    def __le__(self, other):
        if type(other) == RangeValue:
            return self.min_val <= other.min_val and self.max_val <= other.max_val
        else:
            return self.max_val <= other

    def __lt__(self, other):
        if type(other) == RangeValue:
            return self.min_val < other.min_val and self.max_val < other.max_val
        else:
            return self.max_val < other

    ########################################################
    # ARITHMETIC OPERATORS
    ########################################################
    # TODO: Check that the other value is compatible with the current RangeValue
    # TODO: Add handling for performing arithmetic for two RangeValues??
    # TODO: If so, add unit tests for arithmetic involving two RangeValues
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
