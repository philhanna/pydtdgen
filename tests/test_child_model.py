from unittest import TestCase

from dtd import ChildModel


class TestChildModel(TestCase):

    def test_name(self):
        cd = ChildModel("Larry")
        self.assertEqual("Larry", cd.name)

    def test_is_repeatable(self):
        cd = ChildModel("Moe")
        self.assertFalse(cd.repeatable) # Check default
        cd.repeatable = True
        self.assertTrue(cd.repeatable)

    def test_is_optional(self):
        cd = ChildModel("Curly")
        self.assertTrue(cd.optional)    # Check default
        cd.optional = False
        self.assertFalse(cd.optional)
