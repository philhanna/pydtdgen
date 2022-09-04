from typing import List

from dtdgen import ElementModel


class DTDAttributeList:
    """The list of <!ATTLIST> for an element"""
    def __init__(self, element_model: ElementModel):
        self._element_model: ElementModel = element_model
        self._alist: List[str] = []

    def __str__(self):
        element_model = self._element_model
        element_name = element_model.name

