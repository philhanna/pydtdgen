from dtdgen import ElementModel
from dtdgen.dtd import DTDElementModel


class DTDChildContentElement(DTDElementModel):
    """ A DTDElementModel that represents the child content
    of an element """

    def __init__(self, element_model: ElementModel):
        """ Creates a new element declaration over
        the specified element model """
        super().__init__(element_model)

    def __str__(self):
        """ Generates the <!ELEMENT parent (child1, child2, ... etc.) >
        that represents this element """
        output: str = f"<!ELEMENT {self.element_name} ( "
        if self.element_model.is_sequenced:
            # All elements of this type have the same child elements
            # in the same order
            suffixes = []
            for child_model in self.element_model.child_iterator():
                pass
            suffix_string = ", ".join(suffixes)
        else:
            # The children don't always appear in the same order
            # so list them sequentially and indicate that they can
            # be in any order
            pass
