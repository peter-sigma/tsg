# my_shims/django/utils/baseconv.py

import string

ALPHABET = string.digits + string.ascii_lowercase

def base36_encode(number):
    """
    Convert an integer to a base36 string.
    """
    if not isinstance(number, int):
        raise TypeError("number must be an integer")
    if number < 0:
        return '-' + base36_encode(-number)
    if number < 36:
        return ALPHABET[number]
    base36 = ""
    while number:
        number, i = divmod(number, 36)
        base36 = ALPHABET[i] + base36
    return base36