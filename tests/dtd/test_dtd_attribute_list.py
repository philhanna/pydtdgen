from unittest import TestCase

from dtdgen import ElementModel
from dtdgen.dtd import DTDAttributeList


class TestDTDAttributeList(TestCase):

    def test_no_attributes(self):
        element_model = ElementModel("stooges")
        dtd_attribute_list = DTDAttributeList(element_model)
        expected = []
        actual = dtd_attribute_list.alist
        self.assertListEqual(expected, actual)

    def test_two_attributes(self):
        element_model = ElementModel("stooge")
        n_element_occurrences: int = 12
        # Create the "name" attribute
