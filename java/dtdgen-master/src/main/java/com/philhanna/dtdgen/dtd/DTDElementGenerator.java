package com.philhanna.dtdgen.dtd;

import java.io.PrintWriter;

import com.philhanna.dtdgen.ElementModel;

/**
 * Assembles the correct DTD statement for an element and outputs it.
 */
public class DTDElementGenerator {

   // ====================================================================
   // Class constants and variables
   // ====================================================================

   // ====================================================================
   // Class methods
   // ====================================================================

   // ====================================================================
   // Instance variables
   // ====================================================================

   private ElementModel elementModel;

   // ====================================================================
   // Constructors
   // ====================================================================

   /**
    * Creates a DTD element generator for the specified element
    * @param elementModel the element model
    */
   public DTDElementGenerator(ElementModel elementModel) {
      this.elementModel = elementModel;
   }

   // ====================================================================
   // Instance methods
   // ====================================================================

   /**
    * Constructs the DTD string appropriate for this element and writes
    * it to the specified output.
    * @param out a PrintWriter for the generated element.
    */
   public void printDTD(PrintWriter out) {

      DTDElementModel dtdElementModel = null;

      // Get the number of children this element can have

      final int nChildren = elementModel.getChildModelCount();
      final boolean hasCharacterContent = elementModel.hasCharacterContent();

      // No children - must be either EMPTY or have #PCDATA content
      // Has children - either element content or mixed content

      if (nChildren == 0) {
         if (hasCharacterContent)
            dtdElementModel = new DTDPCDATAElement(elementModel);
         else
            dtdElementModel = new DTDEmptyElement(elementModel);
      }
      else {
         if (hasCharacterContent)
            dtdElementModel = new DTDMixedContentElement(elementModel);
         else
            dtdElementModel = new DTDChildContentElement(elementModel);
      }

      // Print this element

      out.println(dtdElementModel.toString());

      // Print the <!ATTLIST> lines, followed by a blank line

      for (final String attlist : DTDGenerator.getATTLISTs(elementModel)) {
         out.println(attlist);
      }

      // Blank line

      out.println();
   }
}
