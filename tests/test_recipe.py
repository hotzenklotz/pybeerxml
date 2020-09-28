from pybeerxml.recipe import Recipe


def test_setters():
    # setters for og, fg, ibu, abv, color should be ignored, since these are calculated properties

    recipe = Recipe()

    try:
        recipe.og = 1.10
    except AttributeError:
        assert recipe.og == 1.0

    try:
        recipe.fg = 1.10
    except AttributeError:
        assert recipe.fg == 1.0

    try:
        recipe.abv = 1.10
    except AttributeError:
        assert recipe.abv == 0.0

    try:
        recipe.ibu = 1.10
    except AttributeError:
        assert recipe.ibu == 0.0

    try:
        recipe.color = 1.10
    except AttributeError:
        assert recipe.color == 0.0
