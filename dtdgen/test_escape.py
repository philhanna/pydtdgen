from unittest import TestCase

from dtdgen import escape


class Test(TestCase):

    def test_escape(self):
        s = "Now, 'Tommy'\n"
        expected = "Now, &#39;Tommy&#39;&#10;"
        actual = escape(s)
        self.assertEqual(expected, actual)