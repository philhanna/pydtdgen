from dataclasses import dataclass, field


@dataclass
class AttributeDetails:
    """A data structure to keep information about attribute types"""
    name: str
    occurrences: int = 0
    unique: bool = True
    values: set[str] = field(default_factory=set)
    all_names: bool = True
    all_nmtokens: bool = True
