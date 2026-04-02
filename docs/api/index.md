---
title: API Reference
description: Full API reference for pybeerxml
---

# API Reference

pybeerxml exposes one entry point — the `Parser` class — which returns `Recipe` objects. Each `Recipe` holds typed ingredient and metadata objects.

## Class overview

| Class | Description |
|-------|-------------|
| [`Parser`](parser.md) | Reads BeerXML files or strings and returns `Recipe` objects |
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
from pybeerxml import Parser          # main entry point
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
