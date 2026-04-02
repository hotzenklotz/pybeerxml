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
| `recipe.og` | From XML if present | `recipe.og_calculated` |
| `recipe.fg` | From XML if present | `recipe.fg_calculated` |
| `recipe.ibu` | From XML if present | `recipe.ibu_calculated` |
| `recipe.abv` | From XML if present | `recipe.abv_calculated` |
| `recipe.color` | From XML if present | `recipe.color_calculated` |

The plain properties (`recipe.og`, `recipe.ibu`, etc.) return the stored XML value when available, and automatically fall back to the calculated value otherwise. The `_calculated` variants always compute from ingredients regardless.

```python
# Uses stored OG from XML, or calculates from fermentables if missing
print(recipe.og)

# Always calculated from the fermentable bill
print(recipe.og_calculated)

# Gravity in degrees Plato
print(recipe.og_plato)
print(recipe.og_calculated_plato)
```

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
