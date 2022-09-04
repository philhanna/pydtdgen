from dtdgen import ElementModel
from dtdgen.dtd import DTDElementModel


class DTDEmptyElement(DTDElementModel):
    """A DTDElementModel that represents an empty element
    (one that has no children)"""

    def __init__(self, element_model: ElementModel):
        """Creates a new empty element for the specified element model"""
        super().__init__(element_model)

    def __str__(self):
        """Generates the <!ELEMENT name EMPTY> string"""
        output = f"<!ELEMENT {self.element_name} EMPTY>"
        return output
