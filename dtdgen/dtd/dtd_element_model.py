from dtdgen import ElementModel


class DTDElementModel:
    """
    Abstract base class for DTD generators for child content,
    empty elements, mixed content elements, and PCDATA.
    """
    def __init__(self, element_model: ElementModel):
        """ Creates a DTDElementModel over the specified element model """
        self._element_model: ElementModel = element_model
        self._element_name: str = element_model.name
        self._n_children: int = element_model.get_child_model_count()

    @property
    def element_name(self):
        return self._element_name