from __future__ import annotations

from pydantic_xml import element

from pybeerxml.recipe import Recipe
from pybeerxml.xml_model import BeerXmlModel


class RecipesDocument(BeerXmlModel, tag="RECIPES"):
    """BeerXML document root containing one or more recipes."""

    recipes: list[Recipe] = element(tag="RECIPE", default_factory=list)
