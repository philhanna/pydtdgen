package com.philhanna.dtdgen.dtd;

import com.philhanna.dtdgen.ElementModel;

/**
 * A DTDElementModel that represents an empty element (one that has no
 * children)
 */
public class DTDEmptyElement extends DTDElementModel {

   /**
    * Creates a new empty element over the specified element model
    * @param elementModel the element model
    */
   public DTDEmptyElement(ElementModel elementModel) {
      super(elementModel);
   }

   /**
    * Generates the &lt;!ELEMENT <i>&lt;name&gt;</i> EMPTY&gt;
    */
   @Override
   public String toString() {
      final String output = String
            .format("<!ELEMENT %s EMPTY >", getElementName());
      return output;
   }

}
