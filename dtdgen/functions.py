# ============================================================
# Internal functions
# ============================================================
import string


def escape(s: str) -> str:
    """
    Escape special characters in a String value.
    Returns he XML representation of the string.

    This static method converts a Unicode string to a string containing
    only ASCII characters, in which non-ASCII characters are represented
    by the usual XML/HTML escape conventions (for example, "&lt;" becomes
    "&amp;lt;").

    Note: if the input consists solely of ASCII or Latin-1 characters,
    the output will be equally valid in XML and HTML. Otherwise it will be valid
    only in XML.
    """
    outstr = ""
    fmt2 = lambda i: ("0" + str(i))[-2:]
    for c in s:
        match c:
            case '<':
                outstr += '&lt;'
            case '>':
                outstr += '&gt;'
            case '&':
                outstr += '&amp;'
            case '\"':
                outstr += '&#34;'
            case '\'':
                outstr += '&#39;'
            case _ if chr(0x1f) < c < chr(0x7f):
                outstr += c
            case _:
                outstr += "&#" + fmt2(ord(c)) + ";"
        pass
    return outstr


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
