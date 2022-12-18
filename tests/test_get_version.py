import re

from dtdgen import get_version
from tests import project_root


def test_get_version():
    actual = get_version()
    setup_file = project_root / "setup.py"
    with open(setup_file, "rt") as fp:
        filedata = fp.read()
        m = re.search(r"version='(.*?)'", filedata)
        if not m:
            raise RuntimeError("No setup.py file found")
    expected = m.group(1)
    assert actual == expected
