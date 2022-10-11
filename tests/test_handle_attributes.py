from unittest import TestCase

from dtdgen import ElementDetails, DTDGenerator, AttributeDetails


class TestHandleAttributes(TestCase):

    def test_rank(self):
        # First occurrence of <stooge name="..." rank="...">
        attrs = {"name": "Larry", "rank": "2"}
        ed = ElementDetails("stooge")
        DTDGenerator.handle_attributes(attrs, ed)
        attributes = ed.attributes
        self.assertIn("rank", attributes)
        attr = attributes["rank"]
        self.assertEqual("rank", attr.name)
        self.assertEqual(1, attr.occurrences)
        self.assertTrue(attr.unique)
        self.assertIn("2", attr.values)
        self.assertFalse(attr.all_names)  # "2" is not a valid name
        self.assertTrue(attr.all_nmtokens)

    def test_rank_required(self):
        ed = ElementDetails("stooge")

        test_values = [
            {"name": "Larry", "rank": "2"},
            {"name": "Curly", "rank": "3"},
            {"name": "Moe", "rank": "1"},
        ]
        for attrs in test_values:
            DTDGenerator.handle_attributes(attrs, ed)

        # Check what we know about the rank attribute
        attr: AttributeDetails = ed.attributes["rank"]
        self.assertEqual("rank", attr.name)
        self.assertEqual(3, attr.occurrences, "We have seen this attribute 3 times")
        self.assertTrue(attr.unique, "Every value was different")
        self.assertSetEqual({"1", "2", "3"}, attr.values)
