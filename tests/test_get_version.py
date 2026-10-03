import tomllib

from dtdgen import get_version
from tests import project_root


def test_get_version():
    actual = get_version()
    pyproject_file = project_root / "pyproject.toml"
    with open(pyproject_file, "rb") as fp:
        pyproject = tomllib.load(fp)
    expected = pyproject["project"]["version"]
    assert actual == expected
