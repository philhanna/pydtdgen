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
        """ Makes sure that the list is not alphabetical,
        but in arrival sequence. """
        am = self.am
        self.assertEqual("Larry", am.first_value)

    def test_get_first_value_on_empty_list(self):
        am = AttributeModel("stooge")
        self.assertIsNone(am.first_value)
        am.add_value("Max")
        self.assertEqual("Max", am.first_value)

    def test_increment_occurrences(self):
        am = self.am
        self.assertEqual(0, am.occurrences)
        am.increment_occurrences()
        am.increment_occurrences()
        am.increment_occurrences()
        self.assertEqual(3, am.occurrences)

    def test_contains(self):
        am = self.am
        for name in ["Larry", "Curly", "Moe", "Shemp", "Curly Joe"]:
            self.assertTrue(am.contains(name), f'Attribute model does not contain "{name}"')
        for name in ["bogus", "", None]:
            self.assertFalse(am.contains(name), f'Attribute model contains "{name}"')

    def test_values(self):
        expected_list = ["Larry", "Curly", "Moe", "Shemp", "Curly Joe"]
        actual_list = self.am.values
        self.assertListEqual(expected_list, actual_list)

    def test_str(self):
        print(self.am)