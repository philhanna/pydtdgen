package com.philhanna.dtdgen;

import java.util.Iterator;
import java.util.LinkedHashSet;
import java.util.Set;

/**
 * Keeps track of what is known about the type and value of an element
 * attribute, based on how it is used in all instances found in the
 * source XML.
 */
public class AttributeModel {

   // ==========================================================
   // Instance variables
   // ==========================================================

   /**
    * Name of the attribute
    */
   private final String name;

   /**
    * Number of occurrences of the attribute
    */
   private int occurrences = 0;

   /**
    * <code>true</code> if no duplicate values encountered
    */
   private boolean unique = true;

   /**
    * set of all distinct values encountered for this attribute
    */
   private final Set<String> values = new LinkedHashSet<String>();

   /**
    * <code>true</code> if all the attribute values are valid names
    */
   private boolean allNames = true;

   /**
    * <code>true</code> if all the attribute values are valid
    * <code>NMTOKEN</code>s
    */
   private boolean allNMTOKENs = true;

   // ==================================================================
   // Constructors
   // ==================================================================

   /**
    * Creates a new attribute model with the specified name
    * @param name the attribute name
    */
   public AttributeModel(String name) {
      this.name = name;
   }

   // ==================================================================
   // Implementation of AttributeModel
   // ==================================================================

   /**
    * Returns the attribute name
    */
   public String getName() {
      return name;
   }

   /**
    * Returns the number of times this attribute was found in the source
    * XML associated with this element
    */
   public int getOccurrences() {
      return occurrences;
   }

   /**
    * Returns the number of distinct values this attribute was found to
    * have in the source XML associated with this element
    */
   public int getValueCount() {
      return values.size();
   }

   /**
    * Returns the first value this attribute has in this element
    */
   public String getFirstValue() {
      if (values.isEmpty())
         return null;
      final Iterator<String> it = valueIterator();
      final String firstValue = it.next();
      return firstValue;
   }

   /**
    * Returns an iterator over the values for this attribute
    */
   public Iterator<String> valueIterator() {
      return values.iterator();
   }

   // ==========================================================
   // Instance methods
   // ==========================================================

   public void incrementOccurrences() {
      occurrences++;
   }

   /**
    * Returns <code>true</code> if every occurrence of this attribute in
    * the element had a value that was a valid name.
    */
   public boolean isAllNames() {
      return allNames;
   }

   /**
    * Returns <code>true</code> if every occurrence of this attribute in
    * the element had a value that was a valid <code>NMTOKEN</code>
    */
   public boolean isAllNMTOKENs() {
      return allNMTOKENs;
   }

   public boolean isUnique() {
      return unique;
   }

   public void setAllNames(boolean allNames) {
      this.allNames = allNames;
   }

   public void setAllNMTOKENs(boolean allNMTOKENs) {
      this.allNMTOKENs = allNMTOKENs;
   }

   public void setUnique(boolean unique) {
      this.unique = unique;
   }

   public boolean contains(String value) {
      return values.contains(value);
   }

   public void addValue(String value) {
      values.add(value);
   }
   
   public void setOccurrences(int occurrences) {
      this.occurrences = occurrences;
   }

   @Override
   public String toString() {
      return "AttributeModelImpl [name="
            + name
            + ", occurrences="
            + occurrences
            + ", unique="
            + unique
            + ", values="
            + values
            + ", allNames="
            + allNames
            + ", allNMTOKENs="
            + allNMTOKENs
            + "]";
   }
   
}
