from unittest import TestCase

from dtdgen import ElementModel, AttributeModel
from dtdgen.dtd import DTDAttributeList


class TestDTDAttributeList(TestCase):

    def test_no_attributes(self):
        element_model = ElementModel("stooges")
        dtd_attribute_list = DTDAttributeList(element_model)
        expected = []
        actual = dtd_attribute_list.alist
        self.assertListEqual(expected, actual)

    def test_name_rank_attributes(self):
        elem_stooge = ElementModel("stooge")

        attr_name = AttributeModel("name")
        attr_name.occurrences = 3
        attr_name.unique = True
        attr_name.all_names = True
        attr_name.all_nmtokens = True
        for value in ["Larry", "Curly", "Moe"]:
            attr_name.add_value(value)
        elem_stooge.add_attribute(attr_name)

        attr_rank = AttributeModel("rank")
        attr_rank.occurrences = 3
        attr_rank.unique = True
        attr_rank.all_names = False
        attr_rank.all_nmtokens = False
        for value in ["1", "2", "3"]:
            attr_rank.add_value(value)
        elem_stooge.add_attribute(attr_rank)

        expected = [
            "<!ATTLIST stooge name NMTOKEN #IMPLIED>",
            "<!ATTLIST stooge rank CDATA #IMPLIED>"
        ]
        actual = DTDAttributeList(elem_stooge).get_attlists()
        self.assertListEqual(expected, actual)