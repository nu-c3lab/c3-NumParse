import unittest
from num_parse.NumParser import NumParser

class TestNumParse(unittest.TestCase):

    def setUp(self):
        self.num_parser = NumParser()

    #######################################################
    # ONLY number words
    #######################################################

    def test_five(self):
        self.assertEqual(self.num_parser.parse_num('five'), 5)

    def test_eleven(self):
        self.assertEqual(self.num_parser.parse_num('eleven'), 11)

    def test_nineteen(self):
        self.assertEqual(self.num_parser.parse_num("nineteen"), 19)

    def test_hundred(self):
        self.assertEqual(self.num_parser.parse_num('hundred'), 100)

    def test_one_two_three(self):
        self.assertEqual(self.num_parser.parse_num('one two three'), 123)

    def test_one_hundred_and_forty_two(self):
        self.assertEqual(self.num_parser.parse_num('one hundred and forty two'), 142)

    def test_thousand(self):
        self.assertEqual(self.num_parser.parse_num('thousand'), 1000)

    def test_two_thousand_and_nineteen(self):
        self.assertEqual(self.num_parser.parse_num("two thousand and nineteen"), 2019)

    def test_million(self):
        self.assertEqual(self.num_parser.parse_num('million'), 1000000)

    def test_two_million_three_thousand_and_nineteen(self):
        self.assertEqual(self.num_parser.parse_num('two million three thousand and nineteen'), 2003019)

    def test_two_million_three_thousand_nine_hundred_and_eighty_four(self):
        self.assertEqual(self.num_parser.parse_num('two million three thousand nine hundred and eighty four'), 2003984)

    def test_three_million(self):
        self.assertEqual(self.num_parser.parse_num('three million'), 3000000)

    def test_one_hundred_twenty_three_million_four_hundred_fifty_six_thousand_seven_hundred_and_eighty_nine(self):
        self.assertEqual(self.num_parser.parse_num('one hundred twenty three million four hundred fifty six thousand seven hundred and eighty nine'), 123456789)

    def test_billion(self):
            self.assertEqual(self.num_parser.parse_num('billion'), 1000000000)

    def test_three_billion(self):
        self.assertEqual(self.num_parser.parse_num('three billion'), 3000000000)

    def test_nineteen_billion_and_nineteen(self):
        self.assertEqual(self.num_parser.parse_num('nineteen billion and nineteen'), 19000000019)

    def test_two_million_twenty_three_thousand_and_forty_nine(self):
        self.assertEqual(self.num_parser.parse_num('two million twenty three thousand and forty nine'), 2023049)

    #######################################################
    # ONLY number values
    #######################################################

    def test_112(self):
        self.assertEqual(self.num_parser.parse_num('112'), 112)

    def test_112_as_int(self):
        self.assertEqual(self.num_parser.parse_num(112), 112)

    def test_11211234(self):
        self.assertEqual(self.num_parser.parse_num('11211234'), 11211234)

    def test_11211234_as_int(self):
        self.assertEqual(self.num_parser.parse_num(11211234), 11211234)

    #######################################################
    # Mixed number words AND number values
    #######################################################

    def test_4_million(self):
        self.assertEqual(self.num_parser.parse_num('4 million'), 4000000)

    def test_812_million(self):
        self.assertEqual(self.num_parser.parse_num('812 million'), 812000000)

    def test_1000_million(self):
        self.assertEqual(self.num_parser.parse_num('1000 million'), 1000000000)

    #######################################################
    # Decimal Values
    #######################################################

    def test_point(self):
        self.assertEqual(self.num_parser.parse_num('point'), 0)

    def test_two_point_three(self):
        self.assertEqual(self.num_parser.parse_num('two point three'), 2.3)

    def test_point_one(self):
        self.assertEqual(self.num_parser.parse_num('point one'), 0.1)

    def test_point_nineteen(self):
        self.assertEqual(self.num_parser.parse_num('point nineteen'), 0.19)

    def test_nine_point_nine_nine_nine(self):
        self.assertEqual(self.num_parser.parse_num('nine point nine nine nine'), 9.999)

    def test_two_million_twenty_three_thousand_and_forty_nine_point_two_three_six_nine(self):
        self.assertEqual(self.num_parser.parse_num('two million twenty three thousand and forty nine point two three six nine'), 2023049.2369)

    def test_one_billion_two_million_twenty_three_thousand_and_forty_nine_point_two_three_six_nine(self):
        self.assertEqual(self.num_parser.parse_num('one billion two million twenty three thousand and forty nine point two three six nine'), 1002023049.2369)

    #######################################################
    # Negative Values
    #######################################################

    def test_negative_one(self):
        self.assertEqual(self.num_parser.parse_num('negative one'), -1)

    def test_negative_1(self):
        self.assertEqual(self.num_parser.parse_num('negative 1'), -1)

    def test_minus_one(self):
        self.assertEqual(self.num_parser.parse_num('minus one'), -1)

    def test_minus_1(self):
        self.assertEqual(self.num_parser.parse_num('minus 1'), -1)

    #######################################################
    # Numbers words with dashes
    #######################################################

    def test_one_hundred_thirty_dash_five(self):
        self.assertEqual(self.num_parser.parse_num('one hundred thirty-five'), 135)

    #######################################################
    # Commas
    #######################################################

    def test_1_000_000(self):
        self.assertEqual(self.num_parser.parse_num('1,000,000'), 1000000)

    def test_1_000(self):
        self.assertEqual(self.num_parser.parse_num('1,000'), 1000)

    def test_124_000(self):
        self.assertEqual(self.num_parser.parse_num('124,000'), 124000)

    #######################################################
    # Value Ranges
    #######################################################

    # def test_one_to_five(self):
    #     self.assertEqual(self.num_parser.parse_num('one to five'), Number(1,5))

    #######################################################
    # Testing Errors
    #######################################################
    def test_errors(self):
        self.assertRaises(ValueError, self.num_parser.parse_num, '112-')
        self.assertRaises(ValueError, self.num_parser.parse_num, '-')
        self.assertRaises(ValueError, self.num_parser.parse_num, 'on')
        self.assertRaises(ValueError, self.num_parser.parse_num, 'million million')
        self.assertRaises(ValueError, self.num_parser.parse_num, 'three million million')
        self.assertRaises(ValueError, self.num_parser.parse_num, 'million four million')
        self.assertRaises(ValueError, self.num_parser.parse_num, 'thousand million')
        self.assertRaises(ValueError, self.num_parser.parse_num, 'one billion point two million twenty three thousand and forty nine point two three six nine')
