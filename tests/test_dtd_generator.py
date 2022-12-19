import filecmp
from pathlib import Path

import pytest

from dtdgen import SchemaModelBuilder, DTDGenerator
from tests import testdata


def test_run(tmp_path, capsys):
    """Compares output from latest code to saved version of the DTD"""

    # Create file names
    old_dtd_filename = Path(testdata) / "workspace.dtd"
    new_dtd_filename = tmp_path / "workspace.dtd"
    xml_input_filename = Path(testdata) / "workspace.xml"

    # Generate a DTD model with the latest code
    model = SchemaModelBuilder()
    model.run(xml_input_filename)

    # Create the DTD and write it to stdout
    generator = DTDGenerator(model)
    generator.run()

    # Write the output to a file for comparison
    output = capsys.readouterr().out
    new_dtd_filename.write_text(output)

    assert filecmp.cmp(old_dtd_filename, new_dtd_filename)


def test_invalid_data():
    """Sees how invalid XML is handled"""
    filename = Path(testdata) / "invalid.xml"
    model = SchemaModelBuilder()
    with pytest.raises(ValueError) as ve:
        model.run(filename)
    errmsg = str(ve.value)

    assert "mismatched tag" in errmsg
