---
title: pybeerxml
description: A BeerXML parser and serializer for Python
---

# pybeerxml

[![PyPi Version](https://img.shields.io/pypi/v/pybeerxml.svg?style=flat-square)](https://pypi.python.org/pypi?:action=display&name=pybeerxml)
[![Build Status](https://img.shields.io/github/actions/workflow/status/hotzenklotz/pybeerxml/test_lint.yaml?branch=master&style=flat-square)](https://github.com/hotzenklotz/pybeerxml/actions/workflows/test_lint.yaml)
[![Docs](https://img.shields.io/badge/docs-pybeerxml.onrender.com-blue?style=flat-square)](https://pybeerxml.onrender.com/)

**pybeerxml** is a Python library for parsing and serializing [BeerXML](http://www.beerxml.com/) recipe files. It reads `.beerxml` documents into structured `Recipe` objects and can write those objects back into valid BeerXML.

## Features

- Parse BeerXML files or XML strings
- Serialize one or more recipes back to BeerXML
- Access hops, fermentables, yeasts, miscs, mash steps, equipment, and style
- Automatic calculation of OG, FG, ABV, IBU, and colour when not provided in the XML
- Supports both Tinseth and Rager IBU formulas
- Gravity values available in both SG and degrees Plato

## Quick Example

```python
from pybeerxml import Parser, Serializer

parser = Parser()
serializer = Serializer()
recipes = parser.parse("/path/to/recipe.beerxml")

for recipe in recipes:
    print(recipe.name)       # "Simcoe IPA"
    print(recipe.og)         # 1.0756
    print(recipe.ibu)        # 64.3
    print(recipe.abv)        # 6.8

    for hop in recipe.hops:
        print(hop.name, hop.alpha)

    for fermentable in recipe.fermentables:
        print(fermentable.name, fermentable.amount)

xml = serializer.serialize(recipes)
serializer.write(recipes, "/path/to/output.beerxml")
```

## Installation

```
pip install pybeerxml
```

See [Getting Started](getting-started.md) for a full walkthrough.
