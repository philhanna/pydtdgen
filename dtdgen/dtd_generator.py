import string
from xml.sax import parse
from xml.sax.handler import ContentHandler

from dtdgen import ElementDetails, StackEntry

__all__ = [
    'is_valid_nmtoken',
    'is_valid_name',
]


class DTDGenerator(ContentHandler):
    """DTDGenerator - Generates a possible DTD from an XML document instance."""

    # Minimum number of appearances of an attribute for it to be considered
    # a candidate for an enumeration type
    MIN_ENUMERATION_INSTANCES: int = 10

    # Maximum number of distinct attribute values to be included in an enumeration
    MAX_ENUMERATION_VALUES: int = 20

    # An attribute will be regarded as an enumeration attribute
    # only if the number of instances divided by the number of
    # distinct values is >= this ratio
    MIN_ENUMERATION_RATIO: int = 3

    # Minimum number of attributes that must appear, with
    # the same value each time, for the value to be regarded
    # as FIXED
    MIN_FIXED: int = 5

    # Minumum number of attribute values that must appear
    # for the attribute to be regarded as an ID value
    MIN_ID_VALUES: int = 10

    # Maximum number of attribute values to be saved
    # while checking for uniqueness
    MAX_ID_VALUES: int = 100000

    # Alphabetical list of element types appearing in the document;
    # each has the element name as a key and an ElementDetails object
    # as the value
    element_list: dict[str, ElementDetails] = None

    # Stack of elements currently open; each entry is a StackEntry object
    element_stack: list[StackEntry] = None

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.element_list = {}
        self.element_stack = []

    def run(self, filename):
        parse(filename, handler=self)


# ============================================================
# Internal functions
# ============================================================

def is_valid_nmtoken(s: str) -> bool:
    """Test whether a string is an XML NMTOKEN.
    TODO: This is currently an incomplete test, it treats all non-ASCII characters
    as being valid in NMTOKENs."""
    if not len(s):
        return False
    for c in s:
        if not any([
            c in string.ascii_uppercase,
            c in string.ascii_lowercase,
            c in string.digits,
            c in '._-:',
            ord(c) > 128,
        ]):
            return False
    return True


def is_valid_name(s: str) -> bool:
    """Test whether a string is an XML name.
        TODO: This is currently an incomplete test, it treats all non-ASCII characters
        as being valid in names."""
    if not is_valid_nmtoken(s):
        return False
    c = s[0]
    return not any([
        c in string.digits,
        c == '.',
        c == '-',
    ])


# ============================================================
# Mainline
# ============================================================
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='DTDGenerator')
    parser.add_argument('-v', '--version', action='store_true', help='display version number')
    parser.add_argument('filename', help='Input xml file')
    args = parser.parse_args()

    app = DTDGenerator(args.filename)
