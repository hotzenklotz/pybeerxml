from pybeerxml.recipe import Recipe


def test_calculated_properties():
    # Values og, fg, ibu, abv, color from the XML should be preferred, calculated properties should
    # ignore these values

    recipe = Recipe()

    try:
        recipe.og = 1.10
    except AttributeError:
        assert recipe.og == 1.10
        assert recipe.og_calculated == 1.0

    try:
        recipe.fg = 1.20
    except AttributeError:
        assert recipe.fg == 1.20
        assert recipe.fg_calculated == 1.0

    try:
        recipe.abv = 1.20
    except AttributeError:
        assert recipe.abv == 1.30
        assert recipe.abv_calculated == 0.0

    try:
        recipe.ibu = 1.40
    except AttributeError:
        assert recipe.ibu == 1.40
        assert recipe.ibu_calculated == 0.0

    try:
        recipe.color = 1.50
    except AttributeError:
        assert recipe.color == 1.50
        assert recipe.color_calculated == 0.0
