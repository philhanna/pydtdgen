package com.philhanna.dtdgen;

import java.io.*;
import java.net.*;
import java.util.Properties;

import org.apache.log4j.Logger;

/**
 * Utility class to provide the software version number
 */
public class Version {

   // ====================================================================
   // Class constants and variables
   // ====================================================================

   private static final Logger log = Logger.getLogger(Version.class);

   /**
    * Name of properties file containing version information, in the
    * form of a resource name that the class loader understands.
    */
   static final String PROPERTIES_FILE_NAME = "/version.properties";

   /**
    * The key in the properties file for the major version number
    */
   static final String KEY_MAJOR = "version.major";

   /**
    * The key in the properties file for the minor version number
    */
   static final String KEY_MINOR = "version.minor";

   /**
    * The key in the properties file for the patch version number
    */
   static final String KEY_PATCH = "version.patch";

   // ====================================================================
   // Class methods
   // ====================================================================

   /**
    * Returns the software version as <i>&lt;major version&gt;.&lt;minor
    * version.&gt;.&lt;patch version&gt;</i>. Accesses this information
    * from a <code>version.properties</code> file in the Java class
    * path.
    */
   public static final String getVersion() {

      log.debug("Entry");

      final URL versionURL = Version.class.getResource(PROPERTIES_FILE_NAME);
      if (versionURL == null) {
         final String errmsg = String.format(
               "Could not find classpath-based resource %s",
               PROPERTIES_FILE_NAME);
         log.warn(errmsg);
         System.err.printf("%s\n", errmsg);
         return null;
      }

      final Properties properties = new Properties();
      try {
         final InputStream inStream = versionURL.openStream();
         properties.load(inStream);
      }
      catch (IOException e) {
         final String errmsg = String
               .format("Unable to open %s for input", versionURL);
         log.warn(errmsg, e);
         System.err.printf("%s\n", errmsg);
         return null;
      }

      final String majorVersion = properties.getProperty(KEY_MAJOR);
      if (majorVersion == null) {
         final String errmsg = String.format(
               "Property %s not found in version properties file",
               KEY_MAJOR);
         log.warn(errmsg);
         System.err.printf("%s\n", errmsg);
         return null;
      }

      final String minorVersion = properties.getProperty(KEY_MINOR);
      if (minorVersion == null) {
         final String errmsg = String.format(
               "Property %s not found in version properties file",
               KEY_MINOR);
         log.warn(errmsg);
         System.err.printf("%s\n", errmsg);
         return null;
      }

      final String patchVersion = properties.getProperty(KEY_PATCH);
      if (patchVersion == null) {
         final String errmsg = String.format(
               "Property %s not found in version properties file",
               KEY_PATCH);
         log.warn(errmsg);
         System.err.printf("%s\n", errmsg);
         return null;
      }

      final String result = String.format(
            "%s.%s.%s",
            majorVersion.trim(),
            minorVersion.trim(),
            patchVersion.trim());

      log.debug("Exit, returning " + result);
      return result;
   }

   // ====================================================================
   // Instance variables
   // ====================================================================

   // ====================================================================
   // Constructors
   // ====================================================================

   // ====================================================================
   // Instance methods
   // ====================================================================
}
