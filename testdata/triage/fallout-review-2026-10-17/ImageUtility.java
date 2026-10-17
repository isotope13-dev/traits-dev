import java.io.*;
import java.util.zip.*;

// Independent utility methods, never executed by the review. Co-occurring
// image, archive, and child-process APIs do not prove concealed execution.
public class ImageUtility {
    public static byte[] imageHeader() {
        return new byte[]{-119, 80, 78, 71, 13, 10, 26, 10};
    }
    public static int inflate(byte[] bytes, byte[] output) throws Exception {
        Inflater inflater = new Inflater();
        inflater.setInput(bytes);
        return inflater.inflate(output);
    }
    public static void extract(InputStream input, File destination) throws Exception {
        try (ZipInputStream zip = new ZipInputStream(input)) {
            ZipEntry entry;
            while ((entry = zip.getNextEntry()) != null) {
                if (entry.isDirectory()) continue;
                File target = new File(destination, entry.getName());
                if (!target.getCanonicalPath().startsWith(destination.getCanonicalPath() + File.separator))
                    throw new IOException("outside destination");
                try (FileOutputStream out = new FileOutputStream(target)) {
                    byte[] buffer = new byte[4096];
                    int size;
                    while ((size = zip.read(buffer)) > 0) out.write(buffer, 0, size);
                }
                zip.closeEntry();
            }
        }
    }
    public static Process launch(String[] arguments) throws IOException {
        return new ProcessBuilder(arguments).start();
    }
}
