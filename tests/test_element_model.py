from unittest import TestCase

from dtdgen import ElementModel, ChildModel, AttributeModel


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

    def test_get_attribute_model(self):
        em = ElementModel("stooge")

        am1 = AttributeModel("rank")
        am1.increment_occurrences()
        am1.increment_occurrences()
        am1.increment_occurrences()
        em.add_attribute(am1)

        actual = em.get_attribute_model("rank")
        self.assertEqual("rank", actual.name)
        self.assertEqual(3, actual.occurrences)

        am2 = AttributeModel("age")
        em.add_attribute(am2)

        actual = em.get_attribute_model("age")
        self.assertEqual("age", actual.name)
        self.assertEqual(0, actual.occurrences)

    def test_id_attribute_name(self):
        em = ElementModel("stooge")

        am = AttributeModel("name")
        am.occurrences = 100
        am.all_names = True
        em.add_attribute(am)
        actual = em.id_attribute_name()

        am = AttributeModel("rank")
        em.add_attribute(am)
        actual = em.id_attribute_name()

        expected = "name"
        self.assertEqual(expected, actual)

