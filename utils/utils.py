def is_not_none(value):
    try:
        label = value is not None
        return label
    except TypeError:
        label = False
        return label