# c3-NumParse

This package provides a set of tools for parsing a number from a string. It currently suppports:
- Parsing numeric values (e.g. "2410")
- Parsing number words (e.g. "one hundred forty five thousand two hundred three")
- Parsing negative numbers (e.g "negative fifty five")
- Parsing mixed numeric values and number words (e.g. "4 million")
- Parsing numeric ranges (e.g. "five to 10")
- Parsing units (e.g. "five miles", "8 to 10 hours")

These strings get parsed into a new `RangeValue` class which allows for ranges to be represented, 
and any values in this form to be compared against each other.

## Installation

```commandline
pip install NumParse
```

## Usage

```python
from num_parse.NumParser import NumParser
num_parser = NumParser()

num_parser.parse_num("4 million")           # returns 4000000
num_parser.parse_num("-135 thousand")       # returns -135000
num_parser.parse_num("2 m")                 # returns 2 meter
num_parser.parse_num("five to six hours")   # returns 5 to 6 hour
num_parser.parse_num("2 m") < num_parser.parse_num("2 in")  # returns False

```

## Unit Tests

In order to run the unit tests, navigate to the `num_parse/tests` directory and run the following command:

```commandline
pytest -q
```
