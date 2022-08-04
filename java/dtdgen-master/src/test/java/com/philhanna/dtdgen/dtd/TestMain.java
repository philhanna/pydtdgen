package com.philhanna.dtdgen.dtd;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.PrintStream;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

/**
 * Unit tests for Main
 */
public class TestMain {

   private ByteArrayOutputStream baos;
   private PrintStream save_stdout;

   @Before
   public void setUp() throws Exception {

      // Save the current stdout so that it can be restored after each
      // test

      save_stdout = System.out;

      // Use an in-memory stdout so that output can be compared in tests

      baos = new ByteArrayOutputStream();
      PrintStream stdout = new PrintStream(baos);
      System.setOut(stdout);
   }

   @After
   public void tearDown() throws Exception {
      if (save_stdout != null) {
         System.setOut(save_stdout);
      }
   }

   @Test
   public void testStateEnum() throws Exception {
      assertEquals(2, Main.State.values().length);
      assertNotNull(Main.State.valueOf("READING_OPTIONS"));
      assertNotNull(Main.State.valueOf("EXPECTING_OUTPUT_FILE"));
      try {
         String badValue = "BOGUS";
         assertNull(Main.State.valueOf(badValue));
         fail("Should have thrown an exception");
      }
      catch (IllegalArgumentException e) {
         // Expected
      }
   }

   @Test
   public void testNoArgs() throws Exception {
      Main.main(new String[] {});
      System.out.flush();
      final String actual = new String(baos.toByteArray());
      assertTrue(actual.contains("<inputFile>"));
   }

   @Test
   public void testGetVersion() throws Exception {
      Main.main(new String[] { "-v" });
      System.out.flush();
      final String actual = new String(baos.toByteArray());
      assertTrue(actual.contains("dtdgen version"));
   }

   @Test
   public void testGetVersionLong() throws Exception {
      Main.main(new String[] { "file1", "file2", "--version" });
   }

   @Test
   public void testGetHelp() throws Exception {
      Main.main(new String[] { "-h" });
   }

   @Test
   public void testGetHelpLong() throws Exception {
      Main.main(new String[] { "file1", "file2", "--help" });
   }

   @Test
   public void testWithFiles() throws Exception {
      try {
         Main.main(new String[] { "file1", "file2"});
         fail("Should have thrown an exception");
      }
      catch (IOException e) {
         // Expected
      }
   }
   
   @Test
   public void testNoOutputFile() throws Exception {
      try {
         Main.main(new String[] {"-o"});
      }
      catch (IllegalArgumentException e) {
         // Expected
      }
   }
}
