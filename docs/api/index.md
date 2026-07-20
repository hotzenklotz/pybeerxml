---
title: API Reference
description: Full API reference for pybeerxml
---

# API Reference

pybeerxml exposes two entry points — the `Parser` and `Serializer` classes — which convert between BeerXML documents and `Recipe` objects. Each `Recipe` holds typed ingredient and metadata objects. All models are [pydantic-xml](https://pydantic-xml.readthedocs.io/) models, so they can be validated, constructed programmatically, and serialized.

## Class overview

| Class | Description |
|-------|-------------|
| [`Parser`](parser.md) | Reads BeerXML files or strings and returns `Recipe` objects |
| [`Serializer`](serializer.md) | Writes `Recipe` objects to BeerXML files or strings |
| [`Recipe`](recipe.md) | A complete beer recipe with calculated properties |
| [`Fermentable`](fermentable.md) | A grain, extract, sugar, or adjunct |
| [`Hop`](hop.md) | A hop addition with bitterness calculation |
| [`Yeast`](yeast.md) | A yeast strain |
| [`Mash` / `MashStep`](mash.md) | Mash profile and individual temperature steps |
| [`Misc`](misc-models.md#misc) | A miscellaneous ingredient (finings, spices, etc.) |
| [`Style`](misc-models.md#style) | Beer style guidelines |
| [`Water`](misc-models.md#water) | Water chemistry profile |
| [`Equipment`](misc-models.md#equipment) | Brewing equipment profile |

## Import paths

```python
from pybeerxml import Parser            # main entry points
from pybeerxml import Serializer
from pybeerxml.recipe import Recipe
from pybeerxml.fermentable import Fermentable
from pybeerxml.hop import Hop
from pybeerxml.yeast import Yeast
from pybeerxml.mash import Mash
from pybeerxml.mash_step import MashStep
from pybeerxml.misc import Misc
from pybeerxml.style import Style
from pybeerxml.water import Water
from pybeerxml.equipment import Equipment
```

## Stored vs. calculated values

The five brewing metrics expose the stored XML value separately from the calculated one. The trailing-underscore fields hold the raw XML values and are the only ones serialized:

| Fallback property | Stored field (serialized) | Calculated property |
|-------------------|---------------------------|---------------------|
| `recipe.og` | `recipe.og_` | `recipe.og_calculated` |
| `recipe.fg` | `recipe.fg_` | `recipe.fg_calculated` |
| `recipe.ibu` | `recipe.ibu_` | `recipe.ibu_calculated` |
| `recipe.abv` | `recipe.abv_` | `recipe.abv_calculated` |
| `recipe.color` | `recipe.color_` | `recipe.color_calculated` |
