from .attribute_model import AttributeModel
from .child_model import ChildModel
from .element_model import ElementModel
from .document_model import DocumentModel
from .run_main import RunMain

__version__ = "0.0.3"
__version_info__ = tuple([ int(num) for num in __version__.split('.')])

# Minimum number of appearances of an attribute for it to be considered
# a candidate for an enumeration type
MIN_ENUMERATION_INSTANCES: int = 10

# Maximum number of distinct attribute values to be included
# in an enumeration
MAX_ENUMERATION_VALUES = 20

# An attribute will be regarded as an enumeration attribute only if the
# number of instances divided by the number of distinct values
# is >= this ratio
MIN_ENUMERATION_RATIO = 3

# Minimum number of attributes that must appear, with the same value
# each time, for the value to be regarded as FIXED
MIN_FIXED: int = 5

# Minumum number of attribute values that must appear for the attribute
# to be regarded as an ID value
MIN_ID_VALUES = 10

# Maximum number of attribute values to be saved while checking for uniqueness
MAX_ID_VALUES = 100000

__all__ = [
    'MIN_ENUMERATION_INSTANCES',
    'MAX_ENUMERATION_VALUES',
    'MIN_ENUMERATION_RATIO',
    'MIN_FIXED',
    'MIN_ID_VALUES',
    'MAX_ID_VALUES',
    'AttributeModel',
    'ChildModel',
    'ElementModel',
    'DocumentModel',
    'RunMain',
]
