class ChildDetails:
    """Records information about the presence of a child element within its
    parent element. If the parent element is sequenced, then the child elements always
    occur in sequence with the given frequency."""

    def __init__(self):
        self._name: str | None = None
        self._position: int = 0
        self._repeatable: bool = False
        self._optional: bool = False

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def position(self) -> int:
        return self._position

    @position.setter
    def position(self, value: int):
        self._position = value

    @property
    def repeatable(self) -> bool:
        return self._repeatable

    @repeatable.setter
    def repeatable(self, value: bool):
        self._repeatable = value

    @property
    def optional(self) -> bool:
        return self._optional

    @optional.setter
    def optional(self, value: bool):
        self._optional = value
