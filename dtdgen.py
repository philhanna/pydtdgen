#! /usr/bin/python
import argparse

from dtdgen import DTDGenerator

parser = argparse.ArgumentParser(description='DTDGenerator')
parser.add_argument('-v', '--version', action='store_true', help='display version number')
parser.add_argument('filename', help='Input xml file')
args = parser.parse_args()

app = DTDGenerator()
app.run(args.filename)
app.print_dtd()
