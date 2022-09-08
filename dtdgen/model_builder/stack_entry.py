from typing import Optional

from dtdgen import ElementModel


class StackEntry:
    """A data structure that is put on the stack for each nested element"""
    def __init__(self, element_model: ElementModel):
        self._element_model: ElementModel = element_model
        self._sequence_number: int = -1
        self._latest_child_name: Optional[str] = None

    @property
    def element_model(self):
        return self._element_model

    @property
    def sequence_number(self):
        return self._sequence_number

    def increment_sequence_number(self):
        self._sequence_number += 1

    @property
    def latest_child_name(self):
        return

    @latest_child_name.setter
    def latest_child_name(self, value: str):
        self._latest_child_name = value
