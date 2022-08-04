package com.philhanna.dtdgen.dtd;

import static org.junit.Assert.*;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import com.philhanna.dtdgen.BaseTest;
import com.philhanna.dtdgen.ChildModel;
import com.philhanna.dtdgen.ElementModel;

/**
 * Unit tests for DTDMixedContentElement
 */
public class TestDTDMixedContentElement extends BaseTest {

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
      final ElementModel model = new ElementModel("stooges");
      model.addChild(new ChildModel("stooge"));
      final DTDMixedContentElement element = new DTDMixedContentElement(model);
      final String actual = element.toString();
      final String expected = "<!ELEMENT stooges ( #PCDATA | stooge )* >";
      assertEquals(expected, actual);
   }

}
