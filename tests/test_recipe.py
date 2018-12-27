import pytest
from pybeerxml.recipe import Recipe

def test_setters():
  "setters for og, fg, ibu, abv, color should be ignored, since these are calculated properties"

  recipe = Recipe()

  recipe.og = 1.10
  assert(recipe.og == 1.0)

  recipe.fg = 1.10
  assert(recipe.fg == 1.0)

  recipe.abv = 1.10
  assert(recipe.abv == 0.0)

  recipe.ibu = 1.10
  assert(recipe.ibu == 0.0)

  recipe.color = 1.10
  assert(recipe.color == 0.0)
