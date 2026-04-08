from pydantic_xml import element

from pybeerxml.xml_model import BeerFloat, BeerInt, BeerXmlModel


class Style(BeerXmlModel, tag="STYLE"):
    """Beer style guidelines from a BeerXML ``<STYLE>`` element.

    All ``_min`` / ``_max`` pairs define the acceptable range for that
    parameter within the style.

    Attributes:
        name: Style name (e.g. ``"American IPA"``).
        category: Style category (e.g. ``"India Pale Ale"``).
        version: BeerXML style record version.
        category_number: Style category identifier from the style guide.
        style_letter: Style subcategory letter or identifier.
        style_guide: Style guide name (e.g. ``"BJCP"``).
        type: Beverage family (e.g. ``"Ale"``, ``"Lager"``, ``"Mead"``).
        og_min: Minimum original gravity.
        og_max: Maximum original gravity.
        fg_min: Minimum final gravity.
        fg_max: Maximum final gravity.
        ibu_min: Minimum bitterness in IBU.
        ibu_max: Maximum bitterness in IBU.
        color_min: Minimum colour in SRM.
        color_max: Maximum colour in SRM.
        abv_min: Minimum ABV percentage.
        abv_max: Maximum ABV percentage.
        carb_min: Minimum carbonation in volumes of CO₂.
        carb_max: Maximum carbonation in volumes of CO₂.
        notes: Free-text style notes.
    """

    name: str | None = element(tag="NAME", default=None)
    category: str | None = element(tag="CATEGORY", default=None)
    version: BeerInt | None = element(tag="VERSION", default=None)
    category_number: str | None = element(tag="CATEGORY_NUMBER", default=None)
    style_letter: str | None = element(tag="STYLE_LETTER", default=None)
    style_guide: str | None = element(tag="STYLE_GUIDE", default=None)
    type: str | None = element(tag="TYPE", default=None)
    og_min: BeerFloat | None = element(tag="OG_MIN", default=None)
    og_max: BeerFloat | None = element(tag="OG_MAX", default=None)
    fg_min: BeerFloat | None = element(tag="FG_MIN", default=None)
    fg_max: BeerFloat | None = element(tag="FG_MAX", default=None)
    ibu_min: BeerFloat | None = element(tag="IBU_MIN", default=None)
    ibu_max: BeerFloat | None = element(tag="IBU_MAX", default=None)
    color_min: BeerFloat | None = element(tag="COLOR_MIN", default=None)
    color_max: BeerFloat | None = element(tag="COLOR_MAX", default=None)
    abv_min: BeerFloat | None = element(tag="ABV_MIN", default=None)
    abv_max: BeerFloat | None = element(tag="ABV_MAX", default=None)
    carb_min: BeerFloat | None = element(tag="CARB_MIN", default=None)
    carb_max: BeerFloat | None = element(tag="CARB_MAX", default=None)
    notes: str | None = element(tag="NOTES", default=None)
