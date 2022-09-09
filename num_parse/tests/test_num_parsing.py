import unittest
from num_parse.NumParser import NumParser
from num_parse.RangeValue import RangeValue

class TestNumParse(unittest.TestCase):

    def setUp(self):
        self.num_parser = NumParser()
        self.Q_ = self.num_parser.Quantity

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

    def test_112_with_hyphen(self):
        self.assertEqual(self.num_parser.parse_num('112-'), 112)

    def test_11211234(self):
        self.assertEqual(self.num_parser.parse_num('11211234'), 11211234)

    def test_11211234_as_int(self):
        self.assertEqual(self.num_parser.parse_num(11211234), 11211234)

    #######################################################
    # Mixed number words AND number values
    #######################################################

    def test_4_million(self):
        self.assertEqual(self.num_parser.parse_num('4 million'), 4000000)

    def test_4_point_5_million(self):
        self.assertEqual(self.num_parser.parse_num('4.5 million'), 4500000)

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

    def test_negative_one_million(self):
        self.assertEqual(self.num_parser.parse_num('negative one million'), -1000000)

    def test_negative_1000000(self):
        self.assertEqual(self.num_parser.parse_num('negative 1000000'), -1000000)

    def test_negative_1000000_with_commas(self):
        self.assertEqual(self.num_parser.parse_num('negative 1,000,000'), -1000000)

    def test_negative_4_million(self):
        self.assertEqual(self.num_parser.parse_num('negative 4 million'), -4000000)

    def test_negative_sign_4_million(self):
        self.assertEqual(self.num_parser.parse_num('-4 million'), -4000000)

    def test_negative_sign_4_point_5_million(self):
        self.assertEqual(self.num_parser.parse_num('-4.5 million'), -4500000)

    def test_minus_one(self):
        self.assertEqual(self.num_parser.parse_num('minus one'), -1)

    def test_minus_1(self):
        self.assertEqual(self.num_parser.parse_num('minus 1'), -1)

    def test_negative_sign_negative_sign_1(self):
        self.assertEqual(self.num_parser.parse_num('--1'), 1)

    def test_negative_sign_space_negative_sign_1(self):
        self.assertEqual(self.num_parser.parse_num('- -1'), 1)

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

    def test_one_to_five(self):
        rv = RangeValue(self.Q_(1), self.Q_(5))
        self.assertEqual(self.num_parser.parse_num('one to five'), rv)

    def test_one_through_five(self):
        rv = RangeValue(self.Q_(1), self.Q_(5))
        self.assertEqual(self.num_parser.parse_num('one through five'), rv)

    def test_1_to_5(self):
        rv = RangeValue(self.Q_(1), self.Q_(5))
        self.assertEqual(self.num_parser.parse_num('1 to 5'), rv)

    def test_1_through_5(self):
        rv = RangeValue(self.Q_(1), self.Q_(5))
        self.assertEqual(self.num_parser.parse_num('1 through 5'), rv)

    def test_1_to_five(self):
        rv = RangeValue(self.Q_(1), self.Q_(5))
        self.assertEqual(self.num_parser.parse_num('1 to five'), rv)

    def test_1_through_five(self):
        rv = RangeValue(self.Q_(1), self.Q_(5))
        self.assertEqual(self.num_parser.parse_num('1 through five'), rv)

    def test_one_to_5(self):
        rv = RangeValue(self.Q_(1), self.Q_(5))
        self.assertEqual(self.num_parser.parse_num('one to 5'), rv)

    def test_one_through_5(self):
        rv = RangeValue(self.Q_(1), self.Q_(5))
        self.assertEqual(self.num_parser.parse_num('one to 5'), rv)

    def test_negative_1_to_negative_5(self):
        rv = RangeValue(self.Q_(-1), self.Q_(-5))
        self.assertEqual(self.num_parser.parse_num('-1 to -5'), rv)

    def test_negative_1_through_negative_5(self):
        rv = RangeValue(self.Q_(-1), self.Q_(-5))
        self.assertEqual(self.num_parser.parse_num('-1 through -5'), rv)

    def test_negative_1_to_negative_5_v2(self):
        rv = RangeValue(self.Q_(-1), self.Q_(-5))
        self.assertEqual(self.num_parser.parse_num('negative 1 to negative 5'), rv)

    def test_negative_1_through_negative_5_v2(self):
        rv = RangeValue(self.Q_(-1), self.Q_(-5))
        self.assertEqual(self.num_parser.parse_num('negative 1 through negative 5'), rv)

    def test_negative_one_to_negative_five(self):
        rv = RangeValue(self.Q_(-1), self.Q_(-5))
        self.assertEqual(self.num_parser.parse_num('negative one to negative five'), rv)

    def test_negative_one_through_negative_five(self):
        rv = RangeValue(self.Q_(-1), self.Q_(-5))
        self.assertEqual(self.num_parser.parse_num('negative one through negative five'), rv)

    def test_0_to_72(self):
        rv = RangeValue(self.Q_(0), self.Q_(72))
        self.assertEqual(self.num_parser.parse_num('0 to 72'), rv)

    def test_0_through_72(self):
        rv = RangeValue(self.Q_(0), self.Q_(72))
        self.assertEqual(self.num_parser.parse_num('0 through 72'), rv)

    def test_negative_72_to_0(self):
        rv = RangeValue(self.Q_(-72), self.Q_(0))
        self.assertEqual(self.num_parser.parse_num('-72 to 0'), rv)

    def test_negative_72_through_0(self):
        rv = RangeValue(self.Q_(-72), self.Q_(0))
        self.assertEqual(self.num_parser.parse_num('-72 through 0'), rv)

    def test_12_hyphen_14(self):
        rv = RangeValue(self.Q_(12), self.Q_(14))
        self.assertEqual(self.num_parser.parse_num('12 - 14'), rv)

    def test_from_eight_until_ten(self):
        rv = RangeValue(self.Q_(8), self.Q_(10))
        self.assertEqual(self.num_parser.parse_num('from eight until ten'), rv)

    #######################################################
    # Units
    #######################################################

    def test_five_meters(self):
        rv = RangeValue(self.Q_(5, 'meters'))
        self.assertEqual(self.num_parser.parse_num('five meters'), rv)

    def test_5_meters(self):
        rv = RangeValue(self.Q_(5, 'meters'))
        self.assertEqual(self.num_parser.parse_num('5 meters'), rv)

    def test_5_m(self):
        rv = RangeValue(self.Q_(5, 'meters'))
        self.assertEqual(self.num_parser.parse_num('5 m'), rv)

    def test_4_cm(self):
        rv = RangeValue(self.Q_(4, 'cm'))
        self.assertEqual(self.num_parser.parse_num('4 cm'), rv)

    def test_4_centimeters(self):
        rv = RangeValue(self.Q_(4, 'cm'))
        self.assertEqual(self.num_parser.parse_num('4 centimeters'), rv)

    def test_3_km(self):
        rv = RangeValue(self.Q_(3, 'km'))
        self.assertEqual(self.num_parser.parse_num('3 km'), rv)

    def test_3_kilometers(self):
        rv = RangeValue(self.Q_(3, 'km'))
        self.assertEqual(self.num_parser.parse_num('3 kilometers'), rv)

    def test_120_seconds(self):
        rv = RangeValue(self.Q_(120, 'seconds'))
        self.assertEqual(self.num_parser.parse_num('120 seconds'), rv)

    def test_120_s(self):
        rv = RangeValue(self.Q_(120, 's'))
        self.assertEqual(self.num_parser.parse_num('120 s'), rv)

    def test_12_000_ms(self):
        rv = RangeValue(self.Q_(12000, 'ms'))
        self.assertEqual(self.num_parser.parse_num('12,000 ms'), rv)

    def test_12_to_500_ms(self):
        rv = RangeValue(self.Q_(12, 'ms'), self.Q_(500, 'ms'))
        self.assertEqual(self.num_parser.parse_num('12 to 500 ms'), rv)

    def test_10_degrees_Fahrenheit(self):
        rv = RangeValue(self.Q_(10, 'degree_Fahrenheit'))
        self.assertEqual(self.num_parser.parse_num('10 Fahrenheit'), rv)

    def test_45_degrees_Fahrenheit(self):
        rv = RangeValue(self.Q_(45, 'degree_Fahrenheit'))
        self.assertEqual(self.num_parser.parse_num('45 degrees Fahrenheit'), rv)

    def test_45_degree_F(self):
        rv = RangeValue(self.Q_(45, 'degree_Fahrenheit'))
        self.assertEqual(self.num_parser.parse_num('45°F'), rv)

    def test_10_degrees_Celsius(self):
        rv = RangeValue(self.Q_(10, 'degree_Celsius'))
        self.assertEqual(self.num_parser.parse_num('10 Celsius'), rv)

    def test_10_to_20_celsius(self):
        rv = RangeValue(self.Q_(10), self.Q_(20, 'degree_Celsius'))
        self.assertEqual(self.num_parser.parse_num('10 to 20 celsius'), rv)

    def test_10_celsius_to_20_celsius(self):
        rv = RangeValue(self.Q_(10, 'degree_Celsius'), self.Q_(20, 'degree_Celsius'))
        self.assertEqual(self.num_parser.parse_num('10 celsius to 20 celsius'), rv)

    def test_1028_to_1220_km(self):
        rv = RangeValue(self.Q_(1028), self.Q_(1220, 'kilometers'))
        self.assertEqual(self.num_parser.parse_num('1028 to 1220 km'), rv)

    def test_1028_km_to_1220_km(self):
        rv = RangeValue(self.Q_(1028, 'kilometers'), self.Q_(1220, 'kilometers'))
        self.assertEqual(self.num_parser.parse_num('1028 km to 1220 km'), rv)

    def test_between_six_and_seven_years(self):
        rv = RangeValue(self.Q_(6, 'years'), self.Q_(7, 'years'))
        self.assertEqual(self.num_parser.parse_num('between six and seven years'), rv)

    def test_big_duration(self):
        rv = RangeValue(self.Q_(258803256086, 'seconds'))
        self.assertEqual(self.num_parser.parse_num('8 millenniums, 2 centuries, 6 decades, 4 years, 11 months, 3 weeks, 2 days, 5 hours, 51 minutes, and 16 seconds'), rv)

    def test_minutes_duration(self):
        rv = RangeValue(self.Q_(238, 'seconds'))
        self.assertEqual(self.num_parser.parse_num('3:58'), rv)

    #######################################################
    # Combination tests
    #######################################################

    def test_numbers_words_and_units(self):
        self.assertEqual(self.num_parser.parse_num("4 million miles"),
                         RangeValue(self.Q_(4000000, 'miles')))

    def test_dolla_dolla_bills_yall(self):
        self.assertEqual(self.num_parser.parse_num("5 dollars"),
                         RangeValue(self.Q_(5, 'dollars')))
        self.assertEqual(self.num_parser.parse_num("$11"),
                         RangeValue(self.Q_(11, 'dollars')))

    def test_a_dozen_kilos(self):
        self.assertEqual(self.num_parser.parse_num("a dozen kilos"),
                         RangeValue(self.Q_(12, 'kilograms')))

    def test_45_metric_tons(self):
        self.assertEqual(self.num_parser.parse_num("45 metric tons"),
                         RangeValue(self.Q_(45, 'metric_ton')))

    def test_45_thousand_metric_tons(self):
        self.assertEqual(self.num_parser.parse_num("45 thousand metric tons"),
                         RangeValue(self.Q_(45000, 'metric_ton')))

    def test_kips_per_square_inch(self):
        self.assertEqual(self.num_parser.parse_num("four hundred thirty five or four hundred sixty seven kips per square inch"),
                         RangeValue(self.Q_(435, 'kip_per_square_inch'), self.Q_(467, 'kip_per_square_inch')))

    def test_irrational_unit_conversion(self):
        self.assertEqual(self.num_parser.parse_num("2.2046226218487758 pounds"),
                         RangeValue(self.Q_(1, 'kilogram')))
        self.assertEqual(self.num_parser.parse_num("2.2046 pounds"),
                         RangeValue(self.Q_(1, 'kilogram')))
        self.assertNotEqual(self.num_parser.parse_num("2.205 pounds"),
                         RangeValue(self.Q_(1, 'kilogram')))

    def test_range_of_different_units(self):
        self.assertEqual(self.num_parser.parse_num("five hundred kilograms to fifteen hundred pounds"),
                         RangeValue(self.Q_(500, 'kilogram'), self.Q_(680.388555, 'kilogram')))

    def test_million_distribution(self):
        self.assertEqual(self.num_parser.parse_num("$519.2–520.9 million"),
                         RangeValue(self.Q_(519200000, 'dollar'), self.Q_(520900000, 'dollar')))


    #######################################################
    # TODO: More involved strings (e.g. "It has a value between five to ten")
    #######################################################


    #######################################################
    # Testing Errors
    #######################################################
    def test_errors(self):
        self.assertRaises(ValueError, self.num_parser.parse_num, '-')
        self.assertRaises(ValueError, self.num_parser.parse_num, 'on')
        self.assertRaises(ValueError, self.num_parser.parse_num, 'million million')
        self.assertRaises(ValueError, self.num_parser.parse_num, 'three million million')
        self.assertRaises(ValueError, self.num_parser.parse_num, 'million four million')
        self.assertRaises(ValueError, self.num_parser.parse_num, 'thousand million')
        self.assertRaises(ValueError, self.num_parser.parse_num, 'one billion point two million twenty three thousand and forty nine point two three six nine')
