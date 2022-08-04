# DTDGen - XML DTD Generator

## Purpose

DTDGen is a program that takes an XML document as input and produces a
Document Type Definition (DTD) as output.

The aim of the program is to give you a quick start in writing a DTD.
The DTD is one of the many possible DTDs to which the input document
conforms. Typically, you will want to examine the DTD and edit it to
describe your intended documents more precisely. In a few cases you will
have to edit the DTD before you can use it.

## Usage

First install a parser and, if necessary, the SAX Driver for that
parser. Details of SAX parsers are available at
[www.microstar.com](http://www.microstar.com)

Install the supplied class files in a directory on your CLASSPATH.

From the command line, enter:

` java -Dsax.parser=parser DTDGen inputfile >outputfile`

The input file must be an XML document; typically it will have no DTD.
If it does have a DTD, the DTD will be used by the parser but it will be
ignored by the DTDGen utility.

The *parser* parameter must be the name of a class that implements the
SAX interface.

The output file will be an XML external document type definition.

The input file is not modified; if you want to edit it to refer to the
generated DTD, you must do this yourself.

## What it does

The program makes a list of all the elements and attributes that appear
in your document, noting how they are nested, and noting which elements
contain character data.

When the document has been completely processed, the DTD is generated
according to the following rules:

-   It is assumed that the elements appearing within a given element can
    appear in any order and can each be repeated. The generated DTD will
    impose no ordering rules, only nesting rules.
-   If no significant character data is found in an element, it is
    assumed that the element cannot contain character data.
-   If neither character data nor subordinate elements are found in an
    element, it is assumed the element must always be empty.
-   An attribute appearing in an element is assumed to be REQUIRED if it
    appears in every occurrence of the element.
-   An attribute that has a distinct value every time it appears is
    assumed to be an identifying (ID) attribute, provided that there are
    at least 10 instances of the element in the input document.
-   An attribute is assumed to be an enumeration attribute if it has
    less than ten distinct values, provided that the number of instances
    of the attribute is at least three times the number of distinct
    values and at least ten. *There is currently a limitation: DTDGen
    does not check that the attribute values all conform to the XML
    syntax restrictions for enumerated attributes.*

The resulting DTD will often contain rules that are either too
restrictive or too liberal. The DTD may be too restrictive if it
prohibits constructs that do not appear in this document, but might
legitimately appear in others. It may be too liberal if it fails to
detect patterns that are inherent to the structure: for example, the
order of elements within a parent element. These limitations are
inherent in any attempt to infer general rules from a particular example
document.

In general, therefore, you will need to iterate the process. You have a
choice:

-   Either edit the generated DTD to reflect your knowledge of the
    document type.
-   Or edit the input document to provide a more representative sample
    of features that will be encountered in other document instances,
    and run the utility again.

------------------------------------------------------------------------

## About DTDGen

DTDGen was written by [Michael Kay](mailto:M.H.Kay@eng.icl.co.uk) of
[ICL](http://www.icl.com).

It is supplied (and was written) as an demonstration of how to use the
SAX interface to XML parsers. It has not been written or tested to
production quality and you should not rely on it working.

I would like to know about bugs or enhancement suggestions but cannot
guarantee to respond.

You may freely distribute DTDGen provided you include this description
of the program *as is*. If you want to produce an improved version,
please consult the author.

------------------------------------------------------------------------

*Michael H. Kay\
29 April 1998*
