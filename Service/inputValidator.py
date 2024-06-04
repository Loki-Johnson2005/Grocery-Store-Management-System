def is_string_valid_numeric_input(*args):
    for value in args:
        if value is not None and not value.isspace() and value != "":
            try:
                float(value)
            except ValueError:
                return False
    return True
