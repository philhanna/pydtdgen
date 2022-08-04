package com.philhanna.dtdgen.modelbuilder;

import java.io.IOException;
import java.io.InputStream;
import java.util.Stack;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParserFactory;

import org.xml.sax.Attributes;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import org.xml.sax.XMLReader;
import org.xml.sax.helpers.DefaultHandler;

import com.philhanna.dtdgen.AttributeModel;
import com.philhanna.dtdgen.ChildModel;
import com.philhanna.dtdgen.DocumentModel;
import com.philhanna.dtdgen.ElementModel;

/**
 * Analyzes an instance of an XML document to build a documentModel of
 * its structure
 */
public class DocumentModelBuilder extends DefaultHandler {

   // ==================================================================
   // Class constants and variables
   // ==================================================================

   /**
    * Maximum number of distinct attribute values to be included in an
    * enumeration
    */
   public static final int MAX_ENUMERATION_VALUES = 20;

   /**
    * Maximum number of attribute values to be saved while checking for
    * uniqueness
    */
   private static final int MAX_ID_VALUES = 100000;

   // ==================================================================
   // Class methods
   // ==================================================================

   // ==================================================================
   // Instance variables
   // ==================================================================

   private DocumentModel documentModel = new DocumentModel();

   /**
    * Stack of elements currently open; each entry is a StackEntry
    * object
    */
   private Stack<StackEntry> elementStack = new Stack<StackEntry>();

   // ==================================================================
   // Implementation of content handler interface
   // ==================================================================

   /**
    * Make a note whether significant character data is found in the
    * element
    */
   @Override
   public void characters(char ch[], int start, int length)
         throws SAXException {
      final ElementModel elementModel = elementStack.peek().getElementModel();
      if (!elementModel.hasCharacterContent()) {
         for (int i = start; i < start + length; i++) {
            if (ch[i] > 0x20) {
               elementModel.setHasCharacterContent(true);
               break;
            }
         }
      }
   }

   /**
    * Handle the start of an element. Record information about the
    * position of this element relative to its parent, and about the
    * attributes of the element.
    */
   @Override
   public void startElement(
         String uri,
         String localName,
         String elementName,
         Attributes attributes) throws SAXException {

      // Create an entry in the Element List, or locate the cached entry

      ElementModel elementModel = documentModel
            .getElementModel(elementName);
      if (elementModel == null) {
         elementModel = new ElementModel(elementName);
         documentModel.addElementModel(elementModel);
      }

      // Retain the associated element details object and initialize
      // sequence numbering of child element types

      final StackEntry stackEntry = new StackEntry(elementModel);

      // Count occurrences of this element type

      elementModel.incrementOccurrences();

      // Handle the attributes accumulated for this element.
      // Merge the new attribute list into the existing list for the
      // element

      for (int i = 0; i < attributes.getLength(); i++) {
         final String attributeName = attributes.getQName(i);
         final String attributeValue = attributes.getValue(i);

         AttributeModel attributeModel = elementModel
               .getAttribute(attributeName);
         if (attributeModel == null) {
            attributeModel = new AttributeModel(attributeName);
            elementModel.addAttribute(attributeModel);
         }

         if (!attributeModel.contains(attributeValue)) {

            // We haven't seen this attribute value before

            attributeModel.addValue(attributeValue);

            // Check if attribute value is a valid name

            if (attributeModel.isAllNames() && !isValidName(attributeValue)) {
               attributeModel.setAllNames(false);
            }

            // Check if attribute value is a valid NMTOKEN

            if (attributeModel.isAllNMTOKENs()
                  && !isValidNMTOKEN(attributeValue)) {
               attributeModel.setAllNMTOKENs(false);
            }

            // For economy, don't save the new value unless it's needed;
            // it's needed only if we're looking for ID values or
            // enumerated values

            if (attributeModel.isUnique()
                  && attributeModel.isAllNames()
                  && attributeModel.getOccurrences() <= MAX_ID_VALUES) {
               attributeModel.addValue(attributeValue);
            }
            else if (attributeModel.getValueCount() <= MAX_ENUMERATION_VALUES) {
               attributeModel.addValue(attributeValue);
            }

         }
         else {
            // We've seen this attribute value before
            attributeModel.setUnique(false);
         }
         attributeModel.incrementOccurrences();
      }

      // Now keep track of the nesting and sequencing of child elements

      if (!elementStack.isEmpty()) {
         final StackEntry parent = elementStack.peek();
         final ElementModel parentDetails = parent.getElementModel();

         // For sequencing, we're interested in consecutive groups of
         // the same child element type

         final boolean isFirstInGroup = !elementName
               .equals(parent.getLatestChildName());
         if (isFirstInGroup) {
            parent.incrementSequenceNumber();
         }
         parent.setLatestChildName(elementName);

         // If we've seen this child of this parent before, get the
         // details

         ChildModel childDetails = parentDetails.getChildModel(elementName);
         if (childDetails == null) {

            // This is the first time we've seen this child belonging to
            // this parent

            childDetails = new ChildModel(elementName);

            childDetails.setRepeatable(false);
            childDetails.setOptional(false);
            parentDetails.addChild(childDetails);

            // If the first time we see this child is not on the first
            // instance of the parent, then we allow it as an optional
            // element

            if (parentDetails.getOccurrences() != 1) {
               childDetails.setOptional(true);
            }
         }
         else {

            // If it's the first occurrence of the parent element, and
            // we've seen this child before, and it's the first of a new
            // group, then the child occurrences are not consecutive

            if (parentDetails.getOccurrences() == 1 && isFirstInGroup) {
               parentDetails.setSequenced(false);
            }

            // Check whether the position of this group of children in
            // this parent element is the same as its position in
            // previous instances of the parent.

            final int parentIndex = parent.getSequenceNumber();
            final int nChildren = parentDetails.getChildModelCount();
            if (nChildren <= parentIndex) {
               parentDetails.setSequenced(false);
            }
            else {
               final ChildModel childModel = parentDetails
                     .getChildModel(parentIndex);
               if (!childModel.getName().equals(elementName)) {
                  parentDetails.setSequenced(false);
               }
            }
         }

         // If there's more than one child element, mark it as
         // repeatable

         if (!isFirstInGroup) {
            childDetails.setRepeatable(true);
         }
      }
      elementStack.push(stackEntry);
   }

   /**
    * End of element. If sequenced, check that all expected children are
    * accounted for.
    */
   @Override
   public void endElement(String uri, String localName, String elementName)
         throws SAXException {

      // If the number of child element groups in this parent element is
      // less than the number in previous elements, then the absent
      // children are marked as optional

      final ElementModel elementDetails = documentModel
            .getElementModel(elementName);
      if (elementDetails.isSequenced()) {
         final StackEntry stackEntry = elementStack.peek();
         final int seq = stackEntry.getSequenceNumber();
         final int n = elementDetails.getChildModelCount();
         for (int i = seq + 1; i < n; i++) {
            final ChildModel childDetails = elementDetails.getChildModel(i);
            childDetails.setOptional(true);
         }
      }

      // Done with this element

      elementStack.pop();
   }

   // ==================================================================
   // Instance methods
   // ==================================================================

   /**
    * Runs an XML input stream through the model builder
    * @param in an input stream
    * @throws IOException if an I/O error occurs
    */
   public void run(InputStream in) throws IOException, SAXException {
      final InputSource is = new InputSource(in);
      try {
         final XMLReader parser = SAXParserFactory.newInstance().newSAXParser()
               .getXMLReader();
         parser.setContentHandler(this);
         parser.parse(is);
         in.close();
      }
      catch (ParserConfigurationException e) {
         final RuntimeException rte = new RuntimeException(
               "Error creating SAX parser",
               e);
         throw rte;
      }
      finally {
      }
   }

   /**
    * Returns the document model constructed from the XML source
    * file(s).
    */
   public DocumentModel getDocumentModel() {
      return documentModel;
   }

   // ==================================================================
   // Private methods
   // ==================================================================

   /**
    * Test whether a string is an XML name. TODO: This is currently an
    * incomplete test, it treats all non-ASCII characters as being valid
    * in names.
    */
   private boolean isValidName(String s) {
      if (!isValidNMTOKEN(s))
         return false;
      int c = s.charAt(0);
      return !((c >= 0x30 && c <= 0x39) || c == '.' || c == '-');
   }

   /**
    * Test whether a string is an XML NMTOKEN. TODO: This is currently
    * an incomplete test, it treats all non-ASCII characters as being
    * valid in NMTOKENs.
    */
   private boolean isValidNMTOKEN(String s) {
      if (s.length() == 0)
         return false;
      for (int i = 0; i < s.length(); i++) {
         int c = s.charAt(i);
         if (!((c >= 0x41 && c <= 0x5a)
               || (c >= 0x61 && c <= 0x7a)
               || (c >= 0x30 && c <= 0x39)
               || c == '.'
               || c == '_'
               || c == '-'
               || c == ':'
               || c > 128))
            return false;
      }
      return true;
   }
}
