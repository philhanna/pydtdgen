from unittest import TestCase
from dtd import AttributeModel


class TestAttributeModel(TestCase):

    def setUp(self):
        self.am = am = AttributeModel("stooge")
        am.add_value("Larry")
        am.add_value("Curly")
        am.add_value("Moe")
        am.add_value("Shemp")
        am.add_value("Curly Joe")

    def test_defaults(self):
        am = self.am
        self.assertEqual(0, am.occurrences)
        self.assertTrue(am.unique)
        self.assertTrue(am.all_names)
        self.assertTrue(am.all_nmtokens)

    def test_get_first_value(self):
        am = self.am
        self.assertEqual("Larry", am.first_value)
