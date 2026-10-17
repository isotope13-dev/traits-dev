import java.io.*;
import java.util.Base64;
import java.util.zip.*;

// Benign control: Base64 configuration is unrelated to extracted archive bytes.
// This fixture is compiled for static inspection and is never executed.
public class ArchiveLauncher {
    public static final String CONFIG = "\004abcdefghijklmnop";
    public static void unpack(InputStream input, File output) throws IOException {
        Base64.getDecoder().decode("Y29uZmln");
        try (ZipInputStream zip = new ZipInputStream(input);
             FileOutputStream file = new FileOutputStream(output)) {
            ZipEntry entry = zip.getNextEntry();
            byte[] buffer = new byte[1024];
            int count = zip.read(buffer);
            if (entry != null && count > 0) file.write(buffer, 0, count);
        }
    }
    public static void launch(String command) throws IOException {
        new ProcessBuilder(command).start();
    }
}
