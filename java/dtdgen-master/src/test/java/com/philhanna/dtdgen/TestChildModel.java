package com.philhanna.dtdgen;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

import com.philhanna.dtdgen.ChildModel;

/**
 * Unit tests for ChildModel
 */
public class TestChildModel {

   @Test
   public void testConstructor() {
      final ChildModel cd = new ChildModel("Larry");
      assertEquals("Larry", cd.getName());
   }

}
