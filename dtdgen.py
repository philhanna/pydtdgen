#! /usr/bin/python
import argparse
import sys

from dtdgen import DTDGenerator, get_version

parser = argparse.ArgumentParser(description="""
Creates a document type description (DTD) from a sample XML file.
""")
parser.add_argument('-v', '--version', action='version', version=f'{get_version()}',
                    help='display version number')
parser.add_argument('filename', help='Input xml file')
args = parser.parse_args()

app = DTDGenerator()
try:
    app.run(args.filename)
    app.print_dtd()
except Exception as ex:
    print(str(ex), file=sys.stderr)