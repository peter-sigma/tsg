import sys
import types

# Try to import the existing django.utils.baseconv module.
try:
    import django.utils.baseconv as baseconv
except ImportError:
    # If not found, create a new module.
    baseconv = types.ModuleType("django.utils.baseconv")
    sys.modules["django.utils.baseconv"] = baseconv

# If the module doesn't have a 'base62' attribute, add it.
if not hasattr(baseconv, 'base62'):
    import string

    class Base62:
        # Standard Base62 alphabet: digits, uppercase letters, then lowercase letters.
        alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

        @classmethod
        def decode(cls, s):
            """Decode a Base62 string to an integer."""
            base = len(cls.alphabet)
            num = 0
            for char in s:
                num = num * base + cls.alphabet.index(char)
            return num

    baseconv.base62 = Base62