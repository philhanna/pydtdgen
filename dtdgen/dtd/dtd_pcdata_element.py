from dtdgen import ElementModel
from dtdgen.dtd import DTDElementModel


class DTDPCDATAElement(DTDElementModel):
    """A DTDElementModel that represents an element
    with parsed character content (#PCDATA)"""
    def __init__(self, element_model: ElementModel):
        """Creates a new PCDATA element over the specified element model"""
        super().__init__(element_model)

    def __str__(self):
        """Generates the <!ELEMENT> name (#PCDATA)> string"""
        output: str = f"<!ELEMENT {self.element_name} ( #PCDATA ) >"
        return output
