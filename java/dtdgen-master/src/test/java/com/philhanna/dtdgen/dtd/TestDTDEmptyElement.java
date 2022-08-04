package com.philhanna.dtdgen.dtd;

import static org.junit.Assert.*;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import com.philhanna.dtdgen.BaseTest;
import com.philhanna.dtdgen.ElementModel;

/**
 * Unit tests for DTDEmptyElement
 */
public class TestDTDEmptyElement extends BaseTest {

   @Before
   public void setUp() throws Exception {
      super.setUp();
   }

   @After
   public void tearDown() throws Exception {
      super.tearDown();
   }

   @Test
   public void testToString() {
      final ElementModel model = new ElementModel("flag");
      final DTDEmptyElement element = new DTDEmptyElement(model);
      final String actual = element.toString();
      final String expected = "<!ELEMENT flag EMPTY >";
      assertEquals(expected, actual);
   }

}
