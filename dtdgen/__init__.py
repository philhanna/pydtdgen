import re

from .child_details import ChildDetails
from .attribute_details import AttributeDetails
from .element_details import ElementDetails
from .stack_entry import StackEntry
from .functions import escape, is_valid_nmtoken, is_valid_name
from .dtd_generator import DTDGenerator


def get_version():
    import subprocess
    version = None
    cp = subprocess.run(['pip', 'show', 'pydtdgen'], stdout=subprocess.PIPE)
    if cp.returncode == 0:
        output = str(cp.stdout, encoding='utf-8')
        for token in output.split('\n'):
            m = re.match(r'^Version: (.*)', token)
            if m:
                version = m.group(1)
                break
    return version


__all__ = [
    'escape',
    'is_valid_nmtoken',
    'is_valid_name',
    'ChildDetails',
    'AttributeDetails',
    'ElementDetails',
    'StackEntry',
    'DTDGenerator',
    'get_version',
]
