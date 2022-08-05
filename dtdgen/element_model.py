from typing import List

from dtdgen import ChildModel


class ElementModel:
    """Keeps track of the possible contents of an element, based on all
    instances of it found in the source XML."""

    def __init__(self, name: str):
        """
        Creates a new ElementModel with the specified name
        """
        self._name: str = name
        self._occurences: int = 0
        self._character_content: bool = False
        self._sequenced: bool = True
        self._childseq: List[ChildModel] = []

    @property
    def min_id_values(self):
        """Minimum number of attribute values that must appear for the
        attribute to be regarded as an ID value"""
        return 10

    @property
    def occurences(self):
        """
        Returns the number of times this element was found in the input XML
        """
        return self._occurences

    def increment_occurrences(self):
        self._occurences += 1

    @property
    def has_character_content(self):
        return self._character_content

    @has_character_content.setter
    def has_character_content(self, value: bool):
        self._character_content = value

    @property
    def sequenced(self):
        return self._sequenced

    @sequenced.setter
    def sequenced(self, value: bool):
        self._sequenced = value

    def get_child_model_count(self):
        """Returns the number of ChildModel elements this parent has."""
        return len(self._childseq)

    def get_child_model(self, index: int = None, name: str = None):
        """Returns the child model by name or index, or None if it does not exist."""
        if index is not None:
            return self._childseq[index]
        if name is not None:
            child = [x for x in self._childseq if x.name == name][0]
            return child

    def add_child(self, child_model: ChildModel):
        """ Adds a child element for this element """
        self._childseq.append(child_model)
