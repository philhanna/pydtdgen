from unittest import TestCase

from dtdgen import ElementModel, ChildModel


class TestElementModel(TestCase):

    def test_get_child_model(self):

        em = ElementModel("stooges")

        child_name = "stooge"
        cm = ChildModel(child_name)
        em.add_child(cm)

        expected_name = child_name
        actual = em.get_child_model(index=0)
        actual_name = actual.name
        self.assertEqual(expected_name, actual_name)

        actual = em.get_child_model(name=child_name)
        self.assertIsNotNone(actual)
        actual_name = actual.name
        self.assertEqual(expected_name, actual_name)
