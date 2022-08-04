package com.philhanna.dtdgen.dtd;

import com.philhanna.dtdgen.ElementModel;

/**
 * A DTDElementModel that represents the an element with parsed
 * character content (<code>#PCDATA</code>)
 */
public class DTDPCDATAElement extends DTDElementModel {

   /**
    * Creates a new element declaration over the specified element model
    * @param elementModel the element model
    */
   public DTDPCDATAElement(ElementModel elementModel) {
      super(elementModel);
   }

   /**
    * Generates the &lt;!ELEMENT <code>&lt;name&gt;</code> ( #PCDATA ) &gt; string
    */
   @Override
   public String toString() {
      final String output = String
            .format("<!ELEMENT %s ( #PCDATA ) >", getElementName());
      return output;
   }
}
