from dtdgen import escape, fmt2


def test_single_quotes():
    s = "Now, 'Tommy'\n"
    expected = "Now, &#39;Tommy&#39;&#10;"
    actual = escape(s)
    assert actual == expected


def test0020():
    for i in range(0x00, 0x20):
        expected = "&#" + fmt2(i) + ";"
        actual = escape(chr(i))
        assert actual == expected


def test80100():
    for i in range(0x80, 0x100):
        expected = "&#" + fmt2(i) + ";"
        actual = escape(chr(i))
        assert actual == expected


def test_angles():
    s = "<abc&>\""
    expected = "&lt;abc&amp;&gt;&#34;"
    actual = escape(s)
    assert actual == expected