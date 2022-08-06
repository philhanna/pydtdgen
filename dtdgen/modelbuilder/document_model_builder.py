from xml.sax import make_parser
from xml.sax.xmlreader import XMLReader

from dtdgen import DocumentModel


class DocumentModelBuilder:
    """
    Analyzes an instance of an XML document to build a documentModel of
    its structure
    """
    max_enumeration_values = 20
    max_id_values = 100000

    def __init__(self):
        """ Creates a new DocumentModelBuilder """
        self._document_model = DocumentModel()
        self._element_stack = []

    def run(self, fp):
        """ Runs an XML input stream through the model builder """
        try:
            parser: XMLReader = make_parser()
            parser.setContentHandler(self)
            parser.parse(fp)
        finally:
            fp.close()
