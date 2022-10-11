import filecmp
from io import StringIO
from unittest import TestCase
import os.path

from dtdgen import DTDGenerator

from tests import testdata, tmp, stdout_redirected, stderr_redirected


class TestDTDGenerator(TestCase):

    def test_run(self):
        """Compares output from latest code to saved version of the DTD"""
        old_dtd_filename = os.path.join(testdata, "workspace.dtd")

        # Generate a DTD with the latest code
        new_dtd_filename = os.path.join(tmp, "workspace.dtd")
        with StringIO() as out:
            with stdout_redirected(out):
                xml_input_filename = os.path.join(testdata, "workspace.xml")
                app = DTDGenerator()
                app.run(xml_input_filename)
                app.print_dtd()
                output = out.getvalue()
        with open(new_dtd_filename, "w") as fp:
            fp.write(output)

        self.assertTrue(filecmp.cmp(old_dtd_filename, new_dtd_filename))

    def test_invalid_data(self):
        """Sees how invalid XML is handled"""
        filename = os.path.join(testdata, "invalid.xml")
        app = DTDGenerator()
        with self.assertRaises(ValueError) as ve:
            app.run(filename)
        errmsg = str(ve.exception)
        self.assertIn("mismatched tag", errmsg)
