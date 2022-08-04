package com.philhanna.dtdgen;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeMap;

/**
 * Provides access to what is known about the structure of a set of XML
 * document instances
 */
public class DocumentModel {

   // ====================================================================
   // Class constants and variables
   // ====================================================================

   // ====================================================================
   // Class methods
   // ====================================================================

   // ====================================================================
   // Instance variables
   // ====================================================================
   /**
    * Returns the root element name. This is determined by looking at
    * all elements in the element name list and deleting of their known
    * child elements. What remains should be the root element name (if
    * the XML is well-formed)
    */
   public String getRootElementName() {

      // Make a list of the names of all element that are not known to
      // have parent elements. To begin with, this will be every element

      final Set<String> possibleRoots = new HashSet<String>();
      for (final Iterator<String> it = elementNameIterator(); it.hasNext();) {
         final String elementName = it.next();
         possibleRoots.add(elementName);
      }

      // Now systematically remove names from this list by looking
      // through all elements and eliminating their children.

      for (final Iterator<String> it = elementNameIterator(); it.hasNext();) {

         // Get an element name

         final String parentElementName = it.next();
         final ElementModel parentElementModel = getElementModel(
               parentElementName);

         // How many child elements does it have?

         final int nChildren = parentElementModel.getChildModelCount();

         // Get each child element and remove its name from the
         // possibleRoots list

         for (int index = 0; index < nChildren; index++) {
            final ChildModel childModel = parentElementModel
                  .getChildModel(index);
            final String childElementName = childModel.getName();
            possibleRoots.remove(childElementName);
         }
      }

      // There should be only one element left - get the count

      final List<String> rootCandidates = new ArrayList<String>();
      rootCandidates.addAll(possibleRoots);
      final int nRootCandidates = rootCandidates.size();

      // Too few

      if (nRootCandidates == 0) {
         throw new RuntimeException("No possible root elements found");
      }

      // Too many

      if (nRootCandidates > 1) {
         final StringBuilder sb = new StringBuilder();
         for (int i = 0; i < nRootCandidates; i++) {
            if (i > 0)
               sb.append(", ");
            sb.append(rootCandidates.get(i));
         }
         final String rootCandidateNames = sb.toString();

         final String errmsg = String.format(
               "%d possible root elements found: [%s]",
               nRootCandidates,
               rootCandidateNames);
         throw new RuntimeException(errmsg);
      }

      // Found the one possible root element

      final String rootElementName = rootCandidates.get(0);
      return rootElementName;
   }

   /**
    * Alphabetical list of element types appearing in the document; each
    * has the element name as a key and an ElementModelImpl object as
    * the value.
    */
   private final Map<String, ElementModel> elementMap = new TreeMap<String, ElementModel>();

   // ====================================================================
   // Constructors
   // ====================================================================

   // ====================================================================
   // Implementation of DocumentModel
   // ====================================================================

   /**
    * Returns the {@link Foo} with the given name
    * @param elementName the element name
    * @return the element model with that name, or <code>null</code>, if
    *         it does not exist in the document model
    */
   public ElementModel getElementModel(String elementName) {
      return elementMap.get(elementName);
   }

   /**
    * Returns an iterator over the list of element model names
    */
   public Iterator<String> elementNameIterator() {
      return elementMap.keySet().iterator();
   }

   // ====================================================================
   // Instance methods
   // ====================================================================

   public void addElementModel(ElementModel elementModel) {
      final String elementName = elementModel.getName();
      elementMap.put(elementName, elementModel);
   }

}
