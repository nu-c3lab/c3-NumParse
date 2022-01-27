"""
Num Parser

The code for this module has been adapted from the Word2Number library:
https://github.com/akshaynagpal/w2n

As such, we do not claim to have written everything contained in this file, and many thanks go to the original authors.

ASSUMPTIONS:
1. We assume the use of the American number system and its associated standards.
2. We assume only one sentence as a time will be provided to the parser.

"""

from typing import Union, List
from word2number import w2n
import num_parse.word_to_num_values as word_to_num_values

class NumParser(object):
    def __init__(self):
        self.number_words = word_to_num_values.word_to_num_values
        self.decimal_words = word_to_num_values.decimal_words
        self.measures = word_to_num_values.measures
        self.relevant_words = []
        self.decimal_denoters = ['point', 'dot', '.']
        self.negative_denoters = ['negative', '-', 'neg']

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
        clean_input = self.clean_input(number_string)

        #######################################################
        # Check cases where input is a raw number in a string
        #######################################################
        if clean_input.isdigit():
            return int(clean_input)

        if self.is_float(clean_input):
            return float(clean_input)

        #######################################################
        # Split input into potentially relevant words
        #######################################################
        split_words = clean_input.split()
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
        clean_decimal_numbers = []

        # Error message if the user enters invalid input!
        if len(clean_numbers) == 0:
            raise ValueError("No valid number words found! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")

         # Error if user enters decimal point, thousand, million, billion twice
        if clean_numbers.count('thousand') > 1 or clean_numbers.count('million') > 1 or clean_numbers.count('billion') > 1 or clean_numbers.count('point') > 1:
            raise ValueError("Redundant number word! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")

        if clean_numbers.count('point') == 1:
            clean_decimal_numbers = clean_numbers[clean_numbers.index('point') + 1:]
            clean_numbers = clean_numbers[:clean_numbers.index('point')]

        total_sum = 0  # storing the number to be returned

        if len(clean_numbers) > 0:
            integral_sum = self.get_integral_sum(clean_numbers)
            total_sum += integral_sum

        # Adding decimal part to total_sum (if exists)
        if len(clean_decimal_numbers) > 0:
            decimal_sum = self.get_decimal_sum(clean_decimal_numbers)
            total_sum += decimal_sum

        #######################################################
        # Compose the final value
        #######################################################

        # Handle negative numbers
        if isNegative:
            total_sum = -total_sum

        return total_sum

    def clean_input(self,
                    number_string: str) -> str:
        """

        :param number_string:
        :return:
        """

        # Strip whitespace from beginning and end
        cleaned_string = number_string.strip()

        # Lowercase the string
        cleaned_string = cleaned_string.lower()

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
        return word in self.number_words.keys() or \
               word in self.relevant_words or \
               word in self.negative_denoters


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

    def number_formation(self,
                         number_words: List[str]) -> float:
        """

        :param number_words:
        :return:
        """
        numbers = []
        for number_word in number_words:
            numbers.append(self.number_words[number_word])
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
                        decimal_digit_words: List[str]) -> float:
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
        final_decimal_string = '0.' + ''.join(map(str, decimal_number_str))
        return float(final_decimal_string)

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
