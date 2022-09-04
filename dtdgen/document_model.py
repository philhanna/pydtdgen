from dtdgen import ElementModel


class DocumentModel:
    """Provides access to what is known about the structure of a set of XML
    document instances"""

    def __init__(self):
        self._element_map: dict[str, ElementModel] = dict()

    def get_root_element_name(self) -> str:
        """Returns the root element name. This is determined by looking at
        all elements in the element name list and deleting all their known
        child elements. What remains should be the root element name (if
        the XML is well-formed)"""

        # Make a set of the names of all elements that are not known to have
        # parent elements.  To begin with, this will be every element
        possible_roots: set[str] = {name for name in self._element_map}

        # Now systematically remove names from this set by looking through
        # all elements and eliminating their children from the set
        for parent_element_name, parent_element_model in self._element_map.items():
            for child in parent_element_model.child_iterator():
                child_element_name = child.name
                possible_roots.remove(child_element_name)

        # There should be only one element left - get the count
        # and raise an exception if there are too few or too many
        root_candidates: list[str] = list(possible_roots)
        if not root_candidates:
            raise RuntimeError("No possible root elements found")
        if len(root_candidates) > 1:
            errmsg = f"{len(root_candidates)} possible root elements found: "
            errmsg += ", ".join(root_candidates)
            raise RuntimeError(errmsg)

        root_element_name = root_candidates[0]
        return root_element_name

    def add_element_model(self, element_model: ElementModel):
        """Adds an element model to this document model"""
        element_name = element_model.name
        self._element_map[element_name] = element_model

    def get_element_model(self, name: str) -> ElementModel:
        """Returns the element model with the specificd name,
        or None, if it does not exist in the document model"""
        return self._element_map.get(name)

    def element_name_iterator(self):
        """Returns an iterator over the list of element model names"""
        for name in self._element_map:
            yield name
