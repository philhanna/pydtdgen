from unittest import TestCase

from dtdgen import is_valid_nmtoken


class TestIsValidNMTOKEN(TestCase):

    def test_all_alpha(self):
        self.assertTrue(is_valid_nmtoken("NowIsTheTime"))

    def test_all_alpha_or_digits(self):
        self.assertTrue(is_valid_nmtoken("Now2Is34The567Time"))

    def test_dot_dash_hyphen_colon(self):
        self.assertTrue(is_valid_nmtoken("Now.Is_The-Time:"))

    def test_starts_with_digit(self):
        self.assertTrue(is_valid_nmtoken("1"))

    def test_starts_with_dot(self):
        self.assertTrue(is_valid_nmtoken(".Now"))

    def test_starts_with_dash(self):
        self.assertTrue(is_valid_nmtoken("_Now"))

    def test_starts_with_hyphen(self):
        self.assertTrue(is_valid_nmtoken("-Now"))

    def test_starts_with_colon(self):
        self.assertTrue(is_valid_nmtoken(":Now"))

    def test_bad_has_spaces(self):
        self.assertFalse(is_valid_nmtoken("Now is the time"))

    def test_bad_has_semicolon(self):
        self.assertFalse(is_valid_nmtoken("Now;"))
