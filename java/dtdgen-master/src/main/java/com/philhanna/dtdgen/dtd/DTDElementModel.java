package com.philhanna.dtdgen.dtd;

import com.philhanna.dtdgen.ElementModel;

/**
 * Abstract base class for DTD generators for child content, empty
 * elements, mixed content elements, and PCDATA.
 */
public abstract class DTDElementModel {

   protected final ElementModel elementModel;
   protected final int nChildren;

   /**
    * Creates a DTDElementModel over the specified model
    * @param elementModel the element model
    */
   public DTDElementModel(ElementModel elementModel) {
      this.elementModel = elementModel;
      this.nChildren = elementModel.getChildModelCount();
   }

   /**
    * Returns the element model name
    * @return the element model name
    */
   public String getElementName() {
      return elementModel.getName();
   }
}
