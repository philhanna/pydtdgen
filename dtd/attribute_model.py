class AttributeModel:
    """
    Keeps track of what is known about the type and value of an element
    attribute, based on how it is used in all instances found in the
    source XML.
    """
    def __init__(self, name: str):
        """ Creates a new attribute model with the specified name """
        self._name: str = name
        self._occurrences: int = 0
        self._is_unique: bool = True
        self._is_all_names: bool = True
        self._is_all_nmtokens: bool = True
        self._values: set[str] = set()

    @property
    def name(self):
        return self._name

    @property
    def occurrences(self):
        """ Returns the number of times this attribute was found in the source
        XML associated with this element """
        return self._occurrences

    @property
    def is_unique(self):
        return self._is_unique

    @is_unique.setter
    def is_unique(self, value: bool):
        self._is_unique = value

    @property
    def is_all_names(self):
        return self._is_all_names

    @is_all_names.setter
    def is_all_names(self, value: bool):
        self._is_all_names = value

    @property
    def is_all_nmtokens(self):
        return self._is_all_nmtokens

    @is_all_nmtokens.setter
    def is_all_nmtokens(self, value: bool):
        self._is_all_nmtokens = value

    @property
    def first_value(self):
        if self.value_count == 0:
            return None
        first_value: str = next(self.value_iterator())
        return first_value

    @property
    def value_count(self):
        return len(self._values)
    def value_iterator(self):
        """ An iterator over the values for this attribute """
        for value in self._values:
            yield value

    def increment_occurrences(self):
        self._occurrences += 1



