"""
The MIT License (MIT)

Portions of this software are copyrighted under:
Copyright (c) 2016 Akshay Nagpal (https://github.com/akshaynagpal)

The remaining is copyrighted under the following:
Copyright (c) 2022 C3 Lab (https://github.com/c3-NumParse)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Range Value
January 30, 2022

A class for modeling range values with units associated with them.

Author(s): Marko Sterbentz / C3

TODO: Add function to convert to other units (e.g. 5 to 10 cm ==> 1.97 to 3.94 inches)
TODO: Improve handling of temperature units (e.g. 5 degrees Fahrenehit

"""

import pint
from copy import deepcopy

class RangeValue:
    def __init__(self,
                 min_val: pint.Quantity,
                 max_val: pint.Quantity = None):
        self.min_val = min_val
        self.max_val = max_val if max_val is not None else min_val

        # If either one of the Quantities is unitless, then add the units of the other Quantity to it
        if self.max_val is not None and self.max_val.unitless:
            self.max_val._units = self.min_val._units
            self.max_val._dimensionality = self.min_val._dimensionality

        if self.min_val.unitless and self.max_val is not None and self.max_val.units:
            # self.min_val *= self.max_val.units
            self.min_val._units = self.max_val._units
            self.min_val._dimensionality = self.max_val._dimensionality

        # Ensure units of the two values are the same
        assert self.min_val.is_compatible_with(self.max_val)

        # Ensure the min and max values are in the appropriate order
        if self.min_val > self.max_val:
            self.min_val, self.max_val = self.max_val, self.min_val

        # If units differ, convert them to an SI unit
        if not (self.min_val.unitless or self.max_val.unitless) and self.min_val.units != self.max_val.units:
            self.min_val.ito_base_units()
            self.max_val.ito_base_units()

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

    def __key(self):
        return (self.min_val.m, str(self.min_val.units), self.max_val.m, str(self.max_val.units))

    def __hash__(self):
        return hash(self.__key())

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
    # TODO: Add unit tests for arithmetic involving two RangeValues
    def __add__(self, other):
        if type(other) == RangeValue:
            if self.max_val.unitless or other.max_val.unitless:
                self_copy = deepcopy(self)
                other_copy = deepcopy(other)

                if self_copy.max_val.unitless and not other_copy.max_val.unitless:
                    # Set self_copy RangeValue's units/dimensionality to the units/dimensionality of the other RangeValue
                    self_copy.min_val._units = other_copy.max_val._units
                    self_copy.min_val._dimensionality = other_copy.max_val._dimensionality
                    self_copy.max_val._units = other_copy.max_val._units
                    self_copy.max_val._dimensionality = other_copy.max_val._dimensionality

                if other_copy.max_val.unitless and not self_copy.max_val.unitless:
                    # Set this RangeValue's units/dimensionality to the units/dimensionality of the other RangeValue
                    other_copy.min_val._units = self_copy.max_val._units
                    other_copy.min_val._dimensionality = self_copy.max_val._dimensionality
                    other_copy.max_val._units = self_copy.max_val._units
                    other_copy.max_val._dimensionality = self_copy.max_val._dimensionality

                # Perform the addition
                return RangeValue(self_copy.min_val + other_copy.min_val, self_copy.max_val + other_copy.max_val)

            # Perform the addition
            return RangeValue(self.min_val + other.min_val, self.max_val + other.max_val)
        else:
            return RangeValue(self.min_val + other, self.max_val + other)

    def __sub__(self, other):
        if type(other) == RangeValue:
            if self.max_val.unitless or other.max_val.unitless:
                self_copy = deepcopy(self)
                other_copy = deepcopy(other)

                if self_copy.max_val.unitless and not other_copy.max_val.unitless:
                    # Set self_copy RangeValue's units/dimensionality to the units/dimensionality of the other RangeValue
                    self_copy.min_val._units = other.max_val._units
                    self_copy.min_val._dimensionality = other.max_val._dimensionality
                    self_copy.max_val._units = other.max_val._units
                    self_copy.max_val._dimensionality = other.max_val._dimensionality

                if other_copy.max_val.unitless and not self_copy.max_val.unitless:
                    # Set this RangeValue's units/dimensionality to the units/dimensionality of the other RangeValue
                    other_copy.min_val._units = self_copy.max_val._units
                    other_copy.min_val._dimensionality = self_copy.max_val._dimensionality
                    other_copy.max_val._units = self_copy.max_val._units
                    other_copy.max_val._dimensionality = self_copy.max_val._dimensionality

                # Perform the subtraction
                return RangeValue(self_copy.min_val - other_copy.min_val, self_copy.max_val - other_copy.max_val)

            # Perform the subtraction
            return RangeValue(self.min_val - other.min_val, self.max_val - other.max_val)
        else:
            return RangeValue(self.min_val - other, self.max_val - other)

    def __mul__(self, other):
        if type(other) == RangeValue:
            if self.max_val.unitless and not other.max_val.unitless:
                return RangeValue(self.min_val.m * other.min_val, self.max_val.m * other.max_val)
            if not self.max_val.unitless and other.max_val.unitless:
                return RangeValue(self.min_val * other.min_val.m, self.max_val * other.max_val.m)

            return RangeValue(self.min_val * other.min_val, self.max_val * other.max_val)
        else:
            return RangeValue(self.min_val * other, self.max_val * other)

    def __neg__(self):
        return RangeValue(-self.max_val, -self.min_val)

    def __pos__(self):
        return RangeValue(self.min_val, self.max_val)
