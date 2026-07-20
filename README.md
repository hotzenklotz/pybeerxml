# pybeerxml

A simple BeerXML parser and serializer for Python

[![PyPi Version](https://img.shields.io/pypi/v/pybeerxml.svg?style=flat-square)](https://pypi.python.org/pypi?:action=display&name=pybeerxml)
[![Build Status](https://img.shields.io/github/actions/workflow/status/hotzenklotz/pybeerxml/test_lint.yaml?branch=master&style=flat-square)](https://github.com/hotzenklotz/pybeerxml/actions/workflows/test_lint.yaml)
[![Code Style](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square)](https://github.com/astral-sh/ruff)
[![Docs](https://img.shields.io/badge/docs-pybeerxml.onrender.com-blue?style=flat-square)](https://pybeerxml.onrender.com/)


Parses all recipes within a BeerXML file and returns `Recipe` objects containing all ingredients,
style information and metadata. OG, FG, ABV and IBU are calculated from the ingredient list. (your
milage may vary). Recipes can also be serialized back to BeerXML. All models are built on
[pydantic](https://docs.pydantic.dev/) and [pydantic-xml](https://pydantic-xml.readthedocs.io/).

## Installation

```
pip install pybeerxml
```

## Usage

Full documentation is available at [pybeerxml.onrender.com](https://pybeerxml.onrender.com/).

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

## Serialization

Write recipes back to BeerXML with the `Serializer` class. Only values stored in the XML-backed
fields are written — calculated properties (`og_calculated`, `og_plato`, etc.) are never serialized.
The stored values for OG, FG, IBU, ABV and color live in the trailing-underscore fields `og_`,
`fg_`, `ibu_`, `abv_` and `color_`.

```
from pybeerxml import Parser, Serializer

parser = Parser()
recipes = parser.parse("/tmp/SimcoeIPA.beerxml")

serializer = Serializer()

# write to a file
serializer.serialize(recipes, "/tmp/SimcoeIPA-copy.beerxml")

# or to a string
xml_string = serializer.serialize_to_string(recipes)
```

Since all models are pydantic models, you can also build recipes programmatically:

```
from pybeerxml import Serializer
from pybeerxml.recipe import Recipe
from pybeerxml.hop import Hop

recipe = Recipe(name="My IPA", batch_size=20.0)
recipe.hops.append(Hop(name="Simcoe", alpha=13.0, amount=0.05, use="boil", time=60))

print(recipe.og_calculated)

xml_string = Serializer().serialize_to_string(recipe)
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
