# pybeerxml

A simple BeerXML parser for Python

[![PyPi Version](https://img.shields.io/pypi/v/pybeerxml.svg?style=flat-square)](https://pypi.python.org/pypi?:action=display&name=pybeerxml)
[![Build Status](https://img.shields.io/github/actions/workflow/status/hotzenklotz/pybeerxml/test_lint.yaml?branch=master&style=flat-square)](https://github.com/hotzenklotz/pybeerxml/actions/workflows/test_lint.yaml)
[![Code Style](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square)](https://github.com/astral-sh/ruff)


Parses all recipes within a BeerXML file and returns `Recipe` objects containing all ingredients,
style information and metadata. OG, FG, ABV and IBU are calculated from the ingredient list. (your
milage may vary)

## Installation

```
pip install pybeerxml
```

## Usage

```
from pybeerxml.parser import Parser

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

Unit tests can be run with pytest:

```
uv run pytest
```

## Contributing / Development

Community contributions are welcome.

Install [uv](https://docs.astral.sh/uv/), then sync dependencies:

```
uv sync
```

Make sure to test, lint, format, and type-check your code before sending a pull request:

```
uv run pytest
uv run ruff format .
uv run ruff check .
uv run ty check pybeerxml
```

## License

MIT
