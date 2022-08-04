package com.philhanna.dtdgen;

/**
 * Records information about the presence of a child element within its
 * parent element. If the parent element is sequenced, then the child
 * elements always occur in sequence with the given frequency.
 */
public class ChildModel {
   
   // ==================================================================
   // Instance variables
   // ==================================================================
   
   private final String name;
   private boolean repeatable;
   private boolean optional;

   // ==================================================================
   // Constructors
   // ==================================================================

   /**
    * Creates a ChildModel of the specified child element name
    * @param name the child element name
    */
   public ChildModel(String name) {
      this.name = name;
   }

   // ==================================================================
   // Implementation of ChildModel interface
   // ==================================================================
   
   /**
    * Returns the child element name
    */
   public String getName() {
      return name;
   }

   /**
    * Returns <code>true</code> if this child can be repeated in its
    * parent element
    */
   public boolean isRepeatable() {
      return repeatable;
   }

   /**
    * Returns true if this child element is not required to be present
    * under its parent element
    */
   public boolean isOptional() {
      return optional;
   }

   /**
    * Sets the repeatable attribute
    * @param repeatable the repeatable attribute
    */
   public void setRepeatable(boolean repeatable) {
      this.repeatable = repeatable;
   }

   /**
    * Sets the optional attribute
    * @param optional the optional attribute
    */
   public void setOptional(boolean optional) {
      this.optional = optional;
   }
}