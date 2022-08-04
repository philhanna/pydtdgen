package com.philhanna.dtdgen;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

import com.philhanna.dtdgen.ElementModel;

/**
 * Unit tests for ElementModel
 */
public class TestElementModel {

   @Test
   public void verifyDefaultsAreSet() {
      final ElementModel elementModel = new ElementModel("MyQuery");
      assertEquals("MyQuery", elementModel.getName());
      assertEquals(0, elementModel.getOccurrences());
      assertFalse(elementModel.hasCharacterContent());
      assertTrue(elementModel.isSequenced());
   }
}
