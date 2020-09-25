from typing import Text, Any


def to_lower(possible_string: Any) -> Text:
    "Helper function to transform strings to lower case"
    value = ""
    try:
        value = possible_string.lower()
    except AttributeError:
        pass

    return value
