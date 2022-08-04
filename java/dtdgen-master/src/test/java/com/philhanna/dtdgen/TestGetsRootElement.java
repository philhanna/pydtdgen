package com.philhanna.dtdgen;

import static org.junit.Assert.assertEquals;

import java.io.IOException;
import java.io.InputStream;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.xml.sax.SAXException;

import com.philhanna.dtdgen.modelbuilder.DocumentModelBuilder;

/**
 * Unit tests for getting the root element of a body
 */
public class TestGetsRootElement extends BaseTest {

   @Before
   public void setUp() throws Exception {
      super.setUp();
   }

   @After
   public void tearDown() throws Exception {
      super.tearDown();
   }

   @Test
   public void handlesTypicalCase() throws Exception {
      runTest("stooges.xml", "stooges");
   }

   private void runTest(final String fileName, final String expected)
         throws IOException, SAXException {
      
      // Analyze the xml file to get a document model

      final InputStream in = getTestData(fileName);
      final DocumentModelBuilder modelBuilder = new DocumentModelBuilder();
      modelBuilder.run(in);
      in.close();
      
      final DocumentModel model = modelBuilder.getDocumentModel();
      final String actual = model.getRootElementName();
      assertEquals(expected, actual);
   }

}
