from xml.sax import parse
from xml.sax.handler import ContentHandler, ErrorHandler

from dtdgen import ElementDetails, StackEntry, ChildDetails, AttributeDetails
from dtdgen.constants import MAX_ID_VALUES, MAX_ENUMERATION_VALUES
from dtdgen.functions import escape, is_valid_nmtoken, is_valid_name


class SchemaModelBuilder(ContentHandler, ErrorHandler):
    """SchemaModelBuilder - Generates a schema from an XML document instance."""

    # Map of element types appearing in the document;
    # each has the element name as a key and an ElementDetails object
    # as the value
    element_map: dict[str, ElementDetails] = None

    # Stack of elements currently open; each entry is a StackEntry object
    element_stack: list[StackEntry] = None

    def __init__(self):
        """Creates a new SchemaModelBuilder"""
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
