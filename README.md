# pybeerxml

A simple BeerXML parser for Python

[![CircleCI](https://circleci.com/gh/hotzenklotz/pybeerxml/tree/master.svg?style=svg)](https://circleci.com/gh/hotzenklotz/pybeerxml/tree/master)
[![PyPi Version](https://img.shields.io/pypi/v/pybeerxml.svg?style=flat-square)](https://pypi.python.org/pypi?:action=display&name=pybeerxml)

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

Unit test can be run with PyTest:

```
python setup.py test
```

## License

MIT
