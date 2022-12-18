#! /usr/bin/python
import argparse
import sys

from dtdgen import SchemaModelBuilder, get_version, DTDGenerator

parser = argparse.ArgumentParser(description="""
Creates a document type description (DTD) from a sample XML file.
""")
parser.add_argument('-v', '--version', action='version', version=f'{get_version()}',
                    help='display version number')
parser.add_argument('filename', help='Input xml file')
args = parser.parse_args()

model_builder = SchemaModelBuilder()
try:
    model_builder.run(args.filename)
    dtd_generator = DTDGenerator(model_builder)
    dtd_generator.run()
except Exception as ex:
    print(str(ex), file=sys.stderr)