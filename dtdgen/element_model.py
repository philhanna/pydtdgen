from typing import List

from dtdgen import ChildModel, AttributeModel, MIN_ID_VALUES


class ElementModel:
    """Keeps track of the possible contents of an element, based on all
    instances of it found in the source XML."""

    def __init__(self, name: str):
        """ Creates a new ElementModel with the specified name """
        self._name: str = name
        self._occurrences: int = 0
        self._character_content: bool = False
        self._sequenced: bool = True
        self._childseq: List[ChildModel] = []
        self._attributes: dict[str, AttributeModel] = dict()

    @property
    def name(self):
        return self._name

    @property
    def occurrences(self):
        """ Returns the number of times this element was found
            in the input XML """
        return self._occurrences

    @occurrences.setter
    def occurrences(self, value: int):
        self._occurrences = value

    def increment_occurrences(self):
        self._occurrences += 1

    @property
    def has_character_content(self) -> bool:
        return self._character_content

    @has_character_content.setter
    def has_character_content(self, value: bool):
        self._character_content = value

    @property
    def is_sequenced(self):
        return self._sequenced

    @is_sequenced.setter
    def is_sequenced(self, value: bool):
        self._sequenced = value

    def child_iterator(self):
        for child in self._childseq:
            yield child

    def get_child_model(self, index: int = None, name: str = None):
        """Returns the child model by name or index, or None if it does not exist."""
        if index is not None:
            return self._childseq[index]
        if name is not None:
            child = [x for x in self._childseq if x.name == name][0]
            return child

    def get_child_model_count(self):
        """Returns the number of ChildModel elements this parent has."""
        return len(self._childseq)

    def add_child(self, child_model: ChildModel):
        """ Adds a child element for this element """
        self._childseq.append(child_model)

    def attribute_names(self):
        """ Generator that yields attribute names, one for each call """
        for attrname in self._attributes:
            yield attrname

    def get_attribute_model(self, name: str) -> AttributeModel:
        return self._attributes.get(name, None)

    def add_attribute(self, attribute_model: AttributeModel) -> None:
        attrname: str = attribute_model.name
        self._attributes[attrname] = attribute_model

    def id_attribute_name(self):
        found: list[str] = list()
        for attr_name, attr_model in self._attributes.items():
            # If every value of the attribute is distinct, and there are
            # at least MIN_ID_VALUES, treat it as an ID. ID values must be
            # Names. Only allowed one ID attribute per element type.
            if all([
                attr_model.all_names,
                attr_model.unique,
                attr_model.occurrences >= MIN_ID_VALUES,
            ]):
                found.append(attr_name)

        nfound = len(found)
        if nfound == 0:
            # No candidates found
            return None
        if nfound == 1:
            # Found exactly one candidate.  This must be the one.
            return found[0]
        if nfound > 1:
            # More than one candidate.  Can't both be the ID
            return None


