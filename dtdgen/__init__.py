from .attribute_model import AttributeModel
from .child_model import ChildModel
from .element_model import ElementModel
from .document_model import DocumentModel

__version__ = "0.0.3"
__version_info__ = tuple([ int(num) for num in __version__.split('.')])

__all__ = [
    'AttributeModel',
    'ChildModel',
    'ElementModel',
    'DocumentModel',
]
