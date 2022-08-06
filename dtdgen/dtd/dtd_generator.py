from dtdgen import DocumentModel


class DTDGenerator:
    """ Writes a DTD from the specified DocumentModel """
    def __init__(self, document_model: DocumentModel):
        self._document_model = document_model

    def print_dtd(self, fp):
        pass
