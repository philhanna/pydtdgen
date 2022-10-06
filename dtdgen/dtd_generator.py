from xml.sax import parse
from xml.sax.handler import ContentHandler

from dtdgen import ElementDetails, StackEntry, escape


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
    MIN_ENUMERATION_RATIO: float = 3.0

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

    def print_dtd(self):
        # Process the element types encountered, in turn
        for element_name, ed in self.element_list.items():
            children = ed.children
            child_keys = sorted(set([k for k in children]))

            # EMPTY content
            if len(child_keys) == 0 and not ed.has_character_content:
                print("<!ELEMENT " + element_name + " EMPTY >")

            # CHARACTER content
            if len(child_keys) == 0 and ed.has_character_content:
                print("<!ELEMENT " + element_name + " ( #PCDATA ) >")

            # ELEMENT content
            if len(child_keys) > 0 and not ed.has_character_content:
                print("<!ELEMENT " + element_name + " ( ", end='')
                if ed.sequenced:
                    # All elements of this type have the same child elements
                    # in the same sequence, retained in the childseq vector
                    outlist = []
                    for ch in ed.childseq:
                        sb = ch.name
                        if ch.repeatable and not ch.optional:
                            sb += "+"
                        if ch.repeatable and ch.optional:
                            sb += "*"
                        if ch.optional and not ch.repeatable:
                            sb += "?"
                        outlist.append(sb)
                    print(", ".join(outlist) + " ) >")

                # The childen don't always appear in the same sequence,
                # so list them alphabeticall and allow them to be
                # in any order

                sb = " | ".join(child_keys)
                print(sb + " )* ) >")

            # MIXED content
            if len(child_keys) > 0 and ed.has_character_content:
                sb = f"<!ELEMENT {element_name} ( #PCDATA {' | '.join(child_keys)} )* >"
                print(sb)

            # Now examine the attributes encountered for this element type
            attlist = ed.attributes
            done_id = False  # To ensure we have at most one ID attribute per element

            for attname, ad in attlist.items():
                # If the attribute is present on every instance of the element,
                # treat it as required
                required: bool = (ad.occurrences == ed.occurrences)

                # If every value of the attribute is distinct,
                # and there are at least MIN_ID_VALUES, treat it as an ID.
                # TODO: this may give the wrong answer.
                # We should check whether the value sets of two
                # candidate-ID attributes overlap, in which case
                # they can't both be ID's !!
                isid: bool = ad.all_names \
                             and not done_id \
                             and ad.unique \
                             and ad.occurrences >= self.MIN_ID_VALUES

                # If there is only one attribute value, and at least
                # MIN_FIXED occurrences of it, treat it as FIXED
                isfixed: bool = required \
                                and len(ad.values) == 1 \
                                and ad.occurrences >= self.MIN_FIXED

                # If the number of distinct values is small compared with
                # the number of occurrences, treat it as an enumeration
                isenum: bool = ad.all_nmtokens \
                               and ad.occurrences >= self.MIN_ENUMERATION_INSTANCES \
                               and len(ad.values) <= ad.occurrences / self.MIN_ENUMERATION_RATIO \
                               and len(ad.values) <= self.MAX_ENUMERATION_VALUES

                print(f"<!ATTLIST {element_name} {attname} ", end='')
                tokentype = "NMTOKEN" if ad.all_nmtokens else "CDATA"

                if isid:
                    print("ID", end='')
                    don_id = True
                elif isfixed:
                    val: str = list(ad.values)[0]
                    print(f'{tokentype} #FIXID "{escape(val)}" >')
                elif isenum:
                    vals = " | ".join([str(val) for val in ad.values])
                    print(f"( {vals} )", end='')
                else:
                    print(tokentype, end='')
                if not isfixed:
                    if required:
                        print(" #REQUIRED >")
                    else:
                        print(" #IMPLIED >")

    def startElement(self, name, attrs):
        """Handle the start of an element. Record information about
        the position of this element relative to its parent, and about the
         attributes of the element."""
        super().startElement(name, attrs)

    def endElement(self, name):
        """Handle the end of element. If sequenced, check that all
        expected children are accounted for."""

        # If the number of child element groups in this parent element
        # is less than the number if previous elements, then the
        # absent children are marked as optional
        ed = self.element_list[name]
        if ed.sequenced:
            se = self.element_stack[-1]
            seq: int = se.sequence_number
            for i in range(seq + 1, len(ed.childseq)):
                ed.childseq[i].optional = True
        self.element_stack.pop()

    def characters(self, content):
        """Handle character data. Make a note whether significant
        character data is found in the element"""
        ed = self.element_stack[-1].element_details
        if not ed.has_character_content:
            for ch in content:
                if ch > ' ':
                    ed.has_character_content = True
                    break



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
    app.run(args.filename)
