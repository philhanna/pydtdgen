package com.philhanna.dtdgen.dtd;

import com.philhanna.dtdgen.ChildModel;
import com.philhanna.dtdgen.ElementModel;

/**
 * A DTDElementModel that represents the child content of an element
 */
public class DTDChildContentElement extends DTDElementModel {

   /**
    * Creates a new element declaration over the specified element model
    * @param elementModel the element model
    */
   public DTDChildContentElement(ElementModel elementModel) {
      super(elementModel);
   }

   /**
    * Generates the &lt;!ELEMENT (child1, child2, etc)&gt; string that
    * represents this element
    */
   @Override
   public String toString() {

      final StringBuilder sb = new StringBuilder();
      sb.append("<!ELEMENT ");
      sb.append(getElementName());
      sb.append(" ( ");

      if (elementModel.isSequenced()) {

         // All elements of this type have the same child elements
         // in the same sequence

         for (int index = 0; index < nChildren; index++) {
            final ChildModel childModel = elementModel.getChildModel(index);
            if (index > 0)
               sb.append(", ");
            sb.append(childModel.getName());
            if (childModel.isRepeatable() && !childModel.isOptional())
               sb.append("+");
            if (childModel.isRepeatable() && childModel.isOptional())
               sb.append("*");
            if (childModel.isOptional() && !childModel.isRepeatable())
               sb.append("?");
         }
         sb.append(" )");
      }
      else {

         // The children don't always appear in the same sequence,
         // so list them sequentially and allow them to be in
         // any order

         for (int index = 0; index < nChildren; index++) {
            if (index > 0)
               sb.append(" | ");
            final ChildModel childModel = elementModel.getChildModel(index);
            final String childName = childModel.getName();
            sb.append(childName);
         }
         sb.append(" )*");
      }

      sb.append(" >");
      final String output = sb.toString();
      return output;
   }
}
