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
Num Parser

The code for this module has been adapted from the Word2Number library:
https://github.com/akshaynagpal/w2n

As such, we do not claim to have written everything contained in this file, and many thanks go to the original authors.

ASSUMPTIONS:
1. We assume the use of the American number system and its associated standards.
2. We assume only one sentence as a time will be provided to the parser.

"""

from pathlib import Path
import pint
from pint import UnitRegistry, UndefinedUnitError, OffsetUnitCalculusError, DimensionalityError
from pint.compat import is_duck_array_type, zero_or_nan
from pint.definitions import UnitDefinition
from typing import Union, List, Tuple, Optional
import num_parse.word_to_num_values as word_to_num_values
from num_parse.RangeValue import RangeValue
from functools import reduce
from io import BytesIO
import re
import tokenize
import numpy as np

MARGIN = 0.0001

def tokenizer(input_string):
    for tokinfo in tokenize.tokenize(BytesIO(input_string.encode("utf-8")).readline):
        if tokinfo.type != tokenize.ENCODING:
            if tokinfo.type == tokenize.ERRORTOKEN and tokinfo.string != ' ':
                yield tokenize.TokenInfo(type=1, string=tokinfo.string, start=tokinfo.start, end=tokinfo.end, line=tokinfo.line)
            else:
                yield tokinfo

# Injecting the above tokenizer into pint :)
pint.util.tokenizer = tokenizer

class NumUnitRegistry(UnitRegistry):

    def get_name(
        self, name_or_alias: str, case_sensitive: Optional[bool] = None
    ) -> str:
        """Return the canonical name of a unit."""

        if name_or_alias == "dimensionless":
            return ""

        try:
            return self._units[name_or_alias].name
        except KeyError:
            pass

        candidates = self.parse_unit_name(name_or_alias, case_sensitive) or self.parse_unit_name(name_or_alias, case_sensitive=False)
        if not candidates:
            raise UndefinedUnitError(name_or_alias)
        elif len(candidates) == 1:
            prefix, unit_name, _ = candidates[0]
        else:
            # If multiple, prefer the one with fewest "pieces"
            prefix, unit_name, _ = sorted(candidates, key=lambda candidate: len([piece for piece in candidate if len(piece)]))[0]

        if prefix:
            name = prefix + unit_name
            symbol = self.get_symbol(name, case_sensitive)
            prefix_def = self._prefixes[prefix]
            self._units[name] = UnitDefinition(
                name,
                symbol,
                (),
                prefix_def.converter,
                self.UnitsContainer({unit_name: 1}),
            )
            return prefix + unit_name

        return unit_name

def eq(lhs, rhs, check_all: bool, error_margin: float = 0.0):

    out = abs(lhs - rhs) <= error_margin
    if check_all and is_duck_array_type(type(out)):
        return out.all()
    return out

class NumParser(object):
    def __init__(self):
        self.number_words = word_to_num_values.word_to_num_values
        self.decimal_words = word_to_num_values.decimal_words
        self.measures = word_to_num_values.measures
        self.relevant_words = []
        self.decimal_denoters = ['point', 'dot', '.']
        self.negative_denoters = ['negative', '-', 'neg', 'minus']
        self.range_denoters = ['to', 'through', 'until', 'and', 'or']
        numeric_capturing_pattern = r'(-?[\w\. ]+)'
        self.range_expressions = [pattern.format(numeric_capturing_pattern) for pattern in [r'between {0} (and) {0}', r'from {0} (until) {0}', r'{0} (or) {0}', r'{0} (to) {0}', r'{0} (through) {0}', r'{0} ([-–]) {0}']]
        self.multipliers = ['thousand', 'million', 'billion', 'trillion']
        units_path = Path(__file__).parent / 'unit_definitions/basic_units.txt'
        self.ureg = NumUnitRegistry(str(units_path), autoconvert_offset_to_baseunit=True)

        class Quantity(self.ureg.Quantity):

            def __eq__(self, other):
                def bool_result(value):
                    nonlocal other

                    if not is_duck_array_type(type(self._magnitude)):
                        return value

                    if isinstance(other, Quantity):
                        other = other._magnitude

                    template, _ = np.broadcast_arrays(self._magnitude, other)
                    return np.full_like(template, fill_value=value, dtype=np.bool_)

                # We compare to the base class of Quantity because
                # each Quantity class is unique.
                if not isinstance(other, Quantity):
                    if zero_or_nan(other, True):
                        # Handle the special case in which we compare to zero or NaN
                        # (or an array of zeros or NaNs)
                        if self._is_multiplicative:
                            # compare magnitude
                            return eq(self._magnitude, other, False)
                        else:
                            # compare the magnitude after converting the
                            # non-multiplicative quantity to base units
                            if self._REGISTRY.autoconvert_offset_to_baseunit:
                                return eq(self.to_base_units()._magnitude, other, False, MARGIN)
                            else:
                                raise OffsetUnitCalculusError(self._units)

                    if self.dimensionless:
                        return eq(
                            self._convert_magnitude_not_inplace(self.UnitsContainer()),
                            other,
                            False,
                            MARGIN
                        )

                    return bool_result(False)

                if self._units == other._units:
                    return eq(self._magnitude, other._magnitude, False, MARGIN)

                try:
                    return eq(
                        self._convert_magnitude_not_inplace(other._units),
                        other._magnitude,
                        False,
                        MARGIN
                    )
                except DimensionalityError:
                    return bool_result(False)

        self.Quantity = Quantity
        self.time_units = list(self.get_time_units())

    def get_time_units(self):
        def is_time_unit(unit_name):
            try:
                unit = self.Quantity._REGISTRY[unit_name]
            except AttributeError as e:
                return None
            if unit.dimensionality._d == {'[time]': 1}:
                return True
        return filter(is_time_unit, self.Quantity._REGISTRY)

    def parse_num(self,
                  number_string: str) -> RangeValue:
        """
        Parses a given string containing a numeric value into the raw numeric value.
        :param number_string: A string containing a number.
        :return: The raw numeric value in the given string.
        """

        #######################################################
        # Check cases where input is just a number value
        #######################################################
        if type(number_string) in [int, float]:
            return RangeValue(self.Quantity(number_string))

        #######################################################
        # Clean input string
        #######################################################
        normalized_input = self.normalize_input(number_string)

        #######################################################
        # Check cases where input is a raw number in a string
        #######################################################
        if self.is_int(normalized_input) or self.is_float(normalized_input):
            return RangeValue(self.Quantity(normalized_input))

        #######################################################
        # Split input into potentially relevant words
        #######################################################
        # clean_words = [self.clean_word(word) for word in normalized_input.split()]
        clean_words = [self.clean_word(tok.string) for tok in tokenizer(normalized_input) if tok.line and tok.type != tokenize.ERRORTOKEN]
        clean_words = [item if item != '/' else 'per' for item in clean_words]

        if len(clean_words) == 0:
            raise ValueError("No relevant words/numbers in the given string!")

        #######################################################
        # Check for unit words
        #######################################################
        unit_span, unit_string = self.has_unit_word(clean_words, True)
        if not unit_string:
            unit_span, unit_string = self.has_unit_word(clean_words, False)

        range_denoter, min_number_words, max_number_words = self.get_number_range(' '.join(clean_words))
        if range_denoter:
            min_val = self.parse_num(' '.join(min_number_words)).min_val if len(min_number_words) else ''
            max_val = self.parse_num(' '.join(max_number_words)).max_val if len(max_number_words) else ''
            if max_val.m > 1000 * min_val.m and max_number_words[-1] in self.multipliers and min_number_words[-1] not in self.multipliers:
                # distribute multiplier from max val
                min_val = self.parse_num(' '.join(min_number_words + [max_number_words[-1]])).min_val
            q1 = self.Quantity(min_val.m, unit_string) if min_val.unitless else min_val
            q2 = self.Quantity(max_val.m, unit_string) if max_val.unitless else max_val
            final_num = RangeValue(q1, q2)
            return final_num

        if len(clean_words) == 3 and clean_words[1] == ':':
            unit_string = ':'
            clean_words = clean_words[:1] + ['minutes'] + clean_words[2:] + ['seconds']
        if unit_string:
            if not range_denoter and sum(map(lambda word: 1 if word in self.time_units or word.rstrip('s') in self.time_units else 0, clean_words)) > 1:
                quantities = []
                idx = 0
                while idx < len(clean_words):
                    if clean_words[idx] in self.time_units or clean_words[idx].rstrip('s') in self.time_units:
                        unit_string = clean_words[idx]
                        quantities.append(self.parse_num(' '.join(clean_words[:idx+1])))
                        clean_words = clean_words[idx+1:]
                        idx = 0
                    else:
                        idx += 1
                return sum(quantities, start=RangeValue(self.Quantity(0, unit_string)))
            else:
                clean_words = clean_words[:unit_span[0]] + clean_words[unit_span[1]:]
        final_words = [word for word in clean_words if self.is_relevant_word(word)]

        #######################################################
        # Check if the input is a negative number, as denoted by negative indicator at start of the string
        #######################################################
        isNegative = False
        while final_words and final_words[0] in self.negative_denoters:
            final_words.pop(0)
            isNegative = not isNegative

        clean_numbers = final_words
        is_float_num, dec_word = self.has_float_word(clean_numbers)

        # Error message if the user enters invalid input!
        if len(clean_numbers) == 0:
            raise ValueError("No valid number words found! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")

         # Error if user enters decimal point, thousand, million, billion twice
        if clean_numbers.count('thousand') > 1 or clean_numbers.count('million') > 1 or clean_numbers.count('billion') > 1 or clean_numbers.count('point') > 1:
            raise ValueError("Redundant number word! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")

        #######################################################
        # Compose the final value
        #######################################################
        # CASE 1: FLOAT NUMBER
        if is_float_num:
            clean_decimal_numbers = clean_numbers[clean_numbers.index(dec_word) + 1:]
            clean_numbers = clean_numbers[:clean_numbers.index(dec_word)]
            left_val = str(self.parse_num(' '.join(clean_numbers))) if len(clean_numbers) else ''
            right_val = str(self.parse_num(' '.join(clean_decimal_numbers))) if len(clean_decimal_numbers) else ''
            final_num_string = left_val + '.' + right_val
            if final_num_string == '.':
                final_num = 0.0
            else:
                final_num = float(final_num_string)

        # BASE CASE
        else:
            final_num = 0  # storing the number to be returned

            if len(clean_numbers) > 0:
                if self.is_phrased_as_decimal_val(clean_numbers):
                    decimal_sum = self.get_decimal_sum(clean_numbers, as_float=False)
                    final_num += decimal_sum
                else:
                    integral_sum = self.get_integral_sum(clean_numbers)
                    final_num += integral_sum

        # Handle negative numbers
        if isNegative:
            final_num = -final_num

        return RangeValue(self.Quantity(final_num,  unit_string))

    def is_phrased_as_decimal_val(self,
                                  words: List[str]) -> bool:
        return all(w in self.decimal_words for w in words)

    def normalize_input(self,
                        number_string: str) -> str:
        """
        Cleans up the input string and puts it into a standard form for parsing.
        :param number_string: The string to be cleaned.
        :return: The cleaned/normalized version of the input string.
        """

        # Strip whitespace from beginning and end
        cleaned_string = number_string.strip()

        # Lowercase the string
        # cleaned_string = cleaned_string.lower() # don't do this - the unit definitions are case sensitive

        # Remove commas
        cleaned_string = cleaned_string.replace(',', '')

        # Replace hyphens in spelled out words with spaces (e.g., "thirty-five" -> "thirty five")
        cleaned_string = re.sub(r'([a-zA-Z]+)-([a-zA-Z]+)', r'\1 \2', cleaned_string)

        return cleaned_string

    def clean_word(self,
                   word: str) -> str:
        """
        Function to clean a single word into a usable form.
        :param word: The string/word to be cleaned.
        :return: The cleaned word.
        """

        return word.replace(',', '')

    def is_relevant_word(self,
                         word: str) -> bool:
        """
        Checks if the given word is a word that is useful for further analysis and parsing.
        :param word: The word to check.
        :return: A boolean denoting if the word is useful for further analysis and parsing.
        """

        return word in self.number_words.keys() or \
               word in self.relevant_words or \
               word in self.negative_denoters or \
               word in self.range_denoters or \
               self.is_int(word) or \
               self.is_float(word)

    def is_float(self,
                 s: str) -> bool:
        """
        Determines if the given string can immediately be converted to a float value.
        :param s: The string to be checked.
        :return: Boolean denoting whether the string can be converted to a float.
        """

        # TODO: Do a little string pre-processing to detect cases like "--1"?

        try:
            float(s)
            return True
        except ValueError:
            return False

    def is_int(self,
               s: str) -> bool:
        """
        Determines if the given string can immediately be converted to an integer value.
        :param s: The string to be checked.
        :return: Boolean denoting whether the string can be converted to a integer.
        """

        try:
            int(s)
            return True
        except ValueError:
            return False

    def has_float_word(self,
                       words: List[str]) -> Tuple[bool, str]:
        """
        Determines if the given list of words contains one that indicates a float value is present.
        :param words: The list of strings/words to be checked.
        :return: A boolean denoting if the list of words has a term denoting a float, as well as that term as a string if it exists
        """

        for w in words:
            if w in self.decimal_denoters:
                return True, w
        return False, ''

    def has_number_range(self,
                         words: List[str]) -> Tuple[bool, str]:
        """
        Checks if a list of words has a word denoting a range of values is present.
        :param words: The list of words to check.
        :return: A boolean denoting the words contain a range, as well as what word signaled this.
        """

        for w in words:
            if w in self.range_denoters:
                return True, w
        return False, ''

    def get_number_range(self,
                         text: str) -> Tuple[str, type(None)]:
        """
        Checks if a list of words has a word denoting a range of values is present, and if so
        gets the corresponding range and range value.
        :param text: The text to check.
        :return: The range value and minimum/maximum of that range if found. Otherwise None.
        """

        for pattern in self.range_expressions:
            match = re.search(pattern, text)
            if match:
                return (match.group(2), match.group(1).split(), match.group(3).split())
        return None, None, None

    def has_unit_word(self,
                      words: List[str],
                      case_sensitive: bool) -> Tuple[bool, str]:
        """
        Checks if a list of words has a word denoting units are present.
        :param words: The list of words to check.
        :param case_sensitive: Whether the unit search should be case_sensitive
        :return: the original span of the unit word, as well as the unit itself
        """

        for gram_size in range(len(words)-1, 0, -1):
            for i in range(len(words) - gram_size + 1):
                gram = '_'.join(words[i:i+gram_size])
                if self.ureg.parse_unit_name(gram, case_sensitive=case_sensitive):
                    return (i,i+gram_size), gram
                # Also try removing the letter "s" when it is not at the end
                for j in range(gram_size - 1):
                    gram = '_'.join(words[i:i+j] + [words[i+j].rstrip('s')] + words[i+j+1:i+gram_size])
                    if self.ureg.parse_unit_name(gram, case_sensitive=case_sensitive):
                        return (i,i+gram_size), gram
        return None, None

    def number_formation(self,
                         number_words: List[str]) -> float:
        """
        Generates a single number from a list of words/numbers.
        :param number_words: The list of words to convert to a single number.
        :return: A float representing the number in the string.
        """

        numbers = []
        for number_word in number_words:
            if number_word in self.number_words:
                numbers.append(self.number_words[number_word])
            elif self.is_int(number_word):
                numbers.append(int(number_word))
            elif self.is_float(number_word):
                numbers.append(float(number_word))
        if len(numbers) == 4:
            return (numbers[0] * numbers[1]) + numbers[2] + numbers[3]
        elif len(numbers) == 3:
            return numbers[0] * numbers[1] + numbers[2]
        elif len(numbers) == 2:
            if 100 in numbers:
                return numbers[0] * numbers[1]
            else:
                return numbers[0] + numbers[1]
        else:
            return numbers[0]

    def get_decimal_sum(self,
                        decimal_digit_words: List[str],
                        as_float: bool = True) -> Union[float, int]:
        """
        Converts a list of words to a decimal sum.
        :param decimal_digit_words: The list of words to convert to a decimal value.
        :param as_float: Optional param specifying whether the final value should contain the decimal point or not.
        :return: The value denoted by the given words.
        """

        decimal_number_str = []
        for dec_word in decimal_digit_words:
            if (dec_word not in self.decimal_words):
                return 0
            else:
                decimal_number_str.append(self.number_words[dec_word])
        if as_float:
            final_decimal_string = '0.' + ''.join(map(str, decimal_number_str))
            return float(final_decimal_string)
        else:
            final_decimal_string = ''.join(map(str, decimal_number_str))
            return int(final_decimal_string)

    def get_integral_sum(self,
                         clean_numbers: List[str]) -> int:
        """
        Converts a list of words to an integer number.
        Assumes these numbers would be to the right of a decimal point.
        :param clean_numbers: The list of numbers to convert to the integer value.
        :return: The value denoted by the given words.
        """

        total_sum = 0

        # hack for now, better way TODO
        if len(clean_numbers) == 1:
            if clean_numbers[0] in self.number_words:
                total_sum += self.number_words[clean_numbers[0]]
            elif self.is_int(clean_numbers[0]):
                total_sum += int(clean_numbers[0])
            elif self.is_float(clean_numbers[0]):
                total_sum += float(clean_numbers[0])

        else:
            billion_index = clean_numbers.index('billion') if 'billion' in clean_numbers else -1
            million_index = clean_numbers.index('million') if 'million' in clean_numbers else -1
            thousand_index = clean_numbers.index('thousand') if 'thousand' in clean_numbers else -1

            if (thousand_index > -1 and (thousand_index < million_index or thousand_index < billion_index)) \
                    or (million_index > -1 and million_index < billion_index):
                raise ValueError(
                    "Malformed number! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")

            if billion_index > -1:
                billion_multiplier = self.number_formation(clean_numbers[0:billion_index])
                total_sum += billion_multiplier * 1000000000

            if million_index > -1:
                if billion_index > -1:
                    million_multiplier = self.number_formation(clean_numbers[billion_index + 1:million_index])
                else:
                    million_multiplier = self.number_formation(clean_numbers[0:million_index])
                total_sum += million_multiplier * 1000000

            if thousand_index > -1:
                if million_index > -1:
                    thousand_multiplier = self.number_formation(clean_numbers[million_index + 1:thousand_index])
                elif billion_index > -1 and million_index == -1:
                    thousand_multiplier = self.number_formation(clean_numbers[billion_index + 1:thousand_index])
                else:
                    thousand_multiplier = self.number_formation(clean_numbers[0:thousand_index])
                total_sum += thousand_multiplier * 1000

            if thousand_index > -1 and thousand_index != len(clean_numbers) - 1:
                hundreds = self.number_formation(clean_numbers[thousand_index + 1:])
            elif million_index > -1 and million_index != len(clean_numbers) - 1:
                hundreds = self.number_formation(clean_numbers[million_index + 1:])
            elif billion_index > -1 and billion_index != len(clean_numbers) - 1:
                hundreds = self.number_formation(clean_numbers[billion_index + 1:])
            elif thousand_index == -1 and million_index == -1 and billion_index == -1:
                hundreds = self.number_formation(clean_numbers)
            else:
                hundreds = 0
            total_sum += hundreds

        return total_sum
