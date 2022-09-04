class ChildModel:
    """Records information about the presence of a child element within its
    parent element. If the parent element is sequenced, then the child
    elements always occur in sequence with the given frequency."""

    def __init__(self, name: str):
        """Creates a ChildModel of the specified child element name"""
        self._name: str = name
        self._repeatable: bool = False
        self._optional: bool = True

    @property
    def name(self):
        return self._name

    @property
    def repeatable(self):
        return self._repeatable

    @repeatable.setter
    def repeatable(self, value: bool):
        self._repeatable = value

    @property
    def optional(self):
        return self._optional

    @optional.setter
    def optional(self, value: bool):
        self._optional = value

    def __str__(self):
        class_name = self.__class__.__name__
        return (
            f"{class_name} [name={self.name}"
            f", repeatable={self.repeatable}"
            f", optional={self.optional}"
            "]"
        )