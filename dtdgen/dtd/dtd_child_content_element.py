from dtdgen import ElementModel
from dtdgen.dtd import DTDElementModel


class DTDChildContentElement(DTDElementModel):
    """ A DTDElementModel that represents the child content
    of an element """

    def __init__(self, element_model: ElementModel):
        """Creates a new element declaration over
        the specified element model"""
        super().__init__(element_model)

    def __str__(self):
        """Generates the <!ELEMENT parent (child1, child2, ... etc.) >
        that represents this element"""

        return f"<!ELEMENT {self.element_name} {self.children} >"

    def children(self):
        """Returns a formatted list of child elements"""
        return ""

