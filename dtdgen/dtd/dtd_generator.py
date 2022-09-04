from dtdgen import DocumentModel
from dtdgen.dtd import DTDElementGenerator


class DTDGenerator:
    """Writes a DTD from the specified DocumentModel"""
    def __init__(self, document_model: DocumentModel):
        self._document_model = document_model

    def print_dtd(self, fp):
        """Constructs the DTD from the model"""

        # Make a list of all elements that have been printed. At the
        # start, the list will be empty. As we print each one, we add it
        # to the list to avoid getting into a recursive loop.
        already_printed: set[str] = set()

        # Now get the root element, print it, remove it from the list,
        # and then process all its immediate children
        root_element_name = self._document_model.get_root_element_name()
        self.print_dtd_element(root_element_name, already_printed, fp)

    def print_dtd_element(self, element_name: str, already_printed: set[str], fp):
        """Prints the DTD for one element"""

        # Check the list of already printed elements to prevent
        # recursion. If this name is in the list, just return
        if element_name in already_printed:
            return

        # Immediately add it to the set so that we won't try to print it again
        already_printed.add(element_name)

        # Get the element model and pass it to a DTD element generator
        element_model = self._document_model.get_element_model(element_name)
        element_generator = DTDElementGenerator(element_model)

        # Print the DTD for this element
        element_generator.print_dtd(fp)

        # Recurse over all the children
        for child_model in element_model.child_iterator():
            child_name = child_model.name
            self.print_dtd_element(child_name, already_printed, fp)