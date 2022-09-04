class AttributeModel:
    """Keeps track of what is known about the type and value of an element
    attribute, based on how it is used in all instances found in the
    source XML."""

    def __init__(self, name: str):
        """Creates a new attribute model with the specified name"""
        self._name: str = name
        self._occurrences: int = 0
        self._unique: bool = True
        self._all_names: bool = True
        self._all_nmtokens: bool = True
        self._values: dict[str, str] = dict()

    @property
    def name(self):
        """The attribute name (read-only)"""
        return self._name

    @property
    def occurrences(self):
        """Number of occurrences of this attribute"""
        return self._occurrences

    @occurrences.setter
    def occurrences(self, count: int):
        self._occurrences = count

    def increment_occurrences(self):
        self._occurrences += 1

    @property
    def unique(self):
        """True if no duplicate values were encountered"""
        return self._unique

    @unique.setter
    def unique(self, value: bool):
        self._unique = value

    @property
    def all_names(self):
        """True if all the attribute values are valid names"""
        return self._all_names

    @all_names.setter
    def all_names(self, value: bool):
        self._all_names = value

    @property
    def all_nmtokens(self):
        """True if all the attribute values are valid NMTOKENs"""
        return self._all_nmtokens

    @all_nmtokens.setter
    def all_nmtokens(self, value: bool):
        self._all_nmtokens = value

    @property
    def first_value(self):
        """Set of all distinct values encountered for this attribute"""
        if self.value_count == 0:
            return None
        first_value: str = next(self.value_iterator())
        return first_value

    @property
    def value_count(self):
        return len(self._values)

    @property
    def values(self):
        return list(self._values.keys())

    def add_value(self, value: str):
        if value not in self._values:
            self._values[value] = ""

    def value_iterator(self):
        """An iterator over the values for this attribute"""
        for value in self._values.keys():
            yield value

    def contains(self, value) -> bool:
        return value in self._values

    def __str__(self):
        class_name = self.__class__.__name__
        return (
            f"{class_name} [name={self.name}"
            f", occurrences={self.occurrences}"
            f", unique={self.unique}"
            f", values={self.values}"
            f", allNames={self.all_names}"
            f", allNMTOKENS={self.all_nmtokens}"
            "]"
        )
