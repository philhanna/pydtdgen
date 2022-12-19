from dtdgen import ChildDetails


class ElementDetails:
    """A data structure to keep information about element types"""
    def __init__(self, name: str):
        self._name: str = name
        self._occurrences: int = 0
        self._has_character_content: bool = False
        self._sequenced: bool = True
        self._children: dict = {}
        self._childseq: list[ChildDetails] = []
        self._attributes: dict = {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def occurrences(self) -> int:
        return self._occurrences

    @occurrences.setter
    def occurrences(self, value: int):
        self._occurrences = value

    @property
    def has_character_content(self) -> bool:
        return self._has_character_content

    @has_character_content.setter
    def has_character_content(self, value: bool):
        self._has_character_content = value

    @property
    def sequenced(self) -> bool:
        return self._sequenced

    @sequenced.setter
    def sequenced(self, value: bool):
        self._sequenced = value

    @property
    def children(self) -> dict:
        return self._children

    @children.setter
    def children(self, value: dict):
        self._children = value

    @property
    def childseq(self) -> list[ChildDetails]:
        return self._childseq

    @childseq.setter
    def childseq(self, value: list):
        self._childseq = value

    @property
    def attributes(self) -> dict:
        return self._attributes

    @attributes.setter
    def attributes(self, value: dict):
        self._attributes = value
