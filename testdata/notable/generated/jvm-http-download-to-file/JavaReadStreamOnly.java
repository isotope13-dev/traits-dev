import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

// Near miss for the JVM download-to-disk composite: reads a URL response
// stream but never writes a local file, so only the response-stream read
// capability should fire.
public class JavaReadStreamOnly {
    public static String slurp(String link) throws Exception {
        HttpURLConnection c = (HttpURLConnection) new URL(link).openConnection();
        try (BufferedReader r = new BufferedReader(new InputStreamReader(c.getInputStream()))) {
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = r.readLine()) != null) sb.append(line);
            return sb.toString();
        }
    }
}
