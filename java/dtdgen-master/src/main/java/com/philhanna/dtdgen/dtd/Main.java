package com.philhanna.dtdgen.dtd;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;

import org.xml.sax.SAXException;

import com.philhanna.dtdgen.DocumentModel;
import com.philhanna.dtdgen.Version;
import com.philhanna.dtdgen.modelbuilder.DocumentModelBuilder;

/**
 * Mainline class for invoking DTDGEN
 */
public class Main {

   static enum State {
      READING_OPTIONS,
      EXPECTING_OUTPUT_FILE,
   }

   /**
    * Invokes DTDGEN with the specified arguments
    * @param args the command line arguments
    * @throws IOException if input file(s) cannot be read or output file
    *         cannot be written
    * @throws SAXException if the XML processing fails
    */
   public static void main(String[] args) throws IOException, SAXException {

      // Check for help or version first

      if (args.length == 0) {
         showUsage();
         return;
      }

      for (final String arg : args) {
         if (arg.equals("-h") || arg.equals("--help")) {
            showUsage();
            return;
         }
         if (arg.equals("-v") || arg.equals("--version")) {
            showVersion();
            return;
         }
      }

      // Get the output file and a list of input files

      final List<File> inputFiles = new ArrayList<File>();
      File outputFile = null;
      State state = State.READING_OPTIONS;

      for (final String arg : args) {
         switch (state) {

            case READING_OPTIONS:
               if (arg.equals("-o") || arg.equals("--output"))
                  state = State.EXPECTING_OUTPUT_FILE;
               else if (arg.startsWith("-")) {
                  final String errmsg = String.format(
                        "Unrecognized op      PROBLEM_FOUND\n"
                              + "tion %s. Try -h for help",
                        arg);
                  throw new IllegalArgumentException(errmsg);
               }
               else {
                  final File inputFile = new File(arg);
                  if (!inputFile.exists()) {
                     final String errmsg = String
                           .format("Input file %s does not exist", arg);
                     throw new IOException(errmsg);
                  }
                  inputFiles.add(inputFile);
               }
               break;

            case EXPECTING_OUTPUT_FILE:
               if (arg.startsWith("-")) {
                  final String errmsg = String.format(
                        "Expecting output file name, not %s. Try -h for help",
                        arg);
                  throw new IllegalArgumentException(errmsg);
               }
               outputFile = new File(arg);
               state = State.READING_OPTIONS;
               break;
         }
      }

      // Verify that all options were found

      switch (state) {
         case READING_OPTIONS:
            break;
         case EXPECTING_OUTPUT_FILE:
            final String errmsg = String
                  .format("No output file specified. Try -h for help");
            throw new IllegalArgumentException(errmsg);
      }

      // Create a DocumentModelBuilder and run input files through it

      final DocumentModelBuilder modelBuilder = new DocumentModelBuilder();

      for (final File inputFile : inputFiles) {
         final InputStream in = new FileInputStream(inputFile);
         modelBuilder.run(in);
      }

      // Get the resulting document model

      final DocumentModel model = modelBuilder.getDocumentModel();

      // Write output DTD, either to stdout or to the specified file

      final DTDGenerator dtdgen = new DTDGenerator(model);
      if (outputFile == null) {
         final PrintWriter out = new PrintWriter(
               new OutputStreamWriter(System.out));
         dtdgen.printDTD(out);
         out.flush();
      }
      else {
         final PrintWriter out = new PrintWriter(new FileWriter(outputFile));
         dtdgen.printDTD(out);
         out.flush();
         out.close();
      }
   }

   private static void showUsage() {
      final String[] lines = {
            "usage: dtdgen <inputFile> [, <inputFile>]* [-o | --output <outputFile>]",
            "       dtdgen -h | --help",
            "       dtdgen -v | --version",
            "",
            "where:",
            "",
            "<inputFile>      An XML file (of the same type as the others, if more than one)",
            "<outputFile>     The output .dtd file.  Defaults to stdout",
            "",
            "-h or --help     Displays this help text",
            "-v or --version  Displays the software version number", };
      for (final String line : lines)
         System.out.println(line);
   }

   private static void showVersion() {
      System.out.printf("dtdgen version \"%s\"\n", Version.getVersion());
   }

}
