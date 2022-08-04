package com.philhanna.dtdgen;

import static org.junit.Assert.*;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;

import org.junit.After;
import org.junit.Before;

/**
 * Base class for all unit tests. Provides access to the test directory
 * and contains utility methods for comparing files, etc.
 */
public abstract class BaseTest {

   @Before
   public void setUp() throws Exception {
   }

   @After
   public void tearDown() throws Exception {
   }

   public InputStream getTestData(String fileName) throws IOException {
      final URL url = getClass().getResource(
            "/data/"
                  + fileName);
      if (url == null)
         throw new IOException(
               fileName
                     + " not found in test data");
      return url.openStream();
   }

   /**
    * Helper method to compare two input streams for equality
    * @param stream1
    * @param stream2
    * @throws IOException
    */
   public void assertStreamsEquals(InputStream stream1, InputStream stream2) throws IOException {
      BufferedReader reader1 = null;
      BufferedReader reader2 = null;
      try {
         reader1 = new BufferedReader(new InputStreamReader(stream1));
         reader2 = new BufferedReader(new InputStreamReader(stream2));
         int lineno = 0;
         for (;;) {
            final String lineE = reader1.readLine();
            final String lineA = reader2.readLine();
            lineno++;
            if (lineE == null
                  && lineA != null)
               fail(
                     "File 2 is longer: line "
                           + lineno
                           + ": "
                           + lineA);
            if (lineE != null
                  && lineA == null)
               fail(
                     "File 1 is longer: line "
                           + lineno
                           + ": "
                           + lineE);
            if (lineE == null)
               break;
            if (!lineE.equals(lineA))
               assertEquals(
                     "Different line "
                           + lineno,
                     lineE,
                     lineA);
         }
         // Files match
      }
      finally {
         reader1.close();
         reader2.close();
      }

   }

   /**
    * Helper method to compare two files for equality
    * @param file1
    * @param file2
    * @throws IOException
    */
   public void assertFilesEquals(File file1, File file2) throws IOException {

      assertNotNull(file1);
      assertNotNull(file2);

      final InputStream stream1 = new FileInputStream(file1);
      final InputStream stream2 = new FileInputStream(file2);
      
      assertStreamsEquals(stream1, stream2);
   }

}
