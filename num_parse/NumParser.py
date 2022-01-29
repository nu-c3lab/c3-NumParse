"""
Num Parser

The code for this module has been adapted from the Word2Number library:
https://github.com/akshaynagpal/w2n

As such, we do not claim to have written everything contained in this file, and many thanks go to the original authors.

ASSUMPTIONS:
1. We assume the use of the American number system and its associated standards.
2. We assume only one sentence as a time will be provided to the parser.

"""

from typing import Union, List, Tuple
from word2number import w2n
import num_parse.word_to_num_values as word_to_num_values

class NumParser(object):
    def __init__(self):
        self.number_words = word_to_num_values.word_to_num_values
        self.decimal_words = word_to_num_values.decimal_words
        self.measures = word_to_num_values.measures
        self.relevant_words = []
        self.decimal_denoters = ['point', 'dot', '.']
        self.negative_denoters = ['negative', '-', 'neg', 'minus']

    def parse_num(self,
                  number_string: str) -> Union[int, float]:
        """
        Parses a given string containing a numeric value into the raw numeric value.
        :param number_string: A string containing a number.
        :return: The raw numeric value in the given string.
        """

        # FOR COMPARISON PURPOSES ONLY
        # return w2n.word_to_num(number_string)

        #######################################################
        # Check cases where input is just a number value
        #######################################################
        if type(number_string) is int:
            return int(number_string)

        if type(number_string) is float:
            return float(number_string)

        #######################################################
        # Clean input string
        #######################################################
        normalized_input = self.normalize_input(number_string)

        #######################################################
        # Check cases where input is a raw number in a string
        #######################################################
        if normalized_input.isdigit():
            return int(normalized_input)

        if self.is_float(normalized_input):
            return float(normalized_input)

        #######################################################
        # Split input into potentially relevant words
        #######################################################
        split_words = normalized_input.split()
        useful_words = [word for word in split_words if self.is_relevant_word(word)]
        clean_words = [self.clean_word(word) for word in useful_words]

        if len(useful_words) == 0:
            raise ValueError("No relevant words/numbers in the given string!")

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

        #######################################################
        # TODO: Check for unit words
        #######################################################

        clean_numbers = clean_words
        is_float_num, dec_word = self.has_float_word(clean_numbers)
        is_num_range = False
        units = ''

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

        # TODO: CASE 2: NUMBER RANGE

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

        return final_num

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
               word.isdigit() or \
               self.is_float(word)


    def is_float(self,
                 s: str) -> bool:
        """
        Determines if the given string can immediately be converted to a float value.
        :param s: A string value.
        :return: Boolean denoting whether the string can be converted to a float.
        """

        try:
            float(s)
        except ValueError:
            return False

    def has_float_word(self,
                       words: List[str]) -> Tuple[bool, str]:
        """

        :param words:
        :return: A boolean denoting if the list of words has a term denoting a float, as well as that term as a string if it exists
        """

        for w in words:
            if w in self.decimal_denoters:
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
            elif number_word.isdigit():
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
            total_sum += self.number_words[clean_numbers[0]]

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