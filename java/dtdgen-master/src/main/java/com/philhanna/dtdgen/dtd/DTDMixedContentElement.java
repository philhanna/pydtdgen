package com.philhanna.dtdgen.dtd;

import com.philhanna.dtdgen.ChildModel;
import com.philhanna.dtdgen.ElementModel;

/**
 * A DTDElementModel that represents an element with both element and
 * <code>#PCDATA</code>.
 */
public class DTDMixedContentElement extends DTDElementModel {

   /**
    * Creates a new element declaration over the specified element model
    * @param elementModel the element model
    */
   public DTDMixedContentElement(ElementModel elementModel) {
      super(elementModel);
   }

   /**
    * Generates the &lt;!ELEMENT&gt; string for this mixed content
    * element
    */
   @Override
   public String toString() {
      final StringBuilder sb = new StringBuilder();
      sb.append("<!ELEMENT ");
      sb.append(getElementName());
      sb.append(" ( #PCDATA");
      for (int index = 0; index < nChildren; index++) {
         final ChildModel childModel = elementModel.getChildModel(index);
         final String childName = childModel.getName();
         sb.append(" | " + childName);
      }
      sb.append(" )* >");

      final String output = sb.toString();
      return output;
   }

}
