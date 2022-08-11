from typing import List

from dtdgen import ElementModel


class DTDAttributeList:
    def __init__(self, element_model: ElementModel):
        self._element_model: ElementModel = element_model
        self._alist: List[str] = []

    def __str__(self):
        """ Construct the list of <!ATTLIST> for an element """
        element_model = self._element_model
        element_name = element_model.name

