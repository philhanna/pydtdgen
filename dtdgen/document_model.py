from dtdgen import ElementModel


class DocumentModel:
    """
    Provides access to what is known about the structure of a set of XML
    document instances
    """

    def __init__(self):
        self._element_map: dict[str, ElementModel] = dict()

    def get_root_element_name(self):
        """
        Returns the root element name. This is determined by looking at
        all elements in the element name list and deleting of their known
        child elements. What remains should be the root element name (if
        the XML is well-formed)
        """
        pass

    def add_element_model(self, element_model: ElementModel):
        """
        Adds an element model to this document model
        """
        element_name = element_model.name
        self._element_map.put(element_name, element_model)