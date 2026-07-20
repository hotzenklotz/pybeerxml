---
title: Getting Started
description: Install pybeerxml and parse your first BeerXML recipe file
---

# Getting Started

## Installation

Install pybeerxml from PyPI:

```
pip install pybeerxml
```

Or with [uv](https://docs.astral.sh/uv/):

```
uv add pybeerxml
```

## Parsing a file

Pass the path to a `.beerxml` file to `Parser.parse()`. A single file can contain multiple recipes; the method always returns a list.

```python
from pybeerxml import Parser

parser = Parser()
recipes = parser.parse("/path/to/recipe.beerxml")

recipe = recipes[0]
print(recipe.name)    # e.g. "Simcoe IPA"
print(recipe.brewer)  # e.g. "Joe Smith"
```

## Parsing from a string

If you already have the XML content in memory, use `parse_from_string()`:

```python
from pybeerxml import Parser

xml = open("recipe.beerxml").read()

parser = Parser()
recipes = parser.parse_from_string(xml)
```

## Calculated vs. stored values

BeerXML files may or may not include pre-calculated values for OG, FG, IBU, ABV, and colour. pybeerxml always exposes both:

| Property | Stored value | Calculated fallback |
|----------|-------------|---------------------|
| `recipe.og` | `recipe.og_` (from XML if present) | `recipe.og_calculated` |
| `recipe.fg` | `recipe.fg_` (from XML if present) | `recipe.fg_calculated` |
| `recipe.ibu` | `recipe.ibu_` (from XML if present) | `recipe.ibu_calculated` |
| `recipe.abv` | `recipe.abv_` (from XML if present) | `recipe.abv_calculated` |
| `recipe.color` | `recipe.color_` (from XML if present) | `recipe.color_calculated` |

The plain properties (`recipe.og`, `recipe.ibu`, etc.) return the stored XML value when available, and automatically fall back to the calculated value otherwise. The `_calculated` variants always compute from ingredients regardless. The trailing-underscore fields (`og_`, `fg_`, `ibu_`, `abv_`, `color_`) hold exactly the value stored in the XML — or `None` when the XML did not provide one — and are the only variants written back during serialization.

```python
# Uses stored OG from XML, or calculates from fermentables if missing
print(recipe.og)

# The stored OG from the XML (None if absent)
print(recipe.og_)

# Always calculated from the fermentable bill
print(recipe.og_calculated)

# Gravity in degrees Plato
print(recipe.og_plato)
print(recipe.og_calculated_plato)
```

## Serializing recipes

The `Serializer` class writes recipes back to BeerXML. Only stored values are serialized — calculated properties are never written to the XML.

```python
from pybeerxml import Parser, Serializer

parser = Parser()
recipes = parser.parse("/path/to/recipe.beerxml")

serializer = Serializer()

# Write to a file
serializer.serialize(recipes, "/path/to/copy.beerxml")

# Or to a string
xml_string = serializer.serialize_to_string(recipes)
```

Since all models are pydantic models, recipes can be built programmatically and serialized:

```python
from pybeerxml import Serializer
from pybeerxml.recipe import Recipe
from pybeerxml.hop import Hop

recipe = Recipe(name="My IPA", batch_size=20.0)
recipe.hops.append(Hop(name="Simcoe", alpha=13.0, amount=0.05, use="boil", time=60))

print(recipe.og_calculated)   # calculated from the ingredient list

xml_string = Serializer().serialize_to_string(recipe)
```

Fields left as `None` are omitted from the output, and boolean fields are emitted as `TRUE` / `FALSE` per the BeerXML spec.

## Working with ingredients

```python
recipe = recipes[0]

for hop in recipe.hops:
    print(f"{hop.name}: {hop.alpha}% AA, {hop.amount * 1000:.0f}g, {hop.time:.0f} min")

for fermentable in recipe.fermentables:
    print(f"{fermentable.name}: {fermentable.amount}kg ({fermentable.addition})")

for yeast in recipe.yeasts:
    print(f"{yeast.name}: {yeast.attenuation}% attenuation")

for misc in recipe.miscs:
    print(f"{misc.name}: {misc.use}")
```

## Mash steps

```python
if recipe.mash:
    print(recipe.mash.name)
    for step in recipe.mash.steps:
        print(f"  {step.name}: {step.step_temp}°C for {step.step_time} min")
```

## IBU methods

By default, `ibu_calculated` uses the **Tinseth** formula. The Rager formula is available directly on each hop:

```python
hop = recipe.hops[0]
ibu_tinseth = hop.bitterness("tinseth", recipe.og_calculated, recipe.batch_size)
ibu_rager   = hop.bitterness("rager",   recipe.og_calculated, recipe.batch_size)
```

## Development setup

Clone the repo and install dependencies with [uv](https://docs.astral.sh/uv/):

```
git clone https://github.com/hotzenklotz/pybeerxml.git
cd pybeerxml
uv sync
```

Run the test suite:

```
uv run pytest
```

Lint, format, and type-check before submitting a pull request:

```
uv run ruff format .
uv run ruff check .
uv run ty check pybeerxml
```
