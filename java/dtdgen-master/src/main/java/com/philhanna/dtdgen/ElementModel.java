package com.philhanna.dtdgen;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import com.philhanna.dtdgen.dtd.DTDGenerator;

/**
 * Keeps track of the the possible contents of an element, based on all
 * instances of it found in the source XML.
 */
public class ElementModel {

   // ==================================================================
   // Class constants and variables
   // ==================================================================

   // ==================================================================
   // Class methods
   // ==================================================================

   // ==================================================================
   // Instance variables
   // ==================================================================

   private final String name;
   private int occurrences = 0;
   private boolean hasCharacterContent = false;
   private boolean sequenced = true;
   private final List<ChildModel> childseq = new ArrayList<ChildModel>();
   private final Map<String, AttributeModel> attributes = new LinkedHashMap<String, AttributeModel>();

   /**
    * Minimum number of attribute values that must appear for the
    * attribute to be regarded as an ID value
    */
   protected static final int MIN_ID_VALUES = 10;

   // ==================================================================
   // Constructors
   // ==================================================================

   public ElementModel(String name) {
      this.name = name;
   }

   // ==================================================================
   // Implementation of ElementModel interface
   // ==================================================================

   /**
    * Returns the element tag name
    */
   public String getName() {
      return name;
   }

   /**
    * Returns the number of times this element was found in the input
    * XML
    */
   public int getOccurrences() {
      return occurrences;
   }

   /**
    * Returns the <code>ChildModel</code> for the child element with the
    * specified name
    * @param name the name of the child element
    * @return the <code>ChildModel</code> element, or <code>null</code>,
    *         if this element does not have a child with that name.
    */
   public ChildModel getChildModel(String name) {
      for (final ChildModel childDetails : childseq) {
         if (childDetails.getName().equals(name))
            return childDetails;
      }
      return null;
   }

   /**
    * Returns the number of <code>ChildModel</code> elements this parent
    * element has
    */
   public int getChildModelCount() {
      return childseq.size();
   }

   /**
    * Returns the specified <code>ChildModel</code> element
    * @param index the index within the list of children (zero-based)
    */
   public ChildModel getChildModel(int index) {
      return childseq.get(index);
   }

   /**
    * Returns <code>true</code> if this element can have character
    * content
    */
   public boolean hasCharacterContent() {
      return hasCharacterContent;
   }

   /**
    * Returns <code>true</code> if this element's children always occur
    * in a specific sequence
    */
   public boolean isSequenced() {
      return sequenced;
   }

   /**
    * Returns an iterator over the list of attribute names (in the order
    * that they first appear in the DTD)
    */
   public Iterator<String> attributeNameIterator() {
      return attributes.keySet().iterator();
   }

   /**
    * Returns the attribute with the specified name, or
    * <code>null</code>, if no such attribute exists
    * @param name the attribute name
    */
   public AttributeModel getAttributeModel(String name) {
      return attributes.get(name);
   }

   /**
    * Returns the name of the ID attribute, if one can be inferred,
    * otherwise returns <code>null</code>.
    */
   public String getIDAttributeName() {

      for (final String attrName : attributes.keySet()) {
         final AttributeModel attributeModel = attributes.get(attrName);

         /*
          * If every value of the attribute is distinct, and there are
          * at least MIN_ID_VALUES, treat it as an ID. ID values must be
          * Names. Only allowed one ID attribute per element type.
          */

         if (attributeModel.isAllNames()
               && (attributeModel.isUnique())
               && (attributeModel
                     .getOccurrences() >= ElementModel.MIN_ID_VALUES))
            return attrName;

         /*
          * TODO: This may give the wrong answer. We should check
          * whether the value sets of two candidate-ID attributes
          * overlap, in which case they can't both be IDs !!
          */

      }
      return null;
   }

   public void setHasCharacterContent(boolean hasCharacterContent) {
      this.hasCharacterContent = hasCharacterContent;
   }

   public void setSequenced(boolean sequenced) {
      this.sequenced = sequenced;
   }

   public void incrementOccurrences() {
      occurrences++;
   }

   public AttributeModel getAttribute(String attributeName) {
      return attributes.get(attributeName);
   }

   public void addAttribute(AttributeModel attributeModel) {
      attributes.put(attributeModel.getName(), attributeModel);
   }

   public String[] getATTLISTs() {
      return DTDGenerator.getATTLISTs(this);
   }

   public void addChild(ChildModel childModel) {
      childseq.add(childModel);
   }
}