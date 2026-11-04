import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;

// Near miss for the JVM download-to-disk composite: captures child-process
// output into a file with no URL connection anywhere, so neither the
// response-stream read capability nor the composite should fire.
public class JavaProcessOutToFile {
    public void save(java.lang.Process p, File out) throws Exception {
        try (InputStream in = p.getInputStream();
             FileOutputStream fos = new FileOutputStream(out)) {
            byte[] buf = new byte[4096];
            int n;
            while ((n = in.read(buf)) > 0) fos.write(buf, 0, n);
        }
    }
}
