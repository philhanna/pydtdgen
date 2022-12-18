import pytest

from dtdgen import is_valid_nmtoken


@pytest.mark.parametrize("test_input", [
    "NowIsTheTime",
    "Now2Is34The567Time",
    "Now.Is_The-Time:",
    "1",
    ".Now",
    "_Now",
    "-Now",
    ":Now",
])
def test_good(test_input):
    """These should all be valid"""
    assert is_valid_nmtoken(test_input)


@pytest.mark.parametrize("test_input", [
    "Now is the time",
    "Now;",
])
def test_bad(test_input):
    """These are all invalid"""
    assert not is_valid_nmtoken(test_input)
