from dataclasses import dataclass


@dataclass
class AttributeDetails:
    """a data structure to keep information about attribute types"""
    name: str
    occurrences: int
    unique: bool
    values: set[str]
    all_names: bool
    all_nmtokens: bool
