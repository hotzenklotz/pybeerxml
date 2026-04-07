from dataclasses import dataclass


@dataclass
class Style:
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

    name: str | None = None
    category: str | None = None
    version: int | None = None
    category_number: str | None = None
    style_letter: str | None = None
    style_guide: str | None = None
    type: str | None = None
    og_min: float | None = None
    og_max: float | None = None
    fg_min: float | None = None
    fg_max: float | None = None
    ibu_min: float | None = None
    ibu_max: float | None = None
    color_min: float | None = None
    color_max: float | None = None
    abv_min: float | None = None
    abv_max: float | None = None
    carb_min: float | None = None
    carb_max: float | None = None
    notes: str | None = None
