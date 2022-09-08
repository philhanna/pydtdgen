import string
from typing import List
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from xml.sax.xmlreader import XMLReader

from dtdgen import DocumentModel, ElementModel, AttributeModel, MAX_ENUMERATION_VALUES, MAX_ID_VALUES
from dtdgen.model_builder import StackEntry


class DocumentModelBuilder(ContentHandler):
    """Analyzes an instance of an XML document to build a documentModel
    of its structure"""

    def __init__(self):
        """Creates a new DocumentModelBuilder"""
        super().__init__()
        self.document_model = DocumentModel()
        self.element_stack: List[StackEntry] = []

    def run(self, fp):
        """Runs an XML input stream through the model builder"""
        parser: XMLReader = make_parser()
        parser.setContentHandler(self)
        parser.parse(fp)

    def characters(self, content):
        """Make a note whether significant character data is found in the element"""
        if len(self.element_stack) > 0:
            element_model: ElementModel = self.element_stack[0].element_model
            if not element_model.has_character_content:
                for c in content:
                    if c not in string.whitespace:
                        element_model.has_character_content = True
                        break

    def startElement(self, name, attrs):
        """Handles the start of an element. Records information about the
        position of this element relative to its parent, and about the
        attributes of the element."""

        # Create an entry in the Element list, or locate the cached entry
        element_model: ElementModel = self.document_model.get_element_model(name)
        if not element_model:
            element_model = ElementModel(name)
            self.document_model.add_element_model(element_model)
        element_model.increment_occurrences()

        # Retain the associated element details object and initialize
        # sequence numbering of child element types
        stack_entry: StackEntry = StackEntry(element_model)
        self.element_stack.append(stack_entry)

        # Handle the attributes accumulated for this element.
        # Merge the new attribute list into the existing list for the element.
        for attr_name in attrs.getNames():
            attr_value: str = attrs.getValue(attr_name)
            attr_model: AttributeModel = element_model.get_attribute_model(attr_name)
            if not attr_model:
                attr_model = AttributeModel(attr_name)
                element_model.add_attribute(attr_model)
            if not attr_model.contains(attr_value):
                # We haven't seen this attribute value before
                attr_model.add_value(attr_value)
            else:
                # We have seen this attribute value before
                attr_model.unique = False
            attr_model.increment_occurrences()

        # Now keep track of the nesting and sequencing of child elements
