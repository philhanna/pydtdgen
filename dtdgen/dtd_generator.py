from dtdgen import SchemaModelBuilder
from dtdgen.constants import MIN_ID_VALUES, MIN_FIXED
from dtdgen.constants import MIN_ENUMERATION_INSTANCES, MIN_ENUMERATION_RATIO
from dtdgen.constants import MAX_ENUMERATION_VALUES
from dtdgen.functions import escape


class DTDGenerator:
    """Creates a DTD from a document schema"""

    def __init__(self, model: SchemaModelBuilder):
        self.model: SchemaModelBuilder = model

    def run(self):
        """Generates the DTD"""

        model = self.model

        # Process the element types encountered, in turn
        for element_name, ed in model.element_map.items():

            children = ed.children
            child_keys = sorted(set([k for k in children]))

            # EMPTY content
            if len(child_keys) == 0 and not ed.has_character_content:
                print("<!ELEMENT " + element_name + " EMPTY >")

            # CHARACTER content
            if len(child_keys) == 0 and ed.has_character_content:
                print("<!ELEMENT " + element_name + " ( #PCDATA ) >")

            # ELEMENT content
            if len(child_keys) > 0 and not ed.has_character_content:
                print("<!ELEMENT " + element_name + " ( ", end='')
                if ed.sequenced:
                    # All elements of this type have the same child elements
                    # in the same sequence, retained in the childseq vector
                    outlist = []
                    for ch in ed.childseq:
                        sb = ch.name
                        if ch.repeatable and not ch.optional:
                            sb += "+"
                        if ch.repeatable and ch.optional:
                            sb += "*"
                        if ch.optional and not ch.repeatable:
                            sb += "?"
                        outlist.append(sb)
                    print(", ".join(outlist) + " ) >")

                # The childen don't always appear in the same sequence,
                # so list them alphabetically and allow them to be
                # in any order
                else:
                    sb = " | ".join(child_keys)
                    print(sb + " )* >")

            # MIXED content
            if len(child_keys) > 0 and ed.has_character_content:
                sb = f"<!ELEMENT {element_name} ( #PCDATA | {' | '.join(child_keys)} )* >"
                print(sb)

            # Now examine the attributes encountered for this element type
            attlist = ed.attributes
            done_id = False  # To ensure we have at most one ID attribute per element

            for attname, ad in sorted(attlist.items()):
                # If the attribute is present on every instance of the element,
                # treat it as required
                required: bool = (ad.occurrences == ed.occurrences)

                # If every value of the attribute is distinct,
                # and there are at least MIN_ID_VALUES, treat it as an ID.
                # TODO: this may give the wrong answer.
                # We should check whether the value sets of two
                # candidate-ID attributes overlap, in which case
                # they can't both be ID's !!
                isid: bool = ad.all_names \
                             and not done_id \
                             and ad.unique \
                             and ad.occurrences >= MIN_ID_VALUES

                # If there is only one attribute value, and at least
                # MIN_FIXED occurrences of it, treat it as FIXED
                isfixed: bool = required \
                                and len(ad.values) == 1 \
                                and ad.occurrences >= MIN_FIXED

                # If the number of distinct values is small compared with
                # the number of occurrences, treat it as an enumeration
                isenum: bool = ad.all_nmtokens \
                               and ad.occurrences >= MIN_ENUMERATION_INSTANCES \
                               and len(ad.values) <= ad.occurrences / MIN_ENUMERATION_RATIO \
                               and len(ad.values) <= MAX_ENUMERATION_VALUES

                print(f"<!ATTLIST {element_name} {attname} ", end='')
                tokentype = "NMTOKEN" if ad.all_nmtokens else "CDATA"

                if isid:
                    print("ID", end='')
                    done_id = True
                elif isfixed:
                    val: str = list(ad.values)[0]
                    print(f'{tokentype} #FIXED "{escape(val)}" >')
                elif isenum:
                    vals = " | ".join([str(val) for val in ad.values])
                    print(f"( {vals} )", end='')
                else:
                    print(tokentype, end='')
                if not isfixed:
                    if required:
                        print(" #REQUIRED >")
                    else:
                        print(" #IMPLIED >")
            print()
