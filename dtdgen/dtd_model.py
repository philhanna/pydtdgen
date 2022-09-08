class DTDModel:
    """The abstract representation of a DTD"""
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        return self._name
