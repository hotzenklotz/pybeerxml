def cast_to_bool(value):
    if isinstance(value, str):
        return value.lower() == "true"
    elif isinstance(value, int) or isinstance(value, float):
        return bool(value)
    else:
        return False
