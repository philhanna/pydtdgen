package com.philhanna.dtdgen;

import static org.junit.Assert.assertEquals;

import java.io.*;
import java.util.Properties;

import org.junit.Test;

/**
 * Unit tests for the Version class
 */
public class TestVersion {

   @Test
   public void testNormalCase() throws Exception {

      final Properties config = new Properties();
      final File projectRoot = new File(".").getCanonicalFile();
      final File versionFile = new File(
            projectRoot,
            "src/main/resources/version.properties");
      final Reader reader = new FileReader(versionFile);
      config.load(reader);
      reader.close();
      final String expected = ""
            + config.getProperty(Version.KEY_MAJOR, "-1")
            + "."
            + config.getProperty(Version.KEY_MINOR, "-2")
            + "."
            + config.getProperty(Version.KEY_PATCH, "-3");
      final String actual = Version.getVersion();
      assertEquals(expected, actual);
   }

}
