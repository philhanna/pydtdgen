from dataclasses import dataclass


@dataclass
class AttributeDetails:
    name: str
    occurrences: int
    unique: bool
    values: set[str]
    all_names: bool
    all_nmtokens: bool
