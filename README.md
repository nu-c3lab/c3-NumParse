# c3-NumParse

This package provides a set of tools for parsing a number from a string.

## Installation

```commandline
pip install c3_NumParse
```

## Usage

```python
from num_parse.NumParser import NumParser
num_parser = NumParser()
num_parser.parse_num("4 million")  # returns 4000000
```

## Unit Tests

In order to run the unit tests, navigate to the `num_parse/tests` directory and run the following command:

```commandline
pytest -q
```