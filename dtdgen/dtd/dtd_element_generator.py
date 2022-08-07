from dtdgen import ElementModel
from dtdgen.dtd import DTDElementModel


class DTDElementGenerator:
    """ Assembles the correct DTD statement for an element and outputs it. """
    def __init__(self, element_model: ElementModel):
        self._element_model: ElementModel = element_model

    def print_dtd(self, fp):
        """
        Constructs the DTD string appropriate for this element and writes
        it to the specified output.
        """
        element_model: ElementModel = self._element_model
        dtd_element_model: DTDElementModel = None

        # Get the number of children this element can have

        n_children: int = element_model.get_child_model_count()
        has_character_content: bool = element_model.has_character_content

        # No children - must be either EMPTY or have #PCDATA content
        # Has children - either element content or mixed content

        pass
