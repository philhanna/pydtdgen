package com.philhanna.dtdgen;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;

import org.junit.Before;
import org.junit.Test;

import com.philhanna.dtdgen.AttributeModel;

/**
 * Unit tests for AttributeModel
 */
public class TestAttributeModel {

   private AttributeModel attributeModel;
   
   @Before
   public void setUp() throws Exception {
      attributeModel = new AttributeModel("stooge");
      attributeModel.addValue("Larry");
      attributeModel.addValue("Curly");
      attributeModel.addValue("Moe");
      attributeModel.addValue("Shemp");
      attributeModel.addValue("Curly Joe");
   }

   @Test
   public void checkDefaults() {
      assertEquals(0, attributeModel.getOccurrences());
      assertTrue(attributeModel.isUnique());
      assertTrue(attributeModel.isAllNames());
      assertTrue(attributeModel.isAllNMTOKENs());
   }

   @Test
   public void testGetFirstValue() {
      // Make sure that the list is not alphabetical, but in arrival sequence
      assertEquals("Larry", attributeModel.getFirstValue());
   }

   @Test
   public void testGetFirstValueOnEmptyList() {
      final AttributeModel adNull = new AttributeModel("stooge");
      assertNull(adNull.getFirstValue());
      adNull.addValue("Max");
      assertEquals("Max", adNull.getFirstValue());
   }

   @Test
   public void testIncrementOccurrences() {
      assertEquals(0, attributeModel.getOccurrences());
      attributeModel.incrementOccurrences();
      attributeModel.incrementOccurrences();
      attributeModel.incrementOccurrences();
      assertEquals(3, attributeModel.getOccurrences());
   }
   
   @Test
   public void testNMTokens() {
      assertTrue(attributeModel.isAllNMTOKENs());
   }
   
   @Test
   public void testNMTokensFalse() {
      attributeModel.setAllNMTOKENs(false);
      assertFalse(attributeModel.isAllNMTOKENs());
   }
   
   @Test
   public void testGetDistinctValues() {
      assertTrue(attributeModel.contains("Larry"));
      assertTrue(attributeModel.contains("Curly"));
      assertTrue(attributeModel.contains("Moe"));
      assertTrue(attributeModel.contains("Shemp"));
      assertTrue(attributeModel.contains("Curly Joe"));
      
      assertFalse(attributeModel.contains("bogus"));
   }
}
