from html import escape
from typing import List

from dtdgen import ElementModel, MIN_FIXED, MIN_ENUMERATION_INSTANCES, MIN_ENUMERATION_RATIO, MAX_ENUMERATION_VALUES, \
    AttributeModel


def quoted(arg):
    return '"' + arg + '"'


class DTDAttributeList:
    """The list of <!ATTLIST> for an element"""
    def __init__(self, element_model: ElementModel):
        self._element_model: ElementModel = element_model
        self._alist: List[str] = self.get_attlists()

    @property
    def alist(self):
        return self._alist

    def get_attlists(self):
        element_model: ElementModel = self._element_model
        element_name: str = element_model.name
        attlists: list[str] = []

        for attr_name in element_model.attribute_names():
            attr_model: AttributeModel = element_model.get_attribute_model(attr_name)

            # Start creating the string
            sb: str = f"<!ATTLIST {element_name} {attr_name}"

            # If the attribute is present on every instance of the
            # element, treat it as required
            required: bool = (attr_model.occurrences == element_model.occurrences)

            # If there is only one attribute value, and at least
            # MIN_FIXED occurrences of it, treat it as FIXED
            is_fixed: bool = all([
                required,
                attr_model.value_count == 1,
                attr_model.occurrences >= MIN_FIXED])

            # If the number of distinct values is small compared with
            # the number of occurrences, treat it as an enumeration.
            # NOTE: Enumeration values must be NMTOKENs
            is_enum: bool = all([
                 attr_model.all_nmtokens,
                 attr_model.occurrences >= MIN_ENUMERATION_INSTANCES,
                 attr_model.value_count <= (attr_model.occurrences / MIN_ENUMERATION_RATIO),
                 attr_model.value_count <= MAX_ENUMERATION_VALUES])

            token_type: str = "NMTOKEN" if attr_model.all_nmtokens else "CDATA"
            if attr_name == element_model.id_attribute_name():
                sb += " ID"
            elif is_fixed:
                sb += f" {token_type} #FIXED"
                sb += f" {quoted(escape(attr_model.first_value))}"
                sb += " >"
            elif is_enum:
                sb += " ( "
                sb += " | ".join(attr_model.values)
                sb += " ) "
            else:
                sb += f" {token_type}"

            if not is_fixed:
                sb += " #REQUIRED>" if required else " #IMPLIED>"

            attlists.append(sb)

        return attlists
