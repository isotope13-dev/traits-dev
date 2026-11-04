import java.io.File;
import java.io.FileOutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

// Near miss for the JVM download-to-disk composite: opens a URL connection
// (never reading its stream) in one method and writes an unrelated local
// file in a distant method. The legs are far apart, so no bound
// download-to-disk shape exists and the composite must stay silent.
public class JavaUnboundFar {
    public static void ping(String link) throws Exception {
        HttpURLConnection c = (HttpURLConnection) new URL(link).openConnection();
        c.setConnectTimeout(2000);
        c.connect();
    }

    public static void writeState(File f) throws Exception {
        try (FileOutputStream fos = new FileOutputStream(f)) {
            fos.write(new byte[]{1, 2, 3});
        }
    }
}
