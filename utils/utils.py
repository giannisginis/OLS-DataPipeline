def is_not_none(value):
    """
    Checks if a values is None
    :param value: just a value
    :return: the value if not None else None
    """
    try:
        label = value is not None
        return label
    except TypeError:
        label = None
        return label