import sys
from typing import List, Optional

from dtdgen import DocumentModel
from dtdgen.dtd import DTDGenerator
from dtdgen.modelbuilder import DocumentModelBuilder


class RunMain:
    """ Runs DTDGEN """

    def __init__(self):
        self._input_files: List[str] = []
        self._output_file: Optional[str] = None
        pass

    def build(self) -> DocumentModel:
        """ Builds the document model by parsing the input XML file[s] """
        # Create a DocumentModelBuilder and run input files through it
        model_builder = DocumentModelBuilder()
        for input_file in self._input_files:
            with open(input_file, "rt") as fp:
                model_builder.run(fp)

        # Get the resulting document model
        model = model_builder.document_model
        return model

    def print_dtd(self, model: DocumentModel):
        """ Writes the output DTD, either to stdout or the specified file """
        dtdgen = DTDGenerator(model)
        if self._output_file:
            with open(self._output_file, "wt") as fp:
                dtdgen.print_dtd(fp)
                fp.flush()
        else:
            dtdgen.print_dtd(sys.stdout)
            sys.stdout.flush()
