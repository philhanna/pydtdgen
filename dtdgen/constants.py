"""Global constants"""


# Maximum number of attribute values to be saved
# while checking for uniqueness
MAX_ID_VALUES: int = 100000

# Minumum number of attribute values that must appear
# for the attribute to be regarded as an ID value
MIN_ID_VALUES: int = 10

# Maximum number of distinct attribute values to be included in an enumeration
MAX_ENUMERATION_VALUES: int = 20

# Minimum number of appearances of an attribute for it to be considered
# a candidate for an enumeration type
MIN_ENUMERATION_INSTANCES: int = 10

# An attribute will be regarded as an enumeration attribute
# only if the number of instances divided by the number of
# distinct values is >= this ratio
MIN_ENUMERATION_RATIO: float = 3.0

# Minimum number of attributes that must appear, with
# the same value each time, for the value to be regarded
# as FIXED
MIN_FIXED: int = 5

__all__ = [
    'MAX_ID_VALUES',
    'MIN_ID_VALUES',
    'MAX_ENUMERATION_VALUES',
    'MIN_ENUMERATION_INSTANCES',
    'MIN_ENUMERATION_RATIO',
    'MIN_FIXED',
]