"""Compatibility tests for publicly published BeerXML recipe corpora."""

from pathlib import Path

import pytest

from pybeerxml.parser import Parser, Recipe

FIXTURE_DIRECTORY = Path(__file__).parent / "fixtures" / "public"
PUBLIC_RECIPE_FILES = tuple(sorted(FIXTURE_DIRECTORY.glob("*.xml")))


@pytest.mark.parametrize("recipe_file", PUBLIC_RECIPE_FILES, ids=lambda path: path.stem)
def test_public_recipe_corpus_parses(recipe_file: Path) -> None:
    """Every publicly sourced fixture must parse into at least one recipe."""
    recipes = Parser().parse(str(recipe_file))

    assert recipes
    assert all(isinstance(recipe, Recipe) for recipe in recipes)
    assert all(recipe.name for recipe in recipes)


def test_beerxml_1_0_software_generated_examples_are_complete() -> None:
    """The official BeerXML 1.0 sample corpus retains all four recipes."""
    fixture = FIXTURE_DIRECTORY / "beerxml-1.0-software-generated-examples.xml"

    assert [recipe.name for recipe in Parser().parse(str(fixture))] == [
        "Burton Ale",
        "Dry Stout",
        "Porter",
        "Wit",
    ]


def test_brewtarget_default_content_recipes_are_complete() -> None:
    """The Brewtarget default-content extract retains its 29 recipes."""
    fixture = FIXTURE_DIRECTORY / "brewtarget-default-recipes.xml"
    recipes = Parser().parse(str(fixture))

    assert len(recipes) == 29
    assert [recipes[0].name, recipes[-1].name] == [
        "Bt: American Barleywine",
        "Bt: Weizen - Extract",
    ]
