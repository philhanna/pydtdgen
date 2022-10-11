from xml.sax import parse
from xml.sax.handler import ContentHandler, ErrorHandler

from dtdgen import ElementDetails, StackEntry, ChildDetails, AttributeDetails
from dtdgen.functions import escape, is_valid_nmtoken, is_valid_name

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


class DTDGenerator(ContentHandler, ErrorHandler):
    """DTDGenerator - Generates a possible DTD from an XML document instance."""

    # Map of element types appearing in the document;
    # each has the element name as a key and an ElementDetails object
    # as the value
    element_map: dict[str, ElementDetails] = None

    # Stack of elements currently open; each entry is a StackEntry object
    element_stack: list[StackEntry] = None

    def __init__(self):
        """Creates a new DTDGenerator"""
        super().__init__()
        self.filename = None
        self.element_map = {}
        self.element_stack = []

    def run(self, filename):
        """Runs the SAX parser over the specified file,
        calling methods in this class to handle the parsing
        actions.
        """
        parse(filename, handler=self, errorHandler=self)

    def print_dtd(self):
        """Generates the DTD"""
        # Process the element types encountered, in turn

        for element_name, ed in self.element_map.items():

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
                # so list them alphabetically and allow them to be
                # in any order
                else:
                    sb = " | ".join(child_keys)
                    print(sb + " )* >")

            # MIXED content
            if len(child_keys) > 0 and ed.has_character_content:
                sb = f"<!ELEMENT {element_name} ( #PCDATA | {' | '.join(child_keys)} )* >"
                print(sb)

            # Now examine the attributes encountered for this element type
            attlist = ed.attributes
            done_id = False  # To ensure we have at most one ID attribute per element

            for attname, ad in sorted(attlist.items()):
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
                             and ad.occurrences >= MIN_ID_VALUES

                # If there is only one attribute value, and at least
                # MIN_FIXED occurrences of it, treat it as FIXED
                isfixed: bool = required \
                                and len(ad.values) == 1 \
                                and ad.occurrences >= MIN_FIXED

                # If the number of distinct values is small compared with
                # the number of occurrences, treat it as an enumeration
                isenum: bool = ad.all_nmtokens \
                               and ad.occurrences >= MIN_ENUMERATION_INSTANCES \
                               and len(ad.values) <= ad.occurrences / MIN_ENUMERATION_RATIO \
                               and len(ad.values) <= MAX_ENUMERATION_VALUES

                print(f"<!ATTLIST {element_name} {attname} ", end='')
                tokentype = "NMTOKEN" if ad.all_nmtokens else "CDATA"

                if isid:
                    print("ID", end='')
                    done_id = True
                elif isfixed:
                    val: str = list(ad.values)[0]
                    print(f'{tokentype} #FIXED "{escape(val)}" >')
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
            print()

    ####################################################################
    # SAX callback methods
    ####################################################################

    def fatalError(self, exception):
        """Handles a fatal error"""
        errmsg = str(exception)
        raise ValueError(errmsg)

    def startElement(self, tag_name, attrs):
        """Handles the start of an element. Record information about
        the position of this element relative to its parent, and about the
         attributes of the element."""

        # Create an entry in the Element List, or locate the existing entry
        ed = self.element_map.get(tag_name, None)
        if ed is None:
            ed = ElementDetails(tag_name)
            self.element_map[tag_name] = ed

        # Retain the associated element details object and
        # initialize sequence numbering of child element types
        se = StackEntry(element_details=ed, sequence_number=-1, latest_child=None)

        # Count occurrences of this element type
        ed.occurrences += 1

        # Handle the attributes accumulated for this element.
        # Merge the new attribute list into the existing list
        # for the element
        self.handle_attributes(attrs, ed)

        # If this is a top-level element, there is nothing else to do here
        if len(self.element_stack) == 0:
            self.element_stack.append(se)
            return

        # Keep track of the nesting and sequencing of child elements
        parent = self.element_stack[-1]
        parent_details = parent.element_details
        seq = parent.sequence_number

        # For sequencing, we're interested in consecutive groups
        # of the same child element type
        is_first_in_group = parent.latest_child is None or parent.latest_child != tag_name
        if is_first_in_group:
            seq += 1
            parent.sequence_number += 1
        parent.latest_child = tag_name

        # If we've seen this child of this parent before, get the details
        children = parent_details.children
        c: ChildDetails = children.get(tag_name, None)
        if c is None:
            # This is the first time we've seen this child belonging to
            # this parent
            c = ChildDetails()
            c.name = tag_name
            c.position = seq
            c.repeatable = False
            c.optional = False
            children[tag_name] = c
            parent_details.childseq.append(c)

            # If the first time we see this child is not on the first
            # instance of the parent, then we allow it as an optional
            # element
            if parent_details.occurrences != 1:
                c.optional = True
        else:
            # If it's the first occurrence of the parent element,
            # and we've seen this child before,
            # and it's the first of a new group,
            # then the child occurrences are not consecutive
            if parent_details.occurrences == 1 and is_first_in_group:
                parent_details.sequenced = False

            # Check whether the position of this group of children
            # in this parent element is the same as its position
            # in previous instances of the parent.
            if len(parent_details.childseq) <= seq or \
                    parent_details.childseq[seq].name != tag_name:
                parent_details.sequenced = False

        # If there's more than one child element, mark it as repeatable
        if not is_first_in_group:
            c.repeatable = True

        # Push the stack entry for this element
        self.element_stack.append(se)

    def endElement(self, tag_name):
        """Handle the end of element. If sequenced, check that all
        expected children are accounted for."""

        # If the number of child element groups in this parent element
        # is less than the number if previous elements, then the
        # absent children are marked as optional
        ed = self.element_map[tag_name]
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

    ####################################################################
    # Static methods
    ####################################################################

    @staticmethod
    def handle_attributes(attrs, ed):
        tag_name = ed.name
        for attname, val in attrs.items():

            # Get the attribute object in ElementDetails for this
            # attribute name, or add it if it does not already exist
            ad = ed.attributes.get(attname, None)
            if not ad:
                ad = AttributeDetails(attname)
                ed.attributes[attname] = ad

            if val in ad.values:
                # We've seen this attribute before
                ad.unique = False
            else:
                # We haven't seen this attribute value before
                ad.values.add(val)

                # Check whether attribute value is a valid name
                if ad.all_names and not is_valid_name(val):
                    ad.all_names = False

                # Check whether attribute valud is a valid NMTOKEN
                if ad.all_nmtokens and not is_valid_nmtoken(val):
                    ad.all_nmtokens = False

                # For economy, don't save the new value unless it's needed;
                # it's needed only if we're looking for ID values or
                # enumerated values
                if ad.unique \
                        and ad.all_names \
                        and ad.occurrences <= MAX_ID_VALUES:
                    ad.values.add(val)
                elif len(ad.values) <= MAX_ENUMERATION_VALUES:
                    ad.values.add(val)

            ad.occurrences += 1
