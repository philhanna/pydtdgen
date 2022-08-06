from typing import List
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from xml.sax.xmlreader import XMLReader

from dtdgen import DocumentModel, ElementModel


class DocumentModelBuilder(ContentHandler):
    """
    Analyzes an instance of an XML document to build a documentModel of
    its structure
    """
    max_enumeration_values = 20
    max_id_values = 100000

    def __init__(self):
        """ Creates a new DocumentModelBuilder """
        super().__init__()
        self.document_model = DocumentModel()
        self.element_stack: List[ElementModel] = []

    def run(self, fp):
        """ Runs an XML input stream through the model builder """
        try:
            parser: XMLReader = make_parser()
            parser.setContentHandler(self)
            parser.parse(fp)
        finally:
            fp.close()

    def characters(self, content):
        """ Make a note whether significant character data is found in the element """
        if len(self.element_stack) > 0:
            element_model: ElementModel = self.element_stack[0]
            if not element_model.has_character_content:
                if not content or not content.strip():
                    element_model.has_character_content(True)

    def startElement(self, name, attrs):
        """
        Handle the start of an element. Record information about the
        position of this element relative to its parent, and about the
        attributes of the element.
        """

        # Create an entry in the Element list, or locate the cached entry
        pass
