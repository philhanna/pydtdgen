import os.path
import re
import subprocess
from io import StringIO
from unittest import TestCase

from dtdgen import DTDGenerator
from tests import testdata, project_root_dir, tmp, stdout_redirected


class TestDTDGenerator(TestCase):

    def setUp(self):
        input_file = os.path.join(testdata, "workspace.xml")

        python_output = os.path.join(tmp, "workspace_p.dtd")
        python_program = "./dtdgen.py"
        parms = [python_program, input_file]
        cp = subprocess.run(parms, cwd=project_root_dir, check=True, capture_output=True)
        output = cp.stdout
        with open(python_output, "wb") as fp:
            fp.write(output)

        java_output = os.path.join(tmp, "workspace_j.dtd")
        java_program = "dtdgen"
        parms = [java_program, input_file]
        cp = subprocess.run(parms, cwd=project_root_dir, check=True, capture_output=True)
        output = cp.stdout
        with open(java_output, "wb") as fp:
            fp.write(output)

        self.input_file = input_file
        self.python_output = python_output
        self.java_output = java_output

    def extract_comparison_data(self, regexp):
        with open(self.java_output) as fp:
            for line in fp:
                m = regexp.search(line)
                if m:
                    expected = m.group(1)
                    break
        self.assertIsNotNone(expected)
        with open(self.python_output) as fp:
            for line in fp:
                m = regexp.search(line)
                if m:
                    actual = m.group(1)
                    break
        self.assertIsNotNone(actual)
        return expected, actual

    def test_nmtoken(self):
        app = DTDGenerator()
        app.run(self.input_file)
        with StringIO() as out, stdout_redirected(out):
            app.print_dtd()
        regexp = re.compile(r"ATTLIST ConfirmationsSetting id (\S+)")
        expected, actual = self.extract_comparison_data(regexp)
        self.assertEqual(expected, actual)

    def test_required(self):
        app = DTDGenerator()
        app.run(self.input_file)
        with StringIO() as out, stdout_redirected(out):
            app.print_dtd()
        regexp = re.compile(r"ATTLIST ConfirmationsSetting id \S+ (\S+)")
        expected, actual = self.extract_comparison_data(regexp)
        self.assertEqual(expected, actual)
