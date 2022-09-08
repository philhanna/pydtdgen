from unittest import TestCase

from dtdgen import ElementModel
from dtdgen.dtd import DTDPCDATAElement


class TestDTDPCDATAElement(TestCase):
    def test_with_string(self):
        em = ElementModel("stooges")
        pcde = DTDPCDATAElement(em)
        self.assertEqual("<!ELEMENT stooges ( #PCDATA ) >", str(pcde))

