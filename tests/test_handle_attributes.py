from dtdgen import ElementDetails, SchemaModelBuilder, AttributeDetails


def test_rank():
    # First occurrence of <stooge name="..." rank="...">
    attrs = {"name": "Larry", "rank": "2"}
    ed = ElementDetails("stooge")
    SchemaModelBuilder.handle_attributes(attrs, ed)
    attributes = ed.attributes
    assert "rank" in attributes

    attr: AttributeDetails = attributes["rank"]
    assert "rank" == attr.name
    assert 1 == attr.occurrences
    assert attr.unique
    assert "2" in attr.values
    assert not attr.all_names  # "2" is not a valid name
    assert attr.all_nmtokens


def test_rank_required():
    ed = ElementDetails("stooge")

    test_values = [
        {"name": "Larry", "rank": "2"},
        {"name": "Curly", "rank": "3"},
        {"name": "Moe", "rank": "1"},
    ]
    for attrs in test_values:
        SchemaModelBuilder.handle_attributes(attrs, ed)

    # Check what we know about the rank attribute
    attr: AttributeDetails = ed.attributes["rank"]
    assert "rank" == attr.name
    assert 3 == attr.occurrences
    assert attr.unique
    assert {"1", "2", "3"} == attr.values
