"""A document type definition (DTD) generator"""
import re


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


from .child_details import ChildDetails
from .attribute_details import AttributeDetails
from .element_details import ElementDetails
from .stack_entry import StackEntry
from .schema_model_builder import SchemaModelBuilder
from .dtd_generator import DTDGenerator

__all__ = [
    'ChildDetails',
    'AttributeDetails',
    'ElementDetails',
    'StackEntry',
    'SchemaModelBuilder',
    'DTDGenerator',
    'get_version',
]
