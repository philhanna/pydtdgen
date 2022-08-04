package com.philhanna.dtdgen.dtd;

import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Set;

import org.apache.log4j.Logger;

import com.philhanna.dtdgen.AttributeModel;
import com.philhanna.dtdgen.ChildModel;
import com.philhanna.dtdgen.DocumentModel;
import com.philhanna.dtdgen.ElementModel;
import com.philhanna.dtdgen.modelbuilder.DocumentModelBuilder;

/**
 * Generates a possible DTD from a {@link DocumentModel}
 */
public class DTDGenerator {

   // ====================================================================
   // Class constants and variables
   // ====================================================================

   private static final Logger log = Logger.getLogger(DTDGenerator.class);

   /**
    * Minimum number of appearances of an attribute for it to be
    * considered a candidate for an enumeration type
    */
   private static final int MIN_ENUMERATION_INSTANCES = 10;

   /**
    * An attribute will be regarded as an enumeration attribute only if
    * the number of instances divided by the number of distinct values
    * is &gt;= this ratio
    */
   private static final int MIN_ENUMERATION_RATIO = 3;

   /**
    * Minimum number of attributes that must appear, with the same value
    * each time, for the value to be regarded as FIXED
    */
   private static final int MIN_FIXED = 5;

   // ====================================================================
   // Class methods
   // ====================================================================

   /**
    * Constructs the list of &lt;!ATTLIST&gt; for an element
    * 
    * @param elementModel an element model
    * @return an array of strings with the &lt;!ATTLIST&gt;s
    */
   public static final String[] getATTLISTs(ElementModel elementModel) {

      final String elementName = elementModel.getName();
      final List<String> list = new ArrayList<String>();
      final String idAttributeName = elementModel.getIDAttributeName();
      final StringBuilder sb = new StringBuilder();

      for (Iterator<String> it = elementModel.attributeNameIterator(); it
            .hasNext();) {
         final String attributeName = it.next();
         final AttributeModel attributeModel = elementModel
               .getAttributeModel(attributeName);

         // Start creating the string

         sb.setLength(0);
         sb.append("<!ATTLIST ").append(elementName).append(" ")
               .append(attributeName);

         // If the attribute is present on every instance of the
         // element, treat it as required

         final int nAttributeOccurrences = attributeModel.getOccurrences();
         final int nElementOccurrences = elementModel.getOccurrences();
         final boolean required = (nAttributeOccurrences == nElementOccurrences);

         // If there is only one attribute value, and at least
         // MIN_FIXED occurrences of it, treat it as FIXED

         final boolean isFixed = required
               && attributeModel.getValueCount() == 1
               && attributeModel.getOccurrences() >= DTDGenerator.MIN_FIXED;

         // If the number of distinct values is small compared with
         // the number of occurrences, treat it as an enumeration

         // Enumeration values must be NMTOKENs
         final boolean isEnum = attributeModel.isAllNMTOKENs()
               && (attributeModel
                     .getOccurrences() >= DTDGenerator.MIN_ENUMERATION_INSTANCES)
               && (attributeModel
                     .getValueCount() <= attributeModel.getOccurrences()
                           / DTDGenerator.MIN_ENUMERATION_RATIO)
               && (attributeModel
                     .getValueCount() <= DocumentModelBuilder.MAX_ENUMERATION_VALUES);

         final String tokenType = attributeModel.isAllNMTOKENs()
               ? "NMTOKEN"
               : "CDATA";

         if (attributeName.equals(idAttributeName)) {
            sb.append(" ID");
         }
         else if (isFixed) {
            final String val = attributeModel.getFirstValue();
            sb.append(" ").append(tokenType).append(" #FIXED");
            sb.append(" \"").append(escape(val)).append("\"");
            sb.append(" >");
         }
         else if (isEnum) {
            sb.append(" ( ");
            int n = 0;
            for (Iterator<String> it2 = attributeModel.valueIterator(); it2
                  .hasNext();) {
               n++;
               if (n > 1)
                  sb.append(" | ");
               final String value = it2.next();
               sb.append(value);
            }
            sb.append(" )");
         }
         else
            sb.append(" ").append(tokenType);

         if (!isFixed) {
            if (required)
               sb.append(" #REQUIRED >");
            else
               sb.append(" #IMPLIED >");
         }

         final String result = sb.toString();
         list.add(result);
      }
      return list.toArray(new String[list.size()]);
   }

   /**
    * Escapes special characters in a String value.
    * 
    * @param in The input string
    * @return The XML representation of the string.
    *         <p>
    *         This static method converts a Unicode string to a string
    *         containing only ASCII characters, in which non-ASCII
    *         characters are represented by the usual XML/HTML escape
    *         conventions (for example, "&lt;" becomes "&amp;lt;").
    *         </p>
    *         <p>
    *         <b>Note:</b> If the input consists solely of ASCII or
    *         Latin-1 characters, the output will be equally valid in
    *         XML and HTML. Otherwise it will be valid only in XML.
    *         </p>
    */
   public static String escape(String in) {
      final StringBuffer sb = new StringBuffer();
      for (int i = 0, n = in.length(); i < n; i++) {
         char ch = in.charAt(i);
         switch (ch) {
            case '<':
               sb.append("&lt;");
               break;
            case '>':
               sb.append("&gt;");
               break;
            case '&':
               sb.append("&amp;");
               break;
            case '"':
               sb.append("&#34;");
               break;
            case '\'':
               sb.append("&#39;");
               break;
            default:
               if (ch <= 0x7F)
                  sb.append(ch);
               else {
                  sb.append("&#");
                  sb.append(Integer.toString(ch));
                  sb.append(";");
               }
               break;
         }
      }
      final String output = sb.toString();
      return output;
   }

   // ====================================================================
   // Instance variables
   // ====================================================================

   private DocumentModel model;

   // ====================================================================
   // Constructors
   // ====================================================================

   public DTDGenerator(DocumentModel model) {
      this.model = model;
   }

   // ====================================================================
   // Instance methods
   // ====================================================================

   /**
    * Construct the DTD from the model
    */
   public void printDTD(PrintWriter out) {

      // Make a list of all elements that have been printed. At the
      // start, the list will be empty. As we print each one, we add it
      // to the list to avoid getting into a recursive loop.

      final Set<String> alreadyPrinted = new HashSet<String>();

      // Now get the root element, print it, remove it from the list,
      // and then process all its immediate children

      final String rootElementName = model.getRootElementName();
      printDTD(rootElementName, alreadyPrinted, out);
   }

   /**
    * Print the DTD for one element
    */
   public void printDTD(
         final String elementName,
         final Set<String> alreadyPrinted,
         final PrintWriter out) {

      // Check the list of already printed elements to prevent
      // recursion. If this name is in the list, just return

      if (alreadyPrinted.contains(elementName))
         return;

      log.info(String.format("Printing DTD for element <%s>", elementName));
      // Immediately add it to the list so we won't print it again

      alreadyPrinted.add(elementName);

      // Get the element model and pass it to a DTD element generator

      final ElementModel elementModel = model.getElementModel(elementName);
      final DTDElementGenerator elementGenerator = new DTDElementGenerator(
            elementModel);

      // Print the DTD for this element

      elementGenerator.printDTD(out);

      // Recurse over all the children

      final int nChildren = elementModel.getChildModelCount();
      for (int index = 0; index < nChildren; index++) {
         final ChildModel childModel = elementModel.getChildModel(index);
         final String childName = childModel.getName();
         printDTD(childName, alreadyPrinted, out);
      }
   }
}
