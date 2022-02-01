"""
Num Parser

The code for this module has been adapted from the Word2Number library:
https://github.com/akshaynagpal/w2n

As such, we do not claim to have written everything contained in this file, and many thanks go to the original authors.

ASSUMPTIONS:
1. We assume the use of the American number system and its associated standards.
2. We assume only one sentence as a time will be provided to the parser.

"""

from pint import UnitRegistry
from typing import Union, List, Tuple
import num_parse.word_to_num_values as word_to_num_values
from num_parse.RangeValue import RangeValue

class NumParser(object):
    def __init__(self):
        self.number_words = word_to_num_values.word_to_num_values
        self.decimal_words = word_to_num_values.decimal_words
        self.measures = word_to_num_values.measures
        self.relevant_words = []
        self.decimal_denoters = ['point', 'dot', '.']
        self.negative_denoters = ['negative', '-', 'neg', 'minus']
        self.range_denoters = ['to', 'through']        # TODO: Will want to do regex for this to detect more complex patterns in the string (e.g. "between X and Y")
        self.ureg = UnitRegistry()
        self.unit_denoters = [x for x in self.ureg._units]

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
        if type(number_string) is int or type(number_string) is float:
            return RangeValue(self.ureg.Quantity(number_string))

        #######################################################
        # Clean input string
        #######################################################
        normalized_input = self.normalize_input(number_string)

        #######################################################
        # Check cases where input is a raw number in a string
        #######################################################
        if self.is_int(normalized_input) or self.is_float(normalized_input):
            return RangeValue(self.ureg.Quantity(normalized_input))

        #######################################################
        # Split input into potentially relevant words
        #######################################################
        split_words = normalized_input.split()
        useful_words = [word for word in split_words if self.is_relevant_word(word)]
        clean_words = [self.clean_word(word) for word in useful_words]

        if len(useful_words) == 0:
            raise ValueError("No relevant words/numbers in the given string!")

        #######################################################
        # Check for unit words
        #######################################################
        # TODO: Add unit tests for unit parsing
        # TODO: Figure out how to handle plurals of the units (lemmatize the word first before checking if it's in the set?)
        # TODO: Figure out how to handles pre-fixed units (like cm, mm, etc.)
        has_units, unit_string = self.has_unit_word(clean_words)

        #######################################################
        # Handle value ranges
        #######################################################
        # TODO: Add unit tests RangeValue parsing
        is_num_range, range_denoter = self.has_number_range(clean_words)
        if is_num_range:
            # Mirror the float number code here, but split on the range_denoter word, and stick the values in a RangeValue
            max_number_words = clean_words[clean_words.index(range_denoter) + 1:]
            min_number_words = clean_words[:clean_words.index(range_denoter)]
            min_val = str(self.parse_num(' '.join(min_number_words))) if len(min_number_words) else ''
            max_val = str(self.parse_num(' '.join(max_number_words))) if len(max_number_words) else ''
            final_num = RangeValue(self.ureg.Quantity(min_val + unit_string), self.ureg.Quantity(max_val + unit_string))
            return final_num

        #######################################################
        # Check if the input is a negative number, as denoted by negative indicator at start of the string
        #######################################################
        isNegative = False
        for word in clean_words:
            if word in self.negative_denoters:
                isNegative = not isNegative
                clean_words.remove(word)
            else:
                break

        clean_numbers = clean_words
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

        return RangeValue(self.ureg.Quantity(str(final_num) + unit_string))

    def is_phrased_as_decimal_val(self,
                                  clean_words: List[str]) -> bool:
        return all(w in self.decimal_words for w in clean_words)

    def normalize_input(self,
                        number_string: str) -> str:
        """

        :param number_string:
        :return:
        """

        # Strip whitespace from beginning and end
        cleaned_string = number_string.strip()

        # Lowercase the string
        cleaned_string = cleaned_string.lower()

        # Remove commas
        cleaned_string = cleaned_string.replace(',', '')

        return cleaned_string

    def clean_word(self,
                   word: str) -> str:
        """
        Function to clean a single word into a usable form.
        :param word:
        :return:
        """
        return word.replace(',', '')

    def is_relevant_word(self,
                         word: str) -> bool:
        """

        :param word:
        :return:
        """

        return word in self.number_words.keys() or \
               word in self.relevant_words or \
               word in self.negative_denoters or \
               word in self.range_denoters or \
               word in self.unit_denoters or \
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

        # TODO: Do a little string pre-processing to detect cases like "--1"?

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

        :param words:
        :return:
        """

        for w in words:
            if w in self.range_denoters:
                return True, w
        return False, ''

    def has_unit_word(self,
                      words: List[str]) -> Tuple[bool, str]:
        """

        :param words:
        :return:
        """

        for w in words:
            if w in self.unit_denoters:
                return True, w
        return False, ''

    def number_formation(self,
                         number_words: List[str]) -> float:
        """

        :param number_words:
        :return:
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

        :param decimal_digit_words:
        :return:
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

        :param clean_numbers:
        :return:
        """

        total_sum = 0

        # hack for now, better way TODO
        if len(clean_numbers) == 1:
            if clean_numbers[0] in self.number_words:
                total_sum += self.number_words[clean_numbers[0]]
            elif self.is_int(clean_numbers[0]):
                total_sum += int(clean_numbers[0])

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
