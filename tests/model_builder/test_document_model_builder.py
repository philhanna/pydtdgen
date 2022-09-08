import os
import os.path
from unittest import TestCase

from dtdgen.model_builder import DocumentModelBuilder
from tests.model_builder import test_data_dir


class TestDocumentModelBuilder(TestCase):

    def setUp(self):
        self.input_file = os.path.join(test_data_dir, "stooges.xml")

    def test_characters(self):
        pass

    def test_start_element(self):
        mb = DocumentModelBuilder()
        with open(self.input_file, "r") as fp:
            mb.run(fp)

    def test_end_element(self):
        pass
