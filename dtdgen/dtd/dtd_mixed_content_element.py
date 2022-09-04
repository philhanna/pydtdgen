from dtdgen import ElementModel
from dtdgen.dtd import DTDElementModel


class DTDMixedContentElement(DTDElementModel):
    """A DTDElementModel that represents an element with both element and #PCDATA"""
    def __init__(self, element_model: ElementModel):
        super().__init__(element_model)

    def __str__(self):
        """Generates the <!ELEMENT> string for this mixed content element"""
        prefix: str = f"<!ELEMENT {self.element_name} ( #PCDATA"
        suffixes: list[str] = [child_model.name for child_model in self._element_model.child_iterator()]
        suffix: str = " | ".join(suffixes)
        output = prefix + suffix + " )* >"
        return output
