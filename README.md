# pybeerxml

A simple BeerXML parser for Python

[![PyPi Version](https://img.shields.io/pypi/v/pybeerxml.svg?style=flat-square)](https://pypi.python.org/pypi?:action=display&name=pybeerxml)
[![Build Status](https://img.shields.io/github/workflow/status/hotzenklotz/pybeerxml/Test%20and%20Lint/master)](https://github.com/hotzenklotz/pybeerxml/actions?query=branch%3Amaster+workflow%3A%22Test+and+Lint%22)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


Parses all recipes within a BeerXML file and returns `Recipe` objects containing all ingredients,
style information and metadata. OG, FG, ABV and IBU are calculated from the ingredient list. (your
milage may vary)

## Installation

```
pip install pybeerxml
```

## Usage

```
from pybeerxml import Parser

path_to_beerxml_file = "/tmp/SimcoeIPA.beerxml"

parser = Parser()
recipes = parser.parse(path_to_beerxml_file)

for recipe in recipes:

    # some general recipe properties
    print(recipe.name)
    print(recipe.brewer)

    # calculated properties
    print(recipe.og)
    print(recipe.fg)
    print(recipe.ibu)
    print(recipe.abv)

    # iterate over the ingredients
    for hop in recipe.hops:
        print(hop.name)

    for fermentable in recipe.fermentables:
        print(fermentable.name)

    for yeast in recipe.yeasts:
        print(yeast.name)
        
    for misc in recipe.miscs:
        print(misc.name)
```

## Testing

Unit tests can be run with PyTest:

```
python -m pytest tests
```

## Contributing / Development
Community contributions are welcome.

Dependency management is handled through [Poetry](https://python-poetry.org/):

```
pip install poetry

poetry install
```

Make sure to Test, Lint, Format, & Type-Check your code before sending a pull request:
```
python -m pytest tests
python -m pylint pybeerxml
python -m black pybeerxml
python -m mypy pybeerxml
```

## License

MIT
