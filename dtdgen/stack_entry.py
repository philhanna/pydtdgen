from dataclasses import dataclass

from dtdgen import ElementDetails


@dataclass
class StackEntry:
    """A data structure we put on the stack for each nested element"""
    element_details: ElementDetails
    sequence_number: int
    latest_child: str | None

