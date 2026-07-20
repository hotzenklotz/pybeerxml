from typing import Annotated, Any

from pydantic import ConfigDict, Field, field_serializer
from pydantic_xml import BaseXmlModel
from pydantic_xml.model import SearchMode

#: A float field that tolerates non-numeric XML content (e.g. ``<GRAIN_TEMP>unknown</GRAIN_TEMP>``).
#: Numeric strings are coerced to ``float``; anything else is kept as a string.
LenientFloat = Annotated[float | str | None, Field(union_mode="left_to_right")]

#: An int field that tolerates non-numeric XML content (e.g. alphanumeric yeast product ids).
#: Numeric strings are coerced to ``int``; anything else is kept as a string.
LenientInt = Annotated[int | str | None, Field(union_mode="left_to_right")]


class BeerXmlModel(BaseXmlModel, search_mode=SearchMode.UNORDERED):
    """Shared base class for all BeerXML models.

    Uses the ``unordered`` search mode so that XML elements may appear in any
    order (real-world BeerXML writers do not follow a fixed field order).
    Enables validation on attribute assignment so that assigning raw BeerXML
    strings (e.g. ``"TRUE"``) is coerced the same way as during parsing, and
    serializes boolean fields as ``TRUE`` / ``FALSE`` per the BeerXML spec.
    """

    model_config = ConfigDict(validate_assignment=True)

    @field_serializer("*", when_used="always")
    def _serialize_bool(self, value: Any) -> Any:
        if isinstance(value, bool):
            return "TRUE" if value else "FALSE"
        return value
