from unittest import TestCase

from dtdgen import escape


def fmt2(n: int):
    return ("0" + str(n))[-2:]


class TestEscape(TestCase):

    def test_single_quotes(self):
        s = "Now, 'Tommy'\n"
        expected = "Now, &#39;Tommy&#39;&#10;"
        actual = escape(s)
        self.assertEqual(expected, actual)

    def test0020(self):
        for i in range(0x00,0x20):
            expected = "&#" + fmt2(i) + ";"
            actual = escape(chr(i))
            self.assertEqual(expected, actual)

    def test80100(self):
        for i in range(0x80,0x100):
            expected = "&#" + fmt2(i) + ";"
            actual = escape(chr(i))
            self.assertEqual(expected, actual)
